import re
import tkinter
from tkinter import ttk
from tkinter.simpledialog import askstring

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
            'tabname':tab_name1,
            'setting':setting1,
            'window_setting':window_setting1,
            'window_creater':window_creater1,
        }, 
    tab_id2:
        {
            'tabname':tab_name2,
            'setting':setting2,
            'window_setting':window_setting2,
            'window_creater':window_creater2,
        }, 
}
setting 是一个字典
window_setting 是被创建窗口的内部控件内容，用于事件执行时定位控件
window_creater 是创建窗口 Frame 的函数
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
        nb_names[tab_id]['tabname'] = name
        nb_names[tab_id]['setting'] = setting
        fr_set = frame_setting.pop(frame)
        nb_names[tab_id]['snapshot_get']   = fr_set.pop('snapshot_get')
        nb_names[tab_id]['window_type']    = fr_set.pop('window_type')
        nb_names[tab_id]['window_setting'] = fr_set
        nb_names[tab_id]['window_creater'] = window
        nb_names[tab_id]['window_frame']   = frame
        return tab_id
    nums = []
    for val in nb_names.values():
        v = re.findall(r'{}\d+'.format(prefix), val['tabname'])
        if val['tabname'] == prefix:
            nums.append(0)
        if v:
            num = int(re.findall(r'{}(\d+)'.format(prefix), v[0])[0])
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

def get_cur_frame():
    _select = nb.select()
    return nb_names[_select]['window_frame']

# 获取当前标签和 frame_setting
def get_cur_name_setting():
    _select = nb.select()
    name    = nb_names[_select]['tabname']
    setting = nb_names[_select]['snapshot_get']()
    winname = nb_names[_select]['window_type']
    # 这里的setting 目前并没有进行实时数据的获取，
    # 所以本质上这里的setting 在没有实时获取的方法下是永远 None的
    # 考虑到存在不需要setting 开启的窗口，所以……
    # 或许可以根据window_setting 是否存在一个获取快照的函数进行获取
    # 并且如果数据的初始化和配置都放在Frame 里面或许也会更加方便一些
    return _select, name, setting, winname

# 修改标签的名字
def change_tab_name():
    cname = askstring('修改标签','新的标签名字') # 简单弹窗请求字符串数据
    if cname and cname.strip():
        tab_id,oname,_,_ = get_cur_name_setting()
        allname = [val['tabname'] for val in nb_names.values()]
        while True:
            if cname in allname:
                cname = askstring('修改标签',
                                  '新的标签名字不能与旧标签重复',
                                  initialvalue=cname)
                if not cname or not cname.strip():
                    return
            else:
                break
        # name不能重复，因为需要作为字典的key持久化
        nb_names[tab_id]['tabname'] = cname
        nb.tab(tab_id,text=cname)

delete_list = []
# 删除当前标签，保留最后退出标签是帮助标签
def delete_curr_tab():
    tab_id,cname,_,_ = get_cur_name_setting()
    if tab_id is not '':
        if len(nb.tabs()) == 1 and cname == '帮助':
            root.quit()
        elif len(nb.tabs()) == 1:
            nb.forget(tab_id)
            create_new_tab(helper_window, prefix='帮助')
        else:
            nb.forget(tab_id)
        delete_list.append(nb_names.pop(tab_id))

# 撤销删除标签的功能
def undelete_tab():
    if delete_list:
        d = delete_list.pop()
        tabname = d['tabname']
        setting = d['snapshot_get']()
        window_creater = d['window_creater']
        allname = [val['tabname'] for val in nb_names.values()]
        if tabname not in allname:
            create_new_tab(window_creater, setting, tabname)


def notebook_save(curr_1_or_all_2=1):
    def nb_save_single(tabname,setting,winname):
        d = {}
        d['setting'] = setting
        d['window']  = winname
        config['setting']['nb_setting'][tabname] = d
    _,tabname,setting,winname = get_cur_name_setting()
    config['focus'] = tabname
    if curr_1_or_all_2 == 1:
        nb_save_single(tabname,setting,winname)
    elif curr_1_or_all_2 == 2:
        config['setting']['nb_setting'] = {}
        for tab_id,sett in nb_names.items():
            nb_save_single(
                sett['tabname'],
                sett['snapshot_get'](),
                sett['window_type']
            )
            