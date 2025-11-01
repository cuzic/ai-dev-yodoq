# Slide GREEN - Phase 3: 最小実装

判定処理がパスする最低限のスライドを作成します（GREEN状態にする）。

## 実行タスク

### 1. スライドのマークダウン作成

`all_slides.md` に新しいスライドを追加、または既存スライドを更新：

```markdown
---

<!-- _class: [レイアウト名] -->

# [スライドタイトル]

![width:[表示幅]px](diagrams/diagram_[番号].svg)

- [箇条書き項目1]
- [箇条書き項目2]
- [箇条書き項目3]
- [箇条書き項目4]
- [箇条書き項目5]

---
```

**レイアウト別のテンプレート**:

#### lead レイアウト
```markdown
---

<!-- _class: lead -->

# [メインタイトル]

## [サブタイトル]

---
```

#### layout-diagram-only レイアウト
```markdown
---

<!-- _class: layout-diagram-only -->

# [タイトル]

![width:1100px](diagrams/diagram_[番号].svg)

---
```

#### layout-horizontal-left レイアウト
```markdown
---

<!-- _class: layout-horizontal-left -->

# [タイトル]

![width:900px](diagrams/diagram_[番号].svg)

- [箇条書き項目1]
- [箇条書き項目2]
- [箇条書き項目3]

---
```

#### two-column レイアウト
```markdown
---

<!-- _class: two-column -->

# [タイトル]

## Before

- [項目1]
- [項目2]
- [項目3]

## After

- [項目1]
- [項目2]
- [項目3]

---
```

#### compact レイアウト
```markdown
---

<!-- _class: compact -->

# [タイトル]

- [箇条書き項目1]
- [箇条書き項目2]
- [箇条書き項目3]
- [箇条書き項目4]
- [箇条書き項目5]
- [箇条書き項目6]
- [箇条書き項目7]
- [箇条書き項目8]
- [箇条書き項目9]

---
```

### 2. SVG図表の作成（必要な場合）

Claude Codeに依頼してSVG図表を生成：

**依頼内容の例**:
```
「[図表の説明]」というSVG図表を作成してください。

要件:
- ViewBoxサイズ: 1400x800 程度
- タイトル: [図表タイトル]
- 要素:
  - [要素1の説明]
  - [要素2の説明]
  - [要素3の説明]
- スタイル:
  - フォント: 'Noto Sans JP', sans-serif
  - タイトルフォントサイズ: 56px
  - 本文フォントサイズ: 40-48px
  - カラースキーム: #00146E (濃い青), #00AFF0 (明るい青)
- オーバーフロー防止:
  - すべてのテキストがViewBox内に収まること
  - 長いテキストは複数行に分割
  - 適切な余白を確保

保存先: diagrams/diagram_[番号]_[名前].svg
```

**SVG作成のベストプラクティス**:
1. ViewBoxは余裕を持って設定（1400x800, 1600x900など）
2. 長いテキストは複数行に分割
3. フォントサイズは読みやすさを優先（最小40px）
4. text-anchorを活用（middle, end）
5. 日本語文字幅を考慮（英数字の約2倍）

### 3. Marpでwidth指定

SVGをスライドに埋め込む際、適切なwidth指定を追加：

- ViewBox 1400x800 → width:900px
- ViewBox 1600x900 → width:1000px
- ViewBox 1800x1000 → width:1100px
- ViewBox 2400x450 → width:1100px

アスペクト比を考慮して調整。

### 4. Marpでレンダリング

HTMLを生成して確認：

```bash
npx @marp-team/marp-cli all_slides.md -o index.html --html
```

エラーが出ないことを確認。

### 5. 判定処理の実行

REDフェーズで作成した判定スクリプトを実行：

```bash
python3 validate_slide_[番号].py
```

期待される出力（GREEN状態）:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SLIDE #[番号] VALIDATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ PASSED

📊 Metrics:
  layout: [レイアウト名]
  title: [スライドタイトル]
  bullet_count: 5
  has_svg: True
  svg_overflow: 3px
  text_chars: 320

⚠️  Warnings: (optional)
  - (none)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

すべての必須条件（errors）がパスすればGREEN状態達成。

警告（warnings）があっても構いませんが、REFACTORフェーズで改善します。

### 6. TodoList更新

スライド作成タスクを完了としてマーク。

## 確認ポイント

- ✅ スライドが `all_slides.md` に追加されたか
- ✅ SVG図表が作成されたか（必要な場合）
- ✅ Marpでレンダリングが成功したか
- ✅ 判定処理がパスしたか（GREEN状態）
- ✅ 最低限の品質基準を満たしているか

## 次のフェーズへ

ユーザーの確認を得てから、次のフェーズ（REFACTOR）へ進む。

REFACTORフェーズでは、slidectl の測定機能を使ってスライドの品質をさらに向上させます。
