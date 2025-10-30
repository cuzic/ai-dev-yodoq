# 実践的パターンとTips集

## 概要
1ヶ月以上の実践から生まれた、Claude Code使用における実際に役立つパターンとトリック

出典: "Claude Code After 1 Month: The Patterns That Actually Stuck" & "I Went Deep on Claude Code—These Are My Top 13 Tricks"

---

## 7つの重要パターン

### 1. コンテキスト管理の極意

#### `/clear`コマンドの重要性
**問題**:
ジグソーパズルを解いている最中に、別のパズルのピースを次々と追加されるような状況。コンテキストが肥大化すると、LLMは新旧の情報を混同し、パフォーマンスが低下する。

**解決策**:
```bash
# 新しいトピックに移る前に必ず実行
/clear

# 要約を残しつつコンテキストを圧縮
/compact
```

**実践のポイント**:
- 「さあ、新しいことを始めよう」と感じたら即座に`/clear`
- コンテキストは小さく、タイトに保つ
- 長い会話の場合は途中で`/compact`を実行

#### `/resume`でセッション復帰
```bash
# 過去のセッションを復元
/resume
# → 6分前、1時間前などの会話を選択可能
```

**ユースケース**:
- Claude Codeが落ちた時も会話を失わない
- 複数プロジェクト間の切り替え
- 過去の設計判断の確認

#### コンテキストハンドオフ
**テクニック**: 大きな会話から部分的に引き継ぐ

```
プロンプト例:
「ボタンについての議論と、最近話したスタイリングについて
要約したプロンプトを作成してください。
新しい会話でそれを使いたいので。」
```

**メリット**:
- 重要な情報を保持しつつコンテキスト削減
- より的確な応答
- パフォーマンス向上

---

### 2. claude.mdファイルの活用

#### プロジェクトメモリの最適化

**問題**:
`/init`コマンドで生成されたclaude.mdは巨大すぎて非効率的

**改善アプローチ**:
```markdown
# claude.md - スリム版の例

## プロジェクト概要
- Next.jsアプリケーション (TypeScript)
- Firebase認証使用
- Stripeで決済処理

## コーディング規約
- ✅ 必ずTypeScriptで記述 (JavaScriptは使用禁止)
- ✅ すべての関数にテストを書く
- ✅ ESLintルールに従う
- ✅ コンポーネント名はPascalCase

## プリファレンス
- 大文字化の形式: camelCase
- インデント: 2スペース
- 引用符: シングルクォート

## 避けるべきこと
- ❌ any型の使用
- ❌ console.logの本番コード残存
- ❌ インラインスタイル
```

**claude.mdの役割**:
- すべての新規チャットに自動的に読み込まれる
- プロジェクト固有のルールを記憶
- チーム全体で共有可能（Git管理）

**ベストプラクティス**:
1. `/init`後に必ず手動で簡素化
2. build scripts、start scriptsなど不要な情報を削除
3. 本当に重要なルールのみ記載
4. 定期的に見直し、更新

**メモリへの追加**:
```bash
# Claudeとの会話中に
# メモリに追加してほしい内容に#をつける
```

---

### 3. 音声入力の革命

#### 帯域幅の乗数効果

**統計データ**:
- タイピング: 60-70語/分
- 音声入力: 190語/分
- **生産性: 約3倍**

**重要な洞察**:
> 「音声を使わないということは、ほぼ確実に十分なコンテキストを提供していない」

**音声入力のメリット**:
1. **量の増加**: より多くの考慮事項と懸念を伝えられる
2. **質の向上**: 詳細なプロンプトが容易に作成可能
3. **認知負荷軽減**: タイピングより思考が自然に流れる
4. **情報量の違い**: 初心者と上級者、両方がコンテキスト不足に陥りがちだが、音声で解決

