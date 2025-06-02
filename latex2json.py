#!/usr/bin/env python3
# latex2json.py  ── run once whenever the TeX master file changes
import re, json, pathlib, textwrap

TEX = pathlib.Path("formula_library.tex").read_text(encoding="utf-8")
OUT = pathlib.Path("content/formulas.json")

print("📖 Reading formula_library.tex...")
print(f"📏 File size: {len(TEX)} characters")

# 1. split on subsection headings -------------------------------------------------
blocks = re.split(r'\\subsection\*\{([^}]+)\}', TEX)[1:]   # returns [title, body, title, body, …]
sections = [(blocks[i].strip(), blocks[i+1]) for i in range(0, len(blocks), 2)]

print(f"🔍 Found {len(sections)} major sections")

def slug(s): 
    return re.sub(r'[^a-z0-9\-]+', '-', s.lower()).strip('-')

content = {"math": {}, "physics": {}, "engineering": {}}   # scaffold

def add_page(subject, group, title, cards):
    key = slug(group or title)
    path = f"{subject}/{key}.html"
    
    # Handle special cases for better organization
    if "number theory" in title.lower():
        key = "number_theory"
    elif "plane geometry" in title.lower():
        key = "geometry_plane"  
    elif "solid geometry" in title.lower():
        key = "geometry_solid"
    elif "analytic geometry" in title.lower():
        key = "analytic_geometry"
    elif "differential geometry" in title.lower():
        key = "differential_geometry"
    elif "vector calculus" in title.lower():
        key = "vector_calculus"
    elif "linear algebra" in title.lower():
        key = "linear_algebra"
    elif "abstract algebra" in title.lower():
        key = "abstract_algebra"
    elif "set theory" in title.lower():
        key = "set_theory"
    elif "differential equations" in title.lower():
        key = "differential_equations"
    elif "euclidean" in title.lower():
        key = "geometry"
    elif "waves and oscillations" in title.lower():
        key = "waves_oscillations"
    elif "quantum mechanics" in title.lower():
        key = "quantum_mechanics"
    elif "fluid mechanics" in title.lower():
        key = "fluid_mechanics"
    elif "nuclear physics" in title.lower():
        key = "nuclear_physics"
    
    content.setdefault(subject, {})[key] = {
        "title": title,
        "path": path,
        "lead": f"Formulas and concepts in {title.lower()}",
        "cards": cards
    }

