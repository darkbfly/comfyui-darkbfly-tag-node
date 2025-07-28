#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
将txt文件中的英文-中文对转换为CSV格式
格式要求：
- 输入txt：奇数行为英文，偶数行为对应的中文翻译
- 输出csv：每行格式为 "中文,英文"，如果中文为空或不包含中文字符，则输出"空白,英文"
"""

import os
import csv
from typing import List, Tuple
import re

def has_chinese(text: str) -> bool:
    """
    检查字符串是否包含中文字符
    
    Args:
        text (str): 要检查的字符串
        
    Returns:
        bool: 是否包含中文字符
    """
    # \u4e00-\u9fff 是中文字符的 Unicode 范围
    return bool(re.search('[\u4e00-\u9fff]', text))

def read_translation_pairs(file_path: str) -> List[Tuple[str, str]]:
    """
    读取txt文件中的翻译对
    
    Args:
        file_path (str): txt文件路径
        
    Returns:
        List[Tuple[str, str]]: 翻译对列表，每个元素为(英文, 中文)
    """
    pairs = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]  # 去除空行
            
        i = 0
        while i < len(lines):
            eng = lines[i]
            
            # 检查下一行是否存在且包含中文
            if i + 1 < len(lines) and has_chinese(lines[i + 1]):
                chn = lines[i + 1]
                i += 2  # 跳过两行
            else:
                chn = ""  # 如果下一行不存在或不包含中文，中文部分为空
                i += 1  # 只跳过一行
                
            if eng:  # 确保英文不为空
                pairs.append((eng, chn))
            
    except Exception as e:
        print(f"读取文件时发生错误: {e}")
        
    return pairs

def save_to_csv(pairs: List[Tuple[str, str]], output_file: str) -> bool:
    """
    将翻译对保存为CSV文件
    
    Args:
        pairs (List[Tuple[str, str]]): 翻译对列表
        output_file (str): 输出CSV文件路径
        
    Returns:
        bool: 是否保存成功
    """
    try:
        with open(output_file, 'w', encoding='gbk', newline='') as f:
            writer = csv.writer(f)
            # 写入每一对翻译，格式：中文,英文
            for eng, chn in pairs:
                # 如果中文为空或不包含中文字符，则写入"空白"
                if not chn.strip() or not has_chinese(chn):
                    writer.writerow(["", eng])
                else:
                    writer.writerow([chn, eng])
        return True
        
    except Exception as e:
        print(f"保存CSV文件时发生错误: {e}")
        return False

def main():
    """
    主函数，处理文件转换流程
    """
    # 获取当前目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 让用户输入txt文件名
    input_file = input("请输入要转换的txt文件名（放在test_tag目录下）: ")
    input_path = os.path.join(current_dir, input_file)
    
    # 如果用户没有加.txt后缀，自动添加
    if not input_path.endswith('.txt'):
        input_path += '.txt'
    
    # 检查文件是否存在
    if not os.path.exists(input_path):
        print(f"错误：文件 {input_path} 不存在")
        return
        
    # 生成输出文件名（将.txt替换为.csv）
    output_file = os.path.splitext(input_path)[0] + '.csv'
    
    # 读取翻译对
    print("正在读取翻译对...")
    pairs = read_translation_pairs(input_path)
    
    if not pairs:
        print("未读取到有效的翻译对")
        return
        
    # 保存为CSV
    print("正在保存为CSV格式...")
    if save_to_csv(pairs, output_file):
        print(f"转换完成！共处理 {len(pairs)} 对翻译")
        print(f"CSV文件已保存到: {output_file}")
        
        # 显示前5对翻译作为预览
        print("\n转换结果预览（前5对）:")
        for i, (eng, chn) in enumerate(pairs[:5], 1):
            print(f"{i}. {chn} -> {eng}")
        if len(pairs) > 5:
            print(f"... 还有 {len(pairs) - 5} 对翻译")
    else:
        print("转换失败")

if __name__ == "__main__":
    main()
