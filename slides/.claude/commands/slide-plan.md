# Slide PLAN - Phase 1: 計画

スライド作成の計画フェーズ。レイアウト決定、内容設計、受入条件定義を行います。

## 実行タスク

### 1. スライドの概要確認

ユーザーに以下を確認：
- どのトピックのスライドを作成するか
- スライド番号（新規作成 or 既存修正）
- 前後のスライドのコンテキスト

`all_slides.md` の該当箇所を読み込み、前後のスライドを確認する。

### 2. レイアウト決定

コンテンツの特性に基づいてレイアウトを選択：

- **lead**: タイトルスライド、セクション区切り
  - H1のみ、短い説明文（50文字以内）
  - 画像・コード不要

- **layout-diagram-only**: 図表メイン
  - 画像/SVGが主役
  - テキスト最小限（0-2項目）

- **layout-horizontal-left**: 画像左、説明右
  - 図表が重要（diagram, flow, chart等）
  - 説明文が中程度（3-8項目）

- **layout-horizontal-right**: 説明左、画像右
  - テキストが主、画像は補足
  - 説明文が多め（5-8項目以上）

- **two-column**: 2つの項目を並列比較
  - Before/After、従来/改善など
  - 比較構造が明確

- **two-column compact**: 2カラムで量が多い
  - 各カラム5項目以上
  - 総項目数10以上

- **compact**: 単一カラムで量が多い
  - 箇条書き9項目以上
  - または総文字数800文字以上

- **デフォルト**: 標準的なテキストスライド
  - 箇条書き3-8項目
  - 文字数100-500文字

必要に応じて `recommend_layout.py` を実行してレイアウト候補を提案。

### 3. コンテンツ設計

以下を明確化：
- **スライドタイトル**: 明確で分かりやすいタイトル
- **箇条書き項目**: 構成と項目数（3-8項目が目安）
- **SVG図表**: 必要性と内容
  - 図表のタイプ（フローチャート、ER図、比較図など）
  - 図表に含める要素
  - ViewBoxサイズの目安

### 4. 受入条件の定義

スライドが完成したと判断する基準を明確化：

#### コンテンツ要件
- [ ] タイトルが明確で分かりやすい
- [ ] 箇条書き項目数が適切（3-8項目が目安）
- [ ] 必要な図表が含まれている
- [ ] 前後のスライドとの整合性

#### 品質要件（slidectl で測定可能）
- [ ] SVG境界オーバーフロー < 10px
- [ ] テキスト重なりなし
- [ ] 文字密度 < 80%
- [ ] 適切な余白が確保されている

#### レイアウト要件
- [ ] 指定したレイアウトクラスが適用されている
- [ ] スライド全体のバランスが良い
- [ ] 視覚的に読みやすい

### 5. タスクリスト作成

TodoWriteツールで以下のタスクを作成：
1. 判定処理の作成（RED）
2. スライドのマークダウン作成（GREEN）
3. SVG図表の作成（GREEN、必要な場合）
4. 品質向上の調整（REFACTOR）
5. 最終検証（VERIFY）

## 出力フォーマット

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 SLIDE CREATION PLAN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📌 Basic Info:
  Topic: [トピック名]
  Slide Number: #[番号] (new/update)
  Layout: [選択したレイアウト]

📝 Content Structure:
  Title: [スライドタイトル]
  Bullets: [X項目]
  SVG Diagram: [Yes/No]
    └─ Type: [図表タイプ]
    └─ Content: [図表の説明]

📍 Context:
  Previous Slide: #[番号] - [タイトル]
  Next Slide: #[番号] - [タイトル]

✅ Acceptance Criteria:

  Content Requirements:
  □ Clear and descriptive title
  □ Appropriate number of bullet points (3-8)
  □ SVG diagram included (if needed)
  □ Consistent with surrounding slides

  Quality Requirements (measurable by slidectl):
  □ SVG overflow < 10px
  □ No text overlapping
  □ Text density < 80%
  □ Proper spacing and margins

  Layout Requirements:
  □ Layout class: [選択したレイアウト]
  □ Balanced composition
  □ Visually readable

📋 Task List:
  1. [ ] Create validation script (RED)
  2. [ ] Write slide markdown (GREEN)
  3. [ ] Create SVG diagram (GREEN, if needed)
  4. [ ] Optimize quality (REFACTOR)
  5. [ ] Final verification (VERIFY)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Ready to proceed? (yes/no)
```

## ユーザー確認

計画内容をユーザーに提示し、承認を得てから次のフェーズ（RED）へ進む。

修正が必要な場合は、計画を調整してから次へ進む。
