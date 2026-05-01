"""
Modernize remaining old-style templates:
1. Replace raw pagination loops with {% include 'partials/pagination.html' %}
2. Replace table-striped with table-hover + shadow-sm card wrapper
3. Replace confirm_delete pages with modern card style
"""
import pathlib, re

# Fix pagination in all list templates
list_templates = list(pathlib.Path('.').rglob('*_list.html'))
list_templates = [f for f in list_templates if 'venv' not in str(f)]

pagination_pattern = re.compile(
    r'\{%\s*if is_paginated\s*%\}.*?\{%\s*endif\s*%\}',
    re.DOTALL
)
pagination_replacement = "{% include 'partials/pagination.html' %}"

for f in list_templates:
    txt = f.read_text(encoding='utf-8')
    new = pagination_pattern.sub(pagination_replacement, txt)
    # Also upgrade table styling
    new = new.replace('class="table table-striped table-hover"', 'class="table table-hover align-middle mb-0"')
    new = new.replace('class="table table-bordered table-striped"', 'class="table table-hover align-middle mb-0"')
    if new != txt:
        f.write_text(new, encoding='utf-8')
        print(f'Fixed: {f}')

# Fix confirm_delete templates - replace alert+button pattern with card
confirm_templates = list(pathlib.Path('.').rglob('*_confirm_delete.html'))
confirm_templates = [f for f in confirm_templates if 'venv' not in str(f)]

for f in confirm_templates:
    txt = f.read_text(encoding='utf-8')
    # Only fix if it's the old alert-warning style (not already modernized)
    if 'alert-warning' in txt or ('<h1' in txt and 'fw-bold' not in txt):
        # Extract the cancel URL
        cancel_match = re.search(r"url '([^']+)'", txt)
        cancel_url = cancel_match.group(1) if cancel_match else '#'
        # Extract object description
        obj_match = re.search(r'<strong>([^<]+)</strong>', txt)
        obj_desc = obj_match.group(1) if obj_match else 'this item'
        
        new_content = f"""{{% extends 'base.html' %}}
{{% block content %}}
<div class="row justify-content-center"><div class="col-md-6">
    <div class="card border-0 shadow-sm">
        <div class="card-body p-4 text-center">
            <i class="bi bi-exclamation-triangle display-4 text-danger mb-3"></i>
            <h5 class="fw-bold">Confirm Deletion</h5>
            <p class="text-muted">Are you sure you want to delete <strong>{{{{ object }}}}</strong>? This cannot be undone.</p>
            <form method="post">{{% csrf_token %}}
                <button type="submit" class="btn btn-danger me-2"><i class="bi bi-trash me-1"></i>Delete</button>
                <a href="{{% url '{cancel_url}' %}}" class="btn btn-outline-secondary">Cancel</a>
            </form>
        </div>
    </div>
</div></div>
{{% endblock %}}
"""
        f.write_text(new_content, encoding='utf-8')
        print(f'Fixed confirm_delete: {f}')
