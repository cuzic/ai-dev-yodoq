# Marpスライド レイアウトガイド

このドキュメントでは、利用可能な10種類のレイアウトとその使用方法を説明します。

---

## 📋 レイアウト一覧

| # | レイアウト名 | 用途 | 推奨行数 |
|---|------------|------|---------|
| 1 | デフォルト | 通常のテキストスライド | 最大12行 |
| 2 | `lead` | セクション区切り、タイトルページ | - |
| 3 | `layout-horizontal-left` | 画像左、テキスト右 | 最大8行 |
| 4 | `layout-horizontal-right` | テキスト左、画像右 | 最大8行 |
| 5 | `layout-diagram-only` | 図のみ最大化 | タイトルのみ |
| 6 | `two-column` | 2カラムテキスト | 最大25行 |
| 7 | `three-column` | 3カラムテキスト | チェックリスト向け |
| 8 | `two-images-horizontal` | 画像2枚横並び | Before/After比較 |
| 9 | `image-top-compact` | 画像上、テキスト下（コンパクト） | 詳細説明多め |
| 10 | `card-grid` | カード型グリッド | 選択肢、比較表示 |

---

## 1️⃣ デフォルトレイアウト（指定なし）

### 用途
- 通常のテキストスライド
- 画像を大きく表示したい場合

### 推奨行数
最大12行

### 使用例
```markdown
# タイトル
- テキスト
- テキスト
```

---

## 2️⃣ lead（タイトルスライド）

### 用途
- セクション区切り
- タイトルページ

### 特徴
中央揃え、大きな文字

### 使用例
```markdown
<!-- _class: lead -->

# 大きなタイトル

## サブタイトル
```

---

## 3️⃣ layout-horizontal-left（図を左に配置）

### 用途
画像とテキストを左右に配置（画像55% : テキスト45%）

### 推奨行数
最大8行（画像がある場合）

### 使用例
```markdown
<!-- _class: layout-horizontal-left -->

# タイトル

![画像](path/to/image.svg)

- テキスト
- テキスト
```

---

## 4️⃣ layout-horizontal-right（図を右に配置）

### 用途
画像とテキストを左右に配置（テキスト45% : 画像55%）

### 推奨行数
最大8行（画像がある場合）

### 使用例
```markdown
<!-- _class: layout-horizontal-right -->

# タイトル

![画像](path/to/image.svg)

- テキスト
- テキスト
```

---

## 5️⃣ layout-diagram-only（図のみ最大化）

### 用途
図を最大限に表示したい場合

### 特徴
画像が最大化（max-height: 85vh）

### 使用例
```markdown
<!-- _class: layout-diagram-only -->

# タイトル

![大きな図](path/to/large-diagram.svg)
```

---

## 6️⃣ two-column（2カラムテキスト）

### 用途
テキストのみのスライドで情報量が多い場合

### 推奨行数
最大25行

### 使用例
```markdown
<!-- _class: two-column -->

# タイトル

### セクション1
- テキスト
- テキスト

### セクション2
- テキスト
- テキスト
```

---

## 7️⃣ three-column（3カラムテキスト）⭐ NEW

### 用途
- チェックリスト
- 比較表
- オプション一覧

### 特徴
横幅を有効活用、情報密度UP

### 使用例
```markdown
<!-- _class: three-column -->

# チェックリスト

**カテゴリ1**
- [ ] 項目1
- [ ] 項目2

**カテゴリ2**
- [ ] 項目3
- [ ] 項目4

**カテゴリ3**
- [ ] 項目5
- [ ] 項目6
```

---

## 8️⃣ two-images-horizontal（画像2枚横並び）⭐ NEW

### 用途
- Before/After比較
- 2つのダイアグラム
- 比較スライド

### 特徴
画像を50%ずつ横並びに配置

### 使用例
```markdown
<!-- _class: two-images-horizontal -->

# Before/After比較

![Before](before.svg)
![After](after.svg)
```

---

## 9️⃣ image-top-compact（画像上、テキスト下コンパクト）⭐ NEW

