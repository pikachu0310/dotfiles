# 再現範囲と除外一覧

100スキルとCodex Intentを収録しています。運用手順は移せますが、本人の個人文書、ログイン状態、アプリ接続までは配布していません。以下は2026年10月12日の照合結果です。

| 収録しているもの | 利用者が用意するもの |
| --- | --- |
| スキル100種類とIntent | スキルの配置とIntentの導入 |
| 共通指示・空の個人文書・設定例 | 自分の背景、作業場所、利用可能なモデル |
| 連携の手順と補助スクリプト | 公式プラグイン、各MCP、必要なアプリと認証 |
| Unity Skills 2.9.0とVRCの手順 | Unity・SDK・実プロジェクト・Editor package |

参考設定は自動適用しません。保存されたモデル・Fast modeの設定と、実行中チャットの選択状態は別に確認します。別PCでのアプリ導入・認証・Editor接続は未確認です。

## 元の本文と違うもの

17個のスキルフォルダーの入口を比較すると、改行を除いて11個は現行環境と同じです。次の6個とIntentは公開向けに変更しています。Unityの84種類も省略せず収録しています。

| スキル | 公開用の変更 |
| --- | --- |
| ax | 個人のWindowsパスを置換 |
| frontend-ui-engineering | 参考文書をスキル内へ移動し、配置先に依存しない参照へ修正 |
| unity-skills | 対応条件を本文へ移動。ローカルの接続情報を除外 |
| vrc-world-development | 個人パス・実タスク例を一般化。作者の過去のSDK操作許可を除外 |
| git-commit-style-gitmoji | 元本文の再配布条件を確認できず、自作の互換版を収録。日本語指定などは元版と異なる |
| web-design-guidelines | 毎回最新版を取得する元の処理を、固定したMITのルールと自作の互換版へ変更。更新・報告方法が異なる |

Intentは利用者のprofileを読む公開版です。Brainstorming、Grilling、日本語のスキル、Ponytailは残しています。

## 提供元から導入するスキル

以下は現行環境から削除したものではありません。公式の更新・権限管理を保つため、配布ファイルを複製せず、提供元から導入する対象として記録しています。ファイルの存在だけで、現在のチャットで使えることや実行済みであることは判断しません。

**Windows内蔵5種類**：`imagegen`, `openai-docs`, `review-agent`, `skill-creator`, `skill-installer`

<details>
<summary>Windowsの公式プラグイン由来42種類（クリックして表示）</summary>

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

20種類のartifact-templateも、この42種類に含みます。

</details>

**WSLのCloudflare系11種類**：`agents-sdk`, `cloudflare`, `cloudflare-email-service`, `cloudflare-one`, `cloudflare-one-migrations`, `durable-objects`, `sandbox-sdk`, `turnstile-spin`, `web-perf`, `workers-best-practices`, `wrangler`

WSL内蔵のplugin-creatorも含めていません。WSLの旧接続設定を、Windows Appの必須設定として移すことはしません。

## 以前外したもの

Antigravity codex-handoff、open-in-vscode、iterate-to-evidence、opportunity-solution-tree、workshop-facilitation、旧grill-me、公式Unityプラグイン、旧Computer Useバックアップ、VRC以外の古いWSLリンクは戻していません。公開のために現行スキルを追加で削除したものではありません。

## 個人情報の確認

公開追加分の本文・設定・スクリプト・Git履歴を確認し、既知の認証情報の形式と、実際の認証情報・個人識別子との一致を調べました。追加分に混入は見つかりませんでした。収録画像も公開元と同一で、文字やEXIFのmetadataを持ちません。

公開名・著作権表示・出典URL、既存のGit設定とコミットのメールアドレスは残しています。認証済み設定、個別の信頼パス、本人の個人文書は追加していません。自動検査だけで、自然文に含まれるあらゆる個人情報を検出できるわけではありません。

詳しい一覧は[再現設定](../config/reproduction-map.json)、出典・固定版・差分は[収録component](../config/components.json)を参照してください。
