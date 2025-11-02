# SVG作成: REFACTOR（リファクタリング）フェーズ

**REFACTOR（🔧 リファクタリング）フェーズのSVGダイアグラムを作成**

このコマンドは、TDDサイクルのREFACTORフェーズを視覚化するSVGダイアグラムを作成します。

## 作成するSVG

**ファイル名:** `diagram_refactor_phase.svg`
**配置先:** `assets/diagrams/`
**縦横比:** 16:9 (1600x900)
**用途:** REFACTORフェーズの説明スライド

## SVG要件

### レイアウト要件
- **viewBox:** `0 0 1600 900`（16:9比率、横長スライド用）
- **背景色:** `#FFFFFF`（白）
- **オーバーフロー防止:** すべての要素はviewBox内に収める
- **オーバーラップ防止:** 要素間に最低30pxの余白を確保

### コンテンツ構造
1. **タイトル領域（上部100px）**
   - タイトル: "🔧 REFACTOR（リファクタリング）フェーズ"
   - フォント: Noto Sans JP, 48px, bold
   - 配置: 中央揃え

2. **メイン領域（Before/After比較）**
   - **左半分（x: 50-750）: Before（改善前）**
     - 見出し: "❌ Before（改善前）"
     - 背景: ライトグレー
     - 内容の視覚化:
       - コードの重複
       - 長すぎる関数
       - 不明確な変数名
       - 複雑な条件分岐
     - テキスト例を吹き出しで表示

   - **中央（x: 750-850）: 矢印**
     - 大きな右向き矢印
     - テキスト: "改善"

   - **右半分（x: 850-1550）: After（改善後）**
     - 見出し: "✅ After（改善後）"
     - 背景: ライトブルー
     - 内容の視覚化:
       - DRY原則適用
       - 単一責任の原則
       - 明確な命名
       - シンプルな構造
     - テキスト例を吹き出しで表示

3. **下部領域（y: 650-800）: リファクタリングの観点（4つのボックス）**
   - **ボックス1（x: 50-400）: 重複削減**
     - アイコン: "📦"
     - 内容: DRY原則、共通化

   - **ボックス2（x: 430-780）: 可読性**
     - アイコン: "📖"
     - 内容: 命名改善、コメント

   - **ボックス3（x: 810-1160）: 構造**
     - アイコン: "🏗️"
     - 内容: 責任分離、疎結合

   - **ボックス4（x: 1190-1550）: パフォーマンス**
     - アイコン: "⚡"
     - 内容: 最適化、効率化

4. **フッター領域（下部100px）**
   - ポイント: "🛡️ テストがあるから安心してリファクタリングできる"
   - フォント: Noto Sans JP, 28px
   - 配置: 中央揃え

### スタイル指定
```css
.title {
  font-family: 'Noto Sans JP', sans-serif;
  font-size: 48px;
  font-weight: bold;
  fill: #FF8C00;
  text-anchor: middle;
}
.heading-before {
  font-family: 'Noto Sans JP', sans-serif;
  font-size: 32px;
  font-weight: bold;
  fill: #DC143C;
}
.heading-after {
  font-family: 'Noto Sans JP', sans-serif;
  font-size: 32px;
  font-weight: bold;
  fill: #228B22;
}
.content {
  font-family: 'Noto Sans JP', sans-serif;
  font-size: 22px;
  fill: #333333;
}
.arrow-text {
  font-family: 'Noto Sans JP', sans-serif;
  font-size: 28px;
  font-weight: bold;
  fill: #FF8C00;
  text-anchor: middle;
}
.box-heading {
  font-family: 'Noto Sans JP', sans-serif;
  font-size: 28px;
  font-weight: bold;
  fill: #FF8C00;
  text-anchor: middle;
}
.footer {
  font-family: 'Noto Sans JP', sans-serif;
  font-size: 28px;
  font-weight: bold;
  fill: #FF8C00;
  text-anchor: middle;
}
.before-bg {
  fill: #F5F5F5;
  stroke: #DC143C;
  stroke-width: 3;
  rx: 10;
}
.after-bg {
  fill: #F0F8FF;
  stroke: #228B22;
  stroke-width: 3;
  rx: 10;
}
.small-box {
  fill: #FFF8DC;
  stroke: #FF8C00;
  stroke-width: 3;
  rx: 10;
}
```

### テキスト配置ルール
- **行間:** 35px
- **段落間:** 50px
- **ボックス内パディング:** 25px
- **最大テキスト幅:** カラム幅 - 50px
- **矢印サイズ:** 幅100px、高さ80px

## 作成手順

1. **SVGファイルを作成:**
   - `assets/diagrams/diagram_refactor_phase.svg` に保存
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
  - プライマリ: #FF8C00（ダークオレンジ）
  - Before側: #F5F5F5（グレー背景）、#DC143C（赤枠線）
  - After側: #F0F8FF（ブルー背景）、#228B22（緑枠線）
  - ボックス背景: #FFF8DC（コーンシルク）
  - テキスト: #333333（ダークグレー）

## 実装例

最初に構造を作成し、その後テキストを配置してください。
Before/Afterの対比を明確にし、リファクタリングの効果を視覚的に強調してください。
すべての座標を計算して、オーバーフローとオーバーラップを避けてください。

矢印のパス例：
```svg
<polygon points="750,350 850,300 850,330 920,330 920,370 850,370 850,400" fill="#FF8C00"/>
```
