# Landing Pages — Git Workflow

## Branches

- **main** — Production. Deploys to `get.officialnancy.com`. Protected: requires PR + 1 approval.
- **staging** — Preview/testing. Push freely here. Create PRs from staging → main when ready.

## Workflow

1. **New page or change?** Push to `staging` branch (or create a feature branch like `feat/new-lp-name`)
2. **Preview** at the staging branch URL or locally
3. **Create a PR** from your branch → `main`
4. **Get 1 approval** (Neil, Momo, or Rahul)
5. **Merge** — GitHub Pages auto-deploys to production

## Rules

- ❌ Never push directly to `main`
- ✅ Always use PRs for production changes
- 🔍 Test on staging first
- 📝 Use descriptive commit messages

## Naming Convention

- Folders: `lem-[slug]/index.html` (not loose .html files)
- Images: `shared/images/` for reusable assets
- UTM: `utm_source=advertorial&utm_medium=seo-review&utm_campaign=[page-slug]`

