# AI活用開発セミナー：生産性を劇的に向上させる体系的アプローチ

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Marp](https://img.shields.io/badge/Made%20with-Marp-orange)](https://marp.app/)

2日間で学ぶ実践的AI駆動開発手法のセミナー資料（YODOQ版）です。全5部構成、約160枚のMarpスライドと43種類のSVG図表を含みます。

## 📚 コンテンツ概要

このセミナーでは、AIを活用した体系的な開発手法を学びます：

- **5-STEPフロー**: 要件定義 → 設計 → タスク分解 → 実装 → 品質担保 → リファクタリング
- **AI活用の3原則**: Jagged Intelligence、Trust but Verify、Guardrails
- **TDD/BDD**: AI自己完結型の開発サイクル
- **Living Documentation**: AIの外部メモリとしてのドキュメント戦略

## 📂 ファイル構成

### スライド（Marp形式）

| ファイル | 内容 | スライド数 |
|---------|------|-----------|
| `day1_1.md` | 1日目 Part 1（10:00-12:00）：イントロダクション、Claude Code、要件定義、設計 | 約45枚 |
| `day1_2.md` | 1日目 Part 2（13:00-14:50）：タスク分解、実装、品質担保、リファクタリング | 約40枚 |
| `day1_3.md` | 1日目 Part 3（15:00-17:00）：振り返り、演習 | 約33枚 |
| `day2_1.md` | 2日目 Part 1（10:00-12:00）：リバースエンジニアリング、テストシナリオ | 約40枚 |
| `day2_2.md` | 2日目 Part 2（13:00-17:00）：実践演習、成果発表、まとめ | 約42枚 |

### その他ファイル

- `LAYOUT_GUIDE.md` - 10種類のレイアウト完全ガイド
- `diagram_prompts.md` - 図表作成用プロンプト集（43個）
- `diagrams/` - 全43種類のSVG図表
- `V4_NEW_TOPICS.md` - トピック一覧と概要

## ✨ レイアウト機能

このスライドは10種類のカスタムレイアウトに対応しています：

1. **デフォルト** - 通常のテキストスライド（最大12行）
2. **lead** - セクション区切り、タイトルページ
3. **layout-horizontal-left** - 画像左、テキスト右（8行）
4. **layout-horizontal-right** - テキスト左、画像右（8行）
5. **layout-diagram-only** - 図のみ最大化
6. **two-column** - 2カラムテキスト（25行）
7. **three-column** ⭐ - 3カラムテキスト（35行）
8. **card-grid** ⭐ - カード型グリッド（30行）
9. **image-top-compact** ⭐ - 画像コンパクト＋詳細説明（15行）
10. **two-images-horizontal** ⭐ - 画像2枚横並び（10行）

詳細は [LAYOUT_GUIDE.md](./LAYOUT_GUIDE.md) をご覧ください。

## Marpについて

Marp（Markdown Presentation Ecosystem）は、Markdownからスライドを生成するツールです。

### インストール

```bash
# Marp CLI をインストール
npm install -g @marp-team/marp-cli

# または VS Code拡張機能を使用
# 「Marp for VS Code」をインストール
```

### スライド生成方法

#### PDFに変換

```bash
marp day1_1.md -o day1_1.pdf
marp day1_2.md -o day1_2.pdf
marp day1_3.md -o day1_3.pdf
marp day2_1.md -o day2_1.pdf
marp day2_2.md -o day2_2.pdf

# 全ファイルを一括変換
marp day*.md --pdf
```

#### HTMLに変換

```bash
marp day1_1.md -o day1_1.html
marp day1_2.md -o day1_2.html

# 全ファイルを一括変換
marp day*.md --html
```

#### PowerPointに変換

```bash
marp day1_1.md -o day1_1.pptx
marp day1_2.md -o day1_2.pptx

# 全ファイルを一括変換
marp day*.md --pptx
```

#### プレビュー（VS Code）

1. VS Codeで `.md` ファイルを開く
2. 右上の「Marp Preview」アイコンをクリック
3. リアルタイムでスライドプレビューが表示される

#### プレビュー（CLI）

```bash
marp -s day1_1.md
# ブラウザで http://localhost:8080 を開く
```

## Marp構文のポイント

### スライド区切り

```markdown
---
```

### セクションスライド（タイトルのみ）

```markdown
---

<!-- _class: lead -->

# セクションタイトル
```

### 通常スライド

```markdown
---

# スライドタイトル

- 箇条書き1
- 箇条書き2
```

### Front Matter（ファイル先頭）

```yaml
---
marp: true
theme: default
paginate: true
header: 'ヘッダーテキスト'
footer: '© 2024 AI Development Seminar'
---
```

## カスタマイズ

### テーマの変更

```yaml
---
marp: true
theme: gaia  # default, gaia, uncover
---
```

### ページ番号の表示/非表示

```yaml
---
marp: true
paginate: true  # ページ番号を表示
---
```

### 背景色の変更（個別スライド）

```markdown
---

<!-- _backgroundColor: #123456 -->

# このスライドだけ背景色を変更
```

## 図表の挿入

図表を挿入する場合は、`diagram_prompts.md`のプロンプトを使ってSVGを生成し、以下のように挿入してください：

```markdown
---

# 5-STEPフロー全体像

![w:1000](./diagrams/diagram_03_5step_flow.svg)

- STEP1: 要件定義
- STEP2: 設計
...
```

## トラブルシューティング

### 日本語フォントが表示されない

CSSでフォントを指定：

```yaml
---
marp: true
style: |
  section {
    font-family: 'Noto Sans JP', sans-serif;
  }
---
```

### 箇条書きが多すぎて1スライドに収まらない

以下のいずれかで対応：
1. スライドを分割（`---`で区切る）
2. フォントサイズを小さくする
3. 2カラムレイアウトを使用

```markdown
<style scoped>
section { font-size: 22px; }
</style>
```

## 参考リンク

- [Marp公式サイト](https://marp.app/)
- [Marp CLI ドキュメント](https://github.com/marp-team/marp-cli)
- [Marp for VS Code](https://marketplace.visualstudio.com/items?itemName=marp-team.marp-vscode)
