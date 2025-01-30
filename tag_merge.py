import os
from collections import Counter
import opencc
# T0099.md 里面有很多md文件，文件里面的内容这样做样几部分组成：名称，经文，tags，tag示例如下：
#   #国家/舍衛國
#   #地名/祇樹給孤獨園
#   #八正道/正觀
#   #五蕴/色
#   #五蕴/受
#   #五蕴/想
#   #五蕴/行
#   #五蕴/識
#   #無常
#   #心解脫
#   #苦
#   #空
#   #非我
# 统计下所有的tags，以及它们的数量
# 排序
# 打印

def extract_tags_from_file(file_path):
    tags = []
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        # Look for tags section
        if '#' in content:
            # Split content by lines and filter lines starting with #
            tags = [line.strip() for line in content.split('\n') if line.strip().startswith('#')]
            
    return tags

def process_markdown_files(directory):
    all_tags = []
    
    # Walk through all files in directory
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                print(file)
                file_path = os.path.join(root, file)
                file_tags = extract_tags_from_file(file_path)
                all_tags.extend(file_tags)
    
    # Count tags
    tag_counts = Counter(all_tags)
    
    # Sort by count (descending) and then by tag name (ascending)
    # sorted_tags = sorted(tag_counts.items(), key=lambda x: (-x[1], x[0]))

    # sort by tag name (ascending)
    sorted_tags = sorted(tag_counts.items(), key=lambda x: x[0])
    
    # Print results
    # Create/overwrite the file before the loop
    with open('tag_counts.txt', 'w', encoding='utf-8') as f:
        for tag, count in sorted_tags:
            if tag:  # Only print non-empty tags
                f.write(f"{tag}: {count}\n")


def convert_tags_to_traditional():
    # 创建简体到繁体转换器
    converter = opencc.OpenCC('s2t')
    
    # Walk through all files in directory
    for root, dirs, files in os.walk("T0099.md"):
        for file in files:
            if file.endswith('.md'):
                print(f"Processing: {file}")
                file_path = os.path.join(root, file)
                
                # 读取文件内容
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                
                # 只转换以#开头的标签行
                converted_lines = []
                for line in lines:
                    if line.strip().startswith('#'):
                        converted_line = converter.convert(line)
                        converted_lines.append(converted_line)
                    else:
                        converted_lines.append(line)
                
                # 写回文件
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.writelines(converted_lines)

def merge_tags(merge_this, merge_that): 
    # Walk through all files in directory
    for root, dirs, files in os.walk("T0099.md"):
        for file in files:
            if file.endswith('.md'):
                print(f"Processing: {file}")
                file_path = os.path.join(root, file)
                
                # 读取文件内容
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 替换标签
                old_tag = f"#{merge_this}"
                new_tag = f"#{merge_that}"
                if old_tag in content:
                    content = content.replace(old_tag, new_tag)
                    print(f"Replacing {old_tag} with {new_tag} in {file}")
                    
                    # 写回文件
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
    pass


if __name__ == "__main__":
    directory = "T0099.md"  # Directory containing markdown files
    process_markdown_files(directory)

    # in tag_counts.txt, they are some same tags with different cases, like:
    #  #国家/舍卫国: 129
    #  #国家/舍衛國: 714

    # merge this into that, meaning 
    # change all #国家/舍卫国 to #国家/舍衛國 in all *.md files under folder "T0099.md"
    # merge_tags('七覺分', '国家/舍衛國')
    # 调用转换函数
    
    #convert_tags_to_traditional()

