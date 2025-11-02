# Slide TDD Commands - スライド作成にTDDを適用

このディレクトリには、スライド作成にTDD（Test-Driven Development）の考え方を適用するカスタムスラッシュコマンドが含まれています。

## 🔄 Slide TDDサイクル

```
PLAN → RED → GREEN → REFACTOR → VERIFY
 📋     🔴     🟢       🔧         ✅
```

## 📚 利用可能なコマンド

### `/generate-slides` 📄 原稿からスライド骨組み生成

**原稿テキストからMarpスライドの骨組みを自動生成するコマンド。**

原稿を適切な粒度でスライドに分割し、各スライドに最適なレイアウトを自動選択します。生成された骨組みは `/slide-tdd` で詳細化することを前提としています。

**主な機能**:
- 原稿の構造分析（H1/H2/H3、箇条書き、画像）
- 適切な粒度でのスライド分割
- 自動レイアウト選択（lead, horizontal-left, compact等）
- TODO コメントでの `/slide-tdd` 連携

**ワークフロー**:
```
/generate-slides → /slide-tdd × N → 完成スライド
     ⬇️                ⬇️
  骨組み作成        詳細作成・品質向上
```

---

### `/slide-tdd` ⭐ メインコマンド

**スライド作成のTDDサイクル全体を順次実行する統合コマンド。**

すべてのフェーズ（PLAN → RED → GREEN → REFACTOR → VERIFY）を自動的に順次実行します。各フェーズ終了時にユーザーの承認を得ながら進めます。

このコマンド1つで、計画から最終検証までを完了できます。

---

### 個別フェーズコマンド

特定のフェーズだけを実行したい場合に使用します。

#### `/slide-plan`
**Phase 1: 計画**
- レイアウト決定（lead, layout-horizontal-left等）
- コンテンツ設計（タイトル、箇条書き、SVG図表）
- 受入条件の定義
- タスクリストの作成

#### `/slide-red`
**Phase 2: 判定処理作成**
- スライド検証スクリプトの作成
- 受入条件のコード化
- 初回実行と失敗確認（RED状態）

#### `/slide-green`
**Phase 3: 最小実装**
- スライドのマークダウン作成
- SVG図表の作成（必要な場合）
- 判定処理のパス確認（GREEN状態）

#### `/slide-refactor`
**Phase 4: 品質向上**
- slidectl による品質測定
- SVG境界の調整
- 文字サイズの最適化
- レイアウトの微調整

#### `/slide-verify`
**Phase 5: 最終検証**
- 受入条件の最終チェック
- コンテキストの確認
- 視覚的確認
- ドキュメント化

---

## 🎯 使い方の例

### 新しいスライドを作成する場合

#### 方法1: `/slide-tdd` で全フェーズを実行（推奨）

```bash
/slide-tdd
```

1. **PLAN**: スライドのトピック、レイアウト、受入条件を決定
2. **RED**: 検証スクリプトを作成し、失敗を確認
3. **GREEN**: スライドとSVG図表を作成し、検証をパス
4. **REFACTOR**: slidectl で品質測定し、改善
5. **VERIFY**: 最終確認し、本番準備完了

すべて自動的に順次実行され、各フェーズで確認を取りながら進みます。

#### 方法2: フェーズごとに個別実行

特定のフェーズだけを実行したい場合や、途中から再開したい場合：

1. **計画を立てる**
   ```bash
   /slide-plan
   ```
   - レイアウト: layout-horizontal-left
   - SVG図表: ER図が必要
   - 受入条件: オーバーフロー < 10px

2. **判定処理を作成（RED）**
   ```bash
   /slide-red
   ```
   - validate_slide_42.py を作成
   - 実行して失敗を確認

3. **スライドを作成（GREEN）**
   ```bash
   /slide-green
   ```
   - all_slides.md にスライド追加
   - diagram_07_er_diagram.svg を作成
   - 検証スクリプトがパス

4. **品質向上（REFACTOR）**
   ```bash
   /slide-refactor
   ```
   - SVGオーバーフロー: 45px → 8px
   - フォントサイズ調整
   - スコア: 75 → 92

5. **最終検証（VERIFY）**
   ```bash
   /slide-verify
   ```
   - すべての受入条件をパス
   - 視覚的確認OK
   - 本番準備完了

