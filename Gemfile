source "https://rubygems.org"

# Jekyll and GitHub Pages
gem "jekyll", "~> 3.9.3"
gem "github-pages", "~> 228", group: :jekyll_plugins

# Jekyll plugins
group :jekyll_plugins do
  gem "jekyll-feed", "~> 0.12"
  gem "jekyll-seo-tag", "~> 2.6"
  gem "jekyll-sitemap", "~> 1.4"
  gem "jekyll-relative-links"
  gem "jekyll-optional-front-matter"
  gem "jekyll-readme-index"
  gem "jekyll-titles-from-headings"
  gem "jekyll-github-metadata"
end

# Platform-specific gems
platforms :mingw, :x64_mingw, :mswin, :jruby do
  gem "tzinfo", ">= 1", "< 3"
  gem "tzinfo-data"
end

# Performance booster for watching directories on Windows
gem "wdm", "~> 0.1.1", :platforms => [:mingw, :x64_mingw, :mswin]

# Lock `http_parser.rb` gem to `v0.6.x` on JRuby builds
gem "http_parser.rb", "~> 0.6.0", :platforms => [:jruby]

# kramdown v2 ships without the gfm parser by default
gem "kramdown-parser-gfm"

# webrick is no longer bundled with Ruby 3.0
gem "webrick", "~> 1.7"
