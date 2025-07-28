// multiselect.js
// ComfyUI 多选按钮组 widget
app.registerExtension({
    name: "YourPlugin.Multiselect",
    init() {
        // 创建多选 widget
        function createMultiSelect(node, widget) {
            const options = widget.options || [];
            const selected = new Set();

            // 解析初始值
            if (widget.value) {
                widget.value.split(",").map(s => s.trim()).forEach(s => {
                    if (s) selected.add(s);
                });
            }

            // 容器
            const container = document.createElement("div");
            container.style.padding = "6px";
            container.style.display = "flex";
            container.style.flexWrap = "wrap";
            container.style.gap = "4px";
            container.style.marginTop = "4px";

            // 更新按钮状态
            function updateButtons() {
                container.innerHTML = ""; // 清空
                options.forEach(opt => {
                    const btn = document.createElement("button");
                    btn.type = "button";
                    btn.textContent = opt;
                    btn.style.fontSize = "12px";
                    btn.style.padding = "3px 8px";
                    btn.style.border = "1px solid #555";
                    btn.style.background = selected.has(opt) ? "#0a5" : "#333";
                    btn.style.color = "#fff";
                    btn.style.borderRadius = "6px";
                    btn.style.cursor = "pointer";
                    btn.style.height = "auto";
                    btn.style.minWidth = "max-content";

                    btn.onmouseenter = () => {
                        btn.style.opacity = "0.9";
                    };
                    btn.onmouseleave = () => {
                        btn.style.opacity = "1";
                    };

                    btn.onclick = (e) => {
                        if (selected.has(opt)) {
                            selected.delete(opt);
                            btn.style.background = "#333";
                        } else {
                            selected.add(opt);
                            btn.style.background = "#0a5";
                        }
                        // 更新值（逗号分隔）
                        widget.value = Array.from(selected).join(", ");
                        // 标记节点需要重新计算
                        node.setDirtyCanvas(true, false);
                        e.preventDefault();
                        e.stopPropagation();
                    };

                    container.appendChild(btn);
                });
            }

            updateButtons();

            // 挂载到 widget，防止重复创建
            widget.comfyMultiselectContainer = container;
            node.addDOM(container);

            // 返回 widget 高度（动态计算）
            return 32 + Math.ceil(options.length / 5) * 26; // 每行约 5 个，每行高 26px
        }

        // 拦截节点 widget 渲染
        const oldDrawWidgets = LGraphCanvas.prototype.drawNodeWidgets;
        LGraphCanvas.prototype.drawNodeWidgets = function (node, ctx, posY) {
            const result = oldDrawWidgets.apply(this, arguments);

            if (node.widgets) {
                for (const widget of node.widgets) {
                    // ✅ 识别 comfywidget: multiselect
                    if (widget.comfywidget === "multiselect" && !widget.comfyMultiselectContainer) {
                        createMultiSelect(node, widget);
                    }
                }
            }

            return result;
        };
    }
});