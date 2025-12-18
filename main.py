import json
from parsers.registry import get_parser

html_file_path = "Test 2/Dombing.html"

with open(html_file_path, "r", encoding="utf-8") as f:
    html = f.read()

platform = "bing_search"  

parser = get_parser(platform)
data = parser(html)

print(json.dumps(data, indent=4, ensure_ascii=False))