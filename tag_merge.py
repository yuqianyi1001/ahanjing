import os
from collections import Counter
import opencc
# T0099.md 里面有很多md文件，文件里面的内容这样做样几部分组成：名称，经文，tags，tag示例如下：
#   #国家/舍衛國
#   
#   #八正道
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
    
    # sort by tag name (ascending)
    sorted_tags = sorted(tag_counts.items(), key=lambda x: x[0])
    
    # Print results
    with open('tag_counts.txt', 'w', encoding='utf-8') as f:
        for tag, count in sorted_tags:
            if tag:  # Only print non-empty tags
                f.write(f"{tag}: {count}\n")
    
    return tag_counts  # 返回 Counter 对象而不是 sorted_tags

def keep_core_thoeries_tags(tag_counts):
    threshold = 10
    
    for root, dirs, files in os.walk("T0099.md"):
        for file in files:
            if file.endswith('.md'):
                print(f"Processing: {file}")
                file_path = os.path.join(root, file)

                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                
                filtered_lines = []
                for line in lines:
                    line = line.strip()
                    if line.startswith('#'):
                        if tag_counts[line] >= threshold:  # 使用 Counter 对象的方括号访问
                            filtered_lines.append(line + '\n')
                    else:
                        filtered_lines.append(line + '\n')
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.writelines(filtered_lines)



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

def remove_duplicate_tags(file_path):
    # 读取文件内容
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # 用于记录已经出现过的标签
    seen_tags = set()
    # 存储处理后的行
    filtered_lines = []
    
    for line in lines:
        line = line.strip()
        if line.startswith('#'):
            # 如果是标签行，检查是否已经出现过
            if line not in seen_tags:
                seen_tags.add(line)
                filtered_lines.append(line + '\n')
        else:
            # 非标签行直接保留
            filtered_lines.append(line + '\n')
    
    # 写回文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(filtered_lines)


if __name__ == "__main__":
    #directory = "T0099.md"  # Directory containing markdown files
    #tag_counts = process_markdown_files(directory)
    ## keep_core_thoeries_tags(tag_counts)

    # in tag_counts.txt, they are some same tags with different cases, like:
    #  #国家/舍卫国: 129
    #  #国家/舍衛國: 714

    # merge this into that, meaning 
    # change all #国家/舍卫国 to #国家/舍衛國 in all *.md files under folder "T0099.md"
    # merge_tags('七覺分', '国家/舍衛國')
    # 调用转换函数
    
    #convert_tags_to_traditional()
    for root, dirs, files in os.walk("T0099.md"):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                remove_duplicate_tags(file_path)

