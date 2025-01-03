import requests

url = "https://kirisamevanilla.github.io/ffxiv/dalamudrepo.json"
def fetch_json_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        return None

def generate_markdown_table(data):
    if not data:
        return "无数据可生成表格。"
    
    header = "| 插件名                     | API | 版本      | 作者  |\n|----------------------------|-----|-----------|-------|"
    rows = []
    rows.append("# KirisameVanilla's Dalamud Repo")
    rows.append("## Plugins")
    rows.append(header)
    for item in data:
        rows.append(
            f"| [{item['Name']}]({item['RepoUrl']}) | {item['DalamudApiLevel']}  | {item['AssemblyVersion']}   | {item['Author']} |"
        )
    rows.append("## Repo Url")
    rows.append(f"```\n{url}\n```")
    return "\n".join(rows)

def write_to_md_file(file_name, content):
    try:
        with open(file_name, "w", encoding="utf-8") as file:
            file.write(content)
        print(f"Markdown 表格已成功写入文件: {file_name}")
    except IOError as e:
        print(f"写入文件失败: {e}")

json_data = fetch_json_from_url(url)
markdown_table = generate_markdown_table(json_data)

print(markdown_table)
output_file = "README.md"
write_to_md_file(output_file, markdown_table)