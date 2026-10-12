# 再現範囲と除外したもの

2026年10月12日に、公開候補の追加差分と現行Windows profileのファイル・保存設定を再照合した。ファイルの存在、設定上のenabled、現在のpromptへの表示、実行成功は区別する。

## 結論

現行の個別追加スキル100種類はすべて同じ名前で収録し、Intentを含めて101種類。運用ルールとスキルを持つ環境は構築できるが、現在動いているCodex Appの接続・認証・個人文脈までcloneだけで再現する配布物にはなっていない。

| 部分 | 公開候補 | 同じように使うために必要なもの |
| --- | --- | --- |
| 個別追加100スキル・Intent | 名前をすべて収録 | user skillsかrepo-localを選んで配置、Intentはmarketplaceから導入 |
| 個人運用の進め方 | 公開用へ一般化した共通指示とprivate context template | 利用者自身の文脈・作業先・優先順位をprivateに記入 |
| モデル・推論・動作設定 | Sol／Highの例と非機微な参考設定 | 利用可能なモデルを選び、正式な設定経路へ適用 |
| OpenAI公式skills・Plugins | 提供元から導入する名前を記録、cacheは非収録 | 対応するApp・Pluginsの導入、必要な認証・権限 |
| Roblox／AviUtl2／公式node_repl／Docs MCP | 接続の前提を記録 | 各PCで対応アプリ・MCPを導入し、その環境の実体へ接続 |
| Unity／VRChat | Unity Skills 2.9.0とVRCの制作手順 | Unity・SDK・対象project・対応するEditor packageと接続 |
| 本人の背景・会話・認証・pin | 非収録 | 同じ本人が別PCで使う場合も、privateな移行・再認証が別途必要 |

`reference-preferences.example.toml` は制作者の保存設定のうち機微でない項目を表した参考例。自動適用されず、組織やprojectの上位policyが優先する。Fast modeの機能を有効にするflagと、現在のチャットでFastが選択されていることは同一ではない。保存済みのモデル設定だけから、すべての実行中turnのモデルを証明しない。

## 元の本文と違うもの

17個のskill rootの入口を改行末尾だけ正規化して比べると、11個は現行本文と一致した。違いは次の6個と、公開版Intentのprofile化。Unityの84個を省略したという意味ではない。

| スキル | 公開用の差分 |
| --- | --- |
| ax | 制作者のWindows絶対pathを利用者向けのpathへ変更 |
| frontend-ui-engineering | 支援文書をskill内へ移し、global配置でも参照できるよう修正 |
| unity-skills | compatibility要件を本文へ移動。未接続の公開suiteとして収録し、local bindingを除外 |
| vrc-world-development | 実task例・個人pathを一般化し、制作者の過去のSDK操作許可を除去 |
| git-commit-style-gitmoji | 元本文の再配布条件を確認できず、以前作った公開互換版を収録。元版の日本語指定などと完全同一ではない |
| web-design-guidelines | 元の毎回最新rulesを取得するwrapperを収録せず、固定したMITのrulesと公開互換版を収録。更新方式と報告方法が異なる |

日本語文書、Brainstorming、Grilling、Ponytailなどを、公開のために勝手に減らしていない。Unityの必要なmodule名もすべて残っている。元の進め方を完全に同一にしたい場合、上の互換版の差分とprivate profileの内容を確認する。

## 配布ファイルを収録しない公式skills

これらは現行環境から削除したものではなく、提供元の配布・権限・更新経路に残すもの。Appの内蔵・Plugin cacheや認証済み接続を複製しない。

### Windows内蔵5種類

`imagegen`, `openai-docs`, `review-agent`, `skill-creator`, `skill-installer`

### Windows公式Plugin由来42種類

- `Presentations`
- `Spreadsheets`
- `artifact-template-analytics-dashboard`
- `artifact-template-business-review`
- `artifact-template-design-report`
- `artifact-template-experiment-analysis`
- `artifact-template-financial-budget`
- `artifact-template-investment-committee-memo`
- `artifact-template-legal-memorandum`
- `artifact-template-market-trends-report`
- `artifact-template-minimal-letterhead`
- `artifact-template-operating-calendar`
- `artifact-template-operating-review`
- `artifact-template-project-kickoff`
- `artifact-template-project-tracker`
- `artifact-template-sales-pipeline`
- `artifact-template-simple-dark-mode`
- `artifact-template-simple-light-mode`
- `artifact-template-strategy-memorandum`
- `artifact-template-system-design`
- `artifact-template-team-alignment`
- `artifact-template-three-statement-forecast`
- `computer-use`
- `create-pet`
- `documents`
- `excel-live-control`
- `google-docs`
- `google-drive`
- `google-drive-comments`
- `google-sheets`
- `google-slides`
- `maintain-space`
- `manage-schedules`
- `organize-space`
- `pdf`
- `pets`
- `plugin-management`
- `sites`
- `template-creator`
- `update-pet`
- `visualize`
- `write-page`

20個のartifact-templateもこの42種類に含む。cached fileがあることは、このチャットにすべてのmetadataが表示されることや、すべてが実行済みであることを意味しない。

### WSLのCloudflare系11種類

`agents-sdk`, `cloudflare`, `cloudflare-email-service`, `cloudflare-one`, `cloudflare-one-migrations`, `durable-objects`, `sandbox-sdk`, `turnstile-spin`, `web-perf`, `workers-best-practices`, `wrangler`

WSL内蔵のplugin-creatorも非収録。WSL側の旧設定と現在のWindows Appの接続を混同せず、不要な古い接続を公開版の必須導入にしない。

## 以前外したものは戻していない

- `Antigravity codex-handoff`
- `open-in-vscode`
- `iterate-to-evidence`
- `opportunity-solution-tree`
- `workshop-facilitation`
- `grill-me (former public wrapper)`
- `official Unity plugin`
- `old Computer Use backup plugin`
- `old WSL reference links other than VRC`

これらの除外は、今回の公開のために現行のスキルを追加で削除したものではない。

## 再確認した公開境界

公開する追加分の全text、設定・スクリプト、既知のcredential形式、private path・実thread URL、実際の認証ファイルの機微な値とprivate identifierとの一致を確認した。画像は固定された公開元とGit blob identityが一致し、PNGのtext／EXIF metadataを持たない。

追加分で実際のcredential・private identifierの混入は見つからなかった。公開名・著作権表示・公開元URLは残る。これは自然文の個人情報をあらゆる形で自動検出する保証ではない。

既存dotfilesの.gitconfigと過去commitの作者情報にはメールアドレスがある。これは以前から公開されている部分で、今回のCodex追加で変更・消去していない。repository全体を「個人情報なし」とは報告しない。旧設定・Git履歴の整理を行う場合は、Codex追加とは別の対象と操作になる。

詳しい種類別一覧は[再現map](../config/reproduction-map.json)、snapshotの本文hash・来歴は[components](../config/components.json)を参照。
