import json
from pathlib import Path

README_PATH = Path("README.md")
INDEX_PATH = Path("daily_dev_news/news/index.json")

START = "<!-- DEV-NEWS-LIST:START -->"
END = "<!-- DEV-NEWS-LIST:END -->"

PROFILE_NEWS_REPO = "https://github.com/kong33/daily_dev_news/blob/main"

def build_news_list(items, limit=5):
    lines = []
    for item in items[:limit]:
        date = item["date"]
        title = item["title"]
        path = item["path"]
        url = f"{PROFILE_NEWS_REPO}/{path}"
        lines.append(f"- **{date}** — [{title}]({url})")
    return "\n".join(lines)

def main():
    readme = README_PATH.read_text(encoding="utf-8")
    items = json.loads(INDEX_PATH.read_text(encoding="utf-8"))

    items.sort(key=lambda x: x["date"], reverse=True)

    new_block = build_news_list(items)
    replacement = f"{START}\n{new_block}\n{END}"

    if START not in readme or END not in readme:
        raise ValueError("README.md에 DEV-NEWS-LIST 마커가 없습니다.")

    before = readme.split(START)[0]
    after = readme.split(END)[1]
    updated = before + replacement + after

    README_PATH.write_text(updated, encoding="utf-8")

if __name__ == "__main__":
    main()
