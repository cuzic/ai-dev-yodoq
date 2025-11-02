# SVG作成: VERIFY（検証）フェーズ

**VERIFY（✅ 検証）フェーズのSVGダイアグラムを作成**

このコマンドは、TDDサイクルのVERIFYフェーズを視覚化するSVGダイアグラムを作成します。

## 作成するSVG

**ファイル名:** `diagram_verify_phase.svg`
**配置先:** `assets/diagrams/`
**縦横比:** 16:9 (1600x900)
**用途:** VERIFYフェーズの説明スライド

## SVG要件

### レイアウト要件
- **viewBox:** `0 0 1600 900`（16:9比率、横長スライド用）
- **背景色:** `#FFFFFF`（白）
- **オーバーフロー防止:** すべての要素はviewBox内に収める
- **オーバーラップ防止:** 要素間に最低30pxの余白を確保

### コンテンツ構造
1. **タイトル領域（上部100px）**
   - タイトル: "✅ VERIFY（検証）フェーズ"
   - フォント: Noto Sans JP, 48px, bold
   - 配置: 中央揃え

2. **メイン領域（4段階の検証フロー）**
   - **上段（y: 150-250）: フローチャート**
     - 4つのステップを横に並べる
     - 各ステップを矢印で接続
     - ステップ: テスト実行 → カバレッジ → AI自己レビュー → 品質確認

   - **中段（y: 280-550）: 4カラムレイアウト**
     - **カラム1（x: 50-400）: ステップ1**
       - アイコン: "🧪"
       - 見出し: "テスト実行"
       - 内容:
         - 全テスト実行
         - 成功確認
         - エラー検出
         - 境界値テスト

     - **カラム2（x: 430-780）: ステップ2**
       - アイコン: "📊"
       - 見出し: "カバレッジ"
       - 内容:
         - カバレッジ測定
         - 80%以上確認
         - 未カバー特定
         - 追加テスト

     - **カラム3（x: 810-1160）: ステップ3**
       - アイコン: "🤖"
       - 見出し: "AI自己レビュー"
       - 内容:
         - コードレビュー
         - セキュリティ
         - パフォーマンス
         - ベストプラクティス

     - **カラム4（x: 1190-1550）: ステップ4**
       - アイコン: "✅"
       - 見出し: "品質確認"
       - 内容:
         - すべてグリーン
         - ドキュメント更新
         - コミット準備
         - レビュー依頼

3. **下部領域（y: 580-750）: Trust but Verify原則**
   - 大きなボックス（中央）
   - 見出し: "🛡️ Trust but Verify原則"
   - 内容:
     - AIを信頼する（Trust）
     - しかし必ず検証する（Verify）
     - 自動テストで継続的に確認
     - カバレッジツールで可視化

4. **フッター領域（下部150px）**
   - ポイント: "💡 VERIFYフェーズのゴール：品質を担保し、安心してリリースできる状態にする"
   - フォント: Noto Sans JP, 28px
   - 配置: 中央揃え

### スタイル指定
```css
.title {
  font-family: 'Noto Sans JP', sans-serif;
  font-size: 48px;
  font-weight: bold;
  fill: #4169E1;
  text-anchor: middle;
}
.step-circle {
  fill: #4169E1;
  stroke: #00146E;
  stroke-width: 3;
}
.step-text {
  font-family: 'Noto Sans JP', sans-serif;
  font-size: 20px;
  font-weight: bold;
  fill: white;
  text-anchor: middle;
}
.icon {
  font-family: 'Noto Sans JP', sans-serif;
  font-size: 48px;
  text-anchor: middle;
}
.heading {
  font-family: 'Noto Sans JP', sans-serif;
  font-size: 28px;
  font-weight: bold;
  fill: #4169E1;
  text-anchor: middle;
}
.content {
  font-family: 'Noto Sans JP', sans-serif;
  font-size: 22px;
  fill: #333333;
}
.principle-heading {
  font-family: 'Noto Sans JP', sans-serif;
  font-size: 32px;
  font-weight: bold;
  fill: #4169E1;
  text-anchor: middle;
}
.footer {
  font-family: 'Noto Sans JP', sans-serif;
  font-size: 28px;
  font-weight: bold;
  fill: #4169E1;
  text-anchor: middle;
}
.column-box {
  fill: #F0F8FF;
  stroke: #4169E1;
  stroke-width: 3;
  rx: 10;
}
.principle-box {
  fill: #E6F3FF;
  stroke: #4169E1;
  stroke-width: 4;
  rx: 15;
}
.arrow {
  fill: #4169E1;
}
```

### テキスト配置ルール
- **行間:** 38px
- **段落間:** 55px
- **ボックス内パディング:** 30px
- **最大テキスト幅:** カラム幅 - 60px
- **ステップ円のサイズ:** 直径80px
- **矢印サイズ:** 幅60px、高さ30px

## 作成手順

1. **SVGファイルを作成:**
   - `assets/diagrams/diagram_verify_phase.svg` に保存
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
  - プライマリ: #4169E1（ロイヤルブルー）
  - セカンダリ: #00146E（濃紺）
  - 背景: #F0F8FF（アリスブルー）
  - 原則ボックス背景: #E6F3FF（ライトブルー）
  - テキスト: #333333（ダークグレー）
  - 白: #FFFFFF

## 実装例

最初に構造を作成し、その後テキストを配置してください。
4段階の検証フローを明確にし、Trust but Verify原則を視覚的に強調してください。
すべての座標を計算して、オーバーフローとオーバーラップを避けてください。

フローチャートの円とテキスト例：
```svg
<!-- ステップ1 -->
<circle cx="215" cy="200" r="40" class="step-circle"/>
<text x="215" y="195" class="step-text">テスト</text>
<text x="215" y="215" class="step-text">実行</text>

<!-- 矢印 -->
<polygon points="260,200 320,190 320,210" class="arrow"/>
```

Trust but Verifyボックス例：
```svg
<rect x="400" y="580" width="800" height="170" class="principle-box"/>
<text x="800" y="620" class="principle-heading">🛡️ Trust but Verify原則</text>
```
