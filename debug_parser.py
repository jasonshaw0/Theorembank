#!/usr/bin/env python3
import re

tex = open('formula_library.tex', encoding='utf-8').read()
print(f"Total file size: {len(tex)} chars")

# Test subsection splitting
blocks = re.split(r'\\subsection\*\{([^}]+)\}', tex)[1:]
sections = [(blocks[i].strip(), blocks[i+1]) for i in range(0, len(blocks), 2)]

print(f"Found {len(sections)} sections")

# Look at first few sections
for i, (title, body) in enumerate(sections[:3]):
    print(f"\n=== SECTION {i+1}: {title} ===")
    print(f"Body length: {len(body)} chars")
    print("First 300 chars of body:")
    print(repr(body[:300]))
    
    # Test formula pattern
    formula_blocks = re.split(r'(?=\\textbf\{[^}]+\}:)', body)[1:]
    print(f"Found {len(formula_blocks)} formula blocks")
    
    if formula_blocks:
        print("First formula block:")
        print(repr(formula_blocks[0][:200]))
        
        # Test name extraction
        name_match = re.search(r'\\textbf\{([^}]+)\}:', formula_blocks[0])
        if name_match:
            print(f"Formula name: {name_match.group(1)}")
        
        # Test formula extraction
        inline_match = re.search(r'\\textbf\{[^}]+\}:\s*\$([^$]+)\$', formula_blocks[0])
        if inline_match:
            print(f"Formula: {inline_match.group(1)}")
        else:
            print("No inline formula found") 