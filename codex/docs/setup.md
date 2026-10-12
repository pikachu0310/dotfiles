# 導入手順

まずスキルとIntentを導入し、必要なアプリ・サービスの接続を追加します。公開ファイルには、制作者の認証情報や実projectの設定は含まれていません。

## 配置先を選ぶ

| 使うCodex | スキル・共通指示を置くuser profile | 操作する環境 |
| --- | --- | --- |
| WindowsのCodex App | Windowsのuser profile | Windowsでcloneしたrepoならnative Python。WSLのrepoならWSL PythonからWindows側へ配置 |
| WSLのCodex CLI | WSLのhome | 対象のWSL内でPythonを実行 |
| macOS・native Linux | そのOSのhome | そのOSのPythonを実行 |

**Windows Appを使うときに、WSLのhomeへ配置してもWindows側への導入にはなりません。** CLIのPlugin登録先も同様です。Windows App向けの登録は、native Windowsの対応CLIまたはAppのPlugins画面で行います。

以下のcommandは、cloneしたdotfilesのrootで実行します。Pythonは3.11以降を使います。

## 1. スキルを配置する

このrepoだけで試す場合は、Appに `codex/` をprojectとして追加します。repo-localスキルが読み込まれるため、global配置は不要です。

普段の全projectでも使う場合は、次のいずれかでuser skillsへ配置します。最初は差分表示だけ、`--apply`で配置します。既存の同名スキルが違う内容なら止まります。変更を捨てず、差分を解決してから再実行してください。

### Windows上へcloneした場合

native Windows PowerShellで実行します。

```powershell
$codexUserHome = $env:USERPROFILE
py -3 codex/scripts/sync-skills.py --home $codexUserHome
py -3 codex/scripts/sync-skills.py --home $codexUserHome --apply
```

`py`がない場合は、そのPCにインストールしたPython 3.11以降のcommandへ置き換えます。

### WSL上のrepoからWindows Appへ配置する場合

WSL内で実行します。`<WindowsUser>`は自分のWindowsユーザー名に置き換えます。

```bash
windows_profile_home="/mnt/c/Users/<WindowsUser>"
python3 codex/scripts/sync-skills.py --home "$windows_profile_home"
python3 codex/scripts/sync-skills.py --home "$windows_profile_home" --apply
```

### WSL CLI・macOS・native Linuxへ配置する場合

そのOS内で実行します。

```bash
python3 codex/scripts/sync-skills.py --home "$HOME"
python3 codex/scripts/sync-skills.py --home "$HOME" --apply
```

repo-local版とglobal版を、同じスキルの導入手段として重ねる必要はありません。スキルの更新では同じscriptを使います。配布先の独立した編集・削除・管理外ファイルがあれば全体の更新を止め、上書きしません。

## 2. 個人文書と共通指示を用意する

private文書は公開checkoutの外に作ります。下のscriptは既存の文書を上書きしません。`ME.md`に希望、`PERSONAL.md`に必要な詳細の参照、`PROJECTS.md`に実際の作業先、`CANDIDATES.md`に未決定事項を記入します。

Windows上のrepoから使う場合：

```powershell
$codexUserHome = $env:USERPROFILE
$privateContext = Join-Path $codexUserHome '.codex/ops-context'
py -3 codex/scripts/init-context.py --destination $privateContext
py -3 codex/scripts/install-guidance.py --home $codexUserHome --context-root $privateContext
py -3 codex/scripts/install-guidance.py --home $codexUserHome --context-root $privateContext --apply
```

WSL内のrepoからWindows Appへ配置する場合：

```bash
windows_profile_home="/mnt/c/Users/<WindowsUser>"
private_context="$windows_profile_home/.codex/ops-context"
python3 codex/scripts/init-context.py --destination "$private_context"
python3 codex/scripts/install-guidance.py --home "$windows_profile_home" --context-root "$private_context"
python3 codex/scripts/install-guidance.py --home "$windows_profile_home" --context-root "$private_context" --apply
```

WSL CLI・macOS・native Linuxの場合は、`--home`へ `$HOME`、`--context-root`へ `$HOME/.codex/ops-context` を渡します。

既存の `AGENTS.md` が違う内容なら配置は止まります。`codex/config/AGENTS.global.md` と既存の共通指示を比較し、必要な規則を統合してください。scriptに強制上書きはありません。

WSLから配置した共通指示のpathがWindows Appで解決できない場合は、Windows側で読めるUNC pathへ置き換えます。たとえばWSLの公開sourceは `//wsl.localhost/Ubuntu-24.04/home/<USER>/...`、Windowsのprivate文書は `C:/Users/<WindowsUser>/.codex/ops-context` のように記載します。sourceの所在と実行OSを混同しないでください。

## 3. private profileを用意する

`codex/config/profile.example.json` を、使用するCodexの `CODEX_HOME/ops-profile.json` へコピーして編集します。`CODEX_HOME`が未指定なら、そのuser profileの `.codex/ops-profile.json` です。既存fileがある場合は比較して統合します。

| 項目 | 意味 |
| --- | --- |
| `private_ops_project` | Appに保存した自分の運用project名。未設定ならprojectlessを使う |
| `model` / `thinking` | Intentで新しいチャットを作るときの明示設定。nullならApp既定を使う |
| `wsl_distribution` | Linux toolingを実行するWSLの名前 |
| `windows_codex_home` | Windows履歴を調べる場合の実際の所在 |

