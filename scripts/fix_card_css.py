import pathlib, re

f = pathlib.Path("static/css/custom.css")
txt = f.read_text(encoding="utf-8")

old = """/* Cards */
.card {
    background: var(--glass-bg);
    backdrop-filter: blur(12px);
    border: 1px solid var(--glass-border);
    border-radius: 20px;
    overflow: hidden;
    transition: transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1), box-shadow 0.3s ease;
}

.card:hover {
    transform: translateY(-5px);
    box-shadow: 0 20px 40px rgba(0,0,0,0.08);
}"""

new = """/* Cards — solid white for data, glass only where explicitly applied */
.card {
    background: #fff;
    border: 1px solid rgba(0,0,0,0.06);
    border-radius: 16px;
    overflow: hidden;
}

/* Glass effect only on dashboard stat cards */
.card.glass-effect {
    background: var(--glass-bg);
    backdrop-filter: blur(12px);
    border: 1px solid var(--glass-border);
}

/* Hover animation scoped to action cards only */
.card-action {
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    cursor: pointer;
}
.card-action:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 28px rgba(0,0,0,0.10) !important;
}"""

if old in txt:
    f.write_text(txt.replace(old, new), encoding="utf-8")
    print("Done")
else:
    print("Pattern not found, trying line-by-line")
    lines = txt.split("\n")
    for i, l in enumerate(lines[64:78], 65):
        print(f"{i}: {repr(l)}")
