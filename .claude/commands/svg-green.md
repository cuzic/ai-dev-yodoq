# SVG作成: GREEN（テスト成功）フェーズ

**GREEN（🟢 テスト成功）フェーズのSVGダイアグラムを作成**

このコマンドは、TDDサイクルのGREENフェーズを視覚化するSVGダイアグラムを作成します。

## 作成するSVG

**ファイル名:** `diagram_green_phase.svg`
**配置先:** `assets/diagrams/`
**縦横比:** 16:9 (1600x900)
**用途:** GREENフェーズの説明スライド

## SVG要件

### レイアウト要件
- **viewBox:** `0 0 1600 900`（16:9比率、横長スライド用）
- **背景色:** `#FFFFFF`（白）
- **オーバーフロー防止:** すべての要素はviewBox内に収める
- **オーバーラップ防止:** 要素間に最低30pxの余白を確保

### コンテンツ構造
1. **タイトル領域（上部100px）**
   - タイトル: "🟢 GREEN（テスト成功）フェーズ"
   - フォント: Noto Sans JP, 48px, bold
   - 配置: 中央揃え

2. **メイン領域（2段構成）**
   - **上段（y: 150-450）: TDD原則の視覚化**
     - 大きな緑色のチェックマーク（中央）
     - テキスト: "テストが通る最小実装"
     - 補足: "品質は後で改善、まずは動作を優先"

   - **下段（y: 480-800）: 3カラムレイアウト**
     - **左カラム（x: 50-550）: 実装の原則**
       - 見出し: "📐 実装の原則"
       - 内容:
         - 最小実装を心がける
         - YAGNIの原則
         - テストが通ればOK
         - 過剰実装は避ける

     - **中央カラム（x: 580-1020）: 実装内容**
       - 見出し: "💻 実装内容"
       - 内容:
         - テストケースを満たす
         - エッジケースの処理
         - エラーハンドリング
         - 入力値のバリデーション

     - **右カラム（x: 1050-1550）: AI活用**
       - 見出し: "🤖 AI活用"
       - 内容:
         - 「このテストを通して」
         - コード生成の自動化
         - ベストプラクティスの適用
         - セキュリティ考慮

3. **フッター領域（下部100px）**
   - ポイント: "✅ GREENフェーズのゴール：テストを通す最小限の実装"
   - フォント: Noto Sans JP, 28px
   - 配置: 中央揃え

### スタイル指定
```css
.title {
  font-family: 'Noto Sans JP', sans-serif;
  font-size: 48px;
  font-weight: bold;
  fill: #228B22;
  text-anchor: middle;
}
.check-text {
  font-family: 'Noto Sans JP', sans-serif;
  font-size: 36px;
  font-weight: bold;
  fill: white;
  text-anchor: middle;
}
.check-subtext {
  font-family: 'Noto Sans JP', sans-serif;
  font-size: 24px;
  fill: white;
  text-anchor: middle;
}
.heading {
  font-family: 'Noto Sans JP', sans-serif;
  font-size: 32px;
  font-weight: bold;
  fill: #228B22;
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
  fill: #228B22;
  text-anchor: middle;
}
.box {
  fill: #F0FFF0;
  stroke: #228B22;
  stroke-width: 3;
  rx: 10;
}
.checkmark {
  fill: none;
  stroke: white;
  stroke-width: 40;
  stroke-linecap: round;
  stroke-linejoin: round;
}
.circle {
  fill: #228B22;
  opacity: 0.9;
}
```

### テキスト配置ルール
- **行間:** 40px
- **段落間:** 60px
- **ボックス内パディング:** 30px
- **最大テキスト幅:** カラム幅 - 60px
- **中央円のサイズ:** 直径400px、中央配置
- **チェックマーク:** 円の中央に配置

## 作成手順

1. **SVGファイルを作成:**
   - `assets/diagrams/diagram_green_phase.svg` に保存
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
  - プライマリ: #228B22（フォレストグリーン）
  - 背景: #F0FFF0（ハニーデュー）
  - テキスト: #333333（ダークグレー）
  - 白: #FFFFFF
- **チェックマーク:** SVGパスで描画（✓形状）

## 実装例

最初に構造を作成し、その後テキストを配置してください。
中央の大きな緑のチェックマークを目立たせ、GREENフェーズの達成感を視覚的に強調してください。
すべての座標を計算して、オーバーフローとオーバーラップを避けてください。

チェックマークのパス例：
```svg
<circle cx="800" cy="300" r="200" class="circle"/>
<path d="M 680,300 L 760,380 L 920,220" class="checkmark"/>
```
