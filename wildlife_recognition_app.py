# -*- coding: utf-8 -*-
"""
野生动物图像识别系统 - 主应用程序
基于Tkinter的野生动物物种识别图形用户界面
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import threading
import os
from siamese_network import WildlifeRecognitionModel


class WildlifeRecognitionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("野生动物图像识别系统")
        self.root.geometry("1000x700")
        self.root.configure(bg="#f0f0f0")

        # 初始化模型（延迟加载）
        self.model = None
        self.current_image_path = None
        self.current_photo = None

        # 创建用户界面
        self.create_widgets()

        # 状态
        self.update_status("就绪")

    def create_widgets(self):
        """创建所有UI组件"""

        # 标题栏
        title_frame = tk.Frame(self.root, bg="#2c3e50", height=60)
        title_frame.pack(fill=tk.X, side=tk.TOP)
        title_frame.pack_propagate(False)

        title_label = tk.Label(
            title_frame,
            text="野生动物图像识别系统",
            font=("Microsoft YaHei", 20, "bold"),
            bg="#2c3e50",
            fg="white"
        )
        title_label.pack(pady=15)

        # 主容器
        main_container = tk.Frame(self.root, bg="#f0f0f0")
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 顶部框架 - 按钮
        button_frame = tk.Frame(main_container, bg="#f0f0f0")
        button_frame.pack(fill=tk.X, pady=(0, 10))

        # 上传按钮
        self.upload_btn = tk.Button(
            button_frame,
            text="📁 上传图像",
            command=self.upload_image,
            font=("Microsoft YaHei", 12, "bold"),
            bg="#3498db",
            fg="white",
            activebackground="#2980b9",
            activeforeground="white",
            padx=20,
            pady=10,
            cursor="hand2",
            relief=tk.RAISED,
            bd=3
        )
        self.upload_btn.pack(side=tk.LEFT, padx=5)

        # 清除按钮
        self.clear_btn = tk.Button(
            button_frame,
            text="🗑 清除",
            command=self.clear_all,
            font=("Microsoft YaHei", 12, "bold"),
            bg="#e74c3c",
            fg="white",
            activebackground="#c0392b",
            activeforeground="white",
            padx=20,
            pady=10,
            cursor="hand2",
            relief=tk.RAISED,
            bd=3
        )
        self.clear_btn.pack(side=tk.LEFT, padx=5)

        # 内容框架 - 图像和预测结果
        content_frame = tk.Frame(main_container, bg="#f0f0f0")
        content_frame.pack(fill=tk.BOTH, expand=True)

        # 左侧框架 - 图像显示
        left_frame = tk.LabelFrame(
            content_frame,
            text="已上传图像",
            font=("Microsoft YaHei", 12, "bold"),
            bg="white",
            fg="#2c3e50",
            bd=2,
            relief=tk.GROOVE
        )
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        # 图像画布
        self.canvas = tk.Canvas(
            left_frame,
            bg="#ecf0f1",
            highlightthickness=0
        )
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 画布上的占位文本
        self.canvas_text = self.canvas.create_text(
            0, 0,
            text="尚未上传图像\n点击'上传图像'开始",
            font=("Microsoft YaHei", 14),
            fill="#95a5a6",
            justify=tk.CENTER
        )

        # 右侧框架 - 预测结果
        right_frame = tk.LabelFrame(
            content_frame,
            text="前五预测结果",
            font=("Microsoft YaHei", 12, "bold"),
            bg="white",
            fg="#2c3e50",
            bd=2,
            relief=tk.GROOVE,
            width=300
        )
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(0, 0))
        right_frame.pack_propagate(False)

        # 预测结果容器（带滚动条）
        predictions_container = tk.Frame(right_frame, bg="white")
        predictions_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 滚动条
        scrollbar = tk.Scrollbar(predictions_container)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # 预测结果文本框
        self.predictions_text = tk.Text(
            predictions_container,
            font=("Microsoft YaHei", 10),
            bg="#ffffff",
            fg="#2c3e50",
            wrap=tk.WORD,
            yscrollcommand=scrollbar.set,
            state=tk.DISABLED,
            relief=tk.FLAT,
            padx=10,
            pady=10
        )
        self.predictions_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.predictions_text.yview)

        # 配置文本标签样式
        self.predictions_text.tag_configure("header", font=("Microsoft YaHei", 12, "bold"), foreground="#2c3e50")
        self.predictions_text.tag_configure("species", font=("Microsoft YaHei", 11, "bold"), foreground="#27ae60")
        self.predictions_text.tag_configure("confidence", font=("Microsoft YaHei", 10), foreground="#7f8c8d")
        self.predictions_text.tag_configure("separator", foreground="#bdc3c7")

        # 底部框架 - 状态栏
        status_frame = tk.Frame(self.root, bg="#34495e", height=35)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        status_frame.pack_propagate(False)

        self.status_label = tk.Label(
            status_frame,
            text="就绪",
            font=("Microsoft YaHei", 10),
            bg="#34495e",
            fg="white",
            anchor=tk.W
        )
        self.status_label.pack(fill=tk.X, padx=10, pady=5)

        # 绑定画布调整大小事件
        self.canvas.bind("<Configure>", self.on_canvas_resize)

    def on_canvas_resize(self, event):
        """处理画布大小调整以更新占位文本或图像"""
        # 更新占位文本位置
        self.canvas.coords(self.canvas_text, event.width // 2, event.height // 2)

        # 如果已加载图像，重新绘制
        if self.current_image_path and os.path.exists(self.current_image_path):
            self.display_image(self.current_image_path)

    def upload_image(self):
        """处理图像上传"""
        file_path = filedialog.askopenfilename(
            title="选择野生动物图像",
            filetypes=[
                ("图像文件", "*.jpg *.jpeg *.png *.bmp *.gif *.webp *.tiff *.tif *.jfif *.JPG *.JPEG *.PNG *.BMP *.GIF *.WEBP *.TIFF *.TIF *.JFIF"),
                ("JPEG文件", "*.jpg *.jpeg *.JPG *.JPEG *.jfif *.JFIF"),
                ("PNG文件", "*.png *.PNG"),
                ("所有文件", "*.*")
            ]
        )

        if file_path:
            self.current_image_path = file_path
            self.display_image(file_path)
            self.predict_species(file_path)

    def display_image(self, image_path):
        """在画布上显示图像并自动调整大小"""
        try:
            # 隐藏占位文本
            self.canvas.itemconfig(self.canvas_text, state='hidden')

            # 打开图像
            image = Image.open(image_path)

            # 获取画布尺寸
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()

            # 计算缩放比例以适应画布，同时保持纵横比
            img_width, img_height = image.size
            scale_w = canvas_width / img_width
            scale_h = canvas_height / img_height
            scale = min(scale_w, scale_h) * 0.95  # 95%以留出一些边距

            new_width = int(img_width * scale)
            new_height = int(img_height * scale)

            # 调整图像大小
            image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)

            # 转换为PhotoImage
            self.current_photo = ImageTk.PhotoImage(image)

            # 清除画布并显示图像
            self.canvas.delete("image")
            self.canvas.create_image(
                canvas_width // 2,
                canvas_height // 2,
                image=self.current_photo,
                anchor=tk.CENTER,
                tags="image"
            )

            self.update_status(f"图像已加载: {os.path.basename(image_path)}")

        except Exception as e:
            messagebox.showerror("错误", f"加载图像失败:\n{str(e)}")
            self.update_status("图像加载错误")

    def predict_species(self, image_path):
        """在单独的线程中预测物种"""
        self.update_status("正在预测...")

        # 预测期间禁用按钮
        self.upload_btn.config(state=tk.DISABLED)
        self.clear_btn.config(state=tk.DISABLED)

        # 在单独的线程中运行预测以避免冻结UI
        thread = threading.Thread(target=self._predict_worker, args=(image_path,))
        thread.daemon = True
        thread.start()

    def _predict_worker(self, image_path):
        """预测工作线程"""
        try:
            # 如果尚未完成，初始化模型
            if self.model is None:
                self.root.after(0, self.update_status, "正在加载模型...")
                self.model = WildlifeRecognitionModel()

            # 进行预测
            predictions = self.model.predict(image_path, top_k=5)

            # 在主线程上更新UI
            self.root.after(0, self.display_predictions, predictions)
            self.root.after(0, self.update_status, "预测完成！")

        except Exception as e:
            self.root.after(0, messagebox.showerror, "错误", f"预测失败:\n{str(e)}")
            self.root.after(0, self.update_status, "预测失败")

        finally:
            # 重新启用按钮
            self.root.after(0, lambda: self.upload_btn.config(state=tk.NORMAL))
            self.root.after(0, lambda: self.clear_btn.config(state=tk.NORMAL))

    def display_predictions(self, predictions):
        """显示预测结果"""
        # 启用文本框进行编辑
        self.predictions_text.config(state=tk.NORMAL)
        self.predictions_text.delete(1.0, tk.END)

        # 标题
        self.predictions_text.insert(tk.END, "预测结果\n", "header")
        self.predictions_text.insert(tk.END, "=" * 35 + "\n\n", "separator")

        # 最高预测（突出显示）
        if predictions:
            top_species, top_confidence = predictions[0]
            self.predictions_text.insert(tk.END, "最高预测:\n", "header")
            self.predictions_text.insert(tk.END, f"🦁 {top_species}\n", "species")
            self.predictions_text.insert(tk.END, f"置信度: {top_confidence:.2f}%\n\n", "confidence")
            self.predictions_text.insert(tk.END, "-" * 35 + "\n\n", "separator")

        # 所有预测
        self.predictions_text.insert(tk.END, "所有预测:\n", "header")
        self.predictions_text.insert(tk.END, "-" * 35 + "\n", "separator")

        for i, (species, confidence) in enumerate(predictions, 1):
            # 排名表情符号
            rank_emoji = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"][i-1] if i <= 5 else f"{i}."

            self.predictions_text.insert(tk.END, f"\n{rank_emoji} ", "confidence")
            self.predictions_text.insert(tk.END, f"{species}\n", "species")

            # 置信度条
            bar_length = int(confidence / 5)  # 缩放到最多20个字符
            bar = "█" * bar_length + "░" * (20 - bar_length)
            self.predictions_text.insert(tk.END, f"   {bar} {confidence:.2f}%\n", "confidence")

        # 禁用文本框
        self.predictions_text.config(state=tk.DISABLED)

    def clear_all(self):
        """清除所有数据并重置界面"""
        # 清除图像
        self.canvas.delete("image")
        self.canvas.itemconfig(self.canvas_text, state='normal')
        self.current_image_path = None
        self.current_photo = None

        # 清除预测结果
        self.predictions_text.config(state=tk.NORMAL)
        self.predictions_text.delete(1.0, tk.END)
        self.predictions_text.config(state=tk.DISABLED)

        # 重置状态
        self.update_status("就绪")

    def update_status(self, message):
        """更新状态栏消息"""
        self.status_label.config(text=message)


def main():
    """主入口点"""
    root = tk.Tk()
    app = WildlifeRecognitionApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
