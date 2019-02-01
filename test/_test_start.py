# 增加环境变量，仅测试使用
import os
import sys
p = os.path.split(os.getcwd())[0]
sys.path.append(p)
import sys
import traceback

print('coding:',sys.stdout.encoding)

for i in os.listdir(p):
    if i != 'test':
        try:
            mainpath = os.path.join(p,i,'main.py')
            if os.path.exists(mainpath):
                exec('from {} import main'.format(i))
        except:
            traceback.print_exc()