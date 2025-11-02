# 新しいレイアウトの使用例

このファイルには、新しく追加された4つのレイアウトの具体的な使用例を記載しています。

---

## 1. layout-comparison（比較レイアウト）

### 使用例1: アプローチ比較

```markdown
---
<!-- _class: layout-comparison -->

# AIコーディング：2つのアプローチ

<div>

### スピード重視型
- プロトタイプを素早く作成
- 動けばOKの精神
- テスト後回し
- セキュリティは後で考える
- 技術的負債が蓄積

</div>

<div>VS</div>

<div>

### 品質重視型
- 最初から設計を考慮
- TDDでテスト駆動
- セキュリティファースト
- コードレビュー必須
- 保守性を確保

</div>

---
```

### 使用例2: Before/After

```markdown
---
<!-- _class: layout-comparison -->

# コードレビュー：AI導入前後

<div>

### 導入前
- 人間が全行を手動レビュー
- 時間がかかる（1-2時間/PR）
- 見落としが発生
- レビュー待ちでブロック
- 属人化

</div>

<div>VS</div>

<div>

### 導入後
- AIが第一次レビュー（5分）
- 人間は設計・ビジネスロジックに集中
- セキュリティ観点を網羅
- レビュー待ち時間削減
- 知見がドキュメント化

</div>

---
```

---

## 2. layout-callout（強調メッセージレイアウト）

### 使用例1: 重要原則

```markdown
---
<!-- _class: layout-callout -->

<div class="icon">💡</div>

# Trust but Verify（信頼するが検証する）

<div class="message">
AIの出力を盲信せず、必ずレビュー・テストで検証
</div>

- AIにもエラー・幻覚（Hallucination）がある
- セキュリティ脆弱性を見落とす可能性
- ビジネスロジックの誤解
- 自己レビュープロンプトで大幅改善
- 最終判断は人間が行う

---
```

### 使用例2: セキュリティ警告

```markdown
---
<!-- _class: layout-callout -->

<div class="icon">🔒</div>

# セキュリティ三原則

<div class="message">
AIが生成するコードは必ずセキュリティレビュー
</div>

- パスワードは必ずハッシュ化（BCrypt推奨）
- 環境変数で機密情報管理（.env）
- 入力値の検証必須（@Valid等）
- SQLインジェクション対策（PreparedStatement）
- XSS対策（エスケープ処理）

---
```

### 使用例3: テスト重要性

```markdown
---
<!-- _class: layout-callout -->

<div class="icon">✅</div>

# TDD = AI自己完結の鍵

<div class="message">
テストがあればAIが自分で直せる、なければ無限ループ
</div>

- テストなし → 人間が手動確認 → エラー → 修正依頼 → 繰り返し
- テストあり → AI実装 → 自動テスト → エラー → AI自己修正 → 完了
- Red-Green-Refactorサイクル
- Given-When-Then形式で仕様明確化
- カバレッジ80%以上を目標

---
```

---

## 3. layout-timeline（タイムラインレイアウト）

### 使用例1: 開発フロー

```markdown
---
<!-- _class: layout-timeline -->

# AI活用開発の5ステップ

<div class="timeline">

<div class="step">
<div class="step-number">1</div>
<h3>要件定義</h3>
<p>何を作るか明確化</p>
</div>

<div class="step">
<div class="step-number">2</div>
<h3>設計</h3>
<p>どう作るか定義</p>
</div>

<div class="step">
<div class="step-number">3</div>
<h3>タスク分解</h3>
<p>小さく分割</p>
</div>

<div class="step">
<div class="step-number">4</div>
<h3>実装</h3>
<p>TDD・レビュー</p>
</div>

<div class="step">
<div class="step-number">5</div>
<h3>品質担保</h3>
<p>Doc更新</p>
</div>

</div>

---
```

### 使用例2: TDDサイクル

```markdown
---
<!-- _class: layout-timeline -->

# Red-Green-Refactorサイクル

<div class="timeline">

<div class="step">
<div class="step-number" style="background: #f44336;">1</div>
<h3>Red</h3>
<p>失敗するテストを書く</p>
</div>

<div class="step">
<div class="step-number" style="background: #4CAF50;">2</div>
<h3>Green</h3>
<p>最小実装で通す</p>
</div>

<div class="step">
<div class="step-number" style="background: #2196F3;">3</div>
<h3>Refactor</h3>
<p>コードを改善</p>
</div>

</div>

---
```

### 使用例3: デプロイメントパイプライン

```markdown
---
<!-- _class: layout-timeline -->

# CI/CDパイプライン

<div class="timeline">

<div class="step">
<div class="step-number">1</div>
<h3>Commit</h3>
<p>コードプッシュ</p>
</div>

<div class="step">
<div class="step-number">2</div>
<h3>Build</h3>
<p>ビルド実行</p>
</div>

<div class="step">
<div class="step-number">3</div>
<h3>Test</h3>
<p>自動テスト</p>
</div>

<div class="step">
<div class="step-number">4</div>
<h3>Review</h3>
<p>コードレビュー</p>
</div>

<div class="step">
<div class="step-number">5</div>
<h3>Deploy</h3>
<p>本番展開</p>
</div>

</div>

---
```

---

## 4. layout-code-focus（コード重視レイアウト）

### 使用例1: プロンプト例

