import os
import re
import shutil
from bs4 import BeautifulSoup

BOOKMARKS_FILE = 'temporaries/bookmarks_2026_01_11.html'
OUTPUT_DIR = 'docs/bookmarks'

def clean_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "", name).strip()

def process_folder(folder_node, current_path):
    os.makedirs(current_path, exist_ok=True)
    index_content = []
    
    container = folder_node
    p = folder_node.find('p', recursive=False)
    if p:
        container = p

    for dt in container.find_all('dt', recursive=False):
        h3 = dt.find('h3')
        if h3:
            folder_name = clean_filename(h3.get_text())
            new_path = os.path.join(current_path, folder_name)
            
            dl = dt.find('dl')
            if not dl:
                nxt = dt.next_sibling
                while nxt:
                    if nxt.name == 'dl':
                        dl = nxt
                        break
                    if nxt.name == 'dt':
                        break
                    nxt = nxt.next_sibling
            
            if dl:
                 process_folder(dl, new_path)
                 index_content.append(f"- [{folder_name}]({folder_name}/index.md)")
            continue

        a = dt.find('a')
        if a:
            title = a.get_text()
            href = a.get('href')
            index_content.append(f"- [{title}]({href})")

    with open(os.path.join(current_path, 'index.md'), 'w', encoding='utf-8') as f:
        title = os.path.basename(current_path)
        if title == 'bookmarks':
            title = 'Bookmarks'
        f.write(f"# {title}\n\n")
        f.write("\n".join(index_content))

def main():
    if not os.path.exists(BOOKMARKS_FILE):
        return

    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)

    with open(BOOKMARKS_FILE, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    main_dl = soup.find('dl')
    if main_dl:
        process_folder(main_dl, OUTPUT_DIR)

if __name__ == "__main__":
    main()
