# Codex dotfiles

Codexへ意図を渡し、必要な文脈を選び、一つの成果を同じチャットで完成させる個人運用の公開候補。2026年10月12日の環境から、仕組み・スキル・Intent・導入手順を切り出した。

Codex用のファイルは `codex/` にまとめている。private環境、認証済み設定、会話履歴、private Git履歴はコピーしていない。利用者自身の設定・context・認証は別に用意する。

## 再現できるもの

| 収録 | 内容 |
| --- | --- |
| `codex/.agents/skills/` | 現行の個人スキル、出典と再配布条件を確認した第三者スキル、Unity Skills 2.9.0の未接続suite |
| `codex/plugins/codex-intent/` | 薄い受付、一成果一チャット、固定タイトル、pin、Local／Worktree、利用者profileに基づくモデル指定 |
| `codex/config/AGENTS.global.md` | 現行の進め方・質問・検査量・権限境界を保った共通指示テンプレート |
| `codex/context/examples/` | 本人情報・詳細情報・作業先・未決定事項の空テンプレート |
| `codex/scripts/` | スキル同期、共通指示の配置、context初期化、研究CLI導入、Windowsの操作lease・Unity可視起動・公式runtime復旧・受付shortcut |
| `codex/config/components.json` | 出典、固定revision、license、公開用の差分 |
| `codex/config/research-tools.json` | agtlog・axの版、asset、SHA-256 |

再現するのは運用の仕組み。過去チャットの結論、個人の生活情報、実プロジェクトの素材・状態、接続サービスの認証、Pro契約・利用枠、App内のpin・project登録・automationsは含まない。利用者自身の情報と認証を加えると、その環境で同じ方法を使える。

## 進め方

一つの成果の調査・質問・実装・修正は同じチャットで行う。結果を変える未決定事項だけ質問し、許可された作業は再承認待ちにしない。既存コード・素材・標準機能を先に調べ、必要な体験の品質を保つ。まとまった実装の後、必要な確認だけをまとめる。小変更ごとのQA、固定自己採点の反復、活動台帳は既定にしない。未確認を成功扱いにはしない。

- 大きな判断・繰り返す不具合は `research-and-align`。原因候補と観察を分け、本人の原文を現在の成果物と照合する。
- 実装を簡潔に仕上げる場合は `ponytail`。再利用を理由に見た目・音・作者の素材を削らない。
- 日本語の推敲は `yomiyasu`。新規文書の素材と構成は `natural-japanese`、技術文書の論証と読み物の緩急はそれぞれ専用スキル。
- `grilling` は厳しい思考点検を求めた場合、`prepare-release-candidate` は公開前の点検を求めた場合に使う。
- VRChatでは `vrc-world-development` と必要なUnityモジュールを使う。
- 画像は最新の用途に合うモデルを公式資料で確認し、利用者が許可した経路で生成する。制作者の画像モデル名やPro契約を、別アカウントの利用可能性と扱わない。

## 別の環境に導入する

Python 3.11以降、Git、必要ならCodex CLIを用意する。Windows AppとUbuntu-24.04 WSLが主な構成。macOS・native Linuxではスキルとcontextを使えるが、Windows専用helperは使わない。

1. まず公開内容を読む。このフォルダーをCodexのprojectに追加し、`codex/` を作業場所にするとrepo-localのスキルを使える。
2. 普段の全projectでも使う場合は、以下でuser skillsへ配布する。repo-local版とglobal版の両方を同時に登録する必要はない。既存の同名スキルが違う内容なら停止し、自動で上書きしない。

```bash
python3 codex/scripts/sync-skills.py --home "$HOME"
python3 codex/scripts/sync-skills.py --home "$HOME" --apply
```

Windowsではnative Pythonと自分のprofile pathを使う。WSL PythonからWindowsへ配置する場合は、その人の `/mnt/c/Users/<USER>` を `--home` に渡す。既定で制作者のprofileへ書き込まない。

3. private contextを公開checkoutの外に作る。

```bash
python3 codex/scripts/init-context.py --destination "$HOME/.codex/ops-context"
```

`ME.md`・`PERSONAL.md`・`PROJECTS.md`・`CANDIDATES.md`を自分で埋める。実プロジェクトのpath・優先順位・背景はここだけに置く。既存の文書を上書きしない。

4. 共通指示を配置する。既存のAGENTSがある場合は差分を統合してから配置する。scriptに強制上書きはない。

```bash
python3 codex/scripts/install-guidance.py --home "$HOME" --context-root "$HOME/.codex/ops-context"
python3 codex/scripts/install-guidance.py --home "$HOME" --context-root "$HOME/.codex/ops-context" --apply
```

5. `codex/config/profile.example.json` を **自分のprivate profile** にコピーし、運用project・モデル・推論強度・OS・履歴の場所を選ぶ。例にあるSol／Highは制作者の選択で、必須の利用契約ではない。`codex/config/config.example.toml` は設定項目の例。認証済みのconfig.tomlを上書きしない。App側の既存チャットを自動で変更しない。

6. Intentのmarketplaceを登録する。CLIが対応していなければAppの公式Plugins画面を使う。App付属の新しいCLIと、PATH上の古いCLIは区別する。

```bash
codex plugin marketplace add ./codex
```

AppのPlugins画面で **Codex Dotfiles → Codex Intent** をインストールする。cacheへ直接コピーしない。必要な場合だけAppを再起動し、新しいチャットで `$codex-intent` にprivate profileと保存済みの運用projectを渡して受付を初期化する。`codex/config/profile.example.json` を埋めただけでApp設定が変わったとは扱わない。

