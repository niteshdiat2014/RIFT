import os,sys
import subprocess
from commands import *
import time
import hashlib
from shutil import make_archive
import shutil
import datetime
import argparse

DestinationFolder=''
def extfiles(DirName,fileaccess,fname1):
    dirs=["/root/","/etc/default/","/etc/network/", "/var/log/", "/etc/wpa_supplicant/",
          "/etc/rc.locale","/proc/buddyinfo","/proc/cmdline","/proc/cpuinfo","/proc/filesystems","/proc/meminfo","/proc/uptime",
          "/proc/stat","/proc/diskstats","/home/"]
    f1=open(fname1,'wa')
    filenotaccessed=open(fileaccess,'wa')
    filenotaccessed.write('File name and path'+','+'File Exists'+','+'Access Permission'+'\n')
    f1.write('File name and path'+','+'Hash Value'+','+'Evidence Capture Time'+','+'Last Access Time'+','+'Last Modified Time'+','+'Last Time'+','+'File Size in Bytes'+'\n')
    for i in dirs:
        f1.write(i+"\n")
        accesspermission = os.access(i,os.R_OK)
        fileverification =  os.path.isfile(i)
        dirverification =  os.path.isdir(i)
        if fileverification:
            if accesspermission:
                internaldir = i
                internaldir=internaldir.rsplit('/',1)[0]
                internaldir = DirName+internaldir
                if not os.path.exists(internaldir):
                    os.makedirs(internaldir)
                cmd="cp "+ fname + " " + filepath
                sys.stdout.write('#')
                sys.stdout.flush()
                status,text = getstatusoutput(cmd)
                hashvalue = hashlib.md5(open(fname,'rb').read()).hexdigest()
                lastaccessed = format(datetime.datetime.fromtimestamp(os.stat(fname).st_atime))
                lastmodified = format(datetime.datetime.fromtimestamp(os.stat(fname).st_mtime))
                lastchanged = format(datetime.datetime.fromtimestamp(os.stat(fname).st_ctime))
                size = os.stat(fname).st_size
                f1.write(fname+','+hashvalue+','+time.asctime( time.localtime(time.time()))+','+lastaccessed+','+lastmodified+','+lastchanged+','+str(size)+'\n')
            elif not accesspermission:
                filenotaccessed.write(i+','+str(fileverification)+','+str(accesspermission)+'\n')
        elif dirverification:
            for rt,_, files in os.walk(i):
                internaldir = DirName+rt
                if not os.path.exists(internaldir):
                    os.makedirs(internaldir) 
                for f in files:
                    fname = os.path.join(rt, f)
                    filepath = os.path.join(internaldir,f)
                    cmd="cp "+ fname + " " + filepath 
                    sys.stdout.write('#')
                    sys.stdout.flush()
                    status,text = getstatusoutput(cmd)
                    accesspermission1=os.access(fname,os.R_OK)
                    fileverification1 =  os.path.isfile(fname)
                    if accesspermission1:
                        hashvalue = hashlib.md5(open(fname,'rb').read()).hexdigest()
                    else :
                        hashvalue = '0'
                        filenotaccessed.write(fname+','+str(fileverification1)+','+str(accesspermission1)+'\n')
                    lastaccessed = format(datetime.datetime.fromtimestamp(os.stat(fname).st_atime))
                    lastmodified = format(datetime.datetime.fromtimestamp(os.stat(fname).st_mtime))
                    lastchanged = format(datetime.datetime.fromtimestamp(os.stat(fname).st_ctime))
                    size = os.stat(fname).st_size
                    f1.write(fname+','+hashvalue+','+time.asctime( time.localtime(time.time()))+','+lastaccessed+','+lastmodified+','+lastchanged+','+str(size)+'\n')
    f1.close()
    filenotaccessed.close()
    