### 用途
図の下に詳細な説明を書きたい場合

### 特徴
画像の高さを40vh（デフォルト60vh）に抑えて、テキストスペースを確保

### 使用例
```markdown
<!-- _class: image-top-compact -->

# タイトル

![図](diagram.svg)

- 詳細な説明1
- 詳細な説明2
- 詳細な説明3
- 詳細な説明4
- 詳細な説明5
```

---

## 🔟 card-grid（カード型グリッド）⭐ NEW

### 用途
- 複数の選択肢
- ツール比較
- ユースケース並列表示

### 特徴
各セクションがカードとして視覚的に分離される

### 使用例
```markdown
<!-- _class: card-grid -->

# 演習課題の選択肢

### ①マスター追加
- 新しいマスタテーブルの追加
- CRUD機能の実装
- 難易度: 中

### ②項目追加
- 既存テーブルへのカラム追加
- 関連画面・API修正
- 難易度: 高

### ③検索条件追加
- 既存検索への条件追加
- UI・API・SQL修正
- 難易度: 中

### ④レポート機能追加
- 集計機能の実装
- CSV/PDF出力
- 難易度: 高
```

**注意**: カード型グリッドは2カラム固定です。3つ以上のカードがある場合は自動的に折り返されます。

---

## 💡 レイアウト選択ガイド

| 条件 | 推奨レイアウト |
|------|--------------|
| テキストのみ、12行以内 | `デフォルト` |
| テキストのみ、13-25行 | `two-column` |
| テキストのみ、25行以上 | `three-column` |
| 画像1枚、テキスト8行以内 | `layout-horizontal-left` or `layout-horizontal-right` |
| 画像1枚、テキスト多め | `image-top-compact` |
| 画像2枚、比較 | `two-images-horizontal` |
| 画像のみ、大きく見せたい | `layout-diagram-only` |
| 選択肢、カード表示 | `card-grid` |
| セクション区切り | `lead` |

---

## 🎨 カスタマイズのヒント

### カラム数の変更
`three-column` を4カラムにしたい場合:
```css
section.four-column {
  columns: 4;
  column-gap: 20px;
}
```

### カード型グリッドを3カラムに
```css
section.card-grid-3col {
  grid-template-columns: repeat(3, 1fr);
}
```

### 画像の高さ調整
```css
section.image-top-small img {
  max-height: 30vh;
}
```

---

## 🚀 実際の使用例

### 演習課題の選択肢（card-grid使用）
```markdown
<!-- _class: card-grid -->

# 3つの演習課題から選択

### ①マスター追加
- 新しいマスタテーブル追加
- CRUD機能実装
- 難易度: 中（デグレリスク低）

### ②項目追加
- 既存テーブルへのカラム追加
- 関連画面・API修正
- 難易度: 高（影響大）

### ③検索条件追加
- 既存検索への条件追加
- UI・API・SQL修正
- 難易度: 中（既存検索への影響あり）
```

### チェックリスト（three-column使用）
```markdown
<!-- _class: three-column -->

# Part 1 振り返りチェックリスト

**AI活用の基本**
- [ ] AI活用の3原則
- [ ] Reward Hacking対策

**Claude Code**
- [ ] セットアップ
- [ ] モード使い分け

**STEP1 要件定義**
- [ ] AIに質問させる
- [ ] MoSCoW優先順位付け

**STEP2 設計**
- [ ] Spec-Driven Development
- [ ] Tech Stack Setup
```

### Before/After比較（two-images-horizontal使用）
```markdown
<!-- _class: two-images-horizontal -->

# コードレビュー Before/After

![Before: バグが多い](before_buggy.svg)
![After: バグが40-60%減少](after_reviewed.svg)
```

---

## 📝 まとめ

- **新規追加**: `three-column`, `two-images-horizontal`, `image-top-compact`, `card-grid`
- **合計10種類**のレイアウトで、ほぼすべての表現パターンに対応可能
- レイアウトを適切に使い分けることで、情報量と可読性のバランスを最適化

適切なレイアウトを選択することで、スライドの見やすさが大幅に向上します！
