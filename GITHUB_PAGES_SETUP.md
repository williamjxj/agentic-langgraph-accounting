# GitHub Pages Setup Guide

This guide will help you set up and deploy the documentation site for **Agentic LangGraph Accounting** using GitHub Pages.

## 📋 What's Included

Your GitHub Pages setup includes the following files:

### Core Configuration Files

1. **`_config.yml`** - Jekyll configuration
   - Theme: Cayman
   - Site metadata and SEO settings
   - Build settings and plugins
   - File exclusions for clean deployment

2. **`.github/workflows/pages.yml`** - GitHub Actions workflow
   - Automated deployment on every push to `main`
   - Builds from `docs/` folder
   - Official GitHub Pages actions

3. **`Gemfile`** - Ruby dependencies
   - Jekyll and GitHub Pages gems
   - Plugins for enhanced functionality
   - Cross-platform compatibility

4. **`_layouts/default.html`** - Custom page layout
   - Professional navigation bar
   - Responsive design
   - Enhanced footer with links

5. **`docs/index.md`** - Main documentation landing page
   - Already exists with comprehensive content
   - Links to all documentation sections

## 🚀 Deployment Steps

### Option 1: Automatic Deployment (Recommended)

The site automatically deploys when you push to the `main` branch:

```bash
# Add all GitHub Pages files
git add _config.yml .github/workflows/pages.yml Gemfile _layouts/

# Commit the changes
git commit -m "Add GitHub Pages configuration and custom layout"

# Push to GitHub
git push origin main
```

The GitHub Actions workflow will:
1. Detect the push
2. Build the Jekyll site from `docs/`
3. Deploy to GitHub Pages
4. Provide a URL in the workflow output

### Option 2: Enable via Repository Settings

1. Go to your repository on GitHub
2. Click **Settings** → **Pages**
3. Under **Source**, select:
   - **GitHub Actions** (for automatic workflow deployment)
   - OR **Deploy from a branch** → `main` → `/docs`

## 🌐 Accessing Your Site

After deployment, your site will be available at:

**https://williamjxj.github.io/agentic-langgraph-accounting/**

## 🧪 Local Testing (Optional)

To preview your site locally before deploying:

### Install Ruby and Dependencies

```bash
# Install Ruby (if not already installed)
# macOS: Ruby comes pre-installed, or use Homebrew
brew install ruby

# Install Bundler
gem install bundler

# Install Jekyll and dependencies
bundle install
```

### Serve the Site Locally

```bash
# Build and serve from docs/ folder
bundle exec jekyll serve --source docs --baseurl ""

# Open http://localhost:4000 in your browser
```

## 📝 Customization Guide

### Changing the Theme

Edit `_config.yml`:

```yaml
theme: jekyll-theme-cayman  # Change to another GitHub Pages theme
# Available themes: minimal, cayman, slate, architect, etc.
```

### Modifying Navigation

Edit `_layouts/default.html` to update navigation links:

```html
<ul class="nav-links">
  <li><a href="{{ '/your-page.html' | relative_url }}">Your Page</a></li>
</ul>
```

### Adding New Pages

1. Create a new `.md` file in `docs/`
2. Add front matter (optional):
   ```yaml
   ---
   title: My New Page
   layout: default
   ---
   ```
3. Write your content in Markdown
4. Link to it from `index.md` or navigation

### SEO and Metadata

Edit `_config.yml` to improve SEO:

```yaml
title: Your Site Title
description: Your site description
author: Your Name
```

## 🔧 Advanced Configuration

### Custom Domain

To use a custom domain (e.g., `docs.yourdomain.com`):

1. Create a `CNAME` file in `docs/`:
   ```
   docs.yourdomain.com
   ```

2. Configure DNS records with your domain provider:
   - Add a CNAME record pointing to `williamjxj.github.io`

3. In GitHub Settings → Pages → Custom domain, enter your domain

### Analytics

Add Google Analytics to `_config.yml`:

```yaml
google_analytics: UA-XXXXXXXXX-X
```

### Additional Plugins

Edit `Gemfile` to add more plugins:

```ruby
group :jekyll_plugins do
  gem "jekyll-mentions"
  gem "jemoji"
end
```

Then update `_config.yml`:

```yaml
plugins:
  - jekyll-mentions
  - jemoji
```

