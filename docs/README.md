# AI Development Training Slides

2日間のAI開発研修スライド (HTML版)

## 📖 View Slides

**[→ スライドを見る / View Slides](https://cuzic.github.io/ai-dev-yodoq/)**

## 📋 Contents

### Day 1: AI開発の基礎
- AI開発の3原則
- 役割変化: Developer → AI Navigator
- 5-STEPフロー
  - STEP1: 要件定義
  - STEP2: 設計
  - STEP3: タスク分解
  - STEP4: 実装 (TDD)
  - STEP5: 品質担保＆ドキュメント反映

### Day 2: 保守開発とベストプラクティス
- リバースエンジニアリング
- フィットギャップ分析
- テストシナリオ作成
- デグレ防止
- よくある失敗と対策

## 🛠️ Build from Source

このスライドはMarkdownから生成されています。

```bash
# Clone repository
git clone https://github.com/cuzic/ai-dev-yodoq.git
cd ai-dev-yodoq/slides

# Install dependencies
mise install
mise run install

# Generate HTML
npx -y @marp-team/marp-cli@latest all_slides.md --html --allow-local-files -o index.html
```

## 📄 License

© 2025 AI Development Training

---

**Repository**: https://github.com/cuzic/ai-dev-yodoq
