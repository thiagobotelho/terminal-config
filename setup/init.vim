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

" --- COLUNA ATIVA no cursor ---
set cursorcolumn
highlight CursorColumn ctermbg=NONE guibg=#2c2c2c

" --- COMENTÁRIOS SEM ITÁLICO ---
highlight Comment guifg=#7f849c gui=NONE cterm=NONE