---

## 🛠️ slidectl との連携

このTDDサイクルでは、`$HOME/slidectl` の以下の機能を活用します：

### 1. 品質測定機能
- Playwrightによる文字密度測定
- 余白の定量評価
- テキスト重なり検出

### 2. SVG境界検証
- `validate_svg_bounds.py` でViewBox超過チェック
- オーバーフロー量の測定
- 推奨ViewBoxサイズの算出

### 3. レイアウト推奨
- `recommend_layout.py` でレイアウト提案
- コンテンツ解析に基づく判定
- 箇条書き項目数、文字数、画像有無の考慮

---

## 💡 ベストプラクティス

### Test-First Approach（テストファースト）
- 必ず判定処理を先に作成
- 受入条件を明確にしてからスライド作成
- RED → GREEN の順序を守る

### Quality-Driven Refactoring（品質駆動のリファクタリング）
- slidectl のメトリクスを活用
- データに基づいて改善
- 小さな変更を積み重ねる
- 継続的に品質を測定

### Context Awareness（コンテキスト意識）
- 前後のスライドとの整合性を重視
- セクション全体の流れを考慮
- 重複する内容を避ける

### Visual Excellence（視覚的な卓越性）
- 読みやすさを最優先
- フォントサイズは十分に大きく（最小40px）
- 適切な余白を確保
- 色のコントラストを確保

---

## 📊 成功基準

以下をすべて満たせば成功とします：

### 必須条件
- ✅ すべての受入条件をパス
- ✅ SVG境界オーバーフロー < 10px
- ✅ テキスト重なりなし
- ✅ 文字密度 < 80%
- ✅ 指定レイアウトが適用されている

### 推奨条件
- ✅ 前後のスライドとの整合性
- ✅ 総合スコア 85/100 以上（slidectl使用時）
- ✅ 視覚的に美しく読みやすい
- ✅ ドキュメントが適切に記録されている

---

## 🎨 サポートされるレイアウト

### 1. `lead`
- **用途**: タイトルスライド、セクション区切り
- **特徴**: 中央揃え、大きいフォント
- **条件**: H1のみ、テキスト最小限

### 2. `layout-diagram-only`
- **用途**: 図表・画像メイン
- **特徴**: 図表を大きく表示
- **条件**: 画像あり、テキスト最小限

### 3. `layout-horizontal-left`
- **用途**: 画像左、説明右
- **特徴**: 図表を優先的に表示
- **条件**: 図表が重要、説明3-8項目

### 4. `layout-horizontal-right`
- **用途**: 説明左、画像右
- **特徴**: テキストを優先的に表示
- **条件**: テキストが主、画像は補足

### 5. `two-column`
- **用途**: 2つの項目を並列比較
- **特徴**: 左右均等分割
- **条件**: Before/After等の比較構造

### 6. `two-column compact`
- **用途**: 2カラムで量が多い
- **特徴**: フォントサイズ縮小、パディング削減
- **条件**: 各カラム5項目以上

### 7. `compact`
- **用途**: 単一カラムで量が多い
- **特徴**: フォントサイズ縮小、行間縮小
- **条件**: 箇条書き9項目以上

### 8. デフォルト（クラス指定なし）
- **用途**: 標準的なテキストスライド
- **特徴**: 通常フォント、通常間隔
- **条件**: 箇条書き3-8項目

---

## 🔧 関連ツール

```bash
# SVG境界検証
python3 validate_svg_bounds.py

# レイアウト推奨
python3 recommend_layout.py

# Marpレンダリング
npx @marp-team/marp-cli all_slides.md -o index.html --html

# slidectl 品質測定（オプション）
cd $HOME/slidectl
uv run slidectl measure --slide [番号] --html [path/to/index.html]
```

---

## 📖 参考資料

- [LAYOUT_RECOMMENDATION_SPEC.md](../LAYOUT_RECOMMENDATION_SPEC.md)
- [slidectl README](../../../slidectl/README.md)
- [Marp Documentation](https://marpit.marp.app/)

---

**作成者**: Claude Code
**対象プロジェクト**: ai-dev-yodoq/slides
**slidectl**: $HOME/slidectl
**バージョン**: 1.0
