# GitHub Pages Deployment

This project automatically deploys slides to GitHub Pages.

## 🌐 Live URL

**https://cuzic.github.io/ai-dev-yodoq/**

## 📁 Structure

```
ai-dev-yodoq/
├── docs/                    # GitHub Pages root
│   ├── index.html          # Generated Marp slides
│   ├── diagrams/           # SVG diagrams
│   ├── README.md           # Landing page
│   ├── .nojekyll           # Disable Jekyll processing
│   └── _config.yml         # GitHub Pages config
├── .github/
│   └── workflows/
│       └── deploy-slides.yml  # Auto-deployment workflow
└── slides/                 # Source files
    ├── day1_1.md
    ├── day1_2.md
    ├── ...
    └── all_slides.md       # Combined markdown
```

## 🚀 Deployment

### Automatic Deployment

GitHub Actions automatically builds and deploys when you push changes to:
- `slides/**` - Markdown source files
- `diagrams/**` - SVG diagrams

**Trigger**: Push to `main` branch

### Manual Deployment

```bash
# Build HTML locally
cd slides
mise run build-html

# Or using npx directly
npx -y @marp-team/marp-cli@latest all_slides.md --html --allow-local-files -o ../docs/index.html

# Commit and push
git add docs/
git commit -m "docs: Update slides"
git push
```

### Preview Locally

```bash
cd slides
mise run deploy-preview

# Opens HTTP server on http://localhost:8000
# View slides at http://localhost:8000/index.html
```

## ⚙️ GitHub Pages Settings

1. Go to: **Settings** → **Pages**
2. Set:
   - **Source**: Deploy from a branch
   - **Branch**: `main`
   - **Folder**: `/docs`

Or use GitHub Actions deployment (current setup):
- **Source**: GitHub Actions
- Workflow: `.github/workflows/deploy-slides.yml`

## 🔄 Workflow Details

The deployment workflow:

1. **Triggers** on push to `main` (slides or diagrams changed)
2. **Installs** Node.js and Marp CLI
3. **Generates** HTML from `all_slides.md`
4. **Copies** diagrams to docs folder
5. **Deploys** to GitHub Pages

### Workflow File

`.github/workflows/deploy-slides.yml`:

```yaml
name: Deploy Slides to GitHub Pages

on:
  push:
    branches: [main]
    paths: ['slides/**', 'diagrams/**']
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: npm install -g @marp-team/marp-cli
      - run: marp slides/all_slides.md --html -o docs/index.html
      - uses: actions/upload-pages-artifact@v3

  deploy:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - uses: actions/deploy-pages@v4
```

## 🛠️ Local Development

### Build HTML

```bash
# Using mise (recommended)
mise run build-html

# Using Marp CLI directly
cd slides
npx -y @marp-team/marp-cli@latest all_slides.md --html --allow-local-files -o ../docs/index.html
```

### Preview

```bash
# Start local server
cd docs
python3 -m http.server 8000

# Or use mise task
cd slides
mise run deploy-preview
```

Visit: http://localhost:8000/index.html

## 📝 Making Changes

1. **Edit slides** in `slides/day*.md`
2. **Update diagrams** in `diagrams/`
3. **Build locally** to test:
   ```bash
   mise run build-html
   ```
4. **Commit and push**:
   ```bash
   git add slides/ diagrams/ docs/
   git commit -m "docs: Update slides"
   git push
   ```
5. **Wait 1-2 minutes** for GitHub Actions to deploy

## 🔍 Troubleshooting

### Slides not updating

1. Check GitHub Actions: https://github.com/cuzic/ai-dev-yodoq/actions
2. Verify workflow ran successfully
3. Clear browser cache (Ctrl+Shift+R)

### Diagrams not showing

1. Ensure diagrams are copied to `docs/diagrams/`
2. Check file paths in HTML (should be relative: `diagrams/...`)
3. Verify `.nojekyll` file exists in `docs/`

### Build failures

1. Check workflow logs in Actions tab
2. Test locally: `mise run build-html`
3. Verify `all_slides.md` is up to date

## 📊 File Sizes

- **HTML**: ~1.7 MB (includes inline SVGs)
- **Individual SVGs**: ~2 MB total (44 files)
- **Total**: ~3.7 MB

## 🎨 Customization

### Marp Themes

Edit `slides/all_slides.md` front matter:

```yaml
---
marp: true
theme: default
size: 16:9
---
```

Available themes: `default`, `gaia`, `uncover`

### Custom CSS

Add to markdown:

```markdown
<style>
section {
  font-family: 'Noto Sans JP', sans-serif;
}
</style>
```

## 🔐 Security

- ✅ No secrets required
- ✅ Static HTML only
- ✅ No server-side processing
- ✅ Safe for public viewing

## 📚 Resources

- [Marp Documentation](https://marp.app/)
- [GitHub Pages Docs](https://docs.github.com/en/pages)
- [GitHub Actions Docs](https://docs.github.com/en/actions)

## ✅ Checklist

- [x] HTML slides generated
- [x] Diagrams copied to docs/
- [x] GitHub Actions workflow created
- [x] .nojekyll file added
- [x] README updated
- [x] Mise tasks configured
- [ ] Enable GitHub Pages in repo settings
- [ ] Push to GitHub
- [ ] Verify deployment

## 🚀 Next Steps

1. **Enable GitHub Pages**:
   - Go to repo Settings → Pages
   - Select "GitHub Actions" as source

2. **Push changes**:
   ```bash
   git add .
   git commit -m "feat: Add GitHub Pages deployment"
   git push
   ```

3. **Verify**:
   - Check Actions tab for workflow run
   - Visit https://cuzic.github.io/ai-dev-yodoq/

4. **Share**:
   - Share URL with attendees
   - Embed in training materials
