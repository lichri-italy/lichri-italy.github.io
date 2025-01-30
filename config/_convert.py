import os
import re
import json
import markdown
from datetime import datetime

def read_file_content(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def process_markdown_file(md_file_path, template_content, css_content, script_content, post_html_folder):
    # 获取文件名（去除后缀）作为标题
    title = os.path.splitext(os.path.basename(md_file_path))[0]

    # 获取 Markdown 文件的最后修改时间
    last_modified_timestamp = os.path.getmtime(md_file_path)
    last_modified_time = datetime.fromtimestamp(last_modified_timestamp)

    # 读取 Markdown 文件
    md_content = read_file_content(md_file_path)

    # 将 Markdown 转换为 HTML
    html_content = markdown.markdown(md_content)

    # 生成 HTML 文件路径
    html_file_path = os.path.join(post_html_folder, f'{title}.html')

    # 使用原始模板进行替换
    template = template_content.replace('{{css}}', css_content.replace('\n', '\n        '))
    template = template.replace('{{script}}', script_content.replace('\n', '\n        '))
    template = template.replace('{{content}}', html_content.replace('\n', '\n        '))
    template = template.replace('{{title}}', title)

    # 写入输出文件
    with open(html_file_path, 'w', encoding='utf-8') as f:
        f.write(template)

    # 提取纯文本信息
    text_content = re.sub(r'<.*?>', '', html_content)
    text_content = text_content.strip()[:200]

    return {
        'filename': title,  # 文件名不包含后缀
        'file_path': html_file_path,  # 文件路径
        'last_modified_time': last_modified_time.isoformat(),  # 最后编辑时间
        'text_content': text_content
    }

def main():
    template_path = 'config/template.html'
    css_path = 'config/styles.css'
    script_path = 'config/scripts.js'

    post_md_folder = 'post_md'
    post_html_folder = 'post_html'
    output_json_file = 'config/list_post.json'

    # 确保输出文件夹存在
    os.makedirs(post_html_folder, exist_ok=True)

    # 读取模板文件
    template_content = read_file_content(template_path)
    css_content = read_file_content(css_path)
    script_content = read_file_content(script_path)

    # 遍历 Markdown 文件夹中的文件
    posts_info = []
    for filename in os.listdir(post_md_folder):
        if filename.endswith('.md'):
            md_file_path = os.path.join(post_md_folder, filename)
            posts_info.append(process_markdown_file(md_file_path, template_content, css_content, script_content, post_html_folder))

    # 按最后修改时间从新到旧排序
    posts_info.sort(key=lambda x: x['last_modified_time'], reverse=True)

    # 写入输出文件
    with open(output_json_file, 'w', encoding='utf-8') as f:
        json.dump(posts_info, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()
