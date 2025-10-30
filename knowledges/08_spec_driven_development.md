# スペック駆動開発（Spec-Driven Development）

## 概要
AI時代の新しい開発パラダイム - 実装ではなく仕様を中心に据えた開発手法

出典: "Spec-Driven Development: The Future of AI Coding | Guy Podjarny (Tessl)"

---

## スペック駆動開発とは

### 基本概念

**従来の開発（Code-Centric）**:
```
コードが真実の源泉
└─ 実装 = 仕様
└─ ドキュメントは後回し
└─ コードを読んで理解
```

**スペック駆動開発（Spec-Centric）**:
```
仕様が真実の源泉
└─ 仕様 → 実装（AI生成）
└─ 仕様が常に最新
└─ 仕様を読んで理解
```

### パラダイムシフト

> 「ソフトウェア開発はAIによって進化ではなく、変革する。
> その核心は、コードによる定義から仕様による定義への移行である。」
> - Guy Podjarny, Tessl創業者

---

## 3つの段階

### 1. Spec-Assisted Development（仕様支援開発）

**概念**:
仕様やドキュメントがエージェントを「支援」する

**実装例**:
```markdown
# プロジェクトガイドライン

## コーディング規約
- camelCase命名規則
- TypeScript必須
- テストカバレッジ80%以上

## 使用スタック
- フロント: React + Next.js
- バック: Node.js + PostgreSQL
- 認証: Firebase Auth

## ポリシー
- PRレビュー必須
- デプロイは staging → production
```

**メリット**:
- エージェントが一貫した出力を生成
- プロジェクト固有の知識を活用
- チーム標準の自動適用

**現状**:
これが現在のベストプラクティス（.cursorrules.md、claude.mdなど）

---

### 2. Spec-Driven Development（仕様駆動開発）

**概念**:
仕様の一部を「真実の源泉」として扱う

**実装例**:
```yaml
# checkout-process.spec.yaml

name: CheckoutProcess
description: E-commerce checkout workflow

steps:
  1_cart_review:
    name: "カート確認"
    inputs:
      - cart_items: Product[]
      - user: User
    validations:
      - cart_not_empty
      - items_in_stock
    outputs:
      - subtotal: number
      - tax: number
      - total: number

  2_shipping_address:
    name: "配送先入力"
    inputs:
      - user_address: Address?
    validations:
      - valid_postal_code
      - deliverable_area
    outputs:
      - shipping_address: Address
      - shipping_fee: number

  3_payment:
    name: "支払い"
    inputs:
      - payment_method: PaymentMethod
      - total_amount: number
    validations:
      - valid_payment_method
      - sufficient_funds
    outputs:
      - transaction_id: string
      - payment_status: PaymentStatus

  4_confirmation:
    name: "注文確認"
    inputs:
      - order_data: OrderData
    outputs:
      - order_id: string
      - confirmation_email: Email

constraints:
  - all_steps_required: true
  - max_timeout: 30_minutes
  - retry_on_failure: payment_step_only
```

**コードは仕様から生成**:
```typescript
// AIによる自動生成
class CheckoutProcess {
  async execute(cart: Cart, user: User): Promise<Order> {
    // Step 1: Cart Review
    const { subtotal, tax, total } = await this.reviewCart(cart);

    // Step 2: Shipping Address
    const { shipping_address, shipping_fee } =
      await this.getShippingAddress(user);

    // Step 3: Payment
    const { transaction_id, payment_status } =
      await this.processPayment(total + shipping_fee);

    // Step 4: Confirmation
    const { order_id } = await this.createOrder({
      cart,
      shipping_address,
      transaction_id,
    });

    return order_id;
  }
}
```

**メリット**:
- 仕様とコードの乖離がゼロ
- ビジネスロジックの明確化
- AIによる実装の自動生成
- 変更時も仕様を修正すれば自動で反映

---

### 3. Spec-Centric Development（仕様中心開発）

**概念**:
すべての定義を仕様で行い、コードは副産物

**ビジョン**:
```
開発者の役割:
├─ ❌ コードを書く
└─ ✅ 仕様を定義する

AIの役割:
├─ 仕様の解釈
├─ 実装の生成
├─ テストの作成
├─ 最適化
└─ 自律的メンテナンス
```

**未来の姿**:
```yaml
# app.spec.yaml

application:
  name: TaskManager
  description: "チーム向けタスク管理アプリ"

  requirements:
    - real_time_collaboration
    - offline_support
    - cross_platform

  budget:
    performance: high_priority
    cost: moderate

  preferences:
    ui_style: minimalist
    color_scheme: blue_professional

  integrations:
    - slack
    - google_calendar
    - github

# このspecから、AIが:
# - フロント/バックエンドコード生成
# - データベーススキーマ設計
# - API定義
# - テストスイート作成
# - デプロイメント設定
# すべてを自動生成
```

---

## Spec-Driven vs 他の手法

### vs Test-Driven Development (TDD)

