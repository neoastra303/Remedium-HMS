import pathlib, re

f = pathlib.Path("templates/index.html")
txt = f.read_text(encoding="utf-8")
# Remove the dead loop with split filter
txt = re.sub(r"\s*\{%\s*for url_name.*?split.*?endfor\s*%\}", "", txt, flags=re.DOTALL)
f.write_text(txt, encoding="utf-8")
print("Done")
