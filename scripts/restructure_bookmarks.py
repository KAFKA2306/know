import os
import re
import shutil
from bs4 import BeautifulSoup

BOOKMARKS_FILE = 'temporaries/bookmarks_2026_01_11.html'
OUTPUT_DIR = 'docs/bookmarks'

CATEGORIES = {
    'AI': ['chatgpt', 'gemini', 'openai', 'anthropic', 'claude', 'perplexity', 'huggingface', 'stable diffusion', 'midjourney', 'notebooklm', 'vertex', 'aistudio', 'gradio', 'waifu diffusion', 'rvc', 'voice changer'],
    'Dev': ['github', 'stackoverflow', 'qiita', 'zenn', 'kaggle', 'colab', 'python', 'api', 'aws', 'google cloud', 'vscode', 'docker', 'hackmd', 'codex', 'gitlab', 'jira', 'confluence', 'azure', 'scikit', 'pandas', 'numpy', 'matplotlib', 'cursor', 'streamlit', 'rust', 'linux', 'ubuntu', 'wsl'],
    'Finance': ['investing', 'yahoo finance', 'koyfin', 'marketbeat', 'trading', 'rakuten-sec', 'sbi', 'nomura', 'crypto', 'portfoliovisualizer', 'stockrow', 'macrotrends', 'keisan.nta', 'morningstar', 'jpx', 'slickcharts', 'monex', 'sonybank', 'smbc', 'aplus', 'wise', 'ark-funds', 'buffett-code', 'stooq', 'bitcoin', 'fp', 'tax'],
    'Game': ['vrchat', 'booth', 'unity', 'blender', 'steam', 'poker', 'game', 'hearthstone', 'shadowverse', 'battlefy', 'hsreplay', 'dota', 'auto chess', 'yucata', 'dominion', 'nintendo', 'playstation', 'xbox', 'minecraft', 'apex', 'valorant'],
    'Media': ['youtube', 'netflix', 'prime video', 'spotify', 'music', 'stand.fm', 'suno', 'nico', 'twitch', 'pixiv', 'fanbox', 'fantia'],
    'Life': ['amazon', 'rakuten', 'google map', 'calendar', 'mail', 'note', 'twitter', 'x.com', 'google', 'gmail', 'weather', 'tenki', 'recipe', 'cookpad', 'tabelog', 'hotpepper', 'drive'],
    'Academic': ['ynu.ac.jp', 'kaken', 'sciencedirect', 'coursera', 'udemy', 'archive.org', 'ci.nii.ac.jp', 'jstage', 'researchgate', 'arxiv', 'scholar'],
}

IGNORE_KEYWORDS = ['porn', 'xvideos', 'fanza', 'hentai', 'sex', 'erotic', 'adult', '18+', 'r-18', 'jav', 'milf', 'fuck', 'dick', 'pussy', 'masturbat', 'upskirt', 'cam']

def clean_text(text):
    return text.strip() if text else ""

def get_category(title, url):
    title_lower = title.lower()
    url_lower = url.lower()
    
    # Check ignore list first
    for kw in IGNORE_KEYWORDS:
        if kw in title_lower or kw in url_lower:
            return 'Ignore'

    for cat, keywords in CATEGORIES.items():
        for kw in keywords:
            if kw in title_lower or kw in url_lower:
                return cat
    return 'Other'

def main():
    if not os.path.exists(BOOKMARKS_FILE):
        print(f"Error: {BOOKMARKS_FILE} not found")
        return

    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR)

    with open(BOOKMARKS_FILE, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    links_by_cat = {cat: [] for cat in CATEGORIES}
    links_by_cat['Other'] = []
    
    seen_urls = set()

    for a in soup.find_all('a'):
        title = clean_text(a.get_text())
        href = a.get('href')
        
        if not title or not href:
            continue
            
        if href.startswith('javascript:') or href.startswith('file:') or href.startswith('chrome:'):
            continue

        if href in seen_urls:
            continue
        seen_urls.add(href)

        cat = get_category(title, href)
        if cat == 'Ignore':
            continue
            
        links_by_cat[cat].append(f"- [{title}]({href})")

    main_index_content = ["# Bookmarks\n"]
    
    # Strictly select: Only add defined categories to index (Skip Other)
    for cat in sorted(CATEGORIES.keys()):
        links = links_by_cat[cat]
        if not links:
            continue
            
        cat_dir = os.path.join(OUTPUT_DIR, cat)
        os.makedirs(cat_dir, exist_ok=True)
        
        with open(os.path.join(cat_dir, 'index.md'), 'w', encoding='utf-8') as f:
            f.write(f"# {cat}\n\n")
            f.write("\n".join(links))
        
        main_index_content.append(f"- [{cat}]({cat}/index.md)")
        print(f"Category {cat}: {len(links)} items")

    # Handle Other: Write it but don't add to main index (Archived)
    if links_by_cat['Other']:
        other_dir = os.path.join(OUTPUT_DIR, 'Other')
        os.makedirs(other_dir, exist_ok=True)
        with open(os.path.join(other_dir, 'index.md'), 'w', encoding='utf-8') as f:
            f.write("# Other (Uncategorized)\n\n")
            f.write("\n".join(links_by_cat['Other']))
        print(f"Category Other: {len(links_by_cat['Other'])} items (Excluded from main index)")

    with open(os.path.join(OUTPUT_DIR, 'index.md'), 'w', encoding='utf-8') as f:
        f.write("# Strictly Selected Bookmarks\n\n")
        f.write("\n".join(main_index_content))

if __name__ == "__main__":
    main()
