import re
import sys
from pathlib import Path
from typing import List, NamedTuple, Optional
import requests
from urllib.parse import urlparse
TITLE_REMOVALS = [
    r"\s*-\s*YouTube$",
    r"\s*\|\s*Qiita$",
    r"\s*-\s*Wikipedia$",
    r"\s*\|\s*Note$",
    r"\s*\|\s*Zenn$",
    r"\s*\|\s*Medium$",
    r"\s*\|\s*Togetter$",
    r"\s*\|\s*Speaker Deck$",
    r"\s*\|\s*SlideShare$",
    r"\s*\|\s*DocBase$",
    r"\s*\|\s*Scrapbox$",
    r"\s*\|\s*Notion$",
    r"\s*\|\s*Connpass$",
    r"\s*\|\s*TechPlay$",
    r"\s*\|\s*Doorkeeper$",
    r"\s*\|\s*ATND$",
    r"\s*\|\s*Peatix$",
    r"\s*\|\s*Amazon\.co\.jp$",
    r"\s*:\s*Amazon\.co\.jp$",
    r"\s*\|\s*楽天市場$",
    r"\s*\|\s*Yahoo!ショッピング$",
    r"\s*\|\s*ヨドバシ\.com$",
    r"\s*\|\s*ビックカメラ\.com$",
    r"\s*\|\s*価格\.com$",
    r"\s*\|\s*食べログ$",
    r"\s*\|\s*Retty$",
    r"\s*\|\s*ぐるなび$",
    r"\s*\|\s*ホットペッパーグルメ$",
    r"\s*\|\s*一休\.com$",
    r"\s*\|\s*じゃらんnet$",
    r"\s*\|\s*楽天トラベル$",
    r"\s*\|\s*Expedia$",
    r"\s*\|\s*Booking\.com$",
    r"\s*\|\s*Agoda$",
    r"\s*\|\s*TripAdvisor$",
    r"\s*\|\s*Airbnb$",
    r"\s*\|\s*Netflix$",
    r"\s*\|\s*Hulu$",
    r"\s*\|\s*Amazon Prime Video$",
    r"\s*\|\s*U-NEXT$",
    r"\s*\|\s*dTV$",
    r"\s*\|\s*DAZN$",
    r"\s*\|\s*Spotify$",
    r"\s*\|\s*Apple Music$",
    r"\s*\|\s*Amazon Music$",
    r"\s*\|\s*Google Play Music$",
    r"\s*\|\s*AWA$",
    r"\s*\|\s*LINE MUSIC$",
    r"\s*\|\s*SoundCloud$",
    r"\s*\|\s*Bandcamp$",
    r"\s*\|\s*Pixiv$",
    r"\s*\|\s*Twitter$",
    r"\s*\|\s*Facebook$",
    r"\s*\|\s*Instagram$",
    r"\s*\|\s*LinkedIn$",
    r"\s*\|\s*Pinterest$",
    r"\s*\|\s*Tumblr$",
    r"\s*\|\s*Reddit$",
    r"\s*\|\s*GitHub$",
    r"\s*\|\s*GitLab$",
    r"\s*\|\s*Bitbucket$",
    r"\s*\|\s*Stack Overflow$",
    r"\s*\|\s*Quora$",
    r"\s*\|\s*Teratail$",
    r"\s*\|\s*Mosh$",
    r"\s*\|\s*Zm",
    r"\s*\|\s*遊び方・3行解説", 
    r"_哔哩哔哩_bilibili",
    r"\s*-\s*TwiPla$",
    r"\s*-\s*ゲームウィキ\.jp$",
    r"\s*\|\s*ArclightGames Official$",
    r"\s*\|\s*BoardGameGeek$",
    r"\s*•\s*Board Game Arena$",
    r"\s*\|\s*Board Game\s*\|\s*Zatu Games UK$",
    r"\s*\|\s*Board Game\s*\|\s*Zatu Games$",
]
class Bookmark(NamedTuple):
    line_no: int
    original_line: str
    title: str
    url: str
    indent: str
    @property
    def markdown(self) -> str:
        return f"{self.indent}- [{self.title}]({self.url})"
def parse_line(line: str, line_no: int) -> Optional[Bookmark]:
    match = re.match(r"^(\s*)-\s*\[(.*?)\]\((.*?)\)\s*$", line)
    if match:
        return Bookmark(line_no, line, match.group(2), match.group(3), match.group(1))
    return None
def clean_title(title: str) -> str:
    cleaned = title
    for pattern in TITLE_REMOVALS:
        cleaned = re.sub(pattern, "", cleaned, flags=re.IGNORECASE)
    cleaned = cleaned.strip()
    return cleaned
def check_link(url: str, timeout: int = 5) -> bool:
    if not url.startswith(("http://", "https://")):
        return True
    try:
        response = requests.head(url, timeout=timeout, allow_redirects=True)
        return response.status_code < 400
    except requests.RequestException:
        return False
def process_file(file_path: Path, check_links: bool = False, dry_run: bool = False) -> None:
    print(f"Processing: {file_path}")
    content = file_path.read_text(encoding="utf-8")
    lines = content.splitlines()
    new_lines = []
    modified = False
    for i, line in enumerate(lines):
        bookmark = parse_line(line, i)
        if bookmark:
            new_title = clean_title(bookmark.title)
            if new_title != bookmark.title:
                print(f"  Refined: '{bookmark.title}' -> '{new_title}'")
                modified = True
            if check_links:
                if not check_link(bookmark.url):
                    print(f"  Dead Link Found: {bookmark.url}")
            new_lines.append(f"{bookmark.indent}- [{new_title}]({bookmark.url})")
        else:
            new_lines.append(line)
    if modified and not dry_run:
        file_path.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
        print("  Saved changes.")
def main():
    if len(sys.argv) < 2:
        print("Usage: python cleaner.py <directory> [--check-links] [--dry-run]")
        sys.exit(1)
    root_dir = Path(sys.argv[1])
    check_links = "--check-links" in sys.argv
    dry_run = "--dry-run" in sys.argv
    if not root_dir.exists():
        print(f"Directory not found: {root_dir}")
        sys.exit(1)
    for md_file in root_dir.glob("**/*.md"):
        process_file(md_file, check_links=check_links, dry_run=dry_run)
if __name__ == "__main__":
    main()
