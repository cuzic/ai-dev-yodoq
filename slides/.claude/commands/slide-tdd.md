# Slide TDD Development Cycle - スライド作成にTDDを適用

このコマンドは、スライド作成にTDD（Test-Driven Development）の考え方を適用し、高品質なスライドを段階的に作成します。

## 🔄 実行フロー

```
PLAN → RED → GREEN → REFACTOR → VERIFY
 📋     🔴     🟢       🔧         ✅
```

各フェーズを順次実行し、ユーザーの承認を得ながら進めます。

---

## 前提条件

- **slidectl**: `$HOME/slidectl` にインストールされている
- **作業ディレクトリ**: `/home/cuzic/ai-dev-yodoq/slides`
- **スライドファイル**: `all_slides.md` (Marp形式)
- **SVGディレクトリ**: `diagrams/`

---

## Phase 1: PLAN 📋（計画）

### 目的
どのようなスライドを作成するか明確にし、受入条件を定義する

### 実行内容

1. **スライドの概要確認**
   - どのトピックのスライドを作成するか確認
   - 前後のスライドのコンテキストを確認
   - `all_slides.md` の該当箇所を読み込み

2. **レイアウト決定**
   - `recommend_layout.py` を実行してレイアウト候補を提案
   - コンテンツに応じて最適なレイアウトを選択：
     - `lead`: タイトルスライド、セクション区切り
     - `layout-diagram-only`: 図表メイン
     - `layout-horizontal-left/right`: 画像とテキストの横並び
     - `two-column`: 2つの項目を並列比較
     - `compact`: コンテンツ量が多い
     - デフォルト: 標準的なテキストスライド

3. **コンテンツ設計**
   - スライドタイトルを決定
   - 箇条書き項目の構成を決定
   - SVG図表が必要かどうか判断
   - 必要なSVG図表の内容を明確化

4. **受入条件の定義**
   - **コンテンツ要件**:
     - タイトルが明確か
     - 箇条書き項目数が適切か（3-8項目が目安）
     - 図表が必要な場合は含まれているか

   - **品質要件** (slidectl で測定可能):
     - 文字密度: 適切な範囲内か
     - SVG境界: オーバーフロー < 10px
     - テキスト重なり: 重なりなし
     - 余白: 適切な余白があるか

   - **レイアウト要件**:
     - 指定したレイアウトクラスが適用されているか
     - スライド全体のバランスが良いか

5. **TodoList作成**
   - 実装するタスクをTodoWriteで管理
   - タスクの優先順位を決定

### 出力

計画のサマリーを表示し、ユーザーの承認を得る:
```
📋 スライド作成計画
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📌 トピック: [トピック名]
📌 レイアウト: [選択したレイアウト]
📌 図表: [必要/不要]

📝 コンテンツ構成:
  - タイトル: [タイトル]
  - 箇条書き: [X項目]
  - SVG図表: [図表の説明]

✅ 受入条件:
  1. タイトルと箇条書きが明確
  2. SVG境界オーバーフロー < 10px
  3. テキスト重なりなし
  4. [レイアウト]クラスが適用されている

続行しますか？
```

---

## Phase 2: RED 🔴（判定処理作成）

### 目的
スライドが完成しているかを自動判定する処理を作成する

### 実行内容

1. **判定スクリプトの作成**
   - スライド番号を特定
   - 判定用のPythonスクリプトを作成
   - slidectl の機能を活用:
     - `validate_svg_bounds.py` を参考にSVG境界チェック
     - Playwrightによる文字密度測定
     - テキスト重なり検出

2. **判定基準の実装**
   ```python
   # 例: スライド判定スクリプト
   def validate_slide(slide_number: int) -> dict:
       """
       スライドが受入条件を満たすか判定

       Returns:
           dict: {
               'passed': bool,
               'errors': list[str],
               'warnings': list[str],
               'metrics': dict
           }
       """
       errors = []
       warnings = []

       # 1. スライド存在チェック
       if not slide_exists(slide_number):
           errors.append(f"Slide {slide_number} not found")

       # 2. レイアウトクラスチェック
       expected_layout = "layout-horizontal-left"
       actual_layout = get_slide_layout(slide_number)
       if actual_layout != expected_layout:
           errors.append(f"Layout mismatch: expected {expected_layout}, got {actual_layout}")

       # 3. SVG境界チェック（該当する場合）
       if has_svg(slide_number):
           svg_overflow = check_svg_overflow(slide_number)
           if svg_overflow > 10:
               errors.append(f"SVG overflow: {svg_overflow}px")

       # 4. テキスト密度チェック
       text_density = measure_text_density(slide_number)
       if text_density > 0.8:  # 80%以上は詰め込みすぎ
           warnings.append(f"Text density too high: {text_density:.0%}")

       return {
           'passed': len(errors) == 0,
           'errors': errors,
           'warnings': warnings,
           'metrics': {
               'svg_overflow': svg_overflow if has_svg(slide_number) else 0,
               'text_density': text_density
           }
       }
   ```

