"""Remove app_name from all app urls.py files so names resolve without namespace."""

import pathlib, re

apps = [
    "appointments",
    "billing",
    "care_monitoring",
    "core",
    "hospital",
    "integration",
    "inventory",
    "laboratory",
    "medical_records",
    "notifications",
    "patients",
    "pharmacy",
    "reporting",
    "staff",
    "surgery",
]

for app in apps:
    f = pathlib.Path(f"{app}/urls.py")
    if not f.exists():
        continue
    txt = f.read_text(encoding="utf-8")
    new = re.sub(r"\napp_name\s*=\s*['\"][\w]+['\"]\n", "\n", txt)
    if new != txt:
        f.write_text(new, encoding="utf-8")
        print(f"Removed app_name from {app}/urls.py")
    else:
        print(f"No app_name in {app}/urls.py")
