import pathlib
f = pathlib.Path('static/css/custom.css')
txt = f.read_text(encoding='utf-8')
old = """.card-header {
    background: rgba(255, 255, 255, 0.4);
    border-bottom: 1px solid var(--glass-border);
    font-weight: 600;
    color: var(--primary-blue);
}"""
new = """.card-header {
    background: #fff;
    border-bottom: 1px solid rgba(0,0,0,0.06);
    font-weight: 600;
}"""
if old in txt:
    f.write_text(txt.replace(old, new), encoding='utf-8')
    print('Done')
else:
    print('Not found')
