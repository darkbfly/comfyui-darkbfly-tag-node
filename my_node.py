# custom_nodes/my_basic_node/my_node.py

class SimpleStringNode:
    """
    一个最简单的节点：输入字符串，原样输出
    """

    # 定义输入类型
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {
                    "default": "你好，ComfyUI！",
                    "multiline": True
                })
            }
        }

    # 定义输出类型
    RETURN_TYPES = ("STRING",)
    # 输出名称（可选）
    RETURN_NAMES = ("输出文本",)

    # 执行函数
    FUNCTION = "run"

    # 在节点菜单中的分类
    CATEGORY = "basic"  # 会在右键菜单中显示为 "basic"

    def run(self, text):
        # 直接返回输入的文本
        return (text,)


# 注册节点（必须！）
NODE_CLASS_MAPPINGS = {
    "SimpleStringNode": SimpleStringNode
}

# 可选：定义节点在界面上显示的名字
NODE_DISPLAY_NAME_MAPPINGS = {
    "SimpleStringNode": "📌 简单文本节点"
}