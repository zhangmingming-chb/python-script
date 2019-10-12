#安装外部依赖库 pip install baidu-aip
#脚本文件要和“图片”文件夹在同一个目录
#将需要录入的选择题图片放入“图片”文件夹后执行脚本
#录入完成后题目保存的文件为"识别结果.txt"
#百度AI平台 http://ai.baidu.com/
import os
from aip import AipOcr
def collect(img_dress):
    global sum
    try:
        cilent=AipOcr(appId="16678637",secretKey="4E4kUEyQvqnRqWTccPfjFWDspuXIyrga",apiKey="2UsI44XqxiquPPjxtHENUPgk")
        with open(img_dress,"rb") as f:
            image=f.read()
        print('文件:'+img_dress+' 开始录入...还剩:'+str(sum-1)+'张',end='')
        data=cilent.basicAccurate(image)
        for i in range(len(data['words_result'])):
            line=data['words_result'][i]['words']
            with open('识别数据.txt','a') as f:
                f.write(line.replace('□','').replace('⊙','').replace('●','')+'\n')
                if i == len(data['words_result'])-1:
                    f.write('来源:'+img_dress)
                    f.write('\n----------------------\n')
        print(' [+]录入成功！')
    except Exception as e:
        print(e)

all_imgname_list=os.listdir('图片')
print(all_imgname_list)
sum = len(all_imgname_list)
print('图片总数:' + str(len(all_imgname_list)))
for oneimg_name in all_imgname_list:
    collect('图片\\'+oneimg_name)
    sum-=1
print('----------------全部识别录入任务已完成！----------------')