Sol／Highは制作者の設定例です。利用できるモデルと本人の選択に合わせます。profileの編集だけで既存チャットの実設定が変わることはありません。

`config.example.toml` は基本項目、`reference-preferences.example.toml` は制作者の非機微な保存設定の参考例です。後者には `never` / `danger-full-access` も含みます。必要な項目だけを自分の正式設定へ適用し、認証済みconfig.tomlを丸ごと置き換えないでください。上位policyがある環境では、その制約が優先します。Fast modeの機能flagと、現在のチャットでの選択状態は分けて確認します。

## 4. Codex Intentを導入する

Appに `codex/` をprojectとして登録し、Plugins画面の **Codex Dotfiles** から **Codex Intent** を導入します。

対応するCLIでmarketplaceを登録する場合は、**使用するAppと同じOS／user profileのCLI** を使います。

```text
codex plugin marketplace add <cloneしたdotfiles内のcodexフォルダーの絶対path>
```

Windows App向けならnative WindowsのCLIへWindows／UNC pathを渡します。WSL CLI向けならWSL内のCLIへLinux pathを渡します。PATH上の古いCLIがPlugin commandに対応していなければ、Appの公式Plugins画面か対応CLIを使います。cacheへ直接コピーしません。

導入後、新しいチャットで次のように依頼します。

```text
$codex-intent で受付を初期化してください。
私のprivate profileを読み、保存済みprojectと実際に利用できるモデルを確認してください。
この受付では意図を一つの成果チャットへ渡し、成果の実装や監視は行わないでください。
```

Appの仕様上、必要な場合だけ再起動します。新しく導入したスキルの検出、Pluginの導入、実際の受付作成はそれぞれ確認します。

## 5. 必要な接続を追加する

| 機能 | 導入するもの・確認すること |
| --- | --- |
| 公式文書・artifact・Computer Use等 | Appの公式Pluginsと、必要なアカウント接続・権限 |
| Roblox | Roblox Studioと対応するMCP proxy。そのPCのlauncherへ接続 |
| AviUtl2 | AviUtl2とagent MCP。そのPCの実行fileへ接続 |
| 公式node_repl | Appが提供するruntimeと対応provider。制作者のpath・pipe・trust bindingをコピーしない |
| OpenAI Docs MCP | 公式documentation MCP、または利用可能な内蔵公式文書tool |
| Unity／VRChat | Unity・SDK・対象project・Unity Skills 2.9.0のEditor package |

公式スキルの配布file、token、cookie、内部connector IDはこのrepoへ入れません。新PCでのApp／Plugin導入と各サービスの再認証は別途行います。[必要な種類と除外一覧](reproduction-and-exclusions.md)を参照してください。

Unity clientにはRequestsが必要です。Unity操作に使うPython環境で次を実行します。必要なら公開checkout外にvenvを作ります。

```bash
python -m pip install -r codex/config/requirements-unity.txt
```

Editorの自動skill同期との重複も確認します。SceneとSDK進行は所有するチャットが保ち、古いbuilderの再生成で本人の修正を消さないようにします。SDK同意・投稿・uploadは、その利用者が対象と内容を許可した範囲で扱います。

## 用途別の補助機能

### agtlogとax

最初は計画だけを表示し、`--apply`で固定assetのhashを確認して配置します。

```bash
python3 codex/scripts/install-research-tools.py
python3 codex/scripts/install-research-tools.py --apply
```

native Windowsでは `py -3` を使います。Windowsにはaxを導入し、agtlogはWSL側で導入します。`agtlog.ps1` はWindows履歴をWSLへ渡すlauncherで、global環境変数を変更せずofflineで読みます。

### 日本語の補助script

文章の執筆・推敲には、スキル本文を読むだけで使えます。任意のnatural-japanese lint helperはPEP 723宣言を `uv run` で使います。semantic.pyは大きなmodelを初回downloadするopt-inで、通常の文章作業へ組み込みません。yomiyasuのhelperは標準ライブラリで動きます。

### Windows操作と復旧

`windows-computer-use-lease.py` はnative Windows Pythonで実行します。実thread UUIDでacquireし、各call前にrenew、短い観察→入力→確認の後にreleaseします。本人がPCを使う間はpauseし、browserとWindowsの観測・入力を止めます。明示再開後は新しいleaseと観察から再開し、待機中は解放します。leaseは協調するチャット間の仕組みで、全チャットやproviderの権限を制御するものではありません。

GUI操作するUnityは `start-unity-visible.ps1` でNormal起動し、同projectのEditorを重複起動しません。`repair-windows-node-repl-assets.py` は公式runtimeのasset保存先の欠損を診断し、必要時だけ `--repair` で復元します。provider構成が違えば停止します。Chromeの失敗をnative APIのブラウザ操作へ迂回しません。

これらの補助scriptは各OSでの通常の実行方法を使い、既存の実行policyを恒久変更しません。

## 更新する

スキルの配置後に独立した編集を加えた場合、同期scriptは上書きせず停止します。sourceと配布先の差分を解決してから再実行します。中断後のlockが残った場合は、記載されたPIDが終了していることを同じ実行OSで確認してからlockだけを除きます。

第三者版を更新するときは、固定revision・license・差分を確認します。制作者向けの改変を上流版で丸ごと上書きしません。公開対象を変更した場合は本文をレビューし、`files.lock.json` とcomponentsのhashを更新してから公開検査を行います。
