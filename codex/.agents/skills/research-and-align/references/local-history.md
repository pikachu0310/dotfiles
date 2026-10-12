# Codexの本人発言を必要な範囲で探す

この運用では：現在の作業に関係する過去の発言は、依頼を待たず自主的に探す。無関係な履歴を一括で読み込まず、本人の訂正と現在の成果を回収できたところで止める。

## 探索の順序

1. 正式な `list_threads` のtitle・summaryから候補を選ぶ。`read_thread`は最初にcommand outputなしで読み、userMessageと関連する最終成果へ絞る。必要なら古いpageをたどる。
2. 用語や原文を探す場合は、WSLの `~/.local/bin/agtlog` を使う。Windows Appの履歴は利用者のWindows CODEX_HOME（既定はuser profile配下の.codex）、WSL CLIの履歴は `~/.codex`。WindowsのディレクトリをWSLのpathへ変換した値をWINDOWS_CODEX_HOMEへ設定する。検索対象を混同しない。
3. 本人発言を読んで、現在のファイル・実装・画像などへ戻る。過去のAIが「完成」「反映」と言っただけで、現物や現在の版を確認したことにしない。

## agtlogの使い方

```bash
~/.local/bin/agtlog search '探す語' --agent codex --codex-dir "$WINDOWS_CODEX_HOME" --since 7d --kind user --limit 8 --offline
~/.local/bin/agtlog search '探す語' --session 'codex:<thread UUID>' --codex-dir "$WINDOWS_CODEX_HOME" --kind user --limit 8 --offline
~/.local/bin/agtlog show 'codex:<thread UUID>' --codex-dir "$WINDOWS_CODEX_HOME" --kind user,assistant-text --offset <event index> --limit 4 --full --offline
```

CLIは0.4.2。`--offline`を付け、価格のdownloadを行わない。本人のPro料金・利用枠はAPI換算のcostから推測せず、必要なら正式なusage toolで読む。`show`ではthinkingやtool outputを初回から展開しない。

`search`のkindを指定しないと、AI文やtool出力の引用にもヒットする。user検索でもharnessの注入文が含まれることがあるため、原文の内容と発言の由来を確認する。`show`のoffsetは全timeline内のindexであり、kindを絞った配列の順番ではない。続きは `page.next_offset` を使う。

WindowsパスをLinuxで読むと、project名がUNCやWindowsパス全体になることがある。`--project <project-name>`が空でも履歴不在と判断せず、正式なthread UUIDか実際のcwdを使う。

warnings・`page.complete`・truncatedを読み、結果が不完全なら公式thread toolか対象のraw logを必要な発言に限定して確認する。0.4.2では、この環境の重複sessionで`unaddressable_session`を確認した。Appで読めるthreadがCLIでは`not_found`になることもあるため、空結果を履歴不在の根拠にしない。広い探索には時間がかかることがあり、毎回全履歴を検索しない。未対応の古いlog、破損、権限の問題を空結果として隠さない。履歴やcacheをGitへ保存せず、外部の検索サービスや画像生成へ送らない。
