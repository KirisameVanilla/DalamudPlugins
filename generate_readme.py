import requests
from collections import defaultdict

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
    
    # 按 InternalName 分组
    plugin_groups = defaultdict(list)
    for item in data:
        plugin_groups[item['InternalName']].append(item)
    
    # 构建表格
    header = "| 插件名                     | API 10 | API 11 | 作者  |\n" + \
             "|----------------------------|--------|--------|-------|"
    rows = []
    rows.append("# KirisameVanilla's Dalamud Repo")
    rows.append("## Plugins")
    rows.append(header)

    for internal_name, plugins in plugin_groups.items():
        # 找到不带 (API XI) 的插件名
        primary_name_plugin = next(
            (plugin for plugin in plugins if "(API XI)" not in plugin['Name']),
            plugins[0]  # 如果没有则选第一个
        )
        name = f"[{primary_name_plugin['Name']}]({primary_name_plugin['RepoUrl']})"
        
        # 合并 API 支持信息
        api_10 = "✔" if any(plugin['DalamudApiLevel'] == 10 for plugin in plugins) else ""
        api_11 = "✔" if any(plugin['DalamudApiLevel'] == 11 for plugin in plugins) else ""
        
        # 作者取第一个插件的作者
        author = plugins[0]['Author']
        rows.append(f"| {name} | {api_10}     | {api_11}     | {author} |")
    
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

output_file = "README.md"
write_to_md_file(output_file, markdown_table)
