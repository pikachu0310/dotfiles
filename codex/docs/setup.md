# Codexの導入

スキルを置き、必要なら個人文書とIntentの受付を追加します。ログイン情報や本人の個人文書は配布していません。

## 1. スキルを使う

このリポジトリだけで試すなら、Codex Appに `codex/` をプロジェクトとして追加してください。すべてのプロジェクトで使うには、以下でユーザー用スキルを配置します。Python 3.11以降が必要です。

**Windows AppはWindowsのユーザーフォルダー、WSL CLIはWSLのホームへ配置します。** WSL側へ置いただけではWindows Appに入りません。以下はリポジトリのルートで実行してください。

Windowsにcloneした場合は、PowerShellで実行します。`py`がなければインストール済みPythonのコマンドに置き換えます。

```powershell
$codexUserHome = $env:USERPROFILE
py -3 codex/scripts/sync-skills.py --home $codexUserHome
py -3 codex/scripts/sync-skills.py --home $codexUserHome --apply
```

WSLにcloneしてWindows Appへ入れる場合は、WSLで実行します。`<WindowsUser>`を自分の名前に変えてください。

```bash
windows_profile_home="/mnt/c/Users/<WindowsUser>"
python3 codex/scripts/sync-skills.py --home "$windows_profile_home"
python3 codex/scripts/sync-skills.py --home "$windows_profile_home" --apply
```

WSL CLI・macOS・Linuxでは、`--home "$HOME"` を使います。

最初の実行は差分表示だけです。`--apply`で配置します。同名スキルに独立した編集・削除・管理外ファイルがあれば止まり、上書きしません。更新も同じコマンドを使います。リポジトリ内とユーザー用の両方へ重ねて置く必要はありません。

## 2. 個人文書と共通指示を用意する

個人文書は公開フォルダーの外へ置きます。Windowsにcloneした場合：

```powershell
$privateContext = Join-Path $codexUserHome '.codex/ops-context'
py -3 codex/scripts/init-context.py --destination $privateContext
py -3 codex/scripts/install-guidance.py --home $codexUserHome --context-root $privateContext
py -3 codex/scripts/install-guidance.py --home $codexUserHome --context-root $privateContext --apply
```

WSLからWindows Appへ入れる場合：

```bash
private_context="$windows_profile_home/.codex/ops-context"
python3 codex/scripts/init-context.py --destination "$private_context"
python3 codex/scripts/install-guidance.py --home "$windows_profile_home" --context-root "$private_context"
python3 codex/scripts/install-guidance.py --home "$windows_profile_home" --context-root "$private_context" --apply
```

WSL CLI・macOS・Linuxでは、ホームを `$HOME`、個人文書を `$HOME/.codex/ops-context` にします。

| 文書 | 書くこと |
| --- | --- |
| `ME.md` | 希望と作業の進め方 |
| `PERSONAL.md` | 必要な個人情報や詳細文書への参照 |
| `PROJECTS.md` | 実際の作業場所 |
| `CANDIDATES.md` | まだ決めていないこと |

既存の文書は保ちます。共通指示の `AGENTS.md` が違う内容なら配置は止まるので、`codex/config/AGENTS.global.md` と比較して統合してください。配置スクリプトは既定の `.codex/` を使います。`CODEX_HOME`を変えている場合は、実際の配置先へ手動で反映してください。

WSLからWindows向けに生成した指示にはLinuxのパスが入るため、Windowsで読めるパスへ直します。WSLの公開フォルダーなら `//wsl.localhost/Ubuntu-24.04/home/<USER>/...`、Windowsの個人文書なら `C:/Users/<WindowsUser>/.codex/ops-context` です。

## 3. 自分の設定を入れる

`codex/config/profile.example.json` を、自分の `CODEX_HOME/ops-profile.json` へコピーして編集します。既定の場所はユーザーフォルダーの `.codex/ops-profile.json` です。既存ファイルがあれば比較して統合してください。