```markdown
---
<!-- _class: layout-code-focus -->

# AIレビュープロンプト：セキュリティ観点

\`\`\`
このコードをセキュリティ観点でレビューして：

1. SQLインジェクション対策
2. XSS対策
3. CSRF対策
4. 認証・認可の不備
5. 機密情報の漏洩リスク

問題があれば具体的な修正案を提示してください。
\`\`\`

<div class="notes">

<div>
<h3>AIが検出すること</h3>
- パラメータバインディング不足
- エスケープ処理漏れ
- トークン検証なし
- ハードコードされた認証情報
</div>

<div>
<h3>AIが提案すること</h3>
- PreparedStatement使用
- OWASPライブラリ推奨
- CSRFトークン実装
- 環境変数への移行
</div>

</div>

---
```

### 使用例2: リファクタリング指示

```markdown
---
<!-- _class: layout-code-focus -->

# リファクタリングプロンプト例

\`\`\`javascript
// このコードをリファクタリングして：
function processUser(user) {
  if (user.type === 'admin') {
    // admin処理（50行）
  } else if (user.type === 'member') {
    // member処理（50行）
  } else if (user.type === 'guest') {
    // guest処理（50行）
  }
}

// 要求：
// 1. Strategy パターン適用
// 2. 各type専用クラスに分離
// 3. 単体テスト追加
\`\`\`

<div class="notes">

<div>
<h3>Before</h3>
- 150行のif-else地獄
- 保守困難
- テスト複雑
</div>

<div>
<h3>After</h3>
- 各Strategyクラス30行
- 拡張容易
- テスト簡単
</div>

</div>

---
```

### 使用例3: エラー再現手順

```markdown
---
<!-- _class: layout-code-focus -->

# エラー調査依頼（効果的なプロンプト）

\`\`\`
【エラー内容】
NullPointerException in UserService.findById()

【再現手順】
1. ログイン画面でユーザーID入力
2. 送信ボタンクリック
3. エラー発生

【期待動作】
ユーザー情報が表示される

【関連ファイル】
- src/services/UserService.java
- src/controllers/UserController.java

原因を特定し、修正案を提示してください。
\`\`\`

<div class="notes">

<div>
<h3>良いプロンプト</h3>
- エラーメッセージ明記
- 再現手順詳細
- 期待動作記載
- 関連ファイル指定
</div>

<div>
<h3>悪いプロンプト</h3>
- 「エラーが出る」だけ
- 手順不明
- ファイル指定なし
- AIが推測に時間浪費
</div>

</div>

---
```

---

## 使い分けガイド

| レイアウト | 最適な用途 | 避けるべきケース |
|-----------|----------|--------------|
| **comparison** | 2つの概念を対比、Before/After、vs比較 | 画像付き（horizontalを使用）、3つ以上の比較 |
| **callout** | 重要原則の強調、注意事項、キーメッセージ | 情報量が多い（8行以上）、詳細説明が必要 |
| **timeline** | 手順・フロー（3-7ステップ）、時系列 | ステップが多すぎる（8+）、画像が主体 |
| **code-focus** | コード例+説明、プロンプト例 | コードが短い（10行未満）、コードなし |

---

## 既存スライドへの適用

### 適用を推奨するスライド

これらのレイアウトは、**新しいスライドを作成する際**、または**既存スライドを大幅に書き直す際**に使用することを推奨します。

既存のスライド（特に画像付き）を無理に変換する必要はありません。現在の horizontal レイアウト等で十分に機能しています。

### 新規スライド作成時のチェックリスト

スライドを新規作成する際：

1. ☐ 2つの概念を比較する？ → `layout-comparison`
2. ☐ 重要メッセージを強調したい？ → `layout-callout`
3. ☐ 手順・フローを示したい（3-7ステップ）？ → `layout-timeline`
4. ☐ コード例と説明をセットで示したい？ → `layout-code-focus`
5. ☐ 上記に該当しない？ → 既存レイアウトを使用

---

## レイアウト選択フローチャート

```
新しいスライドを作る
  │
  ├─ 重要メッセージ1つ？
  │   └─ YES → layout-callout
  │
  ├─ 2つを比較する？
  │   ├─ 画像あり？
  │   │   └─ YES → layout-horizontal
  │   └─ テキストのみ？
  │       └─ YES → layout-comparison
  │
  ├─ 手順・フロー（3-7個）？
  │   ├─ 画像あり？
  │   │   └─ YES → layout-horizontal
  │   └─ テキストのみ？
  │       └─ YES → layout-timeline
  │
  ├─ コード例を大きく見せたい？
  │   └─ YES → layout-code-focus
  │
  └─ それ以外
      └─ 既存レイアウト（two-column, three-column等）
```

---

## まとめ

新しい4つのレイアウトは、特定の用途に特化しています：

1. **layout-comparison**: 対比を視覚的に明確化
2. **layout-callout**: 重要メッセージを印象的に
3. **layout-timeline**: フローを直感的に理解
4. **layout-code-focus**: コードを読みやすく表示

これらは既存レイアウトを置き換えるものではなく、**追加の選択肢**として活用してください。

既存のスライド（220枚）は現在のレイアウトで十分に機能しているため、無理に変換する必要はありません。今後、新しいスライドを作成する際に、これらのレイアウトを検討してください。
