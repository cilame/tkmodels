
from .root import (
    root,
    config,
    save,
)
from .combinekey import (
    bind_ctl_key,
    bind_alt_key,
    bind_menu,
)
from .tab import (
    delete_curr_tab,
    undelete_tab,
    change_tab_name,
)


# 测试用，对于创建 tab 窗口的所有 Frame
# 最最关键的函数就是 create_new_tab
from .tab import create_new_tab
from .frame import test_window,helper_window
a = lambda :create_new_tab(test_window,prefix='测试用窗口')
b = lambda :create_new_tab(helper_window,prefix='测试帮助窗口')
bind_alt_key(a, 'a')
bind_alt_key(b, 'b')
bind_menu(a, '测试1')
bind_menu(b, '测试2')



bind_ctl_key(delete_curr_tab, 'w')
bind_ctl_key(undelete_tab, 'w', shift=True)
bind_ctl_key(change_tab_name, 'e')
bind_ctl_key(save, 's')





# 测试
# from .tab import notebook_save
# notebook_save()
# print(config)




root.mainloop()