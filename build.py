#!/usr/bin/env python3
import json, os, pathlib, shutil, re
from jinja2 import Environment, FileSystemLoader

SRC_DIR   = pathlib.Path(__file__).parent
TEMPLATE  = Environment(loader=FileSystemLoader(SRC_DIR / "templates"))
CONTENT   = json.loads((SRC_DIR / "content" / "formulas.json").read_text(encoding="utf-8"))
DIST      = SRC_DIR / "dist"

def slug(s): return re.sub(r'[^a-z0-9\-]+', '-', s.lower()).strip('-')

def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")

def generate_sidebar():
    """Generate the modern, flat sidebar navigation HTML"""
    sidebar_html = '''
    <nav>
        <ul class="sidebar-nav">
            <!-- Mathematics Section -->
            <li class="section-header">Mathematics</li>
            <li><a href="../math/index.html" class="nav-link">Mathematics Home</a></li>
            <li><a href="../math/arithmetic.html" class="nav-link">Arithmetic</a></li>
            <li><a href="../math/number_theory.html" class="nav-link">Number Theory</a></li>
            <li><a href="../math/algebra.html" class="nav-link">Algebra</a></li>
            <li><a href="../math/geometry.html" class="nav-link">Geometry</a></li>
            <li><a href="../math/trigonometry.html" class="nav-link">Trigonometry</a></li>
            <li><a href="../math/analytic_geometry.html" class="nav-link">Analytic Geometry</a></li>
            <li><a href="../math/differential_geometry.html" class="nav-link">Differential Geometry</a></li>
            <li><a href="../math/calculus.html" class="nav-link">Calculus</a></li>
            <li><a href="../math/vector_calculus.html" class="nav-link">Vector Calculus</a></li>
            <li><a href="../math/linear_algebra.html" class="nav-link">Linear Algebra</a></li>
            <li><a href="../math/abstract_algebra.html" class="nav-link">Abstract Algebra</a></li>
            <li><a href="../math/probability.html" class="nav-link">Probability</a></li>
            <li><a href="../math/statistics.html" class="nav-link">Statistics</a></li>
            <li><a href="../math/logic.html" class="nav-link">Logic</a></li>
            <li><a href="../math/set_theory.html" class="nav-link">Set Theory</a></li>
            <li><a href="../math/topology.html" class="nav-link">Topology</a></li>
            <li><a href="../math/differential_equations.html" class="nav-link">Differential Equations</a></li>
            
            <!-- Physics Section -->
            <li class="section-header">Physics</li>
            <li><a href="../physics/index.html" class="nav-link">Physics Home</a></li>
            <li><a href="../physics/mechanics.html" class="nav-link">Mechanics</a></li>
            <li><a href="../physics/thermodynamics.html" class="nav-link">Thermodynamics</a></li>
            <li><a href="../physics/electromagnetism.html" class="nav-link">Electromagnetism</a></li>
            <li><a href="../physics/optics.html" class="nav-link">Optics</a></li>
            <li><a href="../physics/waves-and-oscillations.html" class="nav-link">Waves & Oscillations</a></li>
            <li><a href="../physics/quantum-mechanics.html" class="nav-link">Quantum Mechanics</a></li>
            <li><a href="../physics/relativity.html" class="nav-link">Relativity</a></li>
            <li><a href="../physics/fluid-mechanics.html" class="nav-link">Fluid Mechanics</a></li>
            <li><a href="../physics/nuclear-physics.html" class="nav-link">Nuclear Physics</a></li>
        </ul>
    </nav>
    '''
    return sidebar_html.strip()

def build_page(subject, page_key, page_data):
    html = TEMPLATE.get_template("formula_page.html").render(
        subject=subject, 
        page_key=page_key, 
        page_data=page_data, 
        slug=slug,
        sidebar_content=generate_sidebar()
    )
    write(DIST / page_data["path"], html)

def copy_assets():
    for f in ("style.css", "script.js"):
        shutil.copy2(SRC_DIR / f, DIST / f)

def main():
    # Try to remove dist directory, handle Windows permission errors
    if DIST.exists():
        try:
            shutil.rmtree(DIST)
        except PermissionError:
            print(f"Warning: Could not remove {DIST} - files may be in use. Trying to clear contents...")
            # Try to remove individual files instead
            try:
                for item in DIST.iterdir():
                    if item.is_file():
                        try:
                            item.unlink()
                        except PermissionError:
                            print(f"Could not remove {item} - file in use")
                    elif item.is_dir():
                        try:
                            shutil.rmtree(item)
                        except PermissionError:
                            print(f"Could not remove directory {item} - files in use")
            except Exception as e:
                print(f"Warning: Could not fully clear {DIST}: {e}")
    
    # Ensure dist directory exists
    DIST.mkdir(exist_ok=True)
    
    # Build all pages from content
    for subject, pages in CONTENT.items():
        for page_key, page in pages.items():
            build_page(subject, page_key, page)
    
    # Landing page → redirect to Math
    idx = TEMPLATE.get_template("base.html").render(
        title="Formula Reference", 
        body='<script>location.href="math/index.html"</script><noscript><a href="math/index.html">Go to Mathematics</a></noscript>'
    )
    write(DIST / "index.html", idx)
    
    copy_assets()
    print(f"Generated {len([p for pages in CONTENT.values() for p in pages])} pages to {DIST}")

if __name__ == "__main__":
    main() 