**TDD**:
```ruby
# テストを先に書く
describe 'Calculator' do
  it 'adds two numbers' do
    calc = Calculator.new
    expect(calc.add(2, 3)).to eq(5)
  end
end

# 次に実装
class Calculator
  def add(a, b)
    a + b
  end
end
```

**Spec-Driven**:
```yaml
# 仕様を定義
calculator.spec:
  operations:
    add:
      inputs: [number, number]
      output: number
      behavior: "returns sum of inputs"
      examples:
        - add(2, 3) = 5
        - add(-1, 1) = 0

# AIが実装とテストの両方を生成
```

**比較**:
| 項目 | TDD | Spec-Driven |
|------|-----|-------------|
| 焦点 | テスト → 実装 | 仕様 → 実装+テスト |
| 自動化 | 低い | 高い（AI生成） |
| ビジネス理解 | コードレベル | 仕様レベル |
| 保守性 | 中 | 高（仕様が文書化） |

---

### vs Agile Development

**Agile**:
```
ユーザーストーリー:
"ユーザーとして、買い物カートに商品を追加したい"

→ スプリント計画
→ 実装
→ レビュー
→ イテレーション
```

**Spec-Driven + Agile**:
```
ユーザーストーリー:
"ユーザーとして、買い物カートに商品を追加したい"

→ 仕様定義（What + Why）
→ AIが実装案を複数生成
→ レビューと選択
→ 仕様の反復改善
```

**相互補完**:
- Agileはプロセス（How）
- Spec-Drivenは定義方法（What）
- 両方を組み合わせることで最強

---

## 実践: GitHub Spec Kit

### 基本的な使い方

**1. 仕様ファイル作成**
```markdown
# specs/user-authentication.md

## 概要
ユーザー認証システムの仕様

## 要件
- メール/パスワードでログイン
- OAuth対応（Google, GitHub）
- 多要素認証オプション
- セッション管理
- パスワードリセット機能

## セキュリティ制約
- パスワードは bcrypt でハッシュ化
- セッションは24時間で期限切れ
- ログイン失敗5回でアカウントロック

## APIエンドポイント
```yaml
/auth/login:
  method: POST
  body:
    email: string
    password: string
  responses:
    200: { token: string, user: User }
    401: { error: "Invalid credentials" }

/auth/oauth/{provider}:
  method: GET
  params:
    provider: "google" | "github"
  responses:
    302: redirect to provider

/auth/logout:
  method: POST
  headers:
    Authorization: "Bearer {token}"
  responses:
    200: { message: "Logged out" }
```

**2. AIに実装を依頼**
```bash
claude code

# プロンプト:
"specs/user-authentication.md に基づいて、
ユーザー認証システムを実装してください。

使用技術:
- Node.js + Express
- PostgreSQL
- JWT

テストも含めてください。"
```

**3. 仕様の更新**
```diff
# specs/user-authentication.md

## 要件
- メール/パスワードでログイン
- OAuth対応（Google, GitHub）
+ - OAuth対応にAppleを追加
- 多要素認証オプション
+ - 生体認証サポート（Face ID, Touch ID）
```

**4. 実装の自動更新**
```bash
# Spec Kitが差分を検出
# AIが変更箇所のみ更新
# テストも自動更新
```

---

## メリットと課題

### メリット

**1. 保守性の向上**
```
従来:
コード変更 → ドキュメント更新忘れ → ドキュメント陳腐化

Spec-Driven:
仕様更新 → コード自動生成 → 常に同期
```

**2. 自律的メンテナンス**
```
仕様が明確 → AIが自律的に:
- バグ修正
- セキュリティパッチ
- パフォーマンス最適化
- 依存関係更新
```

**3. コンテキスト適応**
```yaml
# 同じ仕様、異なるコンテキスト

context_1:
  language: Python
  framework: FastAPI
  database: MongoDB

context_2:
  language: TypeScript
  framework: NestJS
  database: PostgreSQL

# 仕様は同じ、実装は自動で最適化
```

**4. アクセシビリティ**
```
非開発者でも:
- 仕様を書ける（自然言語ベース）
- ビジネスロジックを直接定義
- AIが実装を生成

→ 開発の民主化
```

---

### 課題

**1. LLMの限界**
```
現状のAI:
- 複雑なアルゴリズムは苦手
- エッジケースの処理不足
- パフォーマンス最適化に限界

対策:
- 段階的導入
- 人間のレビュー
- ハイブリッドアプローチ
```

**2. 仕様の品質**
```
問題:
- 曖昧な仕様 → 曖昧な実装
- 過度に詳細 → 柔軟性喪失

解決:
- 仕様の書き方ガイドライン
- AIによる仕様レビュー
- イテレーティブな改善
```

**3. デバッグとトラブルシューティング**
```
疑問:
「AIが生成したコードをどうデバッグ？」

