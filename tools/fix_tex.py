import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
tex_in = ROOT / "exports" / "tex" / "questions_5e_latex.tex"
tex_out = ROOT / "exports" / "tex" / "questions_5e_latex_fixed.tex"

def fix_frac(match):
    a = match.group(1)
    b = match.group(2)
    return r"\\frac{%s}{%s}" % (a, b)


def main():
    if not tex_in.exists():
        print(f"Input TeX not found: {tex_in}")
        return 1

    s = tex_in.read_text(encoding='utf-8')

    # Collapse occurrences of '$ $' (dollar, space, dollar) -> '$'
    s = s.replace('$ $', '$')

    # Replace any double-dollar display math with single-dollar (inline)
    s = s.replace('$$', '$')

    # Fix patterns like \frac\{3\}\{8\} -> \frac{3}{8}
    s = re.sub(r'\\frac\\\{([^}]*)\\\}\\\{([^}]*)\\\}', fix_frac, s)

    # Also fix cases where fractions were produced as \frac\{x\}\{y\} but without double escaping
    s = re.sub(r'\\frac\{([^}]*)\}\{([^}]*)\}', r'\\frac{\1}{\2}', s)

    # Replace literal '\{' and '\}' left in text with '{' and '}'
    s = s.replace('\\{', '{').replace('\\}', '}')

    # Remove spaces just inside math delimiters: convert '$ 8 $' -> '$8$'
    s = re.sub(r"\$(\s*)([^$]*?)(\s*)\$", lambda m: "$%s$" % m.group(2).strip(), s)

    # Collapse multiple consecutive dollars to a single one
    s = re.sub(r"\${2,}", "$", s)

    # Heuristic: remove $...$ wrappers when the inner content is plain words (like $Si$ or $Le$)
    def adjust_dollars(match):
        inner = match.group(1)
        inner_stripped = inner.strip()
        # If inner contains digits, backslash (LaTeX), braces, caret, underscore, slash or common math operators, keep dollars
        if re.search(r"[0-9\\\^_\{\}/+\-*=%()\[\]]", inner_stripped):
            return f"${inner_stripped}$"
        # If inner is a single letter (variable) keep dollars
        if len(inner_stripped) == 1 and re.match(r"[A-Za-zÀ-ÿ]", inner_stripped):
            return f"${inner_stripped}$"
        # Otherwise remove the dollar wrappers
        return inner_stripped

    s = re.sub(r"\$([^$]+)\$", adjust_dollars, s)

    tex_out.write_text(s, encoding='utf-8')
    print(f"Wrote fixed TeX to: {tex_out}")
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
