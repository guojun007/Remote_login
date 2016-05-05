#!/usr/bin/python  
#encoding:UTF-8
#server
#本程序为辽宁大学校园网内网目标主机寻找及登入的服务器端
import socket  
import sys
import time
import signal
	
def Daemon_main():

    #关闭事件处理
    def poweroff(signalnum, frame):
        f.write("server over  %s\r\n"%time.ctime())
        f.flush()
        sys.exit()

    host=''  
    port=10000  
    s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)  
    s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)  
    #s.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1)  
    s.bind((host,port))  
    
    with open("/home/devil/公共的/remote_log.log", "a+") as f:
        f.write("server start %s\r\n"%time.ctime())
        f.flush()
        signal.signal(signal.SIGINT, poweroff)#关闭信号捕获
        signal.signal(signal.SIGTERM, poweroff)#关闭信号捕获
        time_server=1 
    
        try:  
    	    while True:  
                data,addr=s.recvfrom(1024)  
	        if data != "hello devil":
		    time.sleep(0.1)#防止有人恶意攻击，规定限制CPU利用率
	            continue
                f.write("%s %s %s\r\n"%(time_server, addr, time.ctime()))
                f.flush()
                s.sendto("devil may cry",addr)  
	        time_server=time_server+1
        except Exception, e:  
	    f.write("server error %s %s\r\n"%(e, time.ctime()))
	    f.flush()
	    sys.exit()

def createDaemon():
  "Funzione che crea un demone per eseguire un determinato programma…"
  import os
  # create - fork 1
  try:
    if os.fork() > 0: os._exit(0) # exit father…
  except OSError, error:
    print 'fork #1 failed: %d (%s)' % (error.errno, error.strerror)
    os._exit(1)
  # it separates the son from the father
  os.chdir('/')
  os.setsid()
  os.umask(0)
  Daemon_main() # function demo

createDaemon()
