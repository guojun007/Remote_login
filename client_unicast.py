#!/usr/bin/python  
#encoding:UTF-8
#client

import socket, os, sys  
import time
import threading
import signal

s_addr=''  
port=10000

ip_list=[]

sss=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)  
sss.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1)  

flag=False

def ip_produce():
    global ip_list

    if not os.access("net.info", os.F_OK):
        print "UDP单播网络配置文件丢失或出错..."
        sys.exit()
    else:
        f=open("net.info", "r")
        message=f.readlines(2)
        s1=message[0].strip().split(".")
        s2=message[1].strip().split(".")
        if len(s1)==4 and len(s2)==4:
            s_1=[]
            s_2=[]
            for i in s1:
                if i.isdigit() and int(i)>=0 and int(i)<=255:
                    s_1.append((bin(int(i))[2:]).zfill(8))
                else:
                    print "UDP单播网络配置文件出错..."
                    sys.exit()
            for i in s2:
                if i.isdigit() and int(i)>=0 and int(i)<=255:
                    s_2.append((bin(int(i))[2:]).zfill(8))
                else:
                    print "UDP单播网络配置文件出错..."
                    sys.exit()
        else:
            print "UDP单播网络配置文件出错..."
            sys.exit()
    s_1="".join(s_1)
    s_2="".join(s_2)

    loc=s_2.rfind("1")+1
    s1=s_1[:loc]
    
    for i in xrange(1, int('1'*(32-loc), 2)):
        s=s1+bin(i)[2:].zfill(32-loc)
        s_addr=str(int(s[:8], 2))+'.'+str(int(s[8:16], 2))+"."+str(int(s[16:24], 2))+"."+str(int(s[24:], 2))
        ip_list.append(s_addr)





def send_message(start, end):

    global sss
    global flag

    s_time=0

    for ip in ip_list[start:end]:
        for i in xrange(5):

            if not flag:
                sss.sendto("hello devil",(ip, port)) 
            else:
                sys.exit()

            time.sleep(0.5)
    


def fun(signum, frame):
    global flag
    if flag == False:
        print "已经超时, 请检查网络联通或者目的主机不在本网段中..."
        print "或者重新联接..."
        print "\r\n正在为你退出该程序， 请稍后...\r\n"
        sys.exit()

def start_message():
    global flag
    global ip_list

    ip_produce()

    if len(ip_list)>100:
        threading_count=100
        i_count=len(ip_list)/100
        j_count=len(ip_list)%100
        
        start=0

        for i in xrange(100):
            if i < j_count:
                threading.Thread(target=send_message, args=(start, start+i_count+1)).start()
                start=start+i_count+1
            else:
                threading.Thread(target=send_message, args=(start, start+i_count)).start()
                start=start+i_count
    else:
        threading_count=len(ip_list)
        for i in xrange(threading_count):
            threading.Thread(target=send_message, args=(i, i+1)).start()

    signal.signal(signal.SIGALRM, fun)
    signal.alarm((i_count+1+ 3 )*2)
    while True:
        try:
            data, addr=sss.recvfrom(1024)  
            #若信号中断被成功执行，将直接退出
        except:
            #sss.recvfrom被信号中断报错
            print "... ... ..."
            print "... ... ... ... ... ... ... ... ... ... ... ... ... ... ..."
            fun(None, None) 

        #sss.recvfrom被信号中断直接退出 
        #sys.exit()资源清理， 没有成功退出，继续执行
        if data==None or addr==None:
            print "... ... ... ... ... ... ... ... ... ... ... ... ... ... ..."
            fun(None, None) 


        if data=="devil may cry":  
            flag=True
            #time.sleep(1.5)#这里时间大于 提示关闭的1秒时间，保证显示逻辑正确
            #主线程发送及接收信号，可以抢占堆栈
            print "已经成功找到目的主机，正在连接中，请稍后..."
            print '...'
            return addr




if __name__ =="__main__":
    while True:
        flag=False
        signal.signal(signal.SIGALRM, lambda x, y:1+1==2) #利用SIGALRM可以覆盖性将上次循环的信号覆盖
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