3. **初回実行（失敗確認）**
   - 判定スクリプトを実行
   - まだスライドが存在しないため、失敗することを確認
   - エラーメッセージが適切であることを確認

### 確認ポイント

- 判定スクリプトが作成されたか
- スクリプトが失敗したか（期待通り）
- エラーメッセージは明確か

ユーザーの確認を得てから次のフェーズへ。

---

## Phase 3: GREEN 🟢（最小実装）

### 目的
判定処理がパスする最低限のスライドを作成する

### 実行内容

1. **スライドのマークダウン作成**
   - `all_slides.md` に新しいスライドを追加
   - 基本構造を実装:
     ```markdown
     ---

     <!-- _class: layout-horizontal-left -->

     # スライドタイトル

     ![width:900px](diagrams/diagram_XX.svg)

     - 箇条書き項目1
     - 箇条書き項目2
     - 箇条書き項目3
     ```

2. **SVG図表の作成（必要な場合）**
   - Claude Codeに依頼してSVG図表を生成
   - `diagrams/diagram_XX.svg` として保存
   - ViewBoxサイズを適切に設定（オーバーフロー防止）
   - width指定を追加（Marp表示用）

3. **Marpでレンダリング**
   - `npx @marp-team/marp-cli all_slides.md -o index.html --html`
   - HTMLが正常に生成されることを確認

4. **判定処理の実行**
   - RED フェーズで作成した判定スクリプトを実行
   - すべての受入条件をパスすることを確認
   - 結果を表示:
     ```
     ✅ Slide validation PASSED

     📊 Metrics:
       - SVG overflow: 3px (< 10px ✓)
       - Text density: 45% (< 80% ✓)
       - Layout: layout-horizontal-left ✓
       - Content items: 5 ✓
     ```

### 確認ポイント

- スライドが作成されたか
- 判定処理がパスしたか
- 最低限の品質基準を満たしているか

ユーザーの確認を得てから次のフェーズへ。

---

## Phase 4: REFACTOR 🔧（品質向上）

### 目的
slidectl の測定機能を使って、スライドの品質をさらに向上させる

### 実行内容

1. **詳細な品質測定**
   - `validate_svg_bounds.py` でSVG境界を精密測定
   - Playwrightで視覚的な品質を測定
   - スライド全体のバランスを確認

2. **文字サイズの最適化**
   - テキスト密度が高い場合:
     - フォントサイズを削減（例: 24px → 20px）
     - `compact` レイアウトに変更を検討
   - テキスト密度が低い場合:
     - フォントサイズを拡大
     - より大きなレイアウトを検討

3. **SVG図表の調整**
   - オーバーフロー検出時:
     - ViewBoxを拡大
     - テキストを複数行に分割
     - フォントサイズを縮小
   - 表示サイズの調整:
     - width指定を最適化
     - アスペクト比を維持

4. **レイアウトの微調整**
   - 箇条書き項目数に応じてレイアウト変更:
     - 3-8項目: デフォルト
     - 9項目以上: compact
     - 比較構造: two-column
   - 画像とテキストのバランス調整

5. **継続的な測定とフィードバック**
   - 各変更後に判定処理を実行
   - スコアの改善を確認
   - 品質メトリクスの推移を表示

### 出力例

```
🔧 Refactoring in progress...

📊 Before:
  - SVG overflow: 15px
  - Text density: 72%
  - Score: 75/100

🔨 Applied changes:
  1. Expanded ViewBox: 1400x800 → 1600x850
  2. Reduced font size: 24px → 20px
  3. Split long title into 2 lines

📊 After:
  - SVG overflow: 4px ✅
  - Text density: 58% ✅
  - Score: 92/100 ✅

Improvement: +17 points
```

### 確認ポイント

- 品質スコアが向上したか
- すべての基準を満たしているか
- 見た目のバランスが良いか

ユーザーの確認を得てから次のフェーズへ。

---

## Phase 5: VERIFY ✅（最終検証）

