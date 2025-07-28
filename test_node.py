import pandas as pd
import os

class TestNode:
    """
    测试节点：从character.xlsx读取数据，每个表作为一个选项
    """

    def __init__(self):
        # 获取当前文件所在目录的绝对路径
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.excel_file = os.path.join(current_dir, "character.xlsx")
        self.sheet_data = {}
        self.load_excel_data()

    def load_excel_data(self):
        """加载Excel文件数据"""
        if not os.path.exists(self.excel_file):
            print(f"警告: {self.excel_file} 文件不存在")
            return
        
        try:
            xl = pd.ExcelFile(self.excel_file)
            for sheet_name in xl.sheet_names:
                df = pd.read_excel(self.excel_file, sheet_name=sheet_name)
                # 将每个工作表的数据存储为字典
                sheet_dict = {}
                
                # 添加列名作为选项（第一个选项）
                if len(df.columns) >= 2:
                    col1_name = df.columns[0]  # 中文列名
                    col2_name = df.columns[1]  # 英文列名
                    sheet_dict[col1_name] = col2_name
                
                # 添加数据行作为选项
                for _, row in df.iterrows():
                    # 第一列作为中文显示，第二列作为英文值
                    chinese_key = str(row.iloc[0])
                    english_value = str(row.iloc[1])
                    sheet_dict[chinese_key] = english_value
                
                self.sheet_data[sheet_name] = sheet_dict
        except Exception as e:
            print(f"读取Excel文件时出错: {e}")

    @classmethod
    def INPUT_TYPES(cls):
        # 创建临时实例来获取数据
        temp_instance = cls()
        
        input_types = {
            "required": {
                "输入文本": ("STRING", {
                    "forceInput": True  # 强制作为输入端口，可以接收来自其他节点的字符串
                })
            }
        }
        
        # 为每个工作表添加选项
        for sheet_name, sheet_dict in temp_instance.sheet_data.items():
            if sheet_dict:  # 确保工作表有数据
                options = list(sheet_dict.keys())
                input_types["required"][sheet_name] = (options, {
                    "default": options[0] if options else ""
                })
        
        return input_types

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("输出文本",)
    FUNCTION = "process"
    CATEGORY = "darkbfly"

    def process(self, 输入文本, **kwargs):
        """处理输入文本，根据选择的选项进行转换"""
        
        # 重新加载数据以确保最新
        self.load_excel_data()
        
        result_parts = [输入文本]
        
        # 处理每个工作表的选择
        for sheet_name, sheet_dict in self.sheet_data.items():
            if sheet_name in kwargs:
                selected_chinese = kwargs[sheet_name]
                # 获取对应的英文值
                if selected_chinese in sheet_dict:
                    english_value = sheet_dict[selected_chinese]
                    result_parts.append(english_value)
        
        # 组合结果 - 使用逗号和空格分隔，更符合标签格式
        output_text = ", ".join(result_parts)
        
        return (output_text,)


# 注册节点
NODE_CLASS_MAPPINGS = {
    "TestNode": TestNode
}

# 定义节点显示名称
NODE_DISPLAY_NAME_MAPPINGS = {
    "TestNode": "🧪 测试节点"
}
