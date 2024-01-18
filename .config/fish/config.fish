if status is-interactive
    # Commands to run in interactive sessions can go here
end

starship init fish | source
set --export PATH $HOME/.cargo/bin $PATH

#function fish_user_key_bindings
#  bind \cr 'peco_select_history (commandline -b)'
#end

alias fd='fdfind'
alias bat='batcat'

alias ei="eza --icons --git"
alias ea="eza -a --icons --git"
alias ee="eza -aahl --icons --git"
alias et="eza -T -L 3 -a -I 'node_modules|.git|.cache' --icons"
alias eta="eza -T -a -I 'node_modules|.git|.cache' --color=always --icons | less -r"
alias ls=ei
alias la=ea
alias ll=ee
alias lt=et
alias lta=eta
alias l="clear && ls"

fish_add_path /usr/local/bin
fish_add_path /usr/local/go/bin
fish_add_path $HOME/go/bin
set -gx JAVA_HOME "/home/pikachu0310/.jdks/openjdk-21.0.1"
fish_add_path /home/pikachu0310/.jdks/openjdk-21.0.1
set -gx GOPRIVATE "github.com/no9jp/proto"
fish_add_path "$HOME/.rbenv/bin"
status --is-interactive; and . (rbenv init -|psub)
