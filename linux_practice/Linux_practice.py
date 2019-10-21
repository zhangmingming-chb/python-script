import random
import time
import os
number=1
def choose_question():
    with open('linux.txt','r',encoding='gbk') as f:
        command_list=f.read().split('@')
        command_list.remove('')
    question=random.choice(command_list)
    question_cmd=question.split('\n')[0]
    question_content=question.split('\n')[1:]
    question_content.pop()
    # print(question_content)
    print('----------------')
    print('[命令]',question_cmd)
    print('----------------')
    all_question_apart='****************\n'
    for i in range(len(question_content)):
        question_apart='{}.{}'.format(i+1,question_content[i])
        print(question_apart)
        all_question_apart+=question_apart+'\n'
    print('----------------')
    return question_cmd,all_question_apart

def save_record(question_cmd):
    global number
    with open('record.txt', 'a', encoding='gbk') as f:
        quesition_display="""\n\n****************\n题目: {}\n{}----------\n你的回答:\n""".format(question_cmd[0],question_cmd[1])
        f.write(quesition_display)
    while True:
        answer=input('[root@localhost]$ ')
        if answer == 'exit':
            break
        with open('record.txt','a',encoding='gbk') as f:
            f.write('['+str(number)+'] '+answer+'\n')
        number+=1

while True:
    try:
        print('--------Linux命令操作训练系统--------')
        if not os.path.exists('linux.txt'):
            print('[INFO] 检测到题库文件:linux.txt不存在或未放入应用目录')
            time.sleep(5)
            break
        print('*操作规范')
        print('1.创建的文件夹用dir1..n表示')
        print('2.文件名用file1..n表示')
        print('3.命令行题目书写完成后输入exit结束')
        print('----------------------------------')
        print('①开始抽取题目   ②退出')
        switch1=int(input('>>'))
        os.system('cls')
        if switch1 == 1:
            while True:
                save_record(choose_question())
                print('----------------------')
                print('①再来一题 ②返回主菜单')
                switch2= int(input('>>'))
                os.system('cls')
                if switch2 == 1:
                    number=1
                    continue
                elif switch2 == 2:
                    break
                else:
                    print('输入有误！')
                    continue
        elif switch1 == 2:
            print(r'[INFO] 答题记录文件路径:{}\record.txt'.format(os.getcwd()))
            print('[INFO] 系统已退出! 欢迎下次使用！')
            s=5
            while s>=0:
                print('\r{}s后系统将自动关闭...'.format(s),end="")
                time.sleep(1)
                s-=1
            break
        else:
            print('输入有误！')
            continue
    except Exception as e:
        print("错误信息:",e)
