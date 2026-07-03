from __future__ import annotations

import tarfile
import tempfile
import shutil
from pathlib import Path

from ..context import Context


def install(ctx: Context, *, set_shell: bool = True) -> None:
    del set_shell
    print("🔤 Módulo fonts")
    spec = ctx.lock["font"]
    if ctx.runner.dry_run:
        ctx.download_verified(spec["url"], Path("/tmp") / spec["asset"], spec["sha256"])
        return

    destination = ctx.home / ".local/share/fonts/CaskaydiaCove"
    destination.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="terminal-font-") as temp:
        archive = Path(temp) / spec["asset"]
        ctx.download_verified(spec["url"], archive, spec["sha256"])
        with tarfile.open(archive, "r:xz") as bundle:
            for member in bundle.getmembers():
                if member.isfile() and member.name.lower().endswith((".ttf", ".otf")):
                    source = bundle.extractfile(member)
                    if source is None:
                        continue
                    target = destination / Path(member.name).name
                    with source, target.open("wb") as output:
                        shutil.copyfileobj(source, output)
    ctx.runner.run(["fc-cache", "-f", str(destination)])