| 項目 | 内容 |
| --- | --- |
| `private_ops_project` | Appに登録した運用プロジェクト名。未設定ならプロジェクトなしで作成 |
| `model` / `thinking` | Intentで作るチャットの設定。nullならAppの既定値 |
| `wsl_distribution` | Linux用ツールを実行するWSLの名前 |
| `windows_codex_home` | Windowsの履歴を調べる場合の保存場所 |

Sol／Highは作者の設定例です。利用できるモデルに合わせてください。このファイルを書き換えても、既存チャットのモデルは変わりません。

`config.example.toml` は基本設定、`reference-preferences.example.toml` は作者の参考設定です。後者には `never` / `danger-full-access` もあります。必要な項目だけ反映し、認証済みの `config.toml` を丸ごと置き換えないでください。組織などの上位設定が優先します。Fast modeの有効化と、そのチャットでの選択状態も別です。

## Codex Intent

Appに `codex/` をプロジェクトとして登録し、Plugins画面で **Codex Dotfiles → Codex Intent** を導入します。対応CLIで配布元を登録する場合は、Appと同じOS・ユーザーのCLIを使います。

```text
codex plugin marketplace add <dotfiles内のcodexフォルダーの絶対パス>
```

Windows AppにはWindows／UNCパス、WSL CLIにはLinuxパスを渡します。古いCLIがこのコマンドに未対応なら、AppのPlugins画面か対応CLIを使ってください。cacheへ直接コピーしません。[公式の案内](https://developers.openai.com/plugins/build/plugins)も参照できます。

導入後、新しいチャットで依頼します。

```text
$codex-intent で受付を初期化してください。
私のprofileを読み、登録済みプロジェクトと利用できるモデルを確認してください。
受付では依頼を成果チャットへ渡し、実装や監視は成果チャットで行ってください。
```

再起動はAppが必要とする場合だけ行います。ファイル配置、スキルの検出、Intentの導入、受付の作成は別々に確認してください。

## 必要なものだけ追加する

| 用途 | 用意するもの |
| --- | --- |
| 文書・表・Computer Use | Appの公式プラグインと必要なログイン・権限 |
| Roblox・AviUtl2 | 対応アプリとMCP。そのPCの実行ファイルへ接続 |
| node_repl | Appの公式実行環境。作者のパス・pipe・trust設定はコピーしない |
| OpenAIの文書 | 公式Docs MCPか内蔵の公式文書ツール |
| Unity・VRChat | Unity・SDK・プロジェクト・Unity Skills 2.9.0のEditor package |

UnityのPythonクライアントには、`python -m pip install -r codex/config/requirements-unity.txt` でRequestsを入れます。必要なら公開フォルダー外に仮想環境を作ってください。Editorによるスキル自動同期と重複しないかも確認します。SDKの同意・投稿・アップロードは利用者の許可に従います。

agtlog・axは `python3 codex/scripts/install-research-tools.py` で予定を表示し、`--apply`で固定ファイルのhashを確認して導入します。Windowsでは `py -3` を使います。Windowsにはax、WSLにはagtlogを入れます。`agtlog.ps1`はWindows履歴をWSLでoffline閲覧する補助です。

日本語のスキルは本文を読むだけで使えます。natural-japaneseの任意の補助は `uv run`、yomiyasuの補助はPython標準ライブラリで動きます。semantic.pyは大きなモデルをダウンロードするため、必要な場合だけ使います。

Windows操作の補助には、共有lease、Unityの可視起動、公式node_replの保存先修復があります。leaseはnative Windows Pythonと実際のチャットUUIDで取得・更新・解放し、待機中は解放します。本人の停止中はWindows・ブラウザの観測と入力を止め、明示再開後に取得し直します。協調用のleaseであり、全チャットや公式ツールの権限を制御するものではありません。同じUnityプロジェクトを重複起動せず、公式ツールの停止を別のAPIで迂回しないでください。

## 更新する

既存の編集があれば差分を解決してから再同期します。中断後のlockは、同じOSで記載されたPIDが終了していると確認してから、そのlockだけを除きます。

第三者の更新では出典・ライセンス・差分を確認し、作者の改変を丸ごと消さないようにします。公開ファイルを変えたら、`files.lock.json`と該当componentのhashを更新し、`check-public.py`を実行してください。
