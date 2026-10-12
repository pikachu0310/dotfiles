# PATHは存在するディレクトリだけ追加する。再読込でも重複させない。
set -q BUN_INSTALL; or set -gx BUN_INSTALL "$HOME/.bun"
fish_add_path --path "$HOME/.local/bin" "$HOME/.cargo/bin" "$BUN_INSTALL/bin" "$HOME/.deno/bin" /usr/local/bin /usr/local/go/bin "$HOME/go/bin"

# 端末を使うときだけプロンプトを初期化する。
if status is-interactive
    if command -q starship
        starship init fish | source
    end
end

# Java・Ruby・私用の環境変数などは、このPCだけの設定へ。
if test -f "$__fish_config_dir/config.local.fish"
    source "$__fish_config_dir/config.local.fish"
end
