import os

# 以“英文句号+文档名字”作为配置文件的名字，这样方便后续改文档名字就直接能用
DEFAULTS_TITLE = os.path.split(os.path.split(__file__)[0])[1]
DEFAULTS_NAME = '.{}'.format(DEFAULTS_TITLE)

DEFAULTS_HELP = '''
简单的帮助文档
'''