import os
import tkinter
import json
import traceback
root = tkinter.Tk()

# 以“英文句号+文档名字”作为配置文件的名字，这样方便后续改文档名字就直接能用
DEFAULTS_TITLE = os.path.split(os.path.split(__file__)[0])[1]
DEFAULTS_NAME = '.{}'.format(DEFAULTS_TITLE)

'''
#20190117
    # 1 边框大小位置
    # 2 需要的配置数据
    # 初步定下下面的数据结构
    {
        siz:'500x300'
        set:{
            tab_name1:{setting}
            tab_name2:{setting}
            tab_name3:{setting}
        }
    }
    关于 setting的数据结构
    {
        type:request # 这里要有多种类型的配置，为了方便处理保存和恢复选择用的函数
        set:{
            # 不同类型的配置结构不一样
            # 以 request为例，
            method: GET/POST/...
            url: url
            headers: headers
            body: body
            # 也有帮助标签
        }
    }
'''

# 默认的数据结构
config = {
    'title':DEFAULTS_TITLE,
    'size':'600x600+200+200',
    'set':{},
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
def save(func):
    def _save(*a,**kw):
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

# 加载配置参数到全局参数 config 中，如没有，则使用默认配置
get_config_from_homepath()
bing_change_window_siz()