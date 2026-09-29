Development repository for gluex.org

# Setup ruby for compatible version in Homebrew (temporary fix?)
export PATH="/opt/homebrew/opt/ruby@3.4/bin:$PATH"

# Run server locally to be broadcast on http://127.0.0.1:4000
bundle exec jekyll serve

# Build _site/ directory to deploy on gluex.org
bundle exec jekyll build

# Adding new papers: execute python script after modifying source file location
python writePaperYML.py 
## Modify output file: _data/papers/PaperName.yml
## Add `order: N` to place paper in descending order on the webpage 