**上級開発者の罠**:
```
悪い例（簡潔すぎる）:
"ボタンを追加して"

良い例（音声で自然に詳細化）:
"ユーザーがクリックすると確認ダイアログが出るボタンを追加してください。
ボタンは青色でprimaryスタイル、右上に配置、
モバイルでは下部に固定表示されるようにしてください。
テストも含めてお願いします。"
```

**初心者の罠**:
```
悪い例（曖昧すぎる）:
"犬小屋時計を作って"

良い例（音声で詳細を追加）:
"犬小屋の形をした壁掛け時計アプリを作りたいです。
ウェブブラウザで動作し、レスポンシブデザインで、
デジタル表示で現在時刻を表示します。
犬小屋は茶色で、屋根は赤色にしてください。"
```

---

### 4. スクリーンショット活用術

#### 視覚的コミュニケーションの威力

**セットアップ**:
```bash
# Mac: Command + Shift + 4 (スクリーンショット)
# クリップボードに自動保存される設定を推奨
```

**Claude Codeでの使い方**:

**方法1**: ドラッグ&ドロップ
```
1. スクリーンショットを撮る
2. ファイルをClaude Codeのプロンプトエリアにドラッグ
3. ファイルパスが自動挿入される
```

**方法2**: Control+V（重要！）
```bash
# Macでは Command+V ではなく Control+V を使用
# → 画像が直接ペーストされる
```

**方法3**: @記法
```bash
# @を入力してファイル選択
@screenshot_2025.png
```

**実践例**:
```
プロンプト:
「この画面全体のスクリーンショットを見てください。
何が問題か分析して、修正方法を提案してください。」

→ Claudeは視覚的に問題を特定し、的確な修正案を提示
```

**推奨ツール**:
- Mac: CleanShot X, Skitch
- Windows: Greenshot, ShareX
- クリップボードマネージャー: Alfred, Raycast (Mac)

---

### 5. YOLOモード（危険を承知で）

#### dangerously-skip-permissions

**使い方**:
```bash
claude --dangerously-skip-permissions
```

**効果**:
- すべての操作で確認を求めない
- ファイル読み書き、ディレクトリ変更などが即座に実行
- 画面下部に「bypassing permissions」と表示

**推奨事項**:
> ⚠️ 「私は推奨しません。自己責任で使用してください。
> 最初は注視しながら使い、信頼レベルを徐々に上げてください。」

**実践者の声**:
- 「私は常にこれを使っている」
- 「今まで問題は起きていない」
- 「ワークフローが非常にスムーズ」

**適切な使用場面**:
- 信頼できるプロジェクト
- Gitで管理されている（変更を追跡可能）
- テスト環境での作業

---

### 6. Hooks - サウンドフィードバック

#### 聴覚的な完了通知

**設定方法**:
```bash
# ~/.claude/config.json
{
  "hooks": {
    "user-prompt-submit": "afplay ~/sounds/prompt-submitted.mp3",
    "assistant-response-complete": "afplay ~/sounds/response-complete.mp3"
  }
}
```

**ユースケース**:
- プロジェクトごとに異なる音を設定
- 「どのプロジェクトが完了したか」を音で判別
- マルチタスク時の通知

**実践例**:
```
プロジェクトA: ベル音
プロジェクトB: チャイム音
プロジェクトC: クリック音

→ 複数プロジェクトを並行作業していても、
　 音でどれが完了したか即座に分かる
```

---

### 7. カスタムスラッシュコマンド

#### 反復作業の自動化

**基本構造**:
```
~/.claude/commands/
  ├── joke-me.md
  ├── git-save.md
  └── project-settings.md
```

**例1: joke-me.md**
```markdown
Tell me a dad joke

Please tell me a dad joke.
If the user provides a topic using $ARGUMENTS, make a joke about that topic.
Otherwise, tell me any dad joke.
```

**使用方法**:
```bash
/joke-me
# → ランダムなダジャレ

/joke-me programming
# → プログラミング関連のダジャレ
```