7. agtlog／axは必要な実行環境に導入する。最初のcommandは計画だけ、次は固定assetのhashを確認して配置する。

```bash
python3 codex/scripts/install-research-tools.py
python3 codex/scripts/install-research-tools.py --apply
```

Windowsではaxを導入し、agtlogはWSL側へ導入する。`codex/scripts/agtlog.ps1` はその人のWindows履歴をWSLへ渡すlauncher。global環境変数は変更せず、offlineで読む。

日本語の本文を読んで書くことにPython依存は不要。任意のlint helperは、natural-japaneseのPEP 723宣言を `uv run` で使う。semantic.pyは別のopt-inで、大きなembedding modelを初回downloadするため通常の文章作業へ組み込まない。yomiyasuのhelperと公開用のsetup/check scriptは標準ライブラリで動く。これらの依存やモデルをexport作業でインストールしていない。

8. 公式のsystem skillsとComputer Use・Drive・Pages・Sites・artifact等のPluginsはAppから各自で導入・認証する。cache、token、cookie、内部connector IDをこのrepoへ入れない。WSLのCloudflare連携も提供元の導入経路を使う。

## Unity／VRChat

収録suiteはUnity Skills **2.9.0**。スキルの配置だけではEditor APIは動かない。各利用者のUnity projectに対応packageを導入し、通常のEditor設定から接続する。Python clientには[Requests](https://pypi.org/project/requests/)が必要。Unity操作に使うPython環境で `python -m pip install -r codex/config/requirements-unity.txt` を実行する。既存のPython環境を変更したくなければ、公開checkout外にvenvを作る。Editorの自動skill同期との重複に注意し、どのcopyを正本とするか選ぶ。制作者の既存Editorやpackageはこの公開作業で更新していない。

Scene・SDKの状態は所有するチャットが保つ。古いbuilderの再実行で作者や本人の修正を消さない。ClientSim、実VR、複数人、SDK uploadの確認範囲を分ける。SDKの同意・投稿・アップロードは、新しい利用者が対象と内容を許可した範囲だけ行う。

## Computer Use

現在提供される正式なWindows／browser toolを使い、providerの停止・権限と本人のPC操作停止を守る。Windows用leaseは協調するチャット間の競合を減らすだけで、全チャットを強制停止する機構ではない。

`codex/scripts/windows-computer-use-lease.py` はnative Windows Pythonで使う。実thread UUIDでacquireし、各call前にrenew、短い観察→入力→確認の後にreleaseする。本人がPCを使う間はpauseし、browserとWindowsの観測・入力を止める。本人の明示再開後に新しく取得・観察する。待機中は解放する。

GUI操作するUnityは `start-unity-visible.ps1` でNormal起動し、同projectのEditorを重複起動しない。`repair-windows-node-repl-assets.py` は、その環境の公式Windows node_replが示すasset保存先の欠損を直すhelper。read-only診断から始め、必要時だけ `--repair` を使う。provider構成が違えば停止する。Chromeの失敗をnative APIのブラウザ操作へ迂回しない。

## 公開用とprivateの境界

実環境のcontext・config・session・DB・cache・log・鍵・メール・会話・画像参照は取り込まない。自動exportでprivate repo全体をコピーせず、公開対象を選んでレビューする。コピー時の削除ルールだけや.gitignoreだけを漏えい対策の根拠にしない。

```bash
python3 codex/scripts/check-public.py
```

これは収録ファイルのhash・禁止path・既知のcredential形式・個人path・private thread URLを確認する。意味上の個人情報を完全に検出する保証はない。更新時は内容も読み、利用者固有の許可を公開版へ持ち込んでいないことを確かめる。実データを誤ってGitへ入れた場合は、公開を止め、必要ならcredentialを失効させる。private repoのvisibilityを変更して公開しない。

## 来歴と差分

[収録component](codex/config/components.json)と[第三者notice](codex/THIRD_PARTY_NOTICES.md)を参照。原文の再配布条件を確認できなかったGitmoji補助と、mutableな外部命令に依存していたWeb Design Guidelinesは、以前の公開版で作った互換版を使う。privateの導入fileとは同一ではない。

公開版の主な差分は、個人path・実task番号・制作project・生活情報の除去、利用者profileへのモデル／projectの移動、VRCの過去の操作許可の除去。調査・実装の進め方と必要な品質は維持している。旧snapshotにあった `open-in-vscode`・`iterate-to-evidence`・`grill-me` など、今の環境から外したものは戻していない。

## 確認した範囲

公開用の選択した本文・path・許可の意味を確認し、既知のcredential形式とprivate入力の混入を検査した。101件のSkill metadataとIntentのsource契約を確認し、一時的な空のユーザー領域へ17個のskill rootを配置した。独立した編集、既存の個人文書・共通指示を保護し、公開checkout内への実context作成を拒否することを確認した。

別PCでのAppへのplugin導入、サービス認証、Editor接続、実VRの確認は行っていない。これらは各利用者が公式経路で行う。配布源の検査と実環境での成功を区別する。

新しい第三者版へ更新するときは、固定revision・license・差分を確認し、制作者向け改変を丸ごと上流で上書きしない。本人情報と配布する仕組みを別に保つ。

Pluginとmarketplaceの配布形式は[OpenAI公式の配布案内](https://developers.openai.com/plugins/build/plugins)、設定項目は[公式configuration案内](https://developers.openai.com/codex/config-file/config-basic)に基づく。

[MIT](codex/LICENSE)対象の自作部分と、個別licenseの第三者部分を分けている。OpenAI公式配布物、認証済みサービス、ゲーム素材の利用権を再配布するものではない。
