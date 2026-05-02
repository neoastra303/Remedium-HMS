import pathlib

f = pathlib.Path('README.md')
txt = f.read_text(encoding='utf-8')

replacements = [
    ('Tests-93%20Passing', 'Tests-104%20Passing'),
    ('Tests-104%20Passing-brightgreen', 'Tests-104%20Passing-brightgreen'),  # already correct after first
    ('Coverage-75%25', 'Coverage-72%25'),
    ('pytest + pytest-cov (93 tests)', 'pytest + pytest-cov (104 tests)'),
    ('pytest + pytest-cov (104 tests)', 'pytest + pytest-cov (104 tests)'),  # idempotent
    ('**Tests** | 93', '**Tests** | 104'),
    ('**Coverage** | 75%', '**Coverage** | 72%'),
    ('93 passed, 0 failed, 75% coverage', '104 passed, 0 failed, 72% coverage'),
    ('**API Endpoints** | 40+', '**API Endpoints** | 50+'),
    ('**Templates** | 30+', '**Templates** | 78'),
]

for old, new in replacements:
    txt = txt.replace(old, new)

f.write_text(txt, encoding='utf-8')
print('Done')
