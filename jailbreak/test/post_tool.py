import tkinter as tk
from tkinter import messagebox
import requests
import pprint

def send_request():
    url = url_entry.get()
    data = data_text.get("1.0", tk.END).strip()
    option = option_var.get()

    if not url or not data:
        messagebox.showwarning("输入错误", "请输入URL和发送内容")
        return

    full_url = f"{url}{option}"

    try:
        response = requests.post(full_url, data=data)
        response_text = pprint.pformat(response)
    except Exception as e:
        response_text = f"请求失败: {e}"

    result_text.delete("1.0", tk.END)
    result_text.insert(tk.END, response_text)

def update_default_text(*args):
    option = option_var.get()
    if option == "TaskCreate":
        default_text = """
    {
        "Suite_name" : "halluSuite1",
        "Test_name" : "halluTest1",
        "Task_name" : "hallutask1"
    }
    """
    elif option == "TaskDele":
        default_text = """
    {
        "Task_name" : "hallutask1"
    }
    """
    elif option == "TaskExec":
        default_text = """
        {
            "Task_name": "hallutask1"
        }
    """
    data_text.delete("1.0", tk.END)
    data_text.insert(tk.END, default_text)

# 创建主窗口
root = tk.Tk()
root.title("POST请求小工具")

# URL输入框和标签
tk.Label(root, text="URL:").pack()
url_entry = tk.Entry(root, width=50)
url_entry.insert(0, "http://localhost/api/")  # 设置默认值
url_entry.pack()

# 发送内容输入框和标签
tk.Label(root, text="发送内容:").pack()
data_text = tk.Text(root, height=10, width=50)
data_text.pack()

# 选项菜单和标签
tk.Label(root, text="选择选项:").pack()
option_var = tk.StringVar(root)
option_var.set("TaskCreate")  # 默认值
options = ["TaskCreate", "TaskExec", "TaskDele"]
option_menu = tk.OptionMenu(root, option_var, *options)
option_menu.pack()

# 绑定选项菜单变化事件
option_var.trace("w", update_default_text)

# 提交按钮
submit_button = tk.Button(root, text="提交", command=send_request)
submit_button.pack()

# 返回结果标签和文本框
tk.Label(root, text="返回结果:").pack()
result_text = tk.Text(root, height=10, width=50)
result_text.pack()

# 运行主循环
root.mainloop()

