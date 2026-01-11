import os
import re
import subprocess

DOCS_DIR = 'docs/bookmarks'
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'

def check(url):
    args = ['curl', '-s', '-o', '/dev/null', '-w', '%{http_code}', '-A', UA, '--max-time', '3', url]
    res = subprocess.run(args, capture_output=True, text=True)
    code = res.stdout.strip()
    return code.startswith('2') or code.startswith('3')

def process(path):
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    out = []
    for line in lines:
        m = re.search(r'- \[.*?\]\((http.*?)\)', line)
        if not m or check(m.group(1)):
            out.append(line)
        else:
            print(f"Removed: {m.group(1)}")

    with open(path, 'w', encoding='utf-8') as f:
        f.writelines(out)

def main():
    for r, _, fs in os.walk(DOCS_DIR):
        for f in fs:
            if 'Other' not in r:
                process(os.path.join(r, f))

if __name__ == "__main__":
    main()
