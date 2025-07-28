#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
读取CSV文件并查找关键字匹配的所有行，将结果保存到txt文件
"""

import pandas as pd
import os

def find_all_matches(keyword: str) -> list[str]:
    """
    在CSV文件中查找所有匹配关键字的行的第一列数据
    
    Args:
        keyword (str): 要搜索的关键字
        
    Returns:
        list[str]: 所有匹配行的第一列数据列表
    """
    # 获取CSV文件的绝对路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(current_dir, 'danbooru_e621_merged.csv')
    
    try:
        # 读取CSV文件
        df = pd.read_csv(csv_path)
        
        # 检查第一列是否包含关键字
        mask = df.iloc[:, 0].str.contains(keyword, case=False, na=False)
        
        # 获取所有匹配的行的第一列数据
        if mask.any():
            matched_rows = df[mask].iloc[:, 0].tolist()
            return matched_rows
        
        return []
        
    except Exception as e:
        print(f"读取文件时发生错误: {e}")
        return []

def save_results_to_txt(results: list[str], keyword: str) -> str:
    """
    将结果保存到txt文件
    
    Args:
        results (list[str]): 要保存的结果列表
        keyword (str): 搜索的关键字，用于生成文件名
        
    Returns:
        str: 保存的文件路径
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(current_dir, f'search_results_{keyword}.txt')
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            for result in results:
                f.write(f"{result}\n")
        return output_file
    except Exception as e:
        print(f"保存文件时发生错误: {e}")
        return ""

def main():
    """
    主函数，用于执行搜索和保存结果
    """
    keyword = input("请输入要搜索的关键字: ")
    results = find_all_matches(keyword)
    
    if results:
        output_file = save_results_to_txt(results, keyword)
        if output_file:
            print(f"找到 {len(results)} 个匹配项")
            print(f"结果已保存到文件: {output_file}")
            print("\n前5个匹配项预览:")
            for i, result in enumerate(results[:5], 1):
                print(f"{i}. {result}")
            if len(results) > 5:
                print(f"... 还有 {len(results) - 5} 个结果在文件中")
    else:
        print("未找到匹配的行")

if __name__ == "__main__":
    main()