def cmndout(DirName,fname1):
    f=open(fname1,'a')
    dirs=["ifconfig", "uname -a", "gpio readall", "netstat -l", "netstat -s","netstat -ie", "netstat --statistics --raw",
          "netstat -r", "netstat -tp", "ps -alt","cat services","vmstat -S M", "cat /proc/cpuinfo" 
          "free -m","ps aux | sort -n", "uptime", "w", "ps -ejH", "ps axhf", "pstree -ahl","dpkg --get-selections",
          "ss -t", "ss -nt", "ss -ltn", "ss -lun", "ss -ltp", "ss -s", "ss -tn -o", "ss -tl -f inet",
          "ss -tl6", "ss -t4 state established", "ss -t4 state time-wait","fdisk -l"]
    for i in dirs:
        filei=i.replace(" ", "")
        filei=filei.replace("|", "")
        filei=filei.replace("/", "")
        fname = filei+'.txt'
        drname=os.path.join(DirName,fname)
        f1=open(drname,'wa')
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

def archiving(DirName):
    tmarchive = tm
    archvname = os.path.expanduser(os.path.join(DestinationFolder,tmarchive))
    sourcedir = DirName
    make_archive(archvname, 'tar', sourcedir)   

def outputdirectory():
    global DestinationFolder
    print "Directory verification started"
    for rt,_, files in os.walk("/media/"):
        sys.stdout.write('#')
        sys.stdout.flush()
        if "RIFT.py" in files:
            DestinationFolder=rt
    if os.path.isdir(DestinationFolder) or os.access(DestinationFolder, os.W_OK):# DestinationFolder!='':
        print "\n Destination directory identification successful \n \n ----------> %s \n" % DestinationFolder
    elif not os.path.isdir(DestinationFolder) or not os.access(DestinationFolder, os.W_OK):
        raise Exception('\n Unable to identify destination directory %s, %s' % (destination, DestinationFolder,)) 
        #sys.exit(" Unable to identify destination directory %s, %s" % (destination, DestinationFolder,))

def main():
    global DestinationFolder
    DestinationDir=''
    FileAccess=''
    tm = time.asctime( time.localtime(time.time()))
    parser = argparse.ArgumentParser(description='Digital forensics toolkit for significant evidence preservation from Raspbian operating system configured on Raspberry-Pi IoT platform')
    parser.add_argument('-d', '--destination', required=False, type=str, default=DestinationFolder,
                        help='Specify output directory or destination path Eg. /media/pi/3894-8F76/')
    #parser.add_argument('-r', '--rootuser', required=False, type=str, default='pi',help='Root user name.\n Default for this tool is pi')
    #parser.add_argument('-p', '--rootpass', required=False, type=str, default='raspberry',help='Root user password.\n Default for this tool is raspberry')
    args = parser.parse_args()
    if not os.path.isdir(args.destination) or not os.access(args.destination, os.W_OK):
        print args.destination
        outputdirectory()      
    	#sys.exit("Unable to write to locate directory %s" % (args.destination,) )
    elif os.path.isdir(args.destination) or os.access(args.destination, os.W_OK):
        DestinationFolder=args.destination
        print "\n Successfully loccated the destination directory\t ----------> %s \n" % DestinationFolder
    else:
        raise Exception('\n Unable to identify destination directory %s, %s' % (destination, DestinationFolder,)) 
        #sys.exit(" Unable to identify destination directory %s, %s" % (destination, DestinationFolder,))
    tm=tm.replace(" ","")
    tm=tm.replace(':', "")
    DestinationDir = os.path.join(DestinationFolder,tm)
    os.mkdir(DestinationDir)
    FileAccess = os.path.join(DestinationDir,'Accessdenied.csv')
    FileName = os.path.join(DestinationDir,'audit.csv')
    extfiles(DestinationDir,FileAccess,FileName)
    cmndout(DestinationDir,FileName)
    archiving(DestinationDir)

if __name__ == "__main__":
    main()
