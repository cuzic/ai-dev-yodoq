# SVG作成: PLAN（計画）フェーズ

**PLAN（📋 計画）フェーズのSVGダイアグラムを作成**

このコマンドは、TDDサイクルのPLANフェーズを視覚化するSVGダイアグラムを作成します。

## 作成するSVG

**ファイル名:** `diagram_plan_phase.svg`
**配置先:** `assets/diagrams/`
**縦横比:** 16:9 (1600x900)
**用途:** 計画フェーズの説明スライド

## SVG要件

### レイアウト要件
- **viewBox:** `0 0 1600 900`（16:9比率、横長スライド用）
- **背景色:** `#FFFFFF`（白）
- **オーバーフロー防止:** すべての要素はviewBox内に収める
- **オーバーラップ防止:** 要素間に最低30pxの余白を確保

### コンテンツ構造
1. **タイトル領域（上部100px）**
   - タイトル: "📋 PLAN（計画）フェーズ"
   - フォント: Noto Sans JP, 48px, bold
   - 配置: 中央揃え

2. **メイン領域（3カラム）**
   - **左カラム（x: 50-550）: 目的**
     - 見出し: "🎯 目的"
     - 内容:
       - 要件の明確化
       - 受け入れ条件の定義
       - タスクの洗い出し

   - **中央カラム（x: 580-1020）: 実施内容**
     - 見出し: "📝 実施内容"
     - 内容:
       - ユーザーストーリーの作成
       - Given-When-Then形式の受け入れ基準
       - 技術的制約の確認
       - タスクブレークダウン

   - **右カラム（x: 1050-1550）: 成果物**
     - 見出し: "📦 成果物"
     - 内容:
       - 要件定義書
       - 受け入れ基準リスト
       - タスク一覧
       - アーキテクチャ図

3. **フッター領域（下部100px）**
   - ポイント: "⚡ 急がば回れ：前工程を丁寧にやることが結果的に最速"
   - フォント: Noto Sans JP, 28px
   - 配置: 中央揃え

### スタイル指定
```css
.title {
  font-family: 'Noto Sans JP', sans-serif;
  font-size: 48px;
  font-weight: bold;
  fill: #00146E;
  text-anchor: middle;
}
.heading {
  font-family: 'Noto Sans JP', sans-serif;
  font-size: 32px;
  font-weight: bold;
  fill: #00146E;
}
.content {
  font-family: 'Noto Sans JP', sans-serif;
  font-size: 24px;
  fill: #333333;
}
.footer {
  font-family: 'Noto Sans JP', sans-serif;
  font-size: 28px;
  font-weight: bold;
  fill: #00AFF0;
  text-anchor: middle;
}
.box {
  fill: #F0F8FF;
  stroke: #00146E;
  stroke-width: 3;
  rx: 10;
}
```

### テキスト配置ルール
- **行間:** 40px
- **段落間:** 60px
- **ボックス内パディング:** 30px
- **最大テキスト幅:** カラム幅 - 60px

## 作成手順

1. **SVGファイルを作成:**
   - `assets/diagrams/diagram_plan_phase.svg` に保存
   - UTF-8エンコーディング
   - 改行コード: LF

2. **品質検証:**
   - `scripts/slides/validate_svg_bounds.py` で境界チェック
   - オーバーフロー、オーバーラップがないことを確認

3. **テスト表示:**
   - Marpスライドに埋め込んでレンダリング確認
   - ブラウザで直接開いて確認

## 注意事項

- **日本語フォント:** 'Noto Sans JP'を優先使用
- **英数字フォント:** 'Arial', sans-serifをフォールバック
- **テキストの折り返し:** `<tspan>`を使用して手動で折り返し
- **絵文字:** Unicodeで直接記述可能
- **カラーパレット:**
  - プライマリ: #00146E（濃紺）
  - セカンダリ: #00AFF0（水色）
  - 背景: #F0F8FF（アリスブルー）
  - テキスト: #333333（ダークグレー）

## 実装例

最初に構造を作成し、その後テキストを配置してください。
すべての座標を計算して、オーバーフローとオーバーラップを避けてください。
