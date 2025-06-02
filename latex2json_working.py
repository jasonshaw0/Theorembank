#!/usr/bin/env python3
# Working LaTeX to JSON converter
import re, json, pathlib

tex = pathlib.Path("formula_library.tex").read_text(encoding="utf-8")
print(f"📖 Loaded {len(tex)} characters from formula_library.tex")

# Extract all sections
sections = {}
subsection_pattern = r'\\subsection\*\{([^}]+)\}'
section_matches = list(re.finditer(subsection_pattern, tex))

for i, match in enumerate(section_matches):
    section_title = match.group(1)
    start_pos = match.end()
    end_pos = section_matches[i+1].start() if i+1 < len(section_matches) else len(tex)
    section_content = tex[start_pos:end_pos].strip()
    sections[section_title] = section_content

print(f"🔍 Found {len(sections)} sections")

# Fixed formula extraction pattern - colon is inside the textbf block
formula_pattern = r'\\textbf\{([^}]+):\}\s*\$([^$]+)\$\.'

content = {"math": {}, "physics": {}, "engineering": {}}

def slug(s):
    return re.sub(r'[^a-z0-9\-]+', '-', s.lower()).strip('-')

def classify_subject(title):
    physics_keywords = ["mechanics", "thermodynamics", "electromagnetism", "optics", 
                       "waves", "quantum", "relativity", "fluid", "nuclear", "physics"]
    return "physics" if any(kw in title.lower() for kw in physics_keywords) else "math"

for section_title, section_body in sections.items():
    print(f"\n🔧 Processing: {section_title}")
    
    # Extract all formulas from this section
    formula_matches = re.findall(formula_pattern, section_body)
    print(f"   Found {len(formula_matches)} formulas")
    
    if not formula_matches:
        continue
    
    cards = []
    for name, formula in formula_matches:
        # Find the full context for this formula
        formula_context_pattern = rf'\\textbf\{{{re.escape(name)}:\}}.*?(?=\\textbf|$)'
        context_match = re.search(formula_context_pattern, section_body, re.DOTALL)
        
        if context_match:
            context = context_match.group(0)
            
            # Extract variables
            var_match = re.search(r'\\textit\{Variables:\}([^\\]+?)(?=\\textit|\\textbf|$)', context, re.DOTALL)
            variables = []
            if var_match:
                var_text = var_match.group(1).strip()
                # Clean up variables description
                var_text = re.sub(r'\$([^$]*)\$', r'\1', var_text)  # Remove $ signs
                variables = [var_text.strip()]
            
            # Extract description
            desc_match = re.search(r'\\textit\{Description:\}([^\\]+?)(?=\\textit|\\textbf|$)', context, re.DOTALL)
            description = ""
            if desc_match:
                description = desc_match.group(1).strip()
                # Convert LaTeX math to display format
                description = re.sub(r'\$([^$]+)\$', r'\\(\1\\)', description)
                description = re.sub(r'\s+', ' ', description)
        else:
            variables = []
            description = ""
        
        card = {
            "name": name.strip(),
            "tex": formula.strip(),
            "vars": variables,
            "desc": description,
            "visual": "Mathematical concept visualization"
        }
        cards.append(card)
        print(f"   ✅ {name}")
    
    # Add to content structure
    subject = classify_subject(section_title)
    key = slug(section_title)
    
    # Handle special cases
    if "euclidean" in section_title.lower():
        key = "geometry"
    elif "number theory" in section_title.lower():
        key = "number_theory"
    elif "analytic geometry" in section_title.lower():
        key = "analytic_geometry"
    elif "differential geometry" in section_title.lower():
        key = "differential_geometry"
    elif "vector calculus" in section_title.lower():
        key = "vector_calculus"
    elif "linear algebra" in section_title.lower():
        key = "linear_algebra"
    elif "abstract algebra" in section_title.lower():
        key = "abstract_algebra"
    elif "set theory" in section_title.lower():
        key = "set_theory"
    elif "differential equations" in section_title.lower():
        key = "differential_equations"
    
    content[subject][key] = {
        "title": section_title,
        "path": f"{subject}/{key}.html",
        "lead": f"Essential formulas and concepts in {section_title.lower()}",
        "cards": cards
    }

# Add index pages
for subject in ["math", "physics"]:
    if content[subject]:
        # Create overview with sample formulas
        sample_cards = []
        for section_data in content[subject].values():
            if section_data.get('cards'):
                sample_cards.append(section_data['cards'][0])
                if len(sample_cards) >= 6:
                    break
        
        content[subject]["index"] = {
            "title": "Mathematics" if subject == "math" else "Physics",
            "path": f"{subject}/index.html",
            "lead": f"Comprehensive {subject} reference with formulas and explanations",
            "cards": sample_cards
        }

# Write output
output_file = pathlib.Path("content/formulas.json")
output_file.write_text(json.dumps(content, indent=2, ensure_ascii=False), encoding='utf-8')

total_sections = sum(len(sections) for sections in content.values())
total_formulas = sum(len(section.get('cards', [])) for sections in content.values() for section in sections.values())

print(f"\n✅ SUCCESS!")
print(f"📊 Generated {total_sections} pages with {total_formulas} formulas")
print(f"💾 Saved to {output_file}")
print(f"🚀 Run: python build.py") 