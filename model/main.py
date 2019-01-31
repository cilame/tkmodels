
from .root import (
    root,
    config,
)
from .combinekey import (
    bind_ctl_key,
    bind_alt_key,
    bind_menu,
)


from .tab import create_new_tab
from .frame import test_window,helper_window

create_new_tab(test_window)
create_new_tab(helper_window,prefix='帮助')

root.title(config['title'])
root.geometry(config['size'])
root.mainloop()