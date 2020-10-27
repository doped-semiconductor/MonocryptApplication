from tkinter import filedialog, messagebox, Text, Button, Frame, Canvas, Scrollbar, OptionMenu, Label, StringVar, Tk
from util import Note, ScrollableFrame, FileOps
from os import path
from login import Login

class Application(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack(padx=20, pady=20) 
        self.config(background='white')         
        self.Note = Note()
        self.noteFiles = self.Note.browse()
        self.browserNav = {}
        self.create_widgets()
        self.encFile = ""
        self.encFileLoc = ""
        self.Key = None

    def noteReader(self,title):
        nt = Note()
        def nt2():
            if nt.fileExist(title):
                content = nt.read(title)
                self.noteEd(title,content)
            else:
                self.noteEd(title+": File not Found","Error :(\nPlease check if file has been deleted")
            return 
        self.browserNav[title] = nt2
        return    

    def clearFrame(self,frame):
        for widget in frame.winfo_children():
            widget.destroy()
    
    def create_widgets(self): 
        self.a = Frame(self,bd=2)
        self.a.pack(side="top")
        self.a.configure(background="white")
        self.menubuttons()      

        self.b = Frame(self)
        self.b.pack(side="top")   
        self.b.configure(background="white")     

        self.left = Frame(self.b,padx=20,pady=10)
        self.left.configure(background="white")
        self.left.pack(side="left",anchor="n")

        self.right = Frame(self.b,padx=20,pady=10)
        self.right.pack(side="right")
        self.right.configure(background="white") 
        self.encBtn()
    
    def menubuttons(self):
        self.note = Button(self.a,text="Notes",command=self.noteFrames,activebackground="green",activeforeground="white",bg="white",font=("Helvetica",18,"bold"),bd=0,height=3,width=15,padx=2,pady=2,fg="green")
        self.note.grid(row=2,column=1)
        
        self.enc = Button(self.a,text="Encrypt",command=self.encBtn,activebackground="green",activeforeground="white",bg="white",font=("Helvetica",18,"bold"),bd=0,height=3,width=15,padx=2,pady=2,fg="gray")
        self.enc.grid(row=2,column=3)

        self.dec = Button(self.a,text="Decrypt",command=self.decBtn,activebackground="green",activeforeground="white",bg="white",font=("Helvetica",18,"bold"),bd=0,height=3,width=15,padx=2,pady=2,fg="gray")
        self.dec.grid(row=2,column=5) 

    def delEd(self):
        title = self.notetitle.get("1.0","end")
        self.Note.remove(title.rstrip())
        self.noteEd("Untitled","Deleted from notes: "+title)
        return

    def noteFrames(self):
        self.enc['fg']="gray"
        self.note['fg']="green"
        self.dec['fg']="gray"

        self.clearFrame(self.left)
        self.clearFrame(self.right)
        self.browse = Button(self.left,text="Browse",command=self.browseBtn,activebackground="green",activeforeground="white",bg="white",font=("Helvetica",12),bd=0,height=2,width=10,padx=2,pady=2,fg="gray",relief="solid")
        self.browse.pack(side="top")

        self.create = Button(self.left,text="Create",command=self.createBtn,highlightbackground="green",activebackground="green",activeforeground="white",bg="white",font=("Helvetica",12),bd=0,height=2,width=10,padx=2,pady=2,fg="gray",relief="solid")
        self.create.pack(side="top")       

        self.browseBtn()

    def clearEdBtn(self):
        self.newnote.delete("1.0","end")

    def saveEdBtn(self):
        title = self.notetitle.get("1.0","end")
        print(title)
        content = self.newnote.get("1.0","end")
        print(content)
        self.Note.save(title.rstrip(),content)
        print("saved")

    def noteEd(self,title,content):
        self.clearFrame(self.right)

        self.notetitle = Text(self.right,width=75,height=1,bd=1,relief="solid",pady=5,padx=3,font=("Helvetica",12,"bold"))
        self.notetitle.insert("1.0",title)
        self.notetitle.pack(side="top")
        
        self.newnote = Text(self.right,width=75,height=20,bd=1,relief="solid",pady=5,padx=3,spacing2=3,font=("Helvetica",12))
        self.newnote.insert("1.0",content)
        self.newnote.pack(side="top")        

        self.addnote = Button(self.right,text="Save",command=self.saveEdBtn,activebackground="green",activeforeground="white",bg="#f8cd0c",relief="flat",font=("Helvetica",12),bd=1,height=2,width=10,padx=2,pady=2,fg="white")
        self.addnote.pack(side="left",anchor="w")

        self.clear = Button(self.right,text="Clear",command=self.clearEdBtn,activebackground="green",activeforeground="white",bg="#f8cd0c",relief="flat",font=("Helvetica",12),bd=1,height=2,width=10,padx=2,pady=2,fg="white")
        self.clear.pack(side="left",anchor="w")

        self.delete = Button(self.right,text="Delete",command=self.delEd,activebackground="green",activeforeground="white",bg="#f8cd0c",relief="flat",font=("Helvetica",12),bd=1,height=2,width=10,padx=2,pady=2,fg="white")
        self.delete.pack(side="right",anchor="w")

        self.back = Button(self.right,text="Back",command=self.browseBtn,activebackground="green",activeforeground="white",bg="#f8cd0c",relief="flat",font=("Helvetica",12),bd=1,height=2,width=10,padx=2,pady=2,fg="white")
        self.back.pack(side="right",anchor="w")

    def createBtn(self):
        self.clearFrame(self.right)

        self.notetitle = Text(self.right,width=75,height=1,bd=1,relief="solid",pady=5,padx=3,font=("Helvetica",12,"bold"))
        self.notetitle.insert("1.0","Untitled")
        self.notetitle.pack(side="top")
        
        self.newnote = Text(self.right,width=75,height=20,bd=1,relief="solid",pady=5,padx=3,spacing2=3,font=("Helvetica",12))
        self.newnote.pack(side="top")

        self.addnote = Button(self.right,text="Save",command=self.saveEdBtn,activebackground="green",activeforeground="white",bg="#f8cd0c",relief="flat",font=("Helvetica",12),bd=1,height=2,width=10,padx=2,pady=2,fg="white")
        self.addnote.pack(side="left",anchor="w")

        self.clear = Button(self.right,text="Clear",command=self.clearEdBtn,activebackground="green",activeforeground="white",bg="#f8cd0c",relief="flat",font=("Helvetica",12),bd=1,height=2,width=10,padx=2,pady=2,fg="white")
        self.clear.pack(side="left",anchor="w")

        self.create['fg'] = 'black'
        self.create['bd'] = 2
        self.browse['fg'] = 'gray'
        self.browse['bd'] = 0
        return
    
    def browseBtn(self):
        self.clearFrame(self.right)
        
        canvas = Canvas(self.right,width=700,height=500,bg="white")
        scroll_y = Scrollbar(self.right, orient="vertical", command=canvas.yview)
        frame = Frame(canvas,width=700,height=500,bg="white")

        self.noteFiles = self.Note.browse()
        for x in self.noteFiles:
            self.noteReader(x)
            temp = Button(frame,text=x,command=self.browserNav[x],activebackground="#5c8066",activeforeground="white",anchor="w",relief="flat",font=("Helvetica",12),padx=5,pady=5,height=2,width=700,bg="#95a69a",fg="white")
            temp.pack(side="top")
            temp2 = Label(frame, bg="white")
            temp2.pack(side="top")            

        canvas.create_window(0, 0, anchor='nw', window=frame)
        canvas.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox('all'),yscrollcommand=scroll_y.set)                    
        canvas.pack(fill='both', expand=True, side='left')
        scroll_y.pack(fill='y', side='right')
            
        self.browse['fg'] = 'black'
        self.browse['bd'] = 2
        self.create['fg'] = 'gray'
        self.create['bd'] = 0
        return    

    def encBtn(self):
        self.enc['fg']="green"
        self.note['fg']="gray"
        self.dec['fg']="gray"
        self.clearFrame(self.left)
        self.clearFrame(self.right)
        self.right2 = Frame(self.right)
        self.right2.pack(side="top")
        self.keyChoice = StringVar(self.right2)
        self.keyChoice.set("Choose Key")
        self.option = OptionMenu(self.left, self.keyChoice, "Generate Key", "Upload Key", "Type Key", command=self.chooseKey)
        self.option['menu'].config(bg="white",selectcolor="blue",relief="solid",font=("Helvetica",12))
        self.option.configure(bg="white",width=12,bd=2,activebackground="white",relief="solid",font=("Helvetica",12))
        self.option.pack(side="top")
        self.keyText = Text(self.right2,width="70",height=1,relief="solid",font=("Helvetica",14),pady=5)
        self.keyText.pack(side="left")
        self.b1 = Button(self.right,text="Select file to be encrypted",activebackground="gray",activeforeground="white",bg="#f28100",font=("Helvetica",12),bd=2,relief='flat',height=3,width=85,padx=2,pady=2,fg="white",command=self.askFileLocation)
        self.b2 = Button(self.right,text="Select location where encrypted file is to be stored",activebackground="gray",activeforeground="white",bg="#f28100",font=("Helvetica",12),bd=2,relief='flat',height=3,width=85,padx=2,pady=2,fg="white",command=self.askFolderStore)
        self.lab = Label(self.right,bg="white")
        self.lab.pack(side="top")
        self.b1.pack(side="top")
        self.t1 = Text(self.right,relief="flat",width="110",height=1,font=("Helvetica",10),pady=10)
        self.t1.pack(side="top")
        self.lab = Label(self.right,bg="white")
        self.lab.pack(side="top")
        self.t2 = Text(self.right,relief="flat",pady=10,width="110",height=1,font=("Helvetica",10))
        self.b2.pack(side="top")
        self.t2.pack(side="top")
        self.lab = Label(self.right,bg="white")
        self.lab.pack(side="top")
        self.b3 = Button(self.right,text="Start",activebackground="gray",activeforeground="white",bg="#3f6621",font=("Helvetica",14),bd=2,relief='flat',height=2,width=10,padx=2,pady=2,fg="white",command=self.startBtn)
        self.b3.pack(side="right")
        return

    def askFileLocation(self):
        x = filedialog.askopenfile(mode="r")
        self.t1.delete('1.0','end')
        self.t1.insert('1.0',x.name)
        self.t1['relief'] = 'solid'
        self.encFile = x.name

    def askFolderStore(self):
        x = filedialog.askdirectory()
        self.t2.delete('1.0','end')
        self.t2.insert('1.0',x)
        self.t2['relief'] = 'solid'
        self.encFileLoc = x

    def startBtn(self):
        if not path.isfile(self.encFile):
            messagebox.showerror(title="File Path Wrong",message="Please enter correct file path. Click on orange button.")
        if not path.exists(self.encFileLoc):
            messagebox.showerror(title="Invalid Folder Location",message="Please enter correct folder path. Click on orange button.") 
        if len(self.keyText.get("1.0","end").rstrip())!=44:
            messagebox.showerror(title="Key Error",message="Please enter a key (length: 44) to encrypt. You can generate one from the options. Remember to save it.") 
        if not self.Key:
            self.Key = self.keyText.get("1.0","end").rstrip()
        print(self.encFile)
        print(self.encFileLoc)
        f = FileOps() 
        f.encryptFile(self.Key,self.encFile,self.encFileLoc)
        messagebox.showinfo('Encryption Done',message='Your file is now secure.')
        return


    def rem(self):
        try:
            self.saveKeyBtn.destroy()  
        except:
            pass        
    
    def chooseKey(self,val=""):
        self.keyText.delete("1.0","end")
        self.rem()              
        if val=="Generate Key":
            k = self.Note.e.generateKey()
            self.Key = k
            self.keyText.insert("1.0",k)
            self.saveKeyBtn = Button(self.right2,text="Save Key",bg="#f8cd0c",fg="white",relief="flat",command=self.saveGeneratedKey,font=("Helvetica",12,"bold"))
            self.saveKeyBtn.pack(side="right")
            
        elif val=="Upload Key":
            self.select = filedialog.askopenfilename(filetypes=(("KEY File","*.key"),("All files","*.*")))
            print(self.select)
            f = open(self.select,'rb')
            k = f.read()
            self.Key = k
            f.close()
            print(k)
            self.keyText.insert("1.0",k)
        
    def saveGeneratedKey(self):
        a = self.keyText.get("1.0","end")
        file = filedialog.asksaveasfile(defaultextension=".key")
        file.write(a.rstrip())
        
    def decStartBtn(self):
        if not path.isfile(self.encFile):
            messagebox.showerror(title="File Path Wrong",message="Please enter correct file path. Click on orange button.")
        if not path.exists(self.encFileLoc):
            messagebox.showerror(title="Invalid Folder Location",message="Please enter correct folder path. Click on orange button.") 
        if len(self.keyText.get("1.0","end").rstrip())!=44:
            messagebox.showerror(title="Key Error",message="Please enter a key (length: 44) to encrypt. You can generate one from the options. Remember to save it.") 
        if not self.Key:
            self.Key = self.keyText.get("1.0","end").rstrip()
        print(self.encFile)
        print(self.encFileLoc)
        f = FileOps() 
        f.decryptFile(self.Key,self.encFile,self.encFileLoc)
        messagebox.showinfo('Decryption Done',message='Your file is now readable.')
        return
    
    def decBtn(self):
        self.enc['fg']="gray"
        self.note['fg']="gray"
        self.dec['fg']="green"
        self.clearFrame(self.left)
        self.clearFrame(self.right)

        self.right2 = Frame(self.right)
        self.right2.pack(side="top")
        self.keyChoice = StringVar(self.right2)
        self.keyChoice.set("Choose Key")
        self.option = OptionMenu(self.left, self.keyChoice, "Generate Key", "Upload Key", "Type Key", command=self.chooseKey)
        self.option['menu'].config(bg="white",selectcolor="blue",relief="solid",font=("Helvetica",12))
        self.option.configure(bg="white",width=12,bd=2,activebackground="white",relief="solid",font=("Helvetica",12))
        self.option.pack(side="top")
        self.keyText = Text(self.right2,width="70",height=1,relief="solid",font=("Helvetica",14),pady=5)
        self.keyText.pack(side="left")
        self.b1 = Button(self.right,text="Select file to be decrypted",activebackground="gray",activeforeground="white",bg="#f28100",font=("Helvetica",12),bd=2,relief='flat',height=3,width=85,padx=2,pady=2,fg="white",command=self.askFileLocation)
        self.b2 = Button(self.right,text="Select location where decrypted file is to be stored",activebackground="gray",activeforeground="white",bg="#f28100",font=("Helvetica",12),bd=2,relief='flat',height=3,width=85,padx=2,pady=2,fg="white",command=self.askFolderStore)
        self.lab = Label(self.right,bg="white")
        self.lab.pack(side="top")
        self.b1.pack(side="top")
        self.t1 = Text(self.right,relief="flat",width="110",height=1,font=("Helvetica",10),pady=10)
        self.t1.pack(side="top")
        self.lab = Label(self.right,bg="white")
        self.lab.pack(side="top")
        self.t2 = Text(self.right,relief="flat",pady=10,width="110",height=1,font=("Helvetica",10))
        self.b2.pack(side="top")
        self.t2.pack(side="top")
        self.lab = Label(self.right,bg="white")
        self.lab.pack(side="top")
        self.b3 = Button(self.right,text="Start",activebackground="gray",activeforeground="white",bg="#3f6621",font=("Helvetica",14),bd=2,relief='flat',height=2,width=10,padx=2,pady=2,fg="white",command=self.decStartBtn)
        self.b3.pack(side="right")        
        return     

    
if __name__ == "__main__":
    log = Login()
    pt = log.start()
    print(pt)
    if pt:
        root = Tk()
        root.title('Monocrypt')
        root.state('zoomed')
        root.iconbitmap("lock.ico")
        root.configure(background='white')
        app = Application(master=root)
        app.mainloop()
    else:
        messagebox.showerror(title='Wrong Password',message='Please enter correct password.')