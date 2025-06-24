import tkinter as tk
from tkinter import messagebox

class NumberFiller:
    def __init__(self, root):
        self.root = root
        self.root.title("自动填充数字")

        # 创建一个字典存储每个数字出现的次数
        self.number_count = {i: 0 for i in range(1, 50)}

        # 每组数字的统计计数
        self.group_count = 0

        # 每个生肖的统计计数
        self.zodiac_count = {zodiac: 0 for zodiac in [
             "蛇","龙", "兔", "虎", "牛", "鼠", "猪", "狗", "鸡", "猴", "羊", "马"
        ]}

        # 数字与汉字映射表
        self.number_to_chinese = {
            (1, 13, 25, 37, 49): "蛇",
            (2, 14, 26, 38): "龙",
            (3, 15, 27, 39): "兔",
            (4, 16, 28, 40): "虎",
            (5, 17, 29, 41): "牛",
            (6, 18, 30, 42): "鼠",
            (7, 19, 31, 43): "猪",
            (8, 20, 32, 44): "狗",
            (9, 21, 33, 45): "鸡",
            (10, 22, 34, 46): "猴",
            (11, 23, 35, 47): "羊",
            (12, 24, 36, 48): "马",
        }

        # 数字与颜色映射表
        self.number_to_color = {
            "red": {1, 13, 2, 40, 29, 18, 30, 7, 19, 8, 45, 34, 46, 23, 35, 12, 24},
            "blue": {25, 37, 14, 26, 3, 15, 4, 41, 42, 31, 20, 9, 10, 47, 36, 48},
            "green": {49, 38, 27, 39, 16, 28, 5, 17, 6, 43, 32, 44, 21, 33, 22, 11},
        }

        # 创建表格并显示数字、汉字和颜色
        self.labels = {}
        self.create_grid()

        # 输入框和提交、复位按钮，调整输入框宽度为60
        self.input_entry = tk.Entry(self.root, width=60)  # 原为50，现改为60
        self.input_entry.grid(row=6, column=0, columnspan=5, pady=10)

        # 数字分组复选框，选择每组数字的个数
        self.group_size = tk.IntVar()
        self.group_size.set(12)  # 默认选择12个数字一组

        self.radio1 = tk.Radiobutton(self.root, text="1个", variable=self.group_size, value=1)
        self.radio1.grid(row=6, column=5)

        self.radio4 = tk.Radiobutton(self.root, text="4个", variable=self.group_size, value=4)
        self.radio4.grid(row=6, column=6)

        self.radio8 = tk.Radiobutton(self.root, text="8个", variable=self.group_size, value=8)
        self.radio8.grid(row=6, column=7)

        self.radio12 = tk.Radiobutton(self.root, text="12个", variable=self.group_size, value=12)
        self.radio12.grid(row=6, column=8)

        submit_button = tk.Button(self.root, text="提交", command=self.submit_numbers)
        submit_button.grid(row=6, column=9, pady=10)

        reset_button = tk.Button(self.root, text="复位", command=self.reset_stats)
        reset_button.grid(row=6, column=10, pady=10)

        # 统计信息区域，使用 Frame 包含两个 Text 控件
        self.stats_frame = tk.Frame(self.root)
        self.stats_frame.grid(row=7, column=0, columnspan=12, pady=10)
        self.create_stats_text()  # 初始化统计信息文本框

    def create_grid(self):
        """ 创建一个每行12个格子，总5行，最后一行只1个格子的表格 """
        grid_rows = 5
        grid_cols = 12
        total_numbers = 49

        for i in range(grid_rows - 1):  # 前4行
            for j in range(grid_cols):
                num = i * grid_cols + j + 1
                if num > total_numbers:  # 超过49时停止
                    break

                # 获取汉字
                chinese = next((text for group, text in self.number_to_chinese.items() if num in group), "")

                # 获取颜色
                bg_color = "white"  # 默认白色
                if num in self.number_to_color["red"]:
                    bg_color = "red"
                elif num in self.number_to_color["blue"]:
                    bg_color = "blue"
                elif num in self.number_to_color["green"]:
                    bg_color = "green"

                label = tk.Label(self.root, text=f"{num}\n{chinese}", width=6, height=3, borderwidth=1, relief="solid", bg=bg_color, fg="white")
                label.grid(row=i, column=j, sticky="nsew")
                self.labels[num] = label

        # 最后一行只有1个格子
        last_num = 49
        chinese = next((text for group, text in self.number_to_chinese.items() if last_num in group), "")
        bg_color = "green"
        label = tk.Label(self.root, text=f"{last_num}\n{chinese}", width=6, height=3, borderwidth=1, relief="solid", bg=bg_color, fg="white")
        label.grid(row=4, column=0, sticky="nsew")  # 只占用第一列
        self.labels[last_num] = label

        # 让所有列宽一致
        for j in range(grid_cols):
            self.root.grid_columnconfigure(j, weight=1, uniform="equal")

        # 让行高一致
        for i in range(grid_rows):
            self.root.grid_rowconfigure(i, weight=1, uniform="equal")

    def submit_numbers(self):
        """ 提交一组或多组数字并更新表格 """
        input_text = self.input_entry.get()
        group_size = self.group_size.get()  # 获取选中的组大小

        try:
            # 解析输入的数字，并将其转换为整数列表
            separators = ', - * ; + . ， 。    / '.split()
            for sep in separators:
                input_text = input_text.replace(sep, ' ')
            numbers = list(map(int, input_text.split()))

            # 检查输入的数字个数是否是选定组大小的倍数
            if len(numbers) % group_size != 0 or not all(1 <= num <= 49 for num in numbers):
                raise ValueError(f"输入的数字总数必须是{group_size}的倍数，且数字范围为1到49之间！")

            # 统计每组的数字个数
            group_counts = len(numbers) // group_size
            self.group_count += group_counts

            # 更新每个数字的计数
            for num in numbers:
                self.number_count[num] += 1
                zodiac = next((text for group, text in self.number_to_chinese.items() if num in group), "")
                if zodiac:
                    self.zodiac_count[zodiac] += 1
                self.update_label(num)

            # 更新统计信息
            self.update_stats_text()

            # 清空输入框
            self.input_entry.delete(0, tk.END)

        except ValueError as e:
            messagebox.showerror("输入错误", str(e))

    def update_label(self, num):
        """ 更新指定数字对应标签的显示，在次数后加‘次’ """
        count = self.number_count[num]
        current_text = self.labels[num]["text"]
        chinese = current_text.split("\n")[1]  # 保留原来的汉字部分
        self.labels[num].config(text=f"{num}\n{chinese}\n{count}次")

    def create_stats_text(self):
        """ 创建两个Text控件来显示统计信息，左右布局 """
        # 左侧Text控件：总组数和数字出现次数
        self.left_stats_text = tk.Text(self.stats_frame, wrap="word", width=30, height=15, font=("Arial", 12))
        self.left_stats_text.grid(row=0, column=0, padx=5, sticky="nsew")
        self.left_stats_text.config(state=tk.DISABLED)

        # 右侧Text控件：生肖出现次数
        self.right_stats_text = tk.Text(self.stats_frame, wrap="word", width=30, height=15, font=("Arial", 12))
        self.right_stats_text.grid(row=0, column=1, padx=5, sticky="nsew")
        self.right_stats_text.config(state=tk.DISABLED)

        # 让两列宽度均分
        self.stats_frame.grid_columnconfigure(0, weight=1)
        self.stats_frame.grid_columnconfigure(1, weight=1)

    def update_stats_text(self):
        """ 更新统计信息区域，左侧显示总组数和数字出现次数，右侧显示生肖出现次数 """
        # 按出现次数排序数字和生肖
        sorted_counts = sorted(self.number_count.items(), key=lambda x: x[1], reverse=True)
        sorted_zodiac_counts = sorted(self.zodiac_count.items(), key=lambda x: x[1], reverse=True)

        # 更新左侧统计信息
        self.left_stats_text.config(state=tk.NORMAL)
        self.left_stats_text.delete(1.0, tk.END)
        self.left_stats_text.insert(tk.END, f"总组数: {self.group_count}\n\n")
        self.left_stats_text.insert(tk.END, "数字出现次数:\n")
        for num, count in sorted_counts:
            self.left_stats_text.insert(tk.END, f"{num}  {count}\n")
        self.left_stats_text.config(state=tk.DISABLED)

        # 更新右侧统计信息
        self.right_stats_text.config(state=tk.NORMAL)
        self.right_stats_text.delete(1.0, tk.END)
        self.right_stats_text.insert(tk.END, "生肖出现次数:\n")
        for zodiac, count in sorted_zodiac_counts:
            self.right_stats_text.insert(tk.END, f"{zodiac}: {count}\n")
        self.right_stats_text.config(state=tk.DISABLED)

    def reset_stats(self):
        """ 重置统计数据和表格 """
        self.number_count = {i: 0 for i in range(1, 50)}
        self.group_count = 0
        self.zodiac_count = {zodiac: 0 for zodiac in self.zodiac_count}

        # 更新所有标签
        for num, label in self.labels.items():
            chinese = label["text"].split("\n")[1]
            label.config(text=f"{num}\n{chinese}")

        # 更新统计信息
        self.update_stats_text()

if __name__ == "__main__":
    root = tk.Tk()
    app = NumberFiller(root)
    root.mainloop()
