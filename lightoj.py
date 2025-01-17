# -*- coding: utf-8 -*-
"""
Created on Mon Feb  11 19:01:25 2020

@author: SSohan
"""
import sys 
import requests
import pickle
import os
import urllib
from bs4 import BeautifulSoup





def download(fname):
   print('File not downloaded. Downloading....')
   url = 'http://lightoj.com/volume_showproblem.php?problem='+fname[:-4]+\
      '&language=english&type=pdf'
   try:
      urllib.request.urlretrieve(url,'problems/'+fname)
      print('download complete')
   except:
      pass


def problem(fname):
   if not os.path.exists('problems'):
      os.mkdir('problems')
      
   try:
      os.startfile('problems\\'+fname)
   except:
      download(fname)
      try:
         os.startfile('problems\\'+fname)
      except:
         print('File not available rightnow')
      

def sub_list(ln):
   cookie()
   source_code = requests.get('http://lightoj.com/volume_usersubmissions.php').text
   soup = BeautifulSoup(source_code,features="lxml")
   table = soup.find('table',id = "mytable3")
   print(soup)
   td = table.find_all('td')
   data = [i.text for i in td]
#   need to fix little bit.. with selenium web
   
   

def login(u,p):
   username = u
   password = p
   s = requests.Session()
   login_data =  {'myrem':'1', 'myuserid':username, 'mypassword':password}
   s.post('http://lightoj.com/login_check.php', login_data)
   
   with open('cookie', 'wb') as f:
      pickle.dump(s.cookies, f)
   
   return s
   
   
def zipdown():
   pass
   
   
def err(ln,lx):
   if ln != lx:
         sys.exit('Wrong command format!! for help use " lightoj \
                  --help"')

def chk(x):
   try:
      x = int(x)
      if(x<1000 or x>1434):
         raise Exception
   except:
      sys.exit("please select problem between 1000-1434")

def cookie():
   s = requests.Session()
   try:
      with open('cookie', 'rb') as f:
         s.cookies.update(pickle.load(f))
         r2 = s.get('http://lightoj.com/')
         if len(r2.content)<500 :
            raise Exception
   except:
      sys.exit('you need to login. For more "lightoj --help"')
   return s


def submit(s,idd,fname,xx):
   xx = xx[-1:]
   if xx=='c':
      xx = 'C'
   elif xx == 'a':
      xx = 'JAVA'
   elif xx=='p':
      xx = 'C++'
   else:
      sys.exit("Can't Identify Programming Language")
   try:
      with open(fname,'rb') as f:
         filedata = f.read()
   except:
      sys.exit('File not found!!')
      
   data = {'sub_problem':idd,'language':xx,'code':filedata,'submit':'Submit'}
   s.post('http://lightoj.com/volume_submit.php',data)
   
   
if __name__ == "__main__":
   print(sys.argv)
   ln = len(sys.argv)
   s = requests.Session()
   
   #default directory
   dr = 'solutions\\'
   if not os.path.exists('solutions'):
      os.mkdir('solutions')
      
   if sys.argv[1] == '-l':
      err(ln,4)
      s = login(sys.argv[2],sys.argv[3])
      r2 = s.get('http://lightoj.com/')
      if len(r2.content)<500 :
         print('wrong username or password!!')
      else:
         print('Login successful!')
   elif sys.argv[1]=='-o':
      err(ln,3)
      chk(sys.argv[2])
      problem(sys.argv[2]+'.PDF')
   elif sys.argv[1]=='-f':
      err(ln,3)
      chk(sys.argv[2])
      download(sys.argv[2]+'.PDF')
      problem(sys.argv[2]+'.PDF')
   elif sys.argv[1]=='-a':
      err(ln,2)
      zipdown()
   elif sys.argv[1]=='-s':
      err(ln,4)
      chk(sys.argv[2])
      s = cookie()
      submit(s,sys.argv[2],dr+sys.argv[3],sys.argv[3])
      sub_list(1)
   elif sys.argv[1]=='-sub':
      sub_list(10)
      
      
   
   
