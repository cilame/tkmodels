import re
import tkinter
from tkinter import ttk

from .root import (
    root,
    config,
    save,
)
from .frame import frame_setting,helper_window

nb = ttk.Notebook(root)
nb.place(relx=0, rely=0, relwidth=1, relheight=1)
nb_names = {} 
'''
nb_names 的数据结构：
{
    tab_id1: 
        {
            'name':tab_name1,
            'setting':setting1,
        }, 
    tab_id2:
        {
            'name':tab_name2,
            'setting':setting2,
        }, 
}
setting 是一个字典，里面至少有一个 type字段描述什么类型。
'''

# 创建窗口，处理frame的数据传递，处理重名
def create_new_tab(window=None,setting=None,prefix='窗口'):
    def bind_frame(frame, name=None):
        frame.master = nb
        name = name if name is not None else frame._name
        v = set(nb.tabs())
        nb.add(frame, text=name)
        tab_id = (set(nb.tabs())^v).pop() # 由于没有接口，只能用这种方式来获取新增的 tab_id
        nb_names[tab_id] = {}
        nb_names[tab_id]['name'] = name
        nb_names[tab_id]['setting'] = frame_setting.pop(frame) if frame in frame_setting else {}
        return tab_id
    nums = []
    for val in nb_names.values():
        v = re.findall('{}\d+'.format(prefix), val['name'])
        if val['name'] == prefix:
            nums.append(0)
        if v:
            num = int(re.findall('{}(\d+)'.format(prefix), v[0])[0])
            nums.append(num)
    idx = 0
    while True:
        if idx in nums:
            idx += 1
        else:
            retn = idx
            break
    name = '{}{}'.format(prefix, '' if retn==0 else retn)
    winf = window(setting)
    nb.select(bind_frame(winf,name))
    return winf

# 获取当前标签和 frame_setting
def get_cur_name_setting():
    _select = nb.select()
    name    = nb_names[_select]['name']
    setting = nb_names[_select]['setting']
    return _select, name, setting









# 删除当前标签，保留最后退出标签是帮助标签
def delete_curr_tab():
    tab_id,name,setting = get_cur_name_setting()
    if tab_id is not '':
        if len(nb.tabs()) == 1 and cname == '帮助':
            root.quit()
        elif len(nb.tabs()) == 1:
            nb.forget(tab_id)
            create_new_tab(helper_window,prefix='帮助')
        else:
            nb.forget(tab_id)