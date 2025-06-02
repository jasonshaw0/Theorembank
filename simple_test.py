#!/usr/bin/env python3
import re

# Read just the arithmetic section to test
tex = open('formula_library.tex', encoding='utf-8').read()

# Find the arithmetic section
start = tex.find('\\subsection*{Arithmetic}')
end = tex.find('\\subsection*{Number Theory}')
arithmetic_section = tex[start:end] if end > start else tex[start:start+2000]

print("Arithmetic section (first 500 chars):")
print(repr(arithmetic_section[:500]))

# Test extracting first formula
first_formula = '''\\textbf{Sum of the first $n$ natural numbers:} $1 + 2 + \\cdots + n = \\frac{n(n+1)}{2}$.'''

print("\nTest formula:")
print(repr(first_formula))

# Test our pattern
pattern = r'\\textbf\{([^}]+)\}:\s*\$([^$]+)\$\.'
match = re.search(pattern, first_formula)
if match:
    print(f"✅ SUCCESS: Name='{match.group(1)}', Formula='{match.group(2)}'")
else:
    print("❌ Pattern failed")

# Test on actual content
print("\nTesting on actual section:")
matches = re.findall(pattern, arithmetic_section)
print(f"Found {len(matches)} matches:")
for i, (name, formula) in enumerate(matches):
    print(f"  {i+1}. {name}: {formula}") 