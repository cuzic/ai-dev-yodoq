# SVG作成: RED（テスト失敗）フェーズ

**RED（🔴 テスト失敗）フェーズのSVGダイアグラムを作成**

このコマンドは、TDDサイクルのREDフェーズを視覚化するSVGダイアグラムを作成します。

## 作成するSVG

**ファイル名:** `diagram_red_phase.svg`
**配置先:** `assets/diagrams/`
**縦横比:** 16:9 (1600x900)
**用途:** REDフェーズの説明スライド

## SVG要件

### レイアウト要件
- **viewBox:** `0 0 1600 900`（16:9比率、横長スライド用）
- **背景色:** `#FFFFFF`（白）
- **オーバーフロー防止:** すべての要素はviewBox内に収める
- **オーバーラップ防止:** 要素間に最低30pxの余白を確保

### コンテンツ構造
1. **タイトル領域（上部100px）**
   - タイトル: "🔴 RED（テスト失敗）フェーズ"
   - フォント: Noto Sans JP, 48px, bold
   - 配置: 中央揃え

2. **メイン領域（2段構成）**
   - **上段（y: 150-450）: TDD原則の視覚化**
     - 大きな赤色の円（中央）
     - テキスト: "まず失敗するテストを書く"
     - 補足: "実装がないので、テストは必ず失敗する"

   - **下段（y: 480-800）: 3カラムレイアウト**
     - **左カラム（x: 50-550）: 書くテスト**
       - 見出し: "✍️ 書くテスト"
       - 内容:
         - Given: 前提条件
         - When: 実行する操作
         - Then: 期待する結果
         - 失敗メッセージの確認

     - **中央カラム（x: 580-1020）: 注意点**
       - 見出し: "⚠️ 注意点"
       - 内容:
         - 1機能1テスト
         - 具体的なアサーション
         - 境界値のテスト
         - エッジケースのカバー

     - **右カラム（x: 1050-1550）: AI活用**
       - 見出し: "🤖 AI活用"
       - 内容:
         - テストシナリオからテストコード生成
         - Given-When-Then形式の指示
         - モックの自動生成
         - 境界値の網羅

3. **フッター領域（下部100px）**
   - ポイント: "💡 REDフェーズのゴール：正しく失敗するテストを作る"
   - フォント: Noto Sans JP, 28px
   - 配置: 中央揃え

### スタイル指定
```css
.title {
  font-family: 'Noto Sans JP', sans-serif;
  font-size: 48px;
  font-weight: bold;
  fill: #DC143C;
  text-anchor: middle;
}
.circle-text {
  font-family: 'Noto Sans JP', sans-serif;
  font-size: 36px;
  font-weight: bold;
  fill: white;
  text-anchor: middle;
}
.circle-subtext {
  font-family: 'Noto Sans JP', sans-serif;
  font-size: 24px;
  fill: white;
  text-anchor: middle;
}
.heading {
  font-family: 'Noto Sans JP', sans-serif;
  font-size: 32px;
  font-weight: bold;
  fill: #DC143C;
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
  fill: #DC143C;
  text-anchor: middle;
}
.box {
  fill: #FFF5F5;
  stroke: #DC143C;
  stroke-width: 3;
  rx: 10;
}
.circle {
  fill: #DC143C;
  opacity: 0.9;
}
```

### テキスト配置ルール
- **行間:** 40px
- **段落間:** 60px
- **ボックス内パディング:** 30px
- **最大テキスト幅:** カラム幅 - 60px
- **中央円のサイズ:** 直径400px、中央配置

## 作成手順

1. **SVGファイルを作成:**
   - `assets/diagrams/diagram_red_phase.svg` に保存
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
  - プライマリ: #DC143C（赤）
  - 背景: #FFF5F5（ライトピンク）
  - テキスト: #333333（ダークグレー）
  - 白: #FFFFFF

## 実装例

最初に構造を作成し、その後テキストを配置してください。
中央の大きな赤い円を目立たせ、REDフェーズの重要性を視覚的に強調してください。
すべての座標を計算して、オーバーフローとオーバーラップを避けてください。
