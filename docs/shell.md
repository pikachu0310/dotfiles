# Fish・Starship・Git

WSLで使っている設定を、別のPCにも置ける形にまとめています。FishのPATHにはBun・Rust・Deno・Goを追加し、Starshipはカラフルな表示を使います。ツールが未導入でもFishの起動時にエラーを出さない構成です。

## 設定を置く

リポジトリのルートで、必要なファイルだけリンクします。既存のファイルやリンクがある場合、以下の操作は失敗して止まります。`-f`で上書きせず、今の設定と比較してください。

```bash
mkdir -p "$HOME/.config/fish" "$HOME/.config/git"
ln -s "$PWD/.config/fish/config.fish" "$HOME/.config/fish/config.fish"
ln -s "$PWD/.config/fish/fish_plugins" "$HOME/.config/fish/fish_plugins"
ln -s "$PWD/.config/starship.toml" "$HOME/.config/starship.toml"
ln -s "$PWD/.config/git/ignore" "$HOME/.config/git/ignore"
```

これはファイルの配置です。FishやStarship本体のインストールは、[Fish](https://fishshell.com/docs/current/index.html)・[Starship](https://starship.rs/guide/)の案内に従ってください。Starshipのアイコン表示にはNerd Fontが必要です。macOSでは、そのOSのパッケージ管理を使います。

Javaの場所、Rubyの初期化、私用の環境変数は、Git管理外の `~/.config/fish/config.local.fish` に書けます。

## FishのプラグインとNode.js

現在使っているプラグインはnvm.fishだけです。Fisherはその管理用に収録しています。Fisher 4.4.8と、確認したnvm.fishのコミットを `fish_plugins` に固定しました。

Fisherがなければ、Fishで次を実行します。

```fish
curl -fsSL https://raw.githubusercontent.com/jorgebucaran/fisher/4.4.8/functions/fisher.fish | source
fisher update
```

Node.jsは、プロジェクトの `.nvmrc` があればそれを優先します。指定がなければ、[現在のLTS](https://nodejs.org/en/about/previous-releases)を選びます。2026年10月12日時点では24系です。

```fish
nvm install lts
set -U nvm_default_version (nvm current)
```

`.nvmrc` のあるプロジェクトでは `nvm use` を実行します。必要な版が未導入なら `nvm install` を使います。シェル設定の読込時に22.15.0を固定したり、Nodeを自動ダウンロードしたりはしません。更新時は `nvm install lts` と既定版の設定を再実行します。

Bashのnvmとnvm.fishは、Nodeの保存先が異なります。WSLのBashにインストール済みでも、Fish側には別途導入が必要です。

## Git

`.gitconfig` は設定例です。作者名とメールが入っているため、他の人はそのままリンクせず、自分の情報へ変えてください。既存の認証設定は保ってください。

- 新規リポジトリのブランチ名は `main`。
- Git LFSを使う場合は、Git LFS本体も導入する。
- GitHubのHTTPS URLはSSHへ変換する。利用者自身のSSH認証が必要。
- このPCだけの設定は `~/.gitconfig.local` に分ける。credential helperと個別の `safe.directory` は配布しない。

`.config/git/ignore` はGitの標準配置です。OSの一時ファイル、私用の設定、`.env`などを無視し、`.env.example`・`.env.sample`・`.env.template`は共有できます。既に追跡中のファイルをGitから消すものではありません。

## 今回更新したところ

2024年の公開版と現在のWSLを比較し、使わなくなったプラグインとezaの別名、古いJava・Rubyの設定、私用のGo設定を外しました。BunなどのPATHとGitの `main` 設定を反映し、Starshipの未使用の右側表示と、その設定にあった未定義色を除きました。

確認時のWSL本体はFish 3.7.0・Starship 1.22.1・Git 2.43.0でした。公式の最新リリースは[Fish 4.9.3](https://github.com/fish-shell/fish-shell/releases/tag/4.9.3)・[Starship 1.26.0](https://github.com/starship/starship/releases/tag/v1.26.0)です。今回更新したのは公開設定で、本体のアップグレードや実行中の環境への上書きは行っていません。
