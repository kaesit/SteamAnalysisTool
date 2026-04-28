import sys
try:
    import pypdf
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pypdf"])
    import pypdf

reader = pypdf.PdfReader("GameOracle.pdf")
text = ""
for page in reader.pages:
    text += page.extract_text() + "\n"

with open("GameOracle_extracted.txt", "w", encoding="utf-8") as f:
    f.write(text)

print("Extraction complete")
