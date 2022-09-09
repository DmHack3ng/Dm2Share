import requests
from bs4 import BeautifulSoup
import socket
import subprocess
import re
import optparse
import sys,os
from fastdownload import FastDownload
import urllib

download_path="Download"

def check_options():
   try:
      option=sys.argv[1]
      if option=="-S":
        path=sys.argv[2]
        change_dir(path)
        os.system("python3 -m http.server")
      elif option=="-R":
        dm2share_run()
   except IndexError:
      print("Specifier une options:\n  dm2share.py -S(envoyeur) -R(receveur)")

def get_content(ip):
    rq=requests.get("http://"+ip+":8000")
    soup=BeautifulSoup(rq.content,"html.parser")
    return soup.find_all('a')
def change_dir(dir):
    os.chdir(dir)

def dm2share_run():
    if sys.platform=="win32":
      v=subprocess.getoutput("arp -a")
    else:
      v=subprocess.check_output("arp -a",shell=True).decode()# linux(ubuntu)
    
    #print(v)
    p=re.findall("\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}",v)
    for h in p:
      host=h
      #print(host)
      v=port_scanner(host)
      if v==0:
         html_c=get_content(host)
         beauty_print(host,html_c)

def interactive_shell():
     try:
        num=int(input("[+] Put File Number >> "))
     except Exception:
        interactive_shell()
     return num

def port_scanner(ip,port=8000):
   s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
   socket.setdefaulttimeout(1)

   r=s.connect_ex((ip,port))
   if r == 0:
     print("\nIP: "+ip)
     print("Port: "+str(port))
     return 0
   s.close()


def download_files(url_file):
   d=FastDownload(base=download_path)
   d.download(url_file)

def beauty_print(ip,data):
   print("\t-----------FILES-------------\n")
   nb=0
   # >1 : sup a 1
   # <1 : inf a 1
   if len(data)==1:
       #print("1 seul fichier"+str(len(data)))
       link_f="http://"+ip+":8000"+"/"+data[0].get('href')
       download_files(link_f)
   else:
      #print("plusieurs "+str(len(data)))
      #print(data)
      for a in data:
         name=a.get('href')
         print(str(nb)+"--> "+urllib.parse.unquote(name))
         nb+=1
      print("\n")
      get_link(ip,data)

def get_link(ip,dt):
   nbt=interactive_shell()
   link_f="http://"+ip+":8000"+"/"+urllib.parse.unquote(dt[nbt].get('href'))
   #print(link_f)
   download_files("\n"+link_f)

#dm2share_run()

try:
   check_options()
except KeyboardInterrupt:
   print("\nDetection de Ctrl + C... Fin du Programe")