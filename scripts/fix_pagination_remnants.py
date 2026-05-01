"""Fix broken pagination remnants left by previous modernize script."""
import pathlib, re

# The previous script replaced the {% if is_paginated %} block but left the
# old raw pagination HTML after the include tag in some templates.
# Pattern: {% include 'partials/pagination.html' %} followed by leftover nav HTML

broken_pattern = re.compile(
    r"\{%\s*include 'partials/pagination\.html'\s*%\}.*?(?=\{%\s*else\s*%\}|\{%\s*endif\s*%\}|$)",
    re.DOTALL
)

list_templates = list(pathlib.Path('.').rglob('*_list.html'))
list_templates = [f for f in list_templates if 'venv' not in str(f)]

for f in list_templates:
    txt = f.read_text(encoding='utf-8')
    if "{% include 'partials/pagination.html' %}" in txt and '<nav aria-label' in txt:
        # Replace everything between the include and the next {% else %} or {% endif %}
        new = re.sub(
            r"(\{%\s*include 'partials/pagination\.html'\s*%\}).*?(\{%\s*(?:else|endif)\s*%\})",
            r'\1\n\n\2',
            txt, flags=re.DOTALL
        )
        if new != txt:
            f.write_text(new, encoding='utf-8')
            print(f'Fixed: {f}')