for sec_title, body in sections:
    print(f"🔧 Processing section: {sec_title}")
    
    # Decide subject bucket by keywords
    subject = "math"  # default
    if any(keyword in sec_title.lower() for keyword in [
        "mechanics", "thermodynamics", "electromagnetism", "electromagnetic", 
        "optics", "waves", "quantum", "relativity", "fluid", "nuclear", "physics"
    ]):
        subject = "physics"
    elif any(keyword in sec_title.lower() for keyword in ["engineering"]):
        subject = "engineering"
    
    cards = []
    
    # Split the body into individual formula blocks
    # Look for \textbf{...}: followed by formula and description
    formula_blocks = re.split(r'(?=\\textbf\{[^}]+\}:)', body)[1:]  # Skip first empty element
    
    for block in formula_blocks:
        if not block.strip():
            continue
            
        # Extract formula name
        name_match = re.search(r'\\textbf\{([^}]+)\}:', block)
        if not name_match:
            continue
            
        name = name_match.group(1).strip()
        
        # Extract LaTeX formula - the key fix is accounting for the period after the formula
        latex = ""
        
        # Pattern 1: Inline math $...$ followed by period
        inline_match = re.search(r'\\textbf\{[^}]+\}:\s*\$([^$]+)\$\.', block)
        if inline_match:
            latex = inline_match.group(1).strip()
        
        # Pattern 2: Multiple formulas separated by semicolons  
        if not latex:
            multi_match = re.search(r'\\textbf\{[^}]+\}:\s*([^.]+?)\.', block)
            if multi_match:
                potential = multi_match.group(1).strip()
                # Check if it contains math
                if '$' in potential or '\\' in potential:
                    latex = potential
        
        # Pattern 3: Display math patterns
        if not latex:
            display_patterns = [
                r'\\textbf\{[^}]+\}:\s*\$\$([^$]+)\$\$',
                r'\\textbf\{[^}]+\}:\s*\\\[([^\]]+)\\\]',
                r'\\textbf\{[^}]+\}:\s*\\displaystyle\s*([^.]+?)\.'
            ]
            
            for pattern in display_patterns:
                match = re.search(pattern, block, re.DOTALL)
                if match:
                    latex = match.group(1).strip()
                    break
        
        if not latex:
            print(f"   ⚠️  Could not extract formula for: {name}")
            continue
        
        # Clean up the LaTeX
        latex = re.sub(r'\s+', ' ', latex)  # Normalize whitespace
        latex = latex.replace('\\displaystyle', '').strip()
        # Remove any trailing punctuation
        latex = latex.rstrip('.,;')
        
        # Extract Variables
        variables = []
        var_match = re.search(r'\\textit\{Variables:\}([^\\]+?)(?=\\textit|\\textbf|$)', block, re.DOTALL)
        if var_match:
            var_text = var_match.group(1).strip()
            # Clean up and split variables - look for sentence-like descriptions
            var_sentences = re.split(r'[.;]\s*(?=[A-Z$\\])', var_text)
            for sentence in var_sentences:
                if sentence.strip():
                    # Extract variable name and description
                    sentence = sentence.strip()
                    # Remove dollar signs for readability
                    sentence = re.sub(r'\$([^$]*)\$', r'\1', sentence)
                    variables.append(sentence)
        
        # Extract Description
        description = ""
        desc_match = re.search(r'\\textit\{Description:\}([^\\]+?)(?=\\textit|\\textbf|$)', block, re.DOTALL)
        if desc_match:
            description = desc_match.group(1).strip()
            # Clean up LaTeX formatting
            description = re.sub(r'\$([^$]+)\$', r'\\(\1\\)', description)  # Convert $ to \( \)
            description = re.sub(r'\\textit\{([^}]+)\}', r'_\1_', description)  # Convert \textit to markdown
            description = re.sub(r'\s+', ' ', description)  # Normalize whitespace
            description = description.rstrip('.')  # Remove trailing period
        
        # Extract Visual if present
        visual = "Mathematical concept visualization"
        visual_match = re.search(r'\\textit\{Visual:\}([^\\]+?)(?=\\textit|\\textbf|$)', block, re.DOTALL)
        if visual_match:
            visual = visual_match.group(1).strip()
            visual = re.sub(r'\s+', ' ', visual)
            visual = visual.rstrip('.')
        
        card = {
            "name": name,
            "tex": latex,
            "vars": variables,
            "desc": description,
            "visual": visual
        }
        
        cards.append(card)
        print(f"   ✅ {name}: {latex[:50]}{'...' if len(latex) > 50 else ''}")
            
    print(f"   📝 Extracted {len(cards)} formulas")
    
    if cards:  # Only add sections that have content
        add_page(subject, None, sec_title, cards)

# Add index pages for each subject
subjects_info = {
    "math": {
        "title": "Mathematics",
        "lead": "Comprehensive mathematics reference covering arithmetic, algebra, geometry, calculus, and advanced topics."
    },
    "physics": {
        "title": "Physics", 
        "lead": "Complete physics reference covering mechanics, thermodynamics, electromagnetism, and modern physics."
    },
    "engineering": {
        "title": "Engineering",
        "lead": "Engineering formulas and principles across multiple disciplines."
    }
}

for subject, info in subjects_info.items():
    if subject in content and content[subject]:
        # Create index page with highlights from various sections
        index_cards = []
        
        # Pick representative formulas from different sections
        for section_key, section_data in content[subject].items():
            if section_data.get('cards') and len(section_data['cards']) > 0:
                # Take first formula from each section as a highlight
                card = section_data['cards'][0].copy()
                index_cards.append(card)
                if len(index_cards) >= 8:  # Limit to 8 highlights
                    break
        
        content[subject]["index"] = {
            "title": info["title"],
            "path": f"{subject}/index.html", 
            "lead": info["lead"],
            "cards": index_cards
        }

print(f"\n🎯 Generated content structure:")
for subject, sections in content.items():
    if sections:
        print(f"  📂 {subject.upper()}: {len(sections)} sections")
        for key, section in sections.items():
            print(f"     📄 {key}: {len(section.get('cards', []))} formulas")

print(f"\n💾 Writing to {OUT}...")
OUT.write_text(json.dumps(content, indent=2, ensure_ascii=False), encoding='utf-8')

total_pages = sum(len(sections) for sections in content.values())
total_formulas = sum(len(section.get('cards', [])) for sections in content.values() for section in sections.values())

print(f"✅ SUCCESS!")
print(f"📊 Generated {total_pages} pages with {total_formulas} formulas")
print(f"🚀 Ready to run: python build.py") 