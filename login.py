from tkinter import Tk, Entry, Button, LEFT, RIGHT
from hashlib import sha256
from os import getcwd
from os.path import join

class Login(object):
    def __init__(self):
        self.p = ''
        self.s = False
        return
    def isPass(self):
        self.p = self.pas.get()
        x = sha256(self.p.encode() + self.p.encode()).hexdigest()
        path = join(getcwd(),'p.p')
        f = open(path,'r')
        t = f.read()
        f.close()
        if x==t:
            self.s = True
            self.login.quit()
            return True
        self.login.quit()
        return False
    def start(self):        
        self.login = Tk()
        self.login.title('Login')
        self.login.iconbitmap("lock.ico")  

        char = "*" 
        self.pas = Entry(self.login,font=('Arial',20),bg="white", show=char)
        self.pas.pack(side=LEFT)
        
        btn = Button(self.login,text="Login",font=('Arial',18),bg="white",command=self.isPass)
        btn.pack(side=RIGHT)
        self.login.mainloop()

        return self.s