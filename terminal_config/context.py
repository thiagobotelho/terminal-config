from __future__ import annotations

import hashlib
import json
import os
import platform
import shutil
import time
import urllib.request
from dataclasses import dataclass
from pathlib import Path

from .runner import Runner


@dataclass
class Context:
    root: Path
    home: Path
    runner: Runner
    lock: dict

    @property
    def is_wsl(self) -> bool:
        release = platform.release().lower()
        return "microsoft" in release or bool(os.environ.get("WSL_DISTRO_NAME"))

    @property
    def package_manager(self) -> str:
        if shutil.which("dnf"):
            return "dnf"
        if shutil.which("apt-get"):
            return "apt"
        raise RuntimeError("Distribuição não suportada: esperado dnf ou apt-get")

    def install_packages(self, fedora: list[str], debian: list[str]) -> None:
        packages = fedora if self.package_manager == "dnf" else debian
        if self.package_manager == "dnf":
            self.runner.run(["dnf", "install", "-y", *packages], sudo=True)
        else:
            self.runner.run(["apt-get", "update"], sudo=True)
            self.runner.run(["apt-get", "install", "-y", *packages], sudo=True)

    def deploy(self, source: Path, destination: Path) -> None:
        if self.runner.dry_run:
            print(f"📄 deploy {source} -> {destination}")
            return
        destination.parent.mkdir(parents=True, exist_ok=True)
        if destination.exists() and destination.read_bytes() != source.read_bytes():
            stamp = time.strftime("%Y%m%d-%H%M%S")
            backup = destination.with_name(f"{destination.name}.bak-{stamp}")
            shutil.copy2(destination, backup)
            print(f"🛟 Backup: {backup}")
        shutil.copy2(source, destination)

    def download_verified(self, url: str, destination: Path, sha256: str) -> None:
        if self.runner.dry_run:
            print(f"📥 download {url} -> {destination} (sha256={sha256})")
            return
        destination.parent.mkdir(parents=True, exist_ok=True)
        with urllib.request.urlopen(url) as response, destination.open("wb") as output:
            shutil.copyfileobj(response, output)
        actual = hashlib.sha256(destination.read_bytes()).hexdigest()
        if actual.lower() != sha256.lower():
            destination.unlink(missing_ok=True)
            raise RuntimeError(f"SHA256 inválido para {url}: {actual}")

    def clone_locked(self, name: str, destination: Path) -> None:
        spec = self.lock["git"][name]
        if not destination.exists():
            self.runner.run(["git", "clone", "--filter=blob:none", spec["url"], destination])
        if self.runner.dry_run:
            print(f"🔒 checkout {name}@{spec['commit']}")
            return
        self.runner.run(["git", "-C", destination, "fetch", "--depth=1", "origin", spec["commit"]])
        self.runner.run(["git", "-C", destination, "checkout", "--detach", spec["commit"]])


def load_context(root: Path, dry_run: bool) -> Context:
    lock = json.loads((root / "versions.lock.json").read_text())
    return Context(root=root, home=Path.home(), runner=Runner(dry_run), lock=lock)
