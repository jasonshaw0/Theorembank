# TheoremBank

TheoremBank is a static formula reference site for mathematics and physics. It is built with plain HTML, CSS and JavaScript and is designed to be hosted directly on GitHub Pages.

## Features

- Organized collections of formulas for many subjects (arithmetic, algebra, calculus, mechanics and more)
- MathJax based rendering of LaTeX expressions
- Responsive sidebar navigation with mobile support
- Built in search (`Ctrl+K`) to filter formulas on each page
- Dark/light theme toggle (`Ctrl+J`) stored in local storage
- Copy to clipboard buttons for LaTeX code
- Live Math editor at `math/editor.html` using MathLive

## Repository Layout

```
/
├── index.html             # Welcome page
├── style.css              # Global styles
├── script.js              # Interactive behaviour
├── content/formulas.json  # Formula data used to generate pages
├── templates/             # Jinja2 templates used by quick_rebuild.py
├── math/ and physics/     # Generated content pages
└── quick_rebuild.py       # Static site generator script
```

## Building the site

1. Ensure Python 3 with Jinja2 is installed.
2. Edit `content/formulas.json` to add or update formulas.
3. Run `python quick_rebuild.py` to regenerate HTML pages from templates.
4. Serve the folder locally with a simple HTTP server to test:

```
python -m http.server 8000
```

All pages are fully static and can be pushed to GitHub Pages without any additional build steps.

## GitHub Pages Deployment

1. Commit and push the contents of this repository to a branch named `gh-pages` or enable GitHub Pages from the repository settings.
2. Ensure the `.nojekyll` file remains so GitHub does not attempt Jekyll processing.
3. Your site will be available at `https://<username>.github.io/<repository>`.

## License

This project is released under the MIT license. See `LICENSE` for details.
