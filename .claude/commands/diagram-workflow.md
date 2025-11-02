# ダイアグラム作成ワークフロー

Marpスライド用ダイアグラムの作成から検証までの完全なワークフローを実行します。

## ワークフロー全体

```
1. スライド分析 → 2. ダイアグラム作成 → 3. 品質検証 → 4. 修正（必要に応じて）
```

## Step 1: スライド分析

### 対象スライドの確認

```bash
# スライドファイルを確認
cat slides/day1_2.md | grep -A 5 "<!-- _class:"
```

### レイアウトクラスの特定

スライド内の `<!-- _class: XXX -->` を確認：
- `layout-diagram-only` - 全画面（16:9）
- `layout-horizontal-right` - 右側（8:9）
- `layout-horizontal-left` - 左側（8:9）
- `layout-comparison` - 比較（1:1）
- `layout-callout` - 強調（3:2）
- `card-grid` - カード（5:3）

### コンテキストの理解

スライドの内容を読み、以下を明確にする：
1. **主題:** 何を説明するスライドか
2. **テキスト内容:** スライドに既に書かれているテキスト
3. **補完すべき情報:** 視覚化すると理解が深まる要素
4. **視覚化の方法:** フロー、関係図、プロセス、比較など

## Step 2: ダイアグラム作成

### `/create-slide-diagram` を実行

コマンドの指示に従って、以下を実行：

1. **レイアウトクラスの確認**
2. **適切な縦横比の選択**
3. **コンテンツの構造化**
4. **テキストと画像の分担を明確化**
   - テキストは箇条書き・説明
   - ダイアグラムは構造・関係性・流れ
5. **viewBoxサイズとフォントサイズの計算**
6. **SVGの生成**

### 出力先

```
assets/diagrams/diagram_XX_descriptive_name.svg
```

命名規則：
- 2桁の連番（既存の最大番号+1）
- 内容を表す英語名（スネークケース）
- 例: `diagram_49_tdd_cycle_overview.svg`

## Step 3: 品質検証

### 3-1: 自動検証

```bash
# オーバーフロー・オーバーラップチェック
python scripts/slides/validate_svg_bounds.py assets/diagrams/diagram_XX_name.svg
```

**期待される出力:**
```
✅ No overflow or overlap issues found
```

### 3-2: スライドへの埋め込み

スライドファイルに以下を追加：

```markdown
<!-- _class: layout-diagram-only -->

# スライドタイトル

![ダイアグラム説明](../assets/diagrams/diagram_XX_name.svg)
```

### 3-3: レンダリング確認

```bash
# Marpでレンダリング
cd slides
marp day1_2.md --html --allow-local-files -o test_day1_2.html

# ブラウザで開く
```

**確認項目:**
- [ ] ダイアグラムがレイアウト内に適切に収まっている
- [ ] テキストが読みやすい
- [ ] オーバーフロー・オーバーラップがない
- [ ] 縦横比が適切
- [ ] スライドのテキストと補完関係にある

### 3-4: 品質スコアチェック（オプション）

```bash
# 全体の品質評価
cd slides
python3 evaluate_slide_quality.py | grep "diagram_XX_name"
```

**目標スコア:** 80/100以上

## Step 4: 修正（必要に応じて）

### 問題: オーバーフロー

**症状:** テキストがviewBoxからはみ出る

**解決策:**
1. viewBoxを10-20%拡大
2. フォントサイズを縮小
3. テキストを簡略化

### 問題: テキスト重なり

**症状:** 複数のテキストが重なっている

**解決策:**
1. `/fix-svg-overlap` コマンドを実行
2. または手動で y座標を再計算（font_size × 1.5 間隔）

### 問題: レイアウトに合わない

**症状:** ダイアグラムが小さすぎる/大きすぎる

**解決策:**
1. レイアウトクラスを再確認
2. 正しいviewBoxを使用しているか確認
3. 必要に応じてレイアウトクラスを変更

