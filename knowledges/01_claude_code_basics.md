# Claude Code 基礎知識

出典: ~/youtube/AI駆動開発/claude_code_20min/

## 3つのモード（cc_042）

### Edit Mode（編集モード）
- ファイルを直接編集
- 複数ファイルの同時編集可能
- コードの生成・修正・リファクタリング
- 使用場面: 実装、バグ修正、リファクタリング

### Chat Mode（チャットモード）
- 質問・相談・コードレビュー
- コンテキストを保持しながら対話
- 実装前の設計相談に最適
- 使用場面: 設計相談、技術調査、問題解決

### Architect Mode（設計モード）
- プロジェクト全体の構造設計
- 複数ファイルにまたがる大規模変更
- ファイル構成の提案
- 使用場面: 新規プロジェクト、大規模リファクタリング

## インストールと初期設定（cc_493, cc_303）

### 前提条件
- Node.js 22以上
- Python 3.12以上（推奨）
- Anthropic APIキー

### インストール手順
```bash
# npmでグローバルインストール
npm install -g @anthropic-ai/claude-code

# 初回起動
claude-code

# APIキー設定（初回のみ）
```

### 基本設定
1. `.claude/` ディレクトリが自動作成される
2. `config.json` でプロジェクト設定
3. `.claudeignore` で除外ファイル指定（重要！）

## ツール比較（cc_124: 9.75点トピック）

### Claude Code vs Cursor vs Windsurf
- **Claude Code**: コマンドライン、柔軟性高、カスタマイズ容易
- **Cursor**: VSCode統合、GUIで使いやすい
- **Windsurf**: 最新、エージェント機能強化

### 選択基準
- CLI好き → Claude Code
- GUI好き → Cursor
- 最新機能 → Windsurf
- **重要**: 学習したスキルは相互応用可能（cc_060）

## 他ツールへの応用（cc_060: 8.75点）

### 応用可能な戦略
1. **Global Rules**: プロジェクト全体ルール設定
2. **Slash Commands**: カスタムコマンド作成
3. **Sub-Agents**: 並列タスク実行

これらの概念は以下でも使える:
- Cursor（.cursorrules.md）
- Windsurf（設定ファイル）
- その他AIツール

## 基本コマンド（cc_303-313）

### ファイル操作
```bash
# 新規ファイル作成
/write <filename>

# ファイル編集
/edit <filename>

# ファイル読み込み
/read <filename>
```

### プロジェクト操作
```bash
# プロジェクト構造分析
/analyze

# ドキュメント生成
/document

# テスト生成
/test
```

### カスタムコマンド（cc_312, cc_047）
`.claude/commands/` ディレクトリにMarkdownファイルで定義:
```markdown
# /review-pr
コードレビューを実施し、以下を確認:
- コーディング規約準拠
- セキュリティ問題
- パフォーマンス懸念
```

## 重要な概念

### Trust but Verify（cc_077）
- AI生成コードは必ず検証
- テストで動作確認
- ブラインド受け入れ禁止

### Context Engineering（cc_062: 10原則）
1. 明確な指示
2. 具体例提供
3. 制約条件明示
4. 段階的な改善
5. コンテキスト最適化

### 価格情報（cc_095: 8.32点）
- Claude 3.7 Sonnet: 入力$3/MTok、出力$15/MTok
- 効率的な使用でコスト削減可能

## ベストプラクティス

### .claudeignore設定（cc_043）
```
node_modules/
.git/
*.log
dist/
build/
.env
```

### CLAUDE.md活用（cc_044）
プロジェクトルートに配置:
```markdown
# プロジェクト概要
Next.js + TypeScriptのWebアプリケーション

# コーディング規約
- ESLint/Prettierに従う
- TypeScript strictモード
- テストカバレッジ80%以上

# 技術スタック
- Next.js 14
- React 18
- TypeScript 5
- Tailwind CSS
```

## 関連トピック
- 中級: Hooks、Sub-Agents → `02_claude_code_advanced.md`
- 実装: TDD、デバッグ → `05_implementation_tdd.md`
- 品質: コードレビュー → `06_quality_assurance.md`
