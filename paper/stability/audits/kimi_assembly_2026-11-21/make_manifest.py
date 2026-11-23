"""Write SHA256SUMS for the assembly audit delivery."""
import hashlib
import os

root = os.path.dirname(os.path.abspath(__file__))
rows = []
for base, dirs, files in os.walk(root):
    dirs[:] = sorted(d for d in dirs if d != "__pycache__")
    for name in sorted(files):
        if name == "SHA256SUMS" or name.endswith((".pyc", ".pyo")):
            continue
        path = os.path.join(base, name)
        rel = os.path.relpath(path, root)
        h = hashlib.sha256()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(1024 * 1024), b""):
                h.update(chunk)
        rows.append((rel, h.hexdigest()))
with open(os.path.join(root, "SHA256SUMS"), "w") as f:
    for rel, digest in sorted(rows):
        f.write(f"{digest}  {rel}\n")
print(len(rows), "files hashed")