### 問題: 視覚的価値が低い

**症状:** テキストの単純な複製になっている

**解決策:**
1. ダイアグラムの種類を見直す（フロー、関係図、プロセスなど）
2. 視覚的要素を追加（矢印、アイコン、色分け）
3. テキストに書かれていない情報を追加（関係性、順序、重要度など）

## Step 5: コミット

品質確認が完了したら、コミット：

```bash
git add assets/diagrams/diagram_XX_name.svg
git add slides/day1_2.md  # スライドも更新した場合

git commit -m "feat: Add diagram_XX_name for layout-diagram-only

- viewBox: 1600×900 (16:9)
- 用途: 5-STEPフロー全体の視覚化
- テキストと補完関係: フローの順序と成果物を視覚的に表現
- 品質: オーバーフロー・オーバーラップなし"
```

## 複数ダイアグラムの一括作成

複数のダイアグラムを作成する場合：

### 1. 必要なダイアグラムのリストアップ

```bash
# スライドからSVG参照を抽出
grep -h "!\[.*\](.*\.svg)" slides/day*.md | \
sed 's/.*(\(.*\))/\1/' | \
sed 's/^\.\.\///' | \
sort -u > required_svgs.txt

# 存在しないSVGを特定
python3 << 'EOF'
from pathlib import Path

required = Path('required_svgs.txt').read_text().splitlines()
for svg_path in required:
    path = Path(svg_path)
    if not path.exists():
        print(f"❌ {svg_path}")
EOF
```

### 2. 優先順位付け

存在しないSVGを使用頻度順に並べる：

```bash
# 各SVGの使用回数をカウント
for svg in $(cat required_svgs.txt); do
    count=$(grep -c "$svg" slides/day*.md)
    echo "$count $svg"
done | sort -rn
```

### 3. 順次作成

優先度の高いものから順に `/create-slide-diagram` を実行

## ベストプラクティス

### DO（推奨）
- ✅ レイアウトクラスに適した縦横比を使用
- ✅ テキストを補完する視覚表現を追加
- ✅ 関係性、順序、構造を明確に
- ✅ オーバーフロー・オーバーラップを事前に計算
- ✅ ai-seminarテーマのカラーパレットを使用
- ✅ 作成後は必ず品質検証

### DON'T（避ける）
- ❌ テキストをそのまま画像化
- ❌ レイアウトに合わない縦横比
- ❌ 情報を詰め込みすぎる
- ❌ 計算せずに座標を決める
- ❌ 検証なしでコミット

## トラブルシューティング

### Q: どのダイアグラム形式を選べばいいか分からない

A: スライドの内容に応じて選択：
- 順序・手順 → フローチャート
- 関係性・影響 → 関係図
- 対比・比較 → 比較図
- 抽象概念 → 概念図
- 段階的プロセス → プロセス図

### Q: 情報量が多すぎてviewBoxに収まらない

A: 以下のいずれかを実施：
1. 情報を簡略化・優先順位付け
2. 複数のダイアグラムに分割
3. より大きなレイアウト（layout-diagram-only）を使用
4. viewBoxを拡大（ただし縦横比は維持）

### Q: テキストとダイアグラムの内容が重複している

A: ダイアグラムの役割を再考：
- テキスト: 説明、箇条書き、詳細
- ダイアグラム: 構造、関係、流れ、視覚的補完

テキストに書かれていない情報（矢印、アイコン、色分け、グループ化など）を追加

## 関連コマンド

- `/create-slide-diagram` - ダイアグラム作成（詳細ガイド）
- `/check-svg-quality` - SVG品質チェック
- `/fix-svg-overlap` - SVG重なり修正

## 目標

すべてのダイアグラムが以下の基準を満たすこと：
- ✅ レイアウトに適した縦横比
- ✅ テキストと補完関係にある
- ✅ 視覚的に理解を深める
- ✅ オーバーフロー・オーバーラップなし
- ✅ 品質スコア 80/100 以上
