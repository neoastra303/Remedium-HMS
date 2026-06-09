import re, pathlib

for path in [
    "patients/templates/patients/patient_list.html",
    "billing/templates/billing/invoice_list.html",
]:
    f = pathlib.Path(path)
    txt = f.read_text(encoding="utf-8")
    txt = re.sub(
        r"\{%\s*if is_paginated\s*%\}.*?\{%\s*endif\s*%\}",
        "{% include 'partials/pagination.html' %}",
        txt,
        flags=re.DOTALL,
    )
    f.write_text(txt, encoding="utf-8")
    print(f"Done: {path}")
