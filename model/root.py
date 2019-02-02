import os
import tkinter
import json
import traceback
import tkinter.messagebox

root = tkinter.Tk()

from .defaults import (
    DEFAULTS_TITLE,
    DEFAULTS_NAME,
)

'''
#20190117
    # 1 边框大小位置
    # 2 需要的配置数据
    # 初步定下下面的数据结构
    {
        title:title
        size:'600x600+200+200'
        setting:{
            tabname1:{setting}
            tabname2:{setting}
            tabname3:{setting}
        }
        focus:focus
    }
    关于 setting的数据结构
    {
        type:request # 这里要有多种类型的配置，为了方便处理保存和恢复选择用的函数
        setting:{
            nb_setting:{
                tabname:{setting:..., window_type:...}
                tabname:{setting:..., window_type:...}
                tabname:{setting:..., window_type:...}
            }
        }
    }
'''

# 默认的数据结构
config = {
    'title':DEFAULTS_TITLE,
    'size':'600x600+200+200',
    'setting':{
        'nb_setting':{},
    },
    'focus':None,
}

# 用来配置一些需要持久化的配置
def get_config_from_homepath():
    global config
    defaults_conf = config.copy()
    try:
        home = os.environ.get('HOME')
        home = home if home else os.environ.get('HOMEDRIVE') + os.environ.get('HOMEPATH')
        configfile = os.path.join(home,DEFAULTS_NAME)
        if os.path.exists(configfile):
            with open(configfile,encoding='utf-8') as f:
                defaults_conf = json.load(f)
                config = defaults_conf
    except:
        print('unlocal homepath.')
        traceback.print_exc()

# 用来持久化当前配置的情况，简单的快照，便于使用
def set_config_from_homepath():
    global config
    defaults_conf = config
    try:
        home = os.environ.get('HOME')
        home = home if home else os.environ.get('HOMEDRIVE') + os.environ.get('HOMEPATH')
        configfile = os.path.join(home,DEFAULTS_NAME)
        with open(configfile,'w',encoding='utf-8') as f:
            f.write(json.dumps(defaults_conf,indent=4))
    except:
        print('unlocal homepath.')
        traceback.print_exc()

# 装饰器，让被装饰函数在执行后进行配置保存的操作
# 也可以是直接使用的函数，默认不写参数则直接进行配置保存的操作
def save(func=None):
    from .tab import notebook_save
    if func is None:
        toggle = tkinter.messagebox.askokcancel('是否保存','确定保存当前全部配置信息吗？')
        if toggle:
            notebook_save(curr_1_or_all_2=2) # 主动保存将保存全部
            set_config_from_homepath()
    else:
        def _save(*a,**kw):
            notebook_save(curr_1_or_all_2=1) # 被动保存将只保存当前tab信息
            v = func(*a,**kw)
            set_config_from_homepath()
            return v
        return _save

# 绑定窗口位置大小信息与全局参数 config 的联系
def bing_change_window_siz():
    def change_siz():
        config['size'] = '{}x{}+{}+{}'.format(
            root.winfo_width(),
            root.winfo_height(),
            root.winfo_x(),
            root.winfo_y(), )
    root.bind('<Configure>',lambda e:change_siz())

# 初始化窗口设置
def init_window_from_config():
    root.title(config['title'])
    root.geometry(config['size'])
    from .tab import nb, create_new_tab
    from .frame import frame_setting, type_descript, helper_window
    fr_funcs = frame_setting['window_all_types']
    # 恢复tab配置的快照处理
    it = config['setting']['nb_setting'].items()
    if it:
        focus = None
        for tabname,setting in it:
            if tabname != config['focus']:
                in_sett = setting['setting']
                winname = setting['window']
                window = type_descript(fr_funcs[winname])
                create_new_tab(window,in_sett,tabname)
            else:
                focus = tabname,setting
        if focus:
            tabname,setting = focus # 保存tab焦点
            in_sett = setting['setting']
            winname = setting['window']
            window = type_descript(fr_funcs[winname])
            create_new_tab(window,in_sett,tabname)
    else:
        create_new_tab(helper_window,prefix='帮助')


get_config_from_homepath() # 加载持久化配置到config参数
init_window_from_config() # 通过config参数初始化窗口（包括size）
bing_change_window_siz() # size的绑定要在size的初始化之后
