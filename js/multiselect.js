// ComfyUI 自定义节点扩展
app.registerExtension({
    name: "Comfy.MultiSelectWidget",
    init() {
        // 定义自定义 widget
        const widget = {
            type: "multiselect_widget",
            draw: function (ctx, node, widget, width, posY) {
                const options = ["Option A", "Option B", "Option C", "Option D"];
                const selected = (node.widgets[0].value || "").split(",").map(s => s.trim());

                // 创建容器
                const container = document.createElement("div");
                container.style.padding = "4px";
                container.style.display = "flex";
                container.style.flexWrap = "wrap";
                container.style.gap = "2px";

                options.forEach(opt => {
                    const btn = document.createElement("button");
                    btn.type = "button";
                    btn.textContent = opt;
                    btn.style.fontSize = "12px";
                    btn.style.padding = "2px 6px";
                    btn.style.border = "1px solid #555";
                    btn.style.background = selected.includes(opt) ? "#0a5" : "#333";
                    btn.style.color = "#fff";
                    btn.style.borderRadius = "4px";
                    btn.onclick = (e) => {
                        const idx = selected.indexOf(opt);
                        if (idx > -1) {
                            selected.splice(idx, 1);
                        } else {
                            selected.push(opt);
                        }
                        // 更新字符串值
                        node.widgets[0].value = selected.join(", ");
                        // 重新绘制
                        node.onResize();
                        e.preventDefault();
                        e.stopPropagation();
                    };
                    container.appendChild(btn);
                });

                // 清理旧内容
                if (widget.comfyMultiselectWidget) {
                    widget.comfyMultiselectWidget.remove();
                }
                widget.comfyMultiselectWidget = container;
                node.addDOM(container);
                return 24; // 高度
            }
        };

        // 注册 widget
        LGraphCanvas.prototype.registerMultiselectWidget = function () {
            this.widgets[widget.type] = widget;
        };

        // 注入 widget
        const orig = LGraphCanvas.prototype.drawNodeWidgets;
        LGraphCanvas.prototype.drawNodeWidgets = function (node, ctx, posY) {
            if (node.widgets) {
                node.widgets.forEach(w => {
                    if (w.type === "multiselect_widget") {
                        return widget.draw(ctx, node, w, node.size[0], posY);
                    }
                });
            }
            return orig.apply(this, arguments);
        };
    }
});