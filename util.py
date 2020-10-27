from os import listdir, path, getcwd, remove
import tkinter as tk
from tkinter import ttk
from cryptography.fernet import Fernet

class ScrollableFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        canvas = tk.Canvas(self)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
class io:
    def __init__(self,file):
        self.file = file
        return
    def writeFile(self,content):
        b = open(self.file,'wb')
        b.write(content)
        b.close()
        return
    def readFile(self):
        b = open(self.file,'rb')
        buff = b.read()
        b.close()
        return buff

class Encrypt:
    def __init__(self):
        return
    def encrypt(self,key,text):
        f = Fernet(key)
        encrypted = f.encrypt(text)
        return encrypted
    def decrypt(self,key,text):
        f = Fernet(key)
        y = f.decrypt(text)
        return y
    def generateKey(self):
        return Fernet.generate_key()        
class Note():    
    def __init__(self):
        self.path = path.join(getcwd(),"Notes")
        f = open('n.p','rb')
        self.key = f.read()
        f.close()
        self.e = Encrypt()
        return
    def save(self,title,message):
        p = path.join(self.path,title)
        x = io(p)
        message = self.e.encrypt(self.key,message.encode())
        x.writeFile(message)        
        return
    def read(self,title=None):
        p = path.join(self.path,title)
        x = io(p)       
        m = x.readFile()
        m = self.e.decrypt(self.key,m)
        m = m.decode()
        return m
    def browse(self):
        files = listdir(self.path)        
        return files
    def fileExist(self,title):
        return  path.isfile(path.join(self.path,title))
    def remove(self,title):
        if self.fileExist(title):
            remove(path.join(self.path,title))

class FileOps:
    def __init__(self):
        return
    def encryptFile(self,key,fpath,fpath2):
        i = io(fpath)
        e = Encrypt()
        t = e.encrypt(key,i.readFile())
        title = path.basename(fpath)
        fpath2 = path.join(fpath2,title+'.monocrypt')
        i = io(fpath2)
        i.writeFile(t)        
        return
    def decryptFile(self,key,fpath,tpath):
        i = io(fpath)
        title = path.basename(fpath).rsplit('.',1)[0]
        e = Encrypt()
        t = e.decrypt(key,i.readFile())
        p = path.join(tpath,title)
        i = io(p)
        i.writeFile(t)
        return