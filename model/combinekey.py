import types
import tkinter

from .root import root

# ctrl+key 绑定
def bind_ctl_key(func, key=None, shift=False):
    if key is None:
        raise TypeError('{} must be a lowercase.'.format(key))
    if not isinstance(func, types.FunctionType):
        raise TypeError('{} must be a FunctionType.'.format(str(func)))
    key = key.upper() if shift else key
    root.bind("<Control-{}>".format(key),lambda e:func())

# alt+key 绑定
def bind_alt_key(func, key=None, shift=False):
    if key is None:
        raise TypeError('{} must be a lowercase.'.format(key))
    if not isinstance(func, types.FunctionType):
        raise TypeError('{} must be a FunctionType.'.format(str(func)))
    key = key.upper() if shift else key
    root.bind("<Alt-{}>".format(key),lambda e:func())

# 右键菜单绑定
menu = tkinter.Menu(root, tearoff=0)
def bind_menu(func, name=None):
    if not isinstance(func, types.FunctionType):
        raise TypeError('{} must be a FunctionType.'.format(str(func)))
    labelname = name if name is not None else func.__name__
    menu.add_command(label=labelname, command=func)
    root.bind("<Button-3>",lambda e:menu.post(e.x_root,e.y_root))