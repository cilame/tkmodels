import types
import tkinter
import inspect

from .root import root

# 考虑全局绑定的影响，在开发过程中
# 对部分窗口实现的绑定函数需要强制与全局区分开
root_bind_keys = set()
frame_bind_keys = set()

# 全局绑定的各种参数和功能。
# ctrl+key 绑定
def bind_ctl_key(func, key=None, shift=False):
    _bind_key(func, key, shift, 'ctl')

# alt+key 绑定
def bind_alt_key(func, key=None, shift=False):
    _bind_key(func, key, shift, 'alt')

def _bind_key(func, key, shift, cls):
    if not isinstance(func, types.FunctionType):
        raise TypeError('{} must be a FunctionType.'.format(str(func)))
    key = key.upper() if shift else key
    if cls == 'ctl': cbk = "<Control-{}>".format(key)
    if cls == 'alt': cbk = "<Alt-{}>".format(key)
    if cbk in frame_bind_keys:
        raise KeyError('window frame bind key must not in root combinekey.{}'.format(cbk))
    if cbk in root_bind_keys:
        raise KeyError('root bind key is duplicated.{}'.format(cbk))
    root_bind_keys.add(cbk)
    root.bind(cbk,lambda e:func())


# 非跨窗口的快捷键绑定操作，针对单个frame的快捷键绑定
# 只能在 窗口创建函数里面才能使用。
def bind_ctl_key_fr(func, key=None, shift=False):
    _bind_key_fr(func, key, shift, 'ctl')

def bind_alt_key_fr(func, key=None, shift=False):
    _bind_key_fr(func, key, shift, 'alt')

# 因为一些原因 frame 在当前框架不能直接绑定键盘操作
# 所以就借助一些其他方法来实现 frame 绑定操作
frame_bind_keys_func = {}
frame_type = type(tkinter.Frame())
def _bind_key_fr(func, key, shift, cls):
    from .tab import get_cur_frame
    if not isinstance(func, types.FunctionType):
        raise TypeError('{} must be a FunctionType.'.format(str(func)))
    key = key.upper() if shift else key
    if cls == 'ctl': cbk = "<Control-{}>".format(key)
    if cls == 'alt': cbk = "<Alt-{}>".format(key)
    frame_bind_keys.add(cbk)
    if cbk in root_bind_keys:
        raise KeyError('window frame bind key must not in root combinekey.{}'.format(cbk))
    frame = None
    for i in inspect.stack():
        if 'fr' in i[0].f_locals and type(i[0].f_locals['fr']) == frame_type:
            frame = i[0].f_locals['fr']
    if frame is None:
        raise KeyError('unfind frame object. pls use this func in window_creater func.')
    frame_bind_keys_func[frame] = func
    def bind_func(e):
        curr_frame = get_cur_frame()
        if curr_frame in frame_bind_keys_func:
            frame_bind_keys_func[curr_frame]()
        else:
            print('no bind func.{}'.format(cbk))
    root.bind(cbk,bind_func)


# 右键菜单绑定
menu = tkinter.Menu(root, tearoff=0)
def bind_menu(func, name=None):
    if not isinstance(func, types.FunctionType):
        raise TypeError('{} must be a FunctionType.'.format(str(func)))
    labelname = name if name is not None else func.__name__
    menu.add_command(label=labelname, command=func)
    root.bind("<Button-3>",lambda e:menu.post(e.x_root,e.y_root))
