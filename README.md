# dotfiles

普段使っているFish・Starship・Gitの設定と、Codexのスキル・運用手順です。WindowsのCodex AppとUbuntu WSLを中心に使っています。

```bash
git clone https://github.com/pikachu0310/dotfiles.git
cd dotfiles
```

| 使いたいもの | 読むところ |
| --- | --- |
| Fish・Starship・Git | [シェル設定](docs/shell.md) |
| Codexのスキルと共通指示 | [Codexの導入手順](codex/docs/setup.md) |
| Codex Intentの受付 | [導入手順のIntent設定](codex/docs/setup.md#codex-intent) |
| 収録スキルの出典・変更点 | [出典一覧](codex/config/components.json) |
| 収録していないもの・再現できる範囲 | [再現範囲と除外一覧](codex/docs/reproduction-and-exclusions.md) |

## Codexを使う

`codex/`をCodex Appのプロジェクトに追加すると、このリポジトリのスキルを試せます。普段のプロジェクトでも使うには、導入手順に沿って自分のユーザーフォルダーへ配置してください。Windows AppとWSL CLIでは配置先が違います。

100種類のスキルとCodex Intentを収録しています。調査・実装・日本語の文章・Web UI・Unity・VRChatに使えます。Intentは、思いつきや依頼を成果ごとのチャットへ振り分ける受付です。

運用では、既存のコードや素材を先に調べ、結果が変わる選択だけを質問します。小変更のたびにテストを繰り返さず、まとまった段階で必要な確認をします。

導入をCodexへ任せるなら、次のように依頼してください。

```text
READMEとcodex/docs/setup.mdを読んで、このPCへ導入してください。
Windows App／WSL CLIの配置先を確認し、既存の設定や編集は保ってください。
個人文書と認証情報は公開フォルダーの外に置いてください。
導入済みのものと、ログイン・アプリ接続などが残るものを報告してください。
```

## 公開しているもの

スキル、共通指示、空の個人文書、設定例、配置用スクリプトを収録しています。本人の個人文書・会話・認証情報は含めていません。公開名と既存のGit設定・コミットのメールアドレスは残しています。

別PCでも同じ進め方を使えますが、Codex App、公式プラグイン、各サービスへのログイン、Unityなどの接続は別途必要です。別PCでのアプリ・Editor接続までは確認していません。

自作部分は[MIT](codex/LICENSE)、第三者のスキルは[各ライセンス](codex/THIRD_PARTY_NOTICES.md)に従います。公開ファイルの整合性と既知の認証情報の形式は、`python3 codex/scripts/check-public.py`で検査できます。
