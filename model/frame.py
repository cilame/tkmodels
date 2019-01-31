import traceback

import tkinter
from tkinter import ttk
from tkinter import scrolledtext
from tkinter.font import Font

Text        = scrolledtext.ScrolledText
Label       = ttk.Label
Button      = ttk.Button
Combobox    = ttk.Combobox
Frame       = tkinter.Frame
PanedWindow = ttk.Panedwindow

frame_setting = {}

def type_descript(window):
    def _(setting):
        fr = window(setting)
        if fr not in frame_setting:
            frame_setting[fr] = {}
        frame_setting[fr]['window_type'] = window.__name__
        return fr
    return _


@type_descript
def test_window(setting):
    # 测试可被拉伸的内部窗口
    fr = Frame()
    fr.rowconfigure(0,weight=1)
    fr.columnconfigure(0,weight=1)

    pane = PanedWindow(fr,orient=tkinter.HORIZONTAL)
    tempfr1 = Frame(pane)
    tempfr2 = Frame(pane)
    tempfr1.grid(row=0,column=0,sticky=tkinter.NSEW)
    tempfr2.grid(row=0,column=0,sticky=tkinter.NSEW)
    tx1 = Text(tempfr1)
    tx2 = Text(tempfr2)
    tx1.pack(fill=tkinter.BOTH,expand=True)
    tx2.pack(fill=tkinter.BOTH,expand=True)
    pane.add(tempfr1,weight=4)
    pane.add(tempfr2,weight=1)
    pane.grid(row=0,column=0,sticky=tkinter.NSEW)

    # 将控件的地址回传的一种方法，
    # 在使用tab创建窗口的时候会默认将这里传入 frame_setting 的参数
    # pop 给全局参数 nb_names 里面，方便于处理控件调度
    frame_setting[fr] = {}
    frame_setting[fr]['test'] = tx1

    return fr


# 1
# 对于每个窗口的设计都需要考虑数据的初始化，
# 每个创建窗口的函数参数都需要一个初始化参数 setting
# 主要是方便扩展恢复状态的功能
# 2
# 对于每个窗口都只需要一个空master的 Frame() 来存放内容
# 直接修饰完 frame 之后直接返回这个 frame 实例即可
# 在其他地方会修改这个实例的绑定对象让其绑定到 tab 上去
# 3
# 对于每个窗口的控件地址可以以示例的方式传到
# 全局参数 nb_names 里面，绑定窗口的 tab_id
# 这样的好处就是方便通过 tab_id 来处理窗口的内容
# 也方便对各种类型的窗口内容进行调度
# 4
# 对于每个窗口创建函数都需要加 type_descript 装饰器
# 因为为了后续对于不同类型窗口进行不同的类型的处理




# 帮助文档
def helper_window(setting):
    fr = Frame()
    ft = Font(family='Consolas',size=10)
    hp = '''
简单的文档扩展
'''
    temp_fr1 = Frame(fr)
    lb1 = ttk.Label(temp_fr1,font=ft,text=hp)
    lb1.pack()
    temp_fr1.pack()
    return fr

if __name__ == '__main__':
    root = tkinter.Tk()
    winf = test_window()
    winf.master = root
    winf.pack()
    root.mainloop()