## 📊 Monitoring Deployments

### Via GitHub Actions

1. Go to your repository → **Actions** tab
2. Click on the latest workflow run
3. View build logs and deployment status
4. Get the deployed URL from the output

### Via Repository Settings

1. Go to **Settings** → **Pages**
2. View "Your site is live at..." message
3. Check deployment history

## 🐛 Troubleshooting

### Build Failures

**Problem**: Workflow fails with "Page build failed"

**Solutions**:
- Check the Actions tab for detailed error logs
- Verify all Markdown files have valid syntax
- Ensure `_config.yml` has valid YAML syntax
- Check for broken internal links

### 404 Errors on Links

**Problem**: Links return 404 errors

**Solutions**:
- Use relative links: `[Link](page.md)` or `[Link](page.html)`
- Verify the `baseurl` in `_config.yml` is correct
- Check file paths are correct (case-sensitive)

### Styles Not Loading

**Problem**: Custom layout doesn't apply

**Solutions**:
- Clear browser cache
- Check `_layouts/default.html` is in the root (not in `docs/_layouts/`)
- Verify the layout is specified in `_config.yml` or page front matter

### Local Preview Issues

**Problem**: `bundle exec jekyll serve` fails

**Solutions**:
```bash
# Update dependencies
bundle update

# Clean and rebuild
bundle exec jekyll clean
bundle exec jekyll build --source docs

# Serve with verbose output
bundle exec jekyll serve --source docs --verbose
```

## 📚 Documentation Structure

Your current documentation structure:

```
docs/
├── index.md                        # Landing page ✅
├── qa.md                           # Query guide
├── estimation.md                   # Technical estimation
├── estimation-zh.md                # Chinese version
├── improvement-1.md                # Phase 1 docs
├── improvement-2.md                # Phase 2 docs
├── improvement-3.md                # Phase 3 docs
├── data-management.md              # Architecture guide
└── cross-platform-validation.md    # Validation report
```

All pages will automatically:
- Use the custom layout with navigation
- Include SEO metadata
- Be responsive and mobile-friendly
- Have anchor links for headings

## 🎨 Theme Customization

The Cayman theme provides a clean, professional look. To customize:

1. **Colors**: Edit `_layouts/default.html` CSS
2. **Typography**: Add custom fonts in the `<head>` section
3. **Layout**: Modify the HTML structure
4. **Components**: Add custom includes in `_includes/`

## 📦 Content Updates

To update documentation:

1. Edit files in `docs/`
2. Commit and push:
   ```bash
   git add docs/
   git commit -m "Update documentation"
   git push
   ```
3. GitHub Actions automatically rebuilds and deploys

## ✅ Checklist

- [✅] `_config.yml` created and configured
- [✅] `.github/workflows/pages.yml` workflow added
- [✅] `Gemfile` with dependencies created
- [✅] `_layouts/default.html` custom layout added
- [✅] `docs/index.md` documentation landing page exists
- [ ] Files committed and pushed to GitHub
- [ ] GitHub Pages enabled in repository settings
- [ ] Deployment successful and site accessible
- [ ] All links verified and working
- [ ] Custom domain configured (optional)

## 🔗 Useful Resources

- [GitHub Pages Documentation](https://docs.github.com/en/pages)
- [Jekyll Documentation](https://jekyllrb.com/docs/)
- [GitHub Pages Themes](https://pages.github.com/themes/)
- [Markdown Guide](https://www.markdownguide.org/)
- [Jekyll Cheat Sheet](https://devhints.io/jekyll)

## 💡 Tips

1. **Write in Markdown**: Keep all documentation in `.md` files for easy editing
2. **Use Relative Links**: Makes navigation work in both local and deployed environments
3. **Test Locally**: Preview changes before pushing to avoid build failures
4. **Monitor Actions**: Check the Actions tab after pushing to ensure successful deployment
5. **Version Control**: Keep documentation updates in separate commits for clarity

## 🆘 Getting Help

If you encounter issues:

1. Check the [Troubleshooting](#-troubleshooting) section above
2. Review GitHub Actions logs in the Actions tab
3. Consult [GitHub Pages documentation](https://docs.github.com/en/pages)
4. Open an issue in your repository

---

**Happy documenting! 🚀**

Your professional documentation site is ready to showcase your Agentic LangGraph Accounting project to the world.
