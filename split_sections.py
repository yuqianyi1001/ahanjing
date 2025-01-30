import os
import re
import requests
from text_processor import process_section_text

def process_file(input_file, output_dir):
    # 读取输入文件
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 使用正则表达式分割章节
    # 保留文件头部信息
    header = content.split(r'（[一二三四五六七八九〇十百]+）')[0]
    
    # 分割所有章节
    sections = re.split(r'（[一二三四五六七八九〇十百]+）\n', content)[1:]
    section_names = re.findall(r'（[一二三四五六七八九〇十百]+）', content)
    
    # 处理每个章节
    for name, section in zip(section_names, sections):
        print(f">处理章节：{name}")

        # 提取数字部分并转换为阿拉伯数字格式
        number = name.strip('（）')
        arabic_number = str(cn2num(number))  # 转换为4位数格式
        output_file = os.path.join(output_dir, f'{arabic_number}.md')
        
        # Skip if file already exists
        if os.path.exists(output_file):
            print(f"Skipping existing file: {output_file}")
            continue

        # 写入文件
        with open(output_file, 'w', encoding='utf-8') as f:
            # 添加原始文件头信息
            # f.write(header)
            # 添加章节标记和内容
            f.write(f'{name}\n{section}')

            tags = get_section_tags(section)
            f.write(f'{tags}')

# 进一步处理section文本，分别获取到这些国名，地名，人名，核心佛法
def get_section_tags(text):
    parsed_result = process_section_text(text)

    empty_result = {
        "国家": [], 
        "地名": [], 
        "人名": [], 
        "四圣谛": [],
        "四正勤": [],
        "四念住": [],
        "五根": [],
        "五力": [],
        "七覺支": [],
        "八正道": [],
        "五蕴": [], "十二处": [], "十八界": [],
        "其他重要理论和概念": []
    }

    tags = ""
    for key, value in parsed_result.items():
        if key == "其他重要理论和概念":
            for v in value:
                tags += f"#{v}\n"
        elif value != empty_result[key]:
            for v in value:
                tags += f"#{key}/{v}\n"

    return tags

# 添加中文数字转阿拉伯数字的函数
def cn2num(chinese_num):
    cn_num = {
        '一': '1', '二': '2', '三': '3', '四': '4', '五': '5',
        '六': '6', '七': '7', '八': '8', '九': '9', '〇': '0'
    }
    
    result = ''
    for char in chinese_num:
        if char in cn_num:
            result += cn_num[char]
    
    return result.zfill(4)

def main():
    input_dir = '/Users/junyinwu/ws/POC2025/T0099/T0099.txt'
    output_dir = '/Users/junyinwu/ws/POC2025/T0099/T0099.md'
    
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    
    # 处理目录下的所有 txt 文件
    for filename in os.listdir(input_dir):
        if filename.endswith('.txt'):
            print(f"处理文件：{filename}")
            input_file = os.path.join(input_dir, filename)
            process_file(input_file, output_dir)

if __name__ == '__main__':
    main()

