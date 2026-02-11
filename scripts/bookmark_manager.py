import os
import re
import sys
import urllib.request
import urllib.error
import socket
import concurrent.futures
from urllib.parse import urlparse
DOCS_DIR = 'docs/bookmarks'
LOG_DIR = 'docs/bookmarks/Log'
CATEGORY_STRUCTURE = {
    'Dev': ['AI', 'Data', 'Tool'],
    'Finance': ['Bank', 'Market', 'Crypto'],
    'Service': ['Cloud', 'Social'],
    'Game': ['VR', 'Board', 'Digital'],
    'Media': ['Video', 'Music'],
    'Academic': ['Library', 'Research'],
    'Life': ['Shopping', 'Utility'],
    'Other': [],
}
CATEGORIES = list(CATEGORY_STRUCTURE.keys())
TEMPORARY_PATTERNS = [
    r'/search\?', r'/login', r'/signin', r'/checkout', r'/cart', r'/order',
    r'/notifications', r'/auth', r'session', r'token=', r'utm_',
    r'/watch\?v=', r'/status/', r'/entry/', r'/articles/', r'/article/',
    r'/post/', r'/blog/', r'/p/', r'/n/', r'/dp/', r'/items/',
    r'qiita.com', r'zenn.dev', r'note.com', r'hatenablog', r'medium.com',
    r'dev.to', r'teratail.com', r'stackoverflow.com/questions/',
    r'reddit.com/r/', r'twitter.com/.*?/status', r'x.com/.*?/status',
    r'/wiki/', r'docs\.', r'/docs/', r'/tutorial', r'/guide/', r'/how-to',
    r'blogspot', r'fc2.com', r'ameblo.jp', r'livedoor.jp',
]
TEMPORARY_TITLE_PATTERNS = [
    r'使い方', r'方法', r'やり方', r'入門', r'初心者', r'tutorial',
    r'チュートリアル', r'とは$', r'guide', r'ガイド', r'備忘録', r'メモ',
    r'まとめ', r'解説', r'紹介', r'おすすめ', r'比較', r'vs', r'対策',
    r'エラー', r'ERROR', r'対処', r'how to', r'howto', r'difference',
    r'comparison', r'introduction', r'getting started', r'始め方',
    r'インストール', r'セットアップ', r'install', r'setup', r'ランキング',
]
PERSONAL_PATTERNS = [
    r'outlook\.office', r'mail\.google\.com', r'gmail\.com',
    r'accounts\.google\.com', r'/my/', r'/mypage', r'/dashboard',
    r'/settings', r'/profile', r'/account', r'@.*\.ac\.jp',
    r'1\.1\.1\.1', r'127\.0\.0\.1', r'192\.168\.', r'localhost',
]
PERSONAL_TITLE_PATTERNS = [
    r'マイページ', r'My Page', r'アカウント設定', r'ダッシュボード',
    r'Dashboard', r'Your Repositories', r'プロフィール', r'設定',
    r'Settings', r'から「.*」が発送', r'Outlook Web App',
    r'Network Authentication',
]
ERROR_PATTERNS = [
    r'存在しません', r'見つかりません', r'Not Found', r'404',
    r'Page Not Found', r'削除されました', r'Deleted', r'Error', r'エラー',
    r'Forbidden', r'Access Denied', r'Unauthorized', r'Service Unavailable',
    r'利用できません', r'suspended', r'凍結', r'503', r'502', r'500',
    r'Temporarily Unavailable', r'database connection', r'Bad Gateway',
    r'Gateway Timeout', r'Internal Server', r'maintenance', r'メンテナンス',
]
MAX_TITLE_LENGTH = 50
def get_domain(url):
    parsed = urlparse(url)
    domain = parsed.netloc.lower()
    return domain[4:] if domain.startswith('www.') else domain
def matches_any(text, patterns, flags=re.IGNORECASE):
    return any(re.search(p, text, flags) for p in patterns)
