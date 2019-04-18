import traceback

import tkinter
from tkinter import ttk
from tkinter import scrolledtext
from tkinter.font import Font

from .defaults import DEFAULTS_HELP
from .combinekey import (
    bind_alt_key_fr,
    bind_ctl_key_fr,
)

Text        = scrolledtext.ScrolledText
Label       = ttk.Label
Button      = ttk.Button
Combobox    = ttk.Combobox
Frame       = tkinter.Frame
PanedWindow = ttk.Panedwindow

frame_setting = {'window_all_types':{}}

def type_descript(window):
    frame_setting['window_all_types'][window.__name__] = window
    def _(setting):
        fr = window(setting)
        if fr not in frame_setting:
            frame_setting[fr] = {}
        frame_setting[fr]['window_type'] = window.__name__
        if 'snapshot_get' not in frame_setting[fr]:
            frame_setting[fr]['snapshot_get'] = lambda:None
        if 'snapshot_set' in frame_setting[fr]:
            if setting is not None:
                frame_setting[fr]['snapshot_set'](setting)
        return fr
    return _


@type_descript
def test_window(setting):
    # 测试可被拉伸的内部窗口
    fr = Frame()
    fr.rowconfigure(0,weight=1)
    fr.columnconfigure(0,weight=1)

    pane = PanedWindow(fr,orient=tkinter.HORIZONTAL)
    tempfr1 = Frame(pane,width=12,height=123)
    tempfr2 = Frame(pane,width=12,height=123)

    tx1 = Text(tempfr1)# 这里使用的长宽都是以字符的长宽来定的，注意
    tx2 = Text(tempfr2)
    tx1.pack(fill=tkinter.BOTH,expand=True)
    tx2.pack(fill=tkinter.BOTH,expand=True)
    tempfr1.pack(fill=tkinter.BOTH,expand=True)
    tempfr2.pack(fill=tkinter.BOTH,expand=True)
    pane.add(tempfr1,weight=1)
    pane.add(tempfr2,weight=1)
    pane.pack(fill=tkinter.BOTH,expand=True)
    #tx1['width'] = 10#通过 [] 来修改原本的参数
    #tx1['width'],tx1['height'] 一个默认的Text的w和h为字符长款的 w:80, h:24
    # 不过对于目前的窗口并不能做到动态获取窗口信息，很难受。


    # ===== 一个tab窗口的开发扩展 ======
    # 如果需要让这个tab窗口能够存储当前快照信息的话（方便用户恢复使用状态）
    # 那么就需要通过下面的方式来实现那些窗口信息需要存储
    # 1 需要实现一个 snapshot_get() 函数来处理快照信息的获取
    #   并且这也是提供给功能函数使用的一个接口，方便功能函数的开发
    # 2 需要实现一个 snapshot_set(setting) 函数来处理快照信息的初始化
    # 3 注意：需要在定义两个函数的后面加上几句固定的代码
    # frame_setting[fr] = {}
    # frame_setting[fr]['snapshot_get'] = snapshot_get
    # frame_setting[fr]['snapshot_set'] = snapshot_set
    # 使用setting 初始化
    def snapshot_set(setting):
        tx1.delete(0.,tkinter.END)
        tx1.insert(0.,setting.get('tx1'))
        tx2.delete(0.,tkinter.END)
        tx2.insert(0.,setting.get('tx2'))
    # 获取快照setting
    def snapshot_get():
        return {
            'tx1':tx1.get(0.,tkinter.END),
            'tx2':tx2.get(0.,tkinter.END),
        }

    # 被绑定的键盘操作函数
    def bind_func(): 
        tx2.insert(0.,'12312312312')

    bind_alt_key_fr(bind_func,  'd') 
    # 绑定 ctl+d 功能键，不同frame的功能键重复无所谓，但是需要保证不与全局功能键重复
    # 使用该绑定函数需要非常注意
    # 因为该函数使用了函数栈寻址功能自动寻找fr，所以需要严格保证：
    # 1/ 首先需要 fr = Frame() 必然存在
    # 2/ 其次就是在该函数环境中能够找到 fr 这个变量，经量放在与fr同级的环境里即可
    # 3/ 该函数有局限性，只能操作本窗口内的数据变化，主要就是这样
    # 虽然局限性很大，但是在窗口内的操作直接就能绑定，就很方便

    frame_setting[fr] = {}
    frame_setting[fr]['snapshot_get']  = snapshot_get
    frame_setting[fr]['snapshot_set']  = snapshot_set

    return fr


# 创建tab窗口需要注意的地方
# 每个创建的窗口需要返回一个 Frame 对象
# 每个创建窗口的函数都需要通过装饰器 type_descript 进行装饰
# 如果有需要考虑窗口快照存储就按照示例上的快照写法进行处理即可


# 帮助文档
@type_descript
def helper_window(setting):
    fr = Frame()
    ft = Font(family='Consolas',size=10)
    hp = DEFAULTS_HELP
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