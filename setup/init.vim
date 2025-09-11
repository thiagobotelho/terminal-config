" --- PLUGINS - via vim-plug ---
call plug#begin('~/.local/share/nvim/plugged')

" Tema Catppuccin para Neovim
Plug 'catppuccin/nvim', { 'as': 'catppuccin' }

" Plugin de indentação com contexto (novo nome: ibl)
Plug 'lukas-reineke/indent-blankline.nvim'

" Treesitter para realce semântico moderno
Plug 'nvim-treesitter/nvim-treesitter', { 'do': ':TSUpdate' }

call plug#end()

" --- CONFIGURAÇÕES GERAIS ---
set termguicolors
syntax enable
filetype plugin indent on


colorscheme catppuccin

" --- INDENTAÇÃO: plugin ibl ---
lua << EOF
vim.opt.list = true
vim.opt.listchars:append("space:⋅")
vim.opt.listchars:append("tab:│ ")
require("ibl").setup({
  indent = {
    char = "│"
  },
  scope = {
    enabled = true,
    show_start = true,
    show_end = false,
  }
})
EOF

" --- TRANSPARêNCIA ---
lua << EOF
require("catppuccin").setup({
  flavour = "mocha",
  transparent_background = true,
  term_colors = true,
})
EOF

" Garantia de transparência pós-tema
highlight Normal        ctermbg=NONE guibg=NONE
highlight NormalNC      ctermbg=NONE guibg=NONE
highlight NormalFloat   ctermbg=NONE guibg=NONE
highlight SignColumn    ctermbg=NONE guibg=NONE
highlight LineNr        ctermbg=NONE guibg=NONE
highlight EndOfBuffer   ctermbg=NONE guibg=NONE

" --- COLUNA ATIVA no cursor ---
set cursorcolumn
highlight CursorColumn ctermbg=NONE guibg=#2c2c2c

" --- COMENTÁRIOS SEM ITÁLICO ---
highlight Comment guifg=#7f849c gui=NONE cterm=NONE