**例2: git-save.md**
```markdown
Create a semantic commit message with emoji

Analyze the current changes and create a semantic commit message.
Use these emoji conventions:
- ✨ new feature
- 🐛 bug fix
- 📝 documentation
- ♻️ refactoring
- 🎨 styling
- ✅ tests

Then execute: git add . && git commit -m "[generated message]"
```

**例3: project-settings.md**
```markdown
Colorize the current workspace for VSCode

Create or modify .vscode/settings.json to add custom color themes.
Prompt the user to choose from:
- Blue theme (calming)
- Green theme (productive)
- Purple theme (creative)
- Red theme (urgent)

Example settings.json:
{
  "workbench.colorCustomizations": {
    "titleBar.activeBackground": "#1e88e5",
    "titleBar.inactiveBackground": "#1e88e599"
  }
}
```

**プロジェクト固有 vs グローバル**:

```
プロジェクト固有:
  .claude/commands/
  → Git管理、チームで共有

グローバル:
  ~/.claude/commands/
  → すべてのプロジェクトで利用可能
```

---

## 高度なテクニック

### Sub-Agents（並行実行）

#### design-iterate.mdの例

**コマンド定義**:
```markdown
Launch concurrent design iterations

Launch $ARGUMENTS (default: 3) concurrent sub-tasks.
For each sub-task, if the user provides an image:
1. Analyze the UI design
2. Create a unique variation with a specific theme
3. Save it to ui-iterations/ folder

Themes to explore:
- Minimalist
- Neon cyberpunk
- Retro 80s
- 3D isometric
- Emoji chaos (be creative!)
```

**実行例**:
```bash
# スクリーンショットをペースト
/design-iterate 5 [image] some simply crazy

→ 5つの並行タスクが起動:
  - Task 1: Minimalist calculator
  - Task 2: Neon cyberpunk calculator
  - Task 3: Retro 80s calculator
  - Task 4: 3D isometric calculator
  - Task 5: Emoji chaos calculator
```

**Sub-Agentsの特徴**:
- Claude Codeがヘッドレスで並行実行
- 各タスクは独立したコンテキスト
- 結果を待たずに次の作業が可能
- 完了後に結果をレビュー

---

## モード切り替え (Shift+Tab)

### 3つのモード

**1. デフォルトモード**
- すべての操作で確認を求める
- 初心者に安全

**2. Auto-Acceptモード** (Shift+Tab 1回)
- ファイル読み書きなどを自動承認
- よく使う操作を高速化
- 一部の重要な操作は確認を求める

**3. Planモード** (Shift+Tab 2回)
- ファイルを書き込まない
- 会話のみで計画を立てる
- 計画レビュー後に承認して実行

**推奨ワークフロー**:
```
1. Planモードで設計を議論
2. 計画を承認
3. Auto-Acceptモードに切り替え
4. 実装を実行
```

---

## IDE統合の活用

### Cursor / VS Codeとの連携

**セットアップ**:
```bash
# Cursor内でターミナルを開く
claude

# IDE統合を有効化
/ide
```

**メリット**:
1. **ファイルの自動参照**: IDEで開いているファイルがClaude Codeのコンテキストに追加
2. **同時編集**: IDEとClaude Codeで同じファイルを編集可能
3. **視覚的な確認**: ファイルツリーとエディタで変更を即座に確認

**Command+Escapeショートカット**:
```
Command+Escape (Mac) / Ctrl+Escape (Windows)
→ Claude Codeをタブとして開く
→ 通常のターミナルウィンドウではなくタブとして統合
```

---

## Anthropic APIモデル選択

### モデルスイッチング

**利用可能モデル**:
- **Claude Opus 4**: 最高性能、複雑なタスク
- **Claude Sonnet 4.5**: バランス型、多くのタスクに最適
- **Auto**: 50%までOpus使用、その後Sonnetに自動切替

**切り替え方法**:
```bash
# 設定画面からモデル選択
# または環境変数で指定
export ANTHROPIC_MODEL="claude-opus-4"
```

