#!/usr/bin/python  
#encoding:UTF-8
#client

import socket, os, sys  
import time
import threading
import signal

s_addr=('<broadcast>',10000)  

s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)  
s.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1)  

flag=False

def send_message():
    global flag
    s_time=0
    while not flag:
        try:
            if s_time in (0, 2, 6, 12, ):
                s.sendto("hello devil",s_addr) 
            if s_time>15:
                signal.alarm(1)#这里是1秒后提示问题，关闭
                print "\r\n.....................\r\n"
                print "\r\n.....................\r\n"
                print "\r\n.....................\r\n"
                print "\r\n.....................\r\n"
                print "\r\n.....................\r\n"
                sys.exit()
        except:
            signal.alarm(1)#这里是1秒后提示问题，关闭
            sys.exit()
        finally:
            s_time=s_time+1
            time.sleep(1)


def fun(signum, frame):
    global flag
    if flag==False: 
        print "已经超时, 请检查网络联通或者目的主机不在本网段中..."
        print "或者重新联接..."
        print "\r\n正在为你退出该程序， 请稍后...\r\n"
        sys.exit()

def start_message():

    data=None
    addr=None
    global flag

    th=threading.Thread(target=send_message)
    th.start()
    signal.signal(signal.SIGALRM, fun)
    while True:
        try:
            data, addr=s.recvfrom(1024)  
            #若信号中断被成功正确执行，主线程将直接退出
        except:
            #s.recvfrom被信号中断报错, 主线程没有直接退出
            print "... ... ...."
            print "... ... ... ... ... ... ... ... ... ... ... ... ..."#socket被唤醒信号中断
            fun(None, None)
	    #主线程退出

        #s.recvfrom被信号中断直接跳出
        #sys.exit()资源清理，没有成功退出，继续执行
        if data==None or addr==None:
            print "... ... ... ... ... ... ... ... ... ... ... ... ..."#socket被唤醒信号中断,但是没有报异常,也没有退出
            fun(None, None)
	    #主线程退出
#说明:
#第一种情况：中断执行，直接退出
#第二种情况：中断执行，退出失败，SOCKET报异常
#第三种情况：中断执行，退出失败，SOCKET没有报异常




        if data=="devil may cry":  
            flag=True
            time.sleep(1.5)#这里时间大于 提示关闭的1秒时间，保证显示逻辑正确
            #主线程堆栈响应抢占
            print "已经成功找到目的主机，正在连接中，请稍后..."
            print '...'
            return addr
        
if __name__=="__main__":
    while True:
        flag=False
        print ""
        print "============================================================"
        print "本程序为在本网段内自动寻找目标主机，然后实现远程登入管理功能"
        print "如果想要远程登入，   请输入数字  1  "
        print "如果想想退出该程序， 请输入数字  0  "
        print "============================================================"
        print ""

        commond=raw_input('请输入命令： ').strip()
        if commond.isdigit() and int(commond)>=0 and int(commond)<=1:
            print "输入的选项有效"
            print ""
            if int(commond)==1:
                
                addr=start_message()
               
                
                print '请输入目的主机密码:'
                os.system("ssh "+addr[0])
                print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
                print "已经成功退出目标主机， 请稍后..."
                print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
                print ""
                time.sleep(1)
            else:
                print "正在为你退出该程序， 请稍后..."
                time.sleep(1)
                sys.exit()
        else:
            print ""
            print "输入的选项无效, 请重新选择"
            print ""
            time.sleep(1)
