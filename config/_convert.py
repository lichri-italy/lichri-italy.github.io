import os
import re
import json
import shutil
import markdown
from datetime import datetime

def read_file_content(file_path):
    """读取文件内容"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def convert_markdown_to_html(md_content):
    """将Markdown内容转换为HTML"""
    return markdown.markdown(md_content)

def generate_html_file(md_file_path, template_content, css_content, script_content, post_html_folder):
    """生成HTML文件并返回相关信息"""
    title = os.path.splitext(os.path.basename(md_file_path))[0]
    last_modified_time = datetime.fromtimestamp(os.path.getmtime(md_file_path))
    
    md_content = read_file_content(md_file_path)
    html_content = convert_markdown_to_html(md_content)

    html_file_path = os.path.join(post_html_folder, f'{title}.html')
    
    # 使用模板替换内容
    template = template_content.replace('{{css}}', css_content.replace('\n', '\n        '))
    template = template.replace('{{script}}', script_content.replace('\n', '\n        '))
    template = template.replace('{{content}}', html_content.replace('\n', '\n        '))
    template = template.replace('{{title}}', title)

    # 写入输出文件
    with open(html_file_path, 'w', encoding='utf-8') as f:
        f.write(template)

    # 提取纯文本信息
    text_content = re.sub(r'<.*?>', '', html_content).strip()[:200]

    return {
        'filename': title,
        'file_path': html_file_path,
        'last_modified_time': last_modified_time.isoformat(),
        'text_content': text_content
    }

def remove_files_from_list(posts_info, filenames_to_remove):
    """根据文件名列表删除对象"""
    return [item for item in posts_info if item["filename"] not in filenames_to_remove]

def save_to_json(data, output_json_file):
    """保存数据到JSON文件"""
    with open(output_json_file, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

def move_and_fix_html(src_path, dst_path):
    """移动HTML文件并修复路径"""
    # 移动文件
    shutil.move(src_path, dst_path)
    
    # 读取文件内容
    with open(dst_path, 'r', encoding='utf-8') as f:
        doc_content = f.read()
        
    # 替换路径
    doc_content = doc_content.replace('../config/', 'config/')  # 更新CSS和JS路径
    doc_content = doc_content.replace('../', '')  # 更新其他路径

    # 写回修改后的内容
    with open(dst_path, 'w', encoding='utf-8') as f:
        f.write(doc_content)


def main():
    template_path = 'config/template.html'
    css_path = 'config/styles.css'
    script_path = 'config/scripts.js'

    post_md_folder = 'post_md'
    post_html_folder = 'post_html'
    output_json_file = 'config/list_post.json'

    # 确保输出文件夹存在
    os.makedirs(post_html_folder, exist_ok=True)

    # 读取模板和样式文件
    template_content = read_file_content(template_path)
    css_content = read_file_content(css_path)
    script_content = read_file_content(script_path)

    # 遍历 Markdown 文件夹中的文件并处理
    posts_info = []
    
    for filename in os.listdir(post_md_folder):
        if filename.endswith('.md'):
            md_file_path = os.path.join(post_md_folder, filename)
            posts_info.append(generate_html_file(md_file_path, template_content, css_content, script_content, post_html_folder))

    # 按最后修改时间从新到旧排序
    posts_info.sort(key=lambda x: x['last_modified_time'], reverse=True)

    # 删除指定的文件名
    filenames_to_remove = ["about", "index"]
    posts_info = remove_files_from_list(posts_info, filenames_to_remove)

    # 保存修改后的数据到JSON文件
    save_to_json(posts_info, output_json_file)

    # 移动和修复HTML文件路径
    move_and_fix_html(r'C:\Users\suanp\Documents\Develop\lichri.github.io\post_html\index.html',
                      r'C:\Users\suanp\Documents\Develop\lichri.github.io\index.html')
    
    move_and_fix_html(r'C:\Users\suanp\Documents\Develop\lichri.github.io\post_html\about.html',
                      r'C:\Users\suanp\Documents\Develop\lichri.github.io\about.html')

if __name__ == "__main__":
    main()