**コスト最適化**:
```
戦略:
- 簡単なタスク: Sonnet
- 複雑な設計: Opus
- 自動選択: Auto (賢いバランス)
```

---

## 実践的なワークフロー例

### 新規プロジェクト立ち上げ

```bash
# 1. プロジェクトフォルダ作成
mkdir my-awesome-app && cd my-awesome-app

# 2. Claude Code起動（Cursor内で）
claude

# 3. 初期化
/init

# 4. claude.mdを編集して簡素化
# （Cursor側で .claude/claude.md を開いて編集）

# 5. プロジェクト設定（カスタムコマンド使用）
/project-settings
# → 色テーマを選択

# 6. 開発開始（音声入力推奨）
"Next.jsとTypeScriptで、ユーザー認証機能付きの
ダッシュボードアプリを作りたいです。
Firebase Authenticationを使用し、
ログイン画面、ダッシュボード、プロフィールページを含めてください。"

# 7. 実装完了後、コミット
/git-save
```

### 既存コードの改善

```bash
# 1. スクリーンショットを撮る（問題のUI）

# 2. Claude Codeで
Control+V  # スクリーンショットペースト
"このUIの問題点を分析して、改善案を5つ提示してください"

# 3. 複数案を並行生成
/design-iterate 5 [image] make them diverse

# 4. 気に入った案を選択
"3番目の案をベースに実装してください"

# 5. テスト
"実装したコンポーネントのテストも書いてください"
```

---

## よくある落とし穴と対策

### 落とし穴1: コンテキストの肥大化
**症状**: 応答が遅くなる、的外れな提案が増える
**対策**: こまめに `/clear`、新トピックごとにリセット

### 落とし穴2: 曖昧なプロンプト
**症状**: 期待と違う実装、何度もやり直し
**対策**: 音声入力で詳細を伝える、スクリーンショット活用

### 落とし穴3: claude.mdの放置
**症状**: プロジェクト固有ルールが無視される
**対策**: `/init`後に必ず手動でカスタマイズ

### 落とし穴4: モード選択ミス
**症状**: Planモードで実装が進まない
**対策**: Shift+Tabでモード確認、適切に切り替え

---

## チェックリスト

### 新規プロジェクト開始時
- [ ] プロジェクトフォルダで`claude`起動
- [ ] `/init`で初期化
- [ ] claude.mdを簡素化・カスタマイズ
- [ ] IDE統合を有効化 (`/ide`)
- [ ] プロジェクト色設定 (`/project-settings`)
- [ ] 音声入力の準備確認
- [ ] スクリーンショットツールの動作確認

### 日常の開発フロー
- [ ] 新トピック開始時に `/clear`
- [ ] 音声入力で詳細なプロンプト
- [ ] スクリーンショットで視覚的説明
- [ ] Planモードで設計検討
- [ ] Auto-Acceptモードで実装
- [ ] 定期的に `/compact`
- [ ] Git commitは `/git-save`

### トラブルシューティング
- [ ] 応答が遅い → `/clear`してリセット
- [ ] 的外れな提案 → コンテキスト確認、詳細追加
- [ ] ルール無視 → claude.md確認・更新
- [ ] ファイルが見つからない → IDE統合確認

---

## さらなる学習リソース

### 公式ドキュメント
- Claude Code公式ガイド
- Anthropic API リファレンス
- カスタムコマンドの詳細

### コミュニティ
- Discord: Claude Code Community
- GitHub Discussions
- Twitter: #ClaudeCode

### 参考動画
- "Claude Code After 1 Month: The Patterns That Actually Stuck"
- "I Went Deep on Claude Code—These Are My Top 13 Tricks"
- "Claude Code Masterclass: From Beginner to Expert"

---

**最終更新**: 2025-10-30
**情報源**: 実践者の1ヶ月以上の使用経験に基づく
