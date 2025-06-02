# 🏦 Theorembank
*Your Mathematical Formula Repository*

A comprehensive, modern web-based reference for mathematical and physics formulas, built with LaTeX rendering and designed for students, researchers, and professionals.

## ✨ Features

- **📐 Comprehensive Formula Library**: Over 128 formulas across 28 mathematical and physics topics
- **🎨 Modern UI**: Clean, responsive design with dark/light theme support
- **📱 Mobile Friendly**: Optimized navigation and formula viewing on all devices
- **🔍 Smart Search**: Instant formula search with Ctrl+K shortcut
- **📋 One-Click Copy**: Copy LaTeX code directly to clipboard
- **⚡ Fast Navigation**: Flat, hierarchical navigation without dropdowns
- **🧮 MathJax Rendering**: Beautiful mathematical formula rendering

## 🌐 Live Demo

Visit the live site at: `http://localhost:8080` (when running locally)

## 📚 Topics Covered

### Mathematics
- Arithmetic & Number Theory
- Algebra & Abstract Algebra
- Geometry & Analytic Geometry
- Trigonometry & Calculus
- Linear Algebra & Vector Calculus
- Differential Equations & Geometry
- Probability & Statistics
- Logic & Set Theory
- Topology

### Physics
- Mechanics & Thermodynamics
- Electromagnetism & Optics
- Quantum Mechanics & Relativity
- Waves & Oscillations
- Fluid Mechanics & Nuclear Physics

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- Modern web browser

### Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/theorembank.git
   cd theorembank
   ```

2. **Install dependencies**:
   ```bash
   pip install jinja2
   ```

3. **Build the website**:
   ```bash
   python build.py
   ```

4. **Launch local server**:
   ```bash
   cd dist
   python -m http.server 8080
   ```

5. **Open in browser**: Navigate to `http://localhost:8080`

## 🏗️ Project Structure

```
theorembank/
├── 📁 content/           # Generated JSON formula data
├── 📁 dist/              # Built website (generated)
├── 📁 templates/         # Jinja2 HTML templates
├── 📁 math/              # Math topic LaTeX sources
├── 📁 physics/           # Physics topic LaTeX sources
├── 📄 formula_library.tex # Main LaTeX formula source
├── 📄 build.py           # Website builder script
├── 📄 latex2json_working.py # LaTeX parser
├── 📄 style.css          # Main stylesheet
├── 📄 script.js          # Frontend JavaScript
└── 📄 index.html         # Entry point template
```

## 🔧 Development

### Adding New Formulas

1. **Edit LaTeX source**: Add formulas to `formula_library.tex` using the format:
   ```latex
   \subsection*{Topic Name}
   \textbf{Formula Name:} $\LaTeX_{formula}$.
   Description text here.
   ```

2. **Rebuild**: Run `python build.py` to regenerate the website

3. **Test**: Launch the local server to verify changes

### Customizing Appearance

- **Styles**: Edit `style.css` for visual customization
- **Layout**: Modify templates in `templates/` directory
- **Functionality**: Update `script.js` for new features

## ⌨️ Keyboard Shortcuts

- **Ctrl+K**: Open formula search
- **Ctrl+J**: Toggle dark/light theme
- **ESC**: Close search dialog

## 🎯 Features in Detail

### Smart Navigation
- **Fixed sidebar** with smooth scrolling
- **Flat hierarchy** - no collapsing menus
- **Current page highlighting**
- **Mobile-responsive** hamburger menu

### Formula Display
- **LaTeX rendering** via MathJax
- **Variable explanations** for each formula
- **Usage descriptions** and examples
- **Copy to clipboard** functionality

### Search & Discovery
- **Real-time search** across all formulas
- **Keyboard shortcuts** for power users
- **Topic-based organization**
- **Cross-references** between related concepts

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Add your formulas or improvements
4. Test thoroughly: `python build.py && cd dist && python -m http.server`
5. Submit a pull request

### Formula Guidelines
- Use clear, descriptive names
- Include variable definitions
- Provide usage context
- Follow existing LaTeX formatting

## 📄 License

MIT License - feel free to use this project for educational or commercial purposes.

## 🙏 Acknowledgments

- **MathJax** for beautiful formula rendering
- **Jinja2** for powerful templating
- **Modern CSS Grid** for responsive layouts
- **Mathematical community** for formula verification

## 📞 Support

- **Issues**: Report bugs or request features via GitHub Issues
- **Discussions**: Join conversations in GitHub Discussions
- **Documentation**: Check the wiki for detailed guides

---

**Theorembank** - *Banking Mathematical Knowledge for Everyone* 🏦📐 