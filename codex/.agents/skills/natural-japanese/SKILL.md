---
name: natural-japanese
description: 日本語の新規文書で素材・読者・構成を整え、仕事文書や記事を執筆する。通常の意味を保つ推敲はyomiyasuを優先し、短い会話には適用しない。
license: MIT
metadata:
  upstream: "coji/natural-japanese@9a78a42964096da509b8f3e011f0085a5f080151"
  adaptation: "pikachu0310 / 2026-10-11"
---

# natural-japanese

伝えたい内容と読者を押さえ、素材と構成を整えてから日本語の文書にする。意味と条件の保持を優先し、短さだけを目的にしない。

## 目的に合う資料だけ使う

新規文書は、依頼と素材から読者・目的・主メッセージをつかむ。不足する事実は現物や一次資料で集め、本人の回答で結果が変わる点だけ質問する。既にある文体プロファイルは利用できるが、新しい台帳やprofileを自動で増やさない。

対応する文書なら、次から一つ選ぶ。仕事の文書を必要以上に物語の型へ当てはめない。

- 議事録：`references/doctypes/minutes.md`
- 調査レポート：`references/doctypes/report.md`
- ガイド：`references/doctypes/guide.md`
- 相談・企画メモ：`references/doctypes/memo.md`
- スライド原稿：`references/doctypes/slide.md`

文章の原則は `references/writing-constitution.md`、具体的な弱点を直す場合は `references/readability-principles.md` 等の該当資料を使う。細かな推敲はyomiyasu、技術書の論証はjapanese-tech-writing、読み物の緩急は依頼された場合のjapanese-cognitive-rhythm-writingへ役割を分け、似たskillを全部同時に読まない。

## 過去原稿の作り直し

本人の不満・原文・訂正と現在の成果を先に照合する。伝えたい機能・体験・具体例が本文や画像にあるかを確かめ、文体の改善で内容不足を代替しない。以前のAIの完成宣言だけで納得済みとせず、本文・画像候補・差込み済み画像・未確認の事実を区別して報告する。

## 仕上げの深さを選ぶ

通常は内容・構成・意味を通読して仕上げる。小変更ごとのlint、テスト、QA、多段レビューを要求しない。機械的な指摘が役立つ文書では、まとまった段階で `scripts/lint.py` 等を必要な範囲で使う。検出結果を全修正の命令や客観的な品質点と扱わない。

詳しい推敲を求められたときは[詳細な執筆・推敲](references/full-workflow.md)の必要な節を読む。文章の診断・採点だけを依頼された場合は `references/diagnose.md` を読み、依頼なく本文を改変しない。診断の数値はその定義に沿う指標であり、AIの採点を合格保証にしない。意味分析の重量級downloadは通常作業へ追加しない。

モデル設定をskillの判断で変えず、委任を許可された環境で必要な場合だけ独立レビューを使う。文書作成の依頼を公開・提出の許可へ広げない。中間メモは一時領域へ置き、本人が求めた原文比較や復元用記録は保持する。

公開元は[coji/natural-japanese](https://github.com/coji/natural-japanese)。同梱の資料・scriptsとMIT表示を保持し、本人向けの運用調整を本文に適用している。
