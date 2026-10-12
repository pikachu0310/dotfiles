# dotfiles

Fish・Starship・Gitの設定と、Codexを使うための運用一式をまとめています。Codex関連はすべて `codex/` にあります。

2026年10月12日の個人環境をもとに、自作・外部由来のスキル100種類とCodex Intentを収録しました。個人文書、会話履歴、認証済み設定は含めていません。利用者が自分の情報と接続を設定して、同じ進め方を使える構成です。

## できること

- **思いつきを仕事にする** — Codex Intentの受付から、一つの成果を一つのチャットへ渡します。調査・質問・実装・修正を同じチャットで進めます。
- **必要な手順を選ぶ** — 調査、実装、日本語の文章、Web UI、Unity・VRChatのスキルを作業に合わせて使います。
- **別のPCへ運用を移す** — スキル、共通指示、空の個人文書、設定例を配置できます。既存の編集や設定があれば自動で上書きしません。

アプリの接続と認証は別途必要です。cloneしただけでは、現在の制作者と同じ実働環境にはなりません。

## まず使う

```bash
git clone https://github.com/pikachu0310/dotfiles.git
cd dotfiles
```

| 目的 | 次にすること |
| --- | --- |
| スキルをこの作業場所で試す | Codex Appに `codex/` をprojectとして追加し、新しいチャットを開始する |
| 普段の全projectでも使う | [導入手順](codex/docs/setup.md)に沿って、使用するCodexのuser profileへ配置する |
| Intentと個人運用も使う | private文書・profileを用意し、PluginsからCodex Intentを導入する |
| Unityや外部サービスも使う | 対応アプリ・公式Plugins・MCPを導入し、利用者自身のアカウントで接続する |

必要なものはPython 3.11以降とGitです。主な基準環境はWindowsのCodex AppとUbuntu-24.04 WSLです。macOS・native Linuxでもスキルと個人文書を配置できますが、Windows専用の補助機能は使いません。

Codexへ導入を任せる場合は、cloneした場所で次のように依頼できます。

```text
このREADMEとcodex/docs/setup.mdに沿って、このPCへ導入してください。
使用するCodexがWindows AppかWSL CLIかを確認し、そのuser profileを配置先にしてください。
既存のスキル・共通指示・個人文書を保ち、違う内容があれば差分を示してください。
個人文書とprofileは公開checkoutの外に置き、認証情報をコピーしないでください。
まずスキル・共通指示・Intentを用意し、必要な公式PluginsとMCPの接続を案内してください。
実際に配置・導入したものと、認証やAppでの確認が残るものを分けて報告してください。
```

## 日常の進め方

結果を変える未決定事項だけを質問し、許可された作業は進めます。既存コード・素材・標準機能を先に調べ、必要な体験の品質を保って実装します。小変更ごとのQAや固定点数を目指す推敲ループは既定にせず、まとまった段階で必要な確認を行います。未確認を成功扱いにはしません。

| 作業 | 主に使うスキル |
| --- | --- |
| 大きな判断・繰り返す不具合 | research-and-align |
| 簡潔で保守しやすい実装 | ponytail |
| 日本語の推敲 | yomiyasu |
| 新規文書の素材・構成 | natural-japanese |
| 技術文書・読み物 | japanese-tech-writing / japanese-cognitive-rhythm-writing |
| 厳しい思考点検・公開前の点検 | 依頼された場合にgrilling / prepare-release-candidate |
| Unity・VRChat制作 | Unity Skills 2.9.0 / vrc-world-development |

画像生成は、その時点の用途に合うモデルと利用可能な経路を公式資料で確認して行います。制作者の契約や過去の操作許可を、新しい利用者へ引き継ぎません。

## 再現範囲

| 収録済み | 利用者が用意するもの |
| --- | --- |
| 個別追加100スキルとIntentの計101種類 | Codex App・利用可能なモデル |
| 共通指示・設定例・個人文書の空テンプレート | 自分の背景・作業先・優先順位を入れたprivate文書 |
| 配置・同期・調査CLI・Windows操作の補助スクリプト | 公式Plugins、各MCP、対応アプリの導入・接続 |
| Unityの操作・設計手順 | Unity・SDK・実project・対応するEditor package |
| 出典・固定revision・license・内容hash | 各サービスへのログインと必要な権限 |

Gitmoji補助とWeb Design Guidelinesは、元本文の再配布条件などを理由に公開用互換版を使っています。OpenAI内蔵5種類・公式Plugin由来42種類・WSLのCloudflare系11種類は、提供元から導入する対象として記録しています。個別追加スキルの名前は省略していません。

[全除外一覧と元本文との差分](codex/docs/reproduction-and-exclusions.md)、[接続の前提と再現map](codex/config/reproduction-map.json)を参照してください。

## ファイルの役割

| 場所 | 内容 |
| --- | --- |
| `codex/.agents/skills/` | repo-localスキルの本文・参考資料・実行補助 |
| `codex/plugins/codex-intent/` | Intentの受付Plugin |
| `codex/config/AGENTS.global.md` | 共通指示のテンプレート |
| `codex/config/*.example.*` | private profileと設定の参考例。自動適用しない |
| `codex/context/examples/` | 個人文書の空テンプレート |
| `codex/scripts/` | 既存編集を保護する配置・同期と、用途別の補助スクリプト |

## 公開する情報

Codex追加分には、実際の個人文書・認証情報・会話・実projectの状態・private Git履歴を取り込んでいません。公開名・著作権表示、既存Git設定のメールと過去commitの作者情報は含まれます。

更新時は、公開対象を選んで本文と差分を確認します。`.gitignore`や削除ルールだけを根拠にprivate repo全体をコピーしません。既知のcredential形式やprivate pathの混入、収録ファイルのhashは次で確認できます。

```bash
python3 codex/scripts/check-public.py
```

この検査だけで、あらゆる自然文の個人情報を検出できるとはしていません。新しいスキルを追加するときは出典・license・差分も確認します。

## 確認済みの範囲

公開候補の本文・設定・画像・Git履歴を調査し、追加分で実際のcredentialやprivate identifierの混入は見つかりませんでした。101種類のスキルmetadataとIntentのsource契約を確認し、一時領域へ17個のskill rootを配置しました。独立した編集・既存の個人文書・共通指示を保護する動作も確認しています。

別PCでのAppへのPlugin導入、サービス認証、Editor接続、実VRの確認は行っていません。

## 出典とlicense

[収録componentと変更点](codex/config/components.json)、[第三者notice](codex/THIRD_PARTY_NOTICES.md)を掲載しています。自作部分は[MIT](codex/LICENSE)、第三者部分は各componentのlicenseに従います。認証済みサービスやゲーム素材の利用権を配布するものではありません。

配布形式は[OpenAI公式のPlugin案内](https://developers.openai.com/plugins/build/plugins)、設定項目は[公式configuration案内](https://developers.openai.com/codex/config-file/config-basic)を参照しています。