### 目的
前後のコンテキストと受入条件を踏まえて、完成度を最終確認

### 実行内容

1. **コンテキストの確認**
   - 前のスライドとの繋がりを確認
   - 次のスライドへの流れを確認
   - セクション全体の整合性を確認

2. **受入条件の最終チェック**
   - PLANフェーズで定義した全受入条件を再確認
   - 各項目をチェックリスト形式で検証:
     ```
     ✅ 受入条件チェック:
     ✓ タイトルが明確で分かりやすい
     ✓ 箇条書きが3-8項目の範囲内
     ✓ SVG図表が適切に含まれている
     ✓ SVG境界オーバーフロー < 10px
     ✓ テキスト重なりなし
     ✓ layout-horizontal-left が適用
     ✓ 文字密度が適切（< 80%）
     ✓ 前後のスライドとの整合性
     ```

3. **全体品質スコアの確認**
   - slidectl での総合評価
   - 各メトリクスの最終値を表示
   - 改善の余地があれば提案

4. **視覚的確認**
   - `index.html` をブラウザで表示
   - スライドの見た目を人間がチェック
   - 読みやすさ、理解しやすさを確認

5. **ドキュメント化**
   - スライド作成の経緯をコメントとして記録
   - 使用したレイアウトの理由を文書化
   - 特記事項があれば記録

### 出力

```
✅ VERIFY COMPLETE

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 Final Quality Report
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Slide: #42 - データベーススキーマ設計

✅ Acceptance Criteria: ALL PASSED
  ✓ Title: clear and descriptive
  ✓ Bullet points: 5 items (within 3-8)
  ✓ SVG diagram: included and proper
  ✓ SVG overflow: 3px (< 10px)
  ✓ Text overlap: none
  ✓ Layout: layout-horizontal-left
  ✓ Text density: 52% (< 80%)
  ✓ Context: consistent with surrounding slides

📈 Quality Metrics:
  - Overall score: 95/100 ⭐
  - SVG quality: 98/100
  - Layout score: 92/100
  - Readability: 96/100

🎯 Status: READY FOR PRODUCTION

Files modified:
  - all_slides.md (added slide #42)
  - diagrams/diagram_07_er_diagram.svg (created)
  - index.html (regenerated)

Next steps:
  1. Commit changes: git add . && git commit
  2. Push to GitHub: git push
  3. Verify on GitHub Pages

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 🎯 使い方

### 統合コマンド（推奨）

```bash
/slide-tdd
```

すべてのフェーズを順次実行し、各フェーズでユーザーの確認を取りながら進めます。

### 個別フェーズの実行

特定のフェーズだけを実行したい場合：

```bash
/slide-plan      # Phase 1: 計画
/slide-red       # Phase 2: 判定処理作成
/slide-green     # Phase 3: 最小実装
/slide-refactor  # Phase 4: 品質向上
/slide-verify    # Phase 5: 最終検証
```

---

## 🛠️ slidectl 活用方法

このTDDサイクルでは、slidectl の以下の機能を活用します：

1. **品質測定** (`measure` コマンド)
   - Playwrightによる文字密度測定
   - 余白の定量評価
   - テキスト重なり検出

2. **SVG境界検証** (`validate_svg_bounds.py`)
   - ViewBox境界超過チェック
   - オーバーフロー量の測定
   - 推奨ViewBoxサイズの算出

3. **レイアウト推奨** (`recommend_layout.py`)
   - コンテンツ解析に基づくレイアウト提案
   - 箇条書き項目数、文字数、画像有無からの判定

---

## 💡 ベストプラクティス

### Test-First Approach
- 必ず判定処理を先に作成
- 受入条件を明確にしてからスライド作成
- RED → GREEN の順序を守る

### Quality-Driven Refactoring
- slidectl のメトリクスを活用
- データに基づいて改善
- 小さな変更を積み重ねる

### Continuous Validation
- 各変更後に判定処理を実行
- スコアの推移を追跡
- 品質が下がっていないか確認

---

## 📊 成功基準

以下をすべて満たせば成功とします：

- ✅ すべての受入条件をパス
- ✅ SVG境界オーバーフロー < 10px
- ✅ テキスト重なりなし
- ✅ 文字密度 < 80%
- ✅ 指定レイアウトが適用
- ✅ 前後のスライドとの整合性
- ✅ 総合スコア 85/100 以上

---

**作成者**: Claude Code
**対象プロジェクト**: ai-dev-yodoq/slides
**slidectl バージョン**: 開発中
