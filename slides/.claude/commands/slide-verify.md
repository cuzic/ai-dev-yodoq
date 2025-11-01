# Slide VERIFY - Phase 5: 最終検証

前後のコンテキストと受入条件を踏まえて、スライドの完成度を最終確認します。

## 実行タスク

### 1. コンテキストの確認

#### 前後のスライドとの整合性

`all_slides.md` を読み込み、以下を確認：

- **前のスライドとの繋がり**
  - トピックの流れが自然か
  - 説明の順序が論理的か
  - 重複する内容がないか

- **次のスライドへの流れ**
  - 次のトピックへの導線があるか
  - 唐突な話題転換になっていないか

- **セクション全体の整合性**
  - セクション内での位置づけが適切か
  - 他のスライドとの一貫性があるか

### 2. 受入条件の最終チェック

PLANフェーズで定義した全受入条件をチェックリスト形式で検証：

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ ACCEPTANCE CRITERIA CHECKLIST
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 Content Requirements:
  □ Clear and descriptive title
  □ Appropriate number of bullet points (3-8)
  □ SVG diagram included (if required)
  □ Content is accurate and complete
  □ Consistent with surrounding slides

📊 Quality Requirements (measurable):
  □ SVG overflow < 10px
  □ No text overlapping
  □ Text density < 80%
  □ Proper spacing and margins
  □ Fonts readable (minimum 40px for SVG)

🎨 Layout Requirements:
  □ Correct layout class applied
  □ Balanced composition
  □ Visually readable and appealing
  □ Images properly sized (width specified)

🔗 Context Requirements:
  □ Flows naturally from previous slide
  □ Leads naturally to next slide
  □ Consistent tone and style with section
  □ No content duplication

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

各項目を順番にチェックし、すべてにチェックが入ることを確認。

### 3. 全体品質スコアの確認

#### 判定スクリプトの最終実行

```bash
python3 validate_slide_[番号].py
```

すべてのエラーが解消され、警告も最小限であることを確認。

#### SVG境界の最終確認

```bash
python3 validate_svg_bounds.py | grep "diagram_[番号]"
```

該当SVGがPASSまたはWARN（軽微なオーバーフロー）であることを確認。

#### slidectl 測定（オプション）

利用可能な場合：

```bash
cd $HOME/slidectl
uv run slidectl measure --slide [番号] --html /home/cuzic/ai-dev-yodoq/slides/index.html
```

総合スコア 85/100 以上を目指す。

### 4. 視覚的最終確認

ブラウザで `index.html` を開き、以下を人間の目でチェック：

#### 読みやすさ
- [ ] フォントサイズが適切で読みやすい
- [ ] 色のコントラストが十分
- [ ] 行間・余白が適切

#### 理解しやすさ
- [ ] タイトルで内容が分かる
- [ ] 箇条書きが論理的
- [ ] 図表が内容を補完している

#### 視覚的バランス
- [ ] テキストと図表のバランスが良い
- [ ] スライド全体が美しい
- [ ] 統一感がある

#### スライドショーとしての流れ
- [ ] 前のスライドからスムーズに繋がる
- [ ] 次のスライドへ自然に流れる
- [ ] 全体のストーリーに沿っている

### 5. 最終メトリクスの記録

すべての測定結果を記録：

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 FINAL QUALITY REPORT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Slide: #[番号] - [スライドタイトル]

✅ Acceptance Criteria: ALL PASSED (12/12)

  Content Requirements: ✓✓✓✓✓
  Quality Requirements: ✓✓✓✓✓
  Layout Requirements: ✓✓✓✓
  Context Requirements: ✓✓✓✓

📈 Quality Metrics:

  Content:
  - Title length: [X] chars
  - Bullet points: [N] items (optimal: 3-8)
  - Total text: [XXX] chars

  SVG Quality (if applicable):
  - SVG overflow: [X]px (target: < 10px)
  - ViewBox: [width]x[height]
  - Display width: [width]px

  Layout:
  - Layout class: [レイアウト名]
  - Text density: [XX]% (target: < 80%)
  - Spacing: adequate

  Overall:
  - slidectl score: [XX]/100 (target: ≥ 85)
  - Visual appeal: ⭐⭐⭐⭐⭐

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 Status: READY FOR PRODUCTION

Files modified:
  - all_slides.md (added/updated slide #[番号])
  - diagrams/diagram_[番号]_[name].svg (created/updated)
  - index.html (regenerated)
  - validate_slide_[番号].py (created)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 6. ドキュメント化

#### スライド作成の記録

作成プロセスを簡潔に記録（コメントまたは別ファイル）：

```markdown
## Slide #[番号] - [タイトル]

### Creation Process (TDD Cycle)

**PLAN**:
- Layout: [レイアウト名]
- Content: [箇条書き項目数]項目 + SVG図表
- Target: [目的・狙い]

**RED**:
- Created validation script: validate_slide_[番号].py
- Initial status: FAILED (slide not created)

**GREEN**:
- Created slide markdown in all_slides.md
- Created SVG diagram: diagram_[番号]_[name].svg
- Status: PASSED (all criteria met)

**REFACTOR**:
- Iteration 1: [実施した改善]
- Iteration 2: [実施した改善]
- Final score: [XX]/100

**VERIFY**:
- All acceptance criteria: PASSED
- Context check: PASSED
- Visual confirmation: PASSED
- Status: PRODUCTION READY

### Quality Metrics (Final)
- SVG overflow: [X]px
- Text density: [XX]%
- Bullet count: [N]
- Overall score: [XX]/100
```

#### 特記事項の記録

特殊な対応や注意点があれば記録：

```markdown
### Notes
- [特記事項1]
- [特記事項2]
```

### 7. 次のステップの提示

ユーザーに次のアクションを提示：

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎉 SLIDE CREATION COMPLETE!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Slide #[番号] is ready for production

📋 Next Steps:

  1. Review in browser:
     open index.html

  2. Commit changes:
     git add all_slides.md diagrams/ index.html
     git commit -m "feat: Add slide #[番号] - [タイトル]"

  3. Push to GitHub:
     git push origin main

  4. Verify on GitHub Pages:
     https://[username].github.io/[repo]/

  5. Optional: Clean up validation script
     mv validate_slide_[番号].py archive/

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Would you like to commit and push now? (yes/no)
```

### 8. TodoList更新

すべてのタスクを完了としてマーク。

## 確認ポイント

- ✅ すべての受入条件を満たしているか
- ✅ 前後のスライドとの整合性があるか
- ✅ 視覚的に美しく読みやすいか
- ✅ 品質メトリクスが目標値を達成しているか
- ✅ ドキュメントが適切に記録されているか

## 成功基準

以下をすべて満たせば成功：

- ✅ すべての受入条件をパス
- ✅ SVG境界オーバーフロー < 10px
- ✅ テキスト重なりなし
- ✅ 文字密度 < 80%
- ✅ 指定レイアウトが適用
- ✅ 前後のスライドとの整合性
- ✅ 総合スコア 85/100 以上（slidectl使用時）
- ✅ 視覚的に美しく読みやすい

## 完了

すべての確認が完了し、ユーザーの最終承認を得たら、スライド作成TDDサイクル完了です。

必要に応じて、git commit と git push を実行してGitHub Pagesに反映します。
