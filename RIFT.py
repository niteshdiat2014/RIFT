import os,sys
import subprocess
from commands import *
import time
import hashlib
from shutil import make_archive
import shutil
import datetime

destdir='/media/pi/3894-8F76/'
tm = time.asctime( time.localtime(time.time()))
drname = os.path.join(destdir,tm).replace(" ", "")
drname1 = drname.replace(':', "")
fname1 = os.path.join(drname1,'fls.csv')
def extfiles():
    print "Entered EXTFILES"
    dirs=["/root/", "/home/", "/proc/", "/var/log/", "/etc/"]#, "/var/log/","/etc/"]
    #mkdir=["root","home"]#,"/varlog/","/etc/"]
    os.mkdir(drname1)
    f1=open(fname1,'wa')
    f1.write('File name and path'+','+'Hash Value'+','+'Evidence Capture Time'+','+'Last Access Time'+','+'Last Modified Time'+','+'Last Time'+','+'File Size in Bytes'+'\n')
    for i in dirs:#,j in zip(dirs,mkdir):
        #drname2 = drname1+j#os.path.join(drname1,i)#
        #os.mkdir(drname2)
        f1.write(i+"\n")
        for rt, _, files in os.walk(i):
            internaldir = drname1+rt#os.path.join(drname2,rt)#drname2+rt  
            os.mkdir(internaldir) 
            for f in files:
                fname = os.path.join(rt, f)
                print fname,internaldir,f
                filepath = os.path.join(internaldir,f)
                cmd="cp "+ fname + " " + filepath#internaldir + f
                print 'CMD ---------------', cmd
                status,text = getstatusoutput(cmd)
                hashvalue = hashlib.md5(open(fname,'rb').read()).hexdigest()
                lastaccessed = format(datetime.datetime.fromtimestamp(os.stat(fname).st_atime))
                lastmodified = format(datetime.datetime.fromtimestamp(os.stat(fname).st_mtime))
                lastchanged = format(datetime.datetime.fromtimestamp(os.stat(fname).st_ctime))
                size = os.stat(fname).st_size
                f1.write(fname+','+hashvalue+','+time.asctime( time.localtime(time.time()))+','+lastaccessed+','+lastmodified+','+lastchanged+','+str(size)+'\n')
    f1.close()

def cmndout():
    f=open(fname1,'a')
    dirs=["ifconfig", "uname -a", "gpio readall", "netstat -l", "netstat -s","netstat -ie", "netstat --statistics --raw",
          "netstat -r", "netstat -tp", "ps -alt","cat services","vmstat -S M", "cat /proc/cpuinfo" 
          "free -m","ps aux | sort -n", "uptime", "w", "ps -ejH", "ps axhf", "pstree -ahl"]#"dmidecode -t bios", "dmidecode -t system","dmidecode -t baseboard", "dmidecode -t chassis"
    for i in dirs:
        filei=i.replace(" ", "")
        filei=filei.replace("|", "")
        fname = filei+'.txt'
        drname=os.path.join(drname1,fname)
        f1=open(drname,'wa')
        print drname, fname, i
        status,text = getstatusoutput(i)
        f1.write(text)
        f1.close()
        hashvalue = hashlib.md5(open(drname,'rb').read()).hexdigest()
        lastaccessed = format(datetime.datetime.fromtimestamp(os.stat(drname).st_atime))
        lastmodified = format(datetime.datetime.fromtimestamp(os.stat(drname).st_mtime))
        lastchanged = format(datetime.datetime.fromtimestamp(os.stat(drname).st_ctime))
        size = os.stat(drname).st_size
        f.write(drname+','+hashvalue+','+time.asctime( time.localtime(time.time()))+','+lastaccessed+','+lastmodified+','+lastchanged+','+str(size)+'\n')
    f.close()

def archiving():
    archvname = os.path.expanduser(os.path.join(destdir,'Evidence'))
    sourcedir = drname1
    make_archive(archvname, 'tar', sourcedir)    

def main():
    extfiles()
    cmndout()
    archiving()

if __name__ == "__main__":
    main()