def filter_bookmarks(filter_func, log_name):
    removed_all = []
    for cat in CATEGORIES:
        path = os.path.join(DOCS_DIR, cat, 'index.md')
        if not os.path.exists(path):
            continue
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        kept, removed = [], []
        for line in lines:
            m = re.search(r'- \[(.*?)\]\((http.*?)\)', line)
            if m:
                title, url = m.group(1), m.group(2)
                if filter_func(title, url):
                    removed.append(f"- [{title[:40]}]({url})")
                else:
                    kept.append(line)
            else:
                kept.append(line)
        if removed:
            removed_all.extend([f"\n
            with open(path, 'w', encoding='utf-8') as f:
                f.writelines(kept)
            print(f"Removed {len(removed)} from {cat}")
    if removed_all:
        os.makedirs(LOG_DIR, exist_ok=True)
        with open(os.path.join(LOG_DIR, f'{log_name}.md'), 'a', encoding='utf-8') as f:
            f.write(f"\n
        print(f"Total: {len([x for x in removed_all if x.startswith('- ')])}")
def cmd_temporary():
    filter_bookmarks(
        lambda t, u: matches_any(u, TEMPORARY_PATTERNS) or matches_any(t, TEMPORARY_TITLE_PATTERNS),
        'temporary_filtered'
    )
def cmd_personal():
    filter_bookmarks(
        lambda t, u: matches_any(u, PERSONAL_PATTERNS) or matches_any(t, PERSONAL_TITLE_PATTERNS),
        'personal_filtered'
    )
def cmd_error():
    filter_bookmarks(lambda t, u: matches_any(t, ERROR_PATTERNS), 'error_filtered')
def cmd_long_titles():
    filter_bookmarks(lambda t, u: len(t) > MAX_TITLE_LENGTH, 'long_title_filtered')
def cmd_dedupe():
    seen = {}
    removed_all = []
    for cat in CATEGORIES:
        path = os.path.join(DOCS_DIR, cat, 'index.md')
        if not os.path.exists(path):
            continue
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        kept, removed = [], []
        for line in lines:
            m = re.search(r'- \[(.*?)\]\((http.*?)\)', line)
            if m:
                domain = get_domain(m.group(2))
                if domain in seen:
                    removed.append(f"- [{m.group(1)[:30]}] (dup: {seen[domain]})")
                else:
                    seen[domain] = cat
                    kept.append(line)
            else:
                kept.append(line)
        if removed:
            removed_all.extend([f"\n
            with open(path, 'w', encoding='utf-8') as f:
                f.writelines(kept)
            print(f"Dedupe {len(removed)} from {cat}")
    if removed_all:
        os.makedirs(LOG_DIR, exist_ok=True)
        with open(os.path.join(LOG_DIR, 'deduplicated.md'), 'a', encoding='utf-8') as f:
            f.write("\n
def cmd_dead_links():
    headers = {'User-Agent': 'Mozilla/5.0'}
    timeout = 5
    def check(url):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return True, r.getcode()
        except urllib.error.HTTPError as e:
            return e.code not in [404, 410, 400], e.code
        except (urllib.error.URLError, socket.timeout):
            return False, "Error"
        except Exception:
            return False, "Error"
    for cat in CATEGORIES:
        path = os.path.join(DOCS_DIR, cat, 'index.md')
        if not os.path.exists(path):
            continue
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        tasks = [(i, l, re.search(r'- \[(.*?)\]\((http.*?)\)', l)) for i, l in enumerate(lines)]
        urls = {m.group(2): [] for _, _, m in tasks if m}
        for i, l, m in tasks:
            if m:
                urls[m.group(2)].append(i)
        print(f"Checking {len(urls)} in {cat}...")
        results = {}
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as ex:
            future_map = {ex.submit(check, u): u for u in urls}
            for f in concurrent.futures.as_completed(future_map):
                results[future_map[f]] = f.result()
        dead_idx = set()
        for url, (alive, _) in results.items():
            if not alive:
                dead_idx.update(urls[url])
        if dead_idx:
            kept = [l for i, l in enumerate(lines) if i not in dead_idx]
            with open(path, 'w', encoding='utf-8') as f:
                f.writelines(kept)
            print(f"Removed {len(dead_idx)} dead from {cat}")
def cmd_export():
    header = """<!DOCTYPE NETSCAPE-Bookmark-file-1>
<!-- This is an automatically generated file.
     It will be read and overwritten.
     DO NOT EDIT! -->
<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">
<TITLE>Bookmarks</TITLE>
<H1>Bookmarks</H1>
<DL><p>
"""
    footer = "</DL><p>\n"
    def build_links(path):
        if not os.path.exists(path):
            return []
        with open(path, 'r', encoding='utf-8') as f:
            return re.findall(r'- \[(.*?)\]\((http.*?)\)', f.read())
    def format_links(links, indent):
        return "".join(f'{indent}<DT><A HREF="{u}">{t}</A>\n' for t, u in links)
    def build(cat):
        cat_path = os.path.join(DOCS_DIR, cat, 'index.md')
        subdirs = CATEGORY_STRUCTURE.get(cat, [])
        links = build_links(cat_path)
        lines = [f'    <DT><H3>{cat}</H3>\n', '    <DL><p>\n']
        lines.append(format_links(links, '        '))
        for sub in subdirs:
            sub_path = os.path.join(DOCS_DIR, cat, sub, 'index.md')
            sub_links = build_links(sub_path)
            if sub_links:
                lines.append(f'        <DT><H3>{sub}</H3>\n')
                lines.append('        <DL><p>\n')
                lines.append(format_links(sub_links, '            '))
                lines.append('        </DL><p>\n')
        lines.append('    </DL><p>\n')
        return "".join(lines)
    html = header + "".join(build(c) for c in CATEGORIES) + footer
    os.makedirs('temporaries', exist_ok=True)
    with open('temporaries/bookmarks.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Created temporaries/bookmarks.html")
def cmd_count():
    total = 0
    for cat in CATEGORIES:
        cat_path = os.path.join(DOCS_DIR, cat, 'index.md')
        cat_count = len(re.findall(r'^- \[', open(cat_path).read(), re.M)) if os.path.exists(cat_path) else 0
        subdirs = CATEGORY_STRUCTURE.get(cat, [])
        sub_counts = []
        for sub in subdirs:
            sub_path = os.path.join(DOCS_DIR, cat, sub, 'index.md')
            sub_count = len(re.findall(r'^- \[', open(sub_path).read(), re.M)) if os.path.exists(sub_path) else 0
            if sub_count > 0:
                sub_counts.append(f"{sub}:{sub_count}")
            cat_count += sub_count
        sub_str = f" ({', '.join(sub_counts)})" if sub_counts else ""
        print(f"{cat}: {cat_count}{sub_str}")
        total += cat_count
    print(f"TOTAL: {total}")
def main():
    cmds = {
        'temporary': cmd_temporary,
        'personal': cmd_personal,
        'error': cmd_error,
        'long': cmd_long_titles,
        'dedupe': cmd_dedupe,
        'dead': cmd_dead_links,
        'export': cmd_export,
        'count': cmd_count,
    }
    if len(sys.argv) < 2 or sys.argv[1] not in cmds:
        print(f"Usage: python bookmark_manager.py <{' | '.join(cmds.keys())}>")
        return
    cmds[sys.argv[1]]()
if __name__ == "__main__":
    main()