アプローチ:
- ログとモニタリングの充実
- 仕様レベルでの問題特定
- AIにデバッグを依頼
```

**4. チームの適応**
```
文化的変化:
- 「コードを書く」 → 「仕様を定義する」
- スキルセットの変化
- 学習曲線

支援:
- トレーニングプログラム
- 段階的な導入
- サクセスストーリーの共有
```

---

## 実践ガイド

### 始め方（段階的アプローチ）

**Phase 1: Spec-Assisted（1-2ヶ月）**
```markdown
目標:
- claude.md / .cursorrules を充実させる
- プロジェクト固有知識を文書化
- AIの出力品質向上を体感

アクション:
1. プロジェクトルールを文書化
2. コーディング規約を明文化
3. よくある質問をFAQ化
4. AIに読み込ませて効果測定
```

**Phase 2: Spec-Driven Lite（2-4ヶ月）**
```markdown
目標:
- 重要なビジネスロジックを仕様化
- 仕様ファイルから実装生成を体験

アクション:
1. 1-2機能を仕様ファイル化
2. GitHub Spec Kitを試用
3. 仕様→実装のフローを確立
4. チームでレビュー
```

**Phase 3: Spec-Driven Full（6ヶ月+）**
```markdown
目標:
- 新規機能はすべて仕様ファースト
- 既存コードも徐々に仕様化

アクション:
1. 仕様テンプレート作成
2. チーム全体でトレーニング
3. CI/CDに仕様検証を組み込み
4. メトリクス追跡と改善
```

---

## ベストプラクティス

### 1. 良い仕様の書き方

**悪い例（曖昧）**:
```markdown
ユーザーがログインできるようにする
```

**良い例（明確）**:
```markdown
# ユーザーログイン機能

## 入力
- email: string (required, valid email format)
- password: string (required, min 8 chars)

## 処理
1. emailでユーザー検索
2. パスワードをbcryptで検証
3. 成功時: JWTトークン生成（24時間有効）
4. 失敗時: ログイン試行回数カウント

## 出力
成功:
  - status: 200
  - body: { token: string, user: { id, email, name } }

失敗:
  - status: 401
  - body: { error: "Invalid credentials", attempts_left: number }

## セキュリティ
- 5回失敗でアカウントロック(30分)
- トークンはhttpOnlyクッキーに保存
- ログイン履歴を記録
```

### 2. レイヤー分け

```
仕様の階層:
├─ システム仕様（全体アーキテクチャ）
├─ モジュール仕様（各機能）
├─ API仕様（インターフェース）
└─ データ仕様（モデル・スキーマ）
```

### 3. バージョニング

```
仕様のバージョン管理:
- Git管理必須
- セマンティックバージョニング
- 変更履歴を明記
- 後方互換性を考慮
```

---

## 成功事例

### ケース1: SaaSスタートアップ

**状況**:
- チーム5人
- リリースまで3ヶ月

**Spec-Driven導入**:
```
Before:
- 開発速度: 2週間/機能
- ドキュメント: 常に古い
- バグ: 多い

After:
- 開発速度: 3日/機能（6.7倍）
- ドキュメント: 常に最新（仕様=ドキュメント）
- バグ: 50%減少（仕様明確化）
```

### ケース2: エンタープライズ移行

**状況**:
- レガシーシステム刷新
- 複雑なビジネスロジック

**アプローチ**:
```
1. 既存コードを仕様化（逆エンジニアリング）
2. 仕様をレビュー・改善
3. 新仕様から新システム生成
4. 段階的移行
```

**結果**:
- 移行期間: 2年 → 9ヶ月
- コスト: 70%削減
- ビジネスロジックの可視化成功

---

## 将来展望

### 2025-2026
```
- AIモデルの精度向上
- Spec-Driven IDEの普及
- 自然言語仕様の実用化
```

### 2027-2030
```
- 完全自律的メンテナンス
- コンテキスト自動最適化
- 「プログラマー」の役割変化
  → 「仕様設計者」「アーキテクト」へ
```

### Long-term Vision
```
開発プロセス:
  問題定義 → 仕様記述 → [AIが全自動] → 完成

人間の役割:
  - What（何を作るか）
  - Why（なぜ作るか）
  - 品質レビュー
  - 戦略的意思決定
```

---

## まとめ

### キーポイント
1. **パラダイムシフト**: Code-Centric → Spec-Centric
2. **段階的導入**: Assisted → Driven → Centric
3. **AI活用**: 仕様からの自動生成
4. **未来志向**: 今から準備を始める

### アクションプラン
```
今日:
- claude.mdを充実させる

今週:
- 1機能を仕様ファイル化してみる

今月:
- GitHub Spec Kitを試す

3ヶ月:
- チームで小規模プロジェクトを Spec-Driven で実施

6ヶ月:
- 主要プロジェクトに導入
```

---

**参考リソース**:
- Tessl: https://www.tessl.io
- GitHub Spec Kit
- 動画: "Spec-Driven Development: The Future of AI Coding"
