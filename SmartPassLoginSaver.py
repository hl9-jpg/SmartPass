"""
SmartPassLoginSaver main code
Originally in different files, but has been combined to make this one
Version 1.2.1
Last updated 4-9-18
"""

"""
A logo was also made, and to make this code more complete, please download logo from link below
https://drive.google.com/file/d/1-mmtfOEhPdiGSno5TUdIeMav1-PvFLgM/view?usp=sharing
Make sure to save logo in same folder this code is in so the GUI will find this file
"""

from random import randint
from base64 import b64encode, b64decode
from hashlib import sha512 as shake
from re import findall
import subprocess
import os
import shutil
import csv
import ctypes
from tkinter import *
from tkinter import filedialog
from tkinter.filedialog import askopenfilename
from tkinter import messagebox

###IT IS IMPORTANT TO NOTE THAT THIS ENCRYPTION IS VERY MUCH BASED OFF OF AES256 ENCRYPTION, AND ALTHOUGH MY ENCRYPTION IS MOST LIKELY NOTHING LIKE IT, IT WILL DO THE JOB
class Cipher(): ###ENCRYPTION AND DECRYPTION CLASS
    
    ###--------------self.nums_key, self.pad, and self.unpad were taken from link below--------------###
    #####https://stackoverflow.com/questions/12524994/encrypt-decrypt-using-pycrypto-aes-256#####
    ########## Written by "mnothic" and edited by "gregoltsov" ##########
    def __init__(self, key): ###INITIALIZES CIPHER AND EVERYTHING NEEDED TO ENCRYPT AND DECRYPT
        self.nums_key = list(map(lambda x: ord(chr(x)), shake(key.encode()).digest())) #64 nums long
        self.block_size = 64 #block_size is 64 cause key must be 64 characters long
        self.pad = lambda s: s + (self.block_size - len(s) % self.block_size) * chr(self.block_size - len(s) % self.block_size) ###pads the password to be 64 characters long
        self.unpad = lambda s: s[:-ord(s[len(s)-1:])] ###unpads to its orginal character length
        
    def encrypter(self, plaintext):  ###ENCRYPTS DATA
        nums_pass = list(map(lambda x: ord(x), self.pad(plaintext))) ###pads plaintext that is entered and changes it to the number
        nums_encrypted = self.encRoundTwo(self.encRoundOne(nums_pass)) ###puts each number through round one and two of the encryption
        chars_encrypted = "".join(list(map(lambda x: chr(x), nums_encrypted))) ###changes each number into a character 
        encrypted = b64encode(chars_encrypted.encode()).decode() #encodes the strings of characters through the base64 encoding
        random = self.random(len(encrypted) + 15).decode()[:len(encrypted)+10] ###calls the random string function and assigns it to random
        if "=" not in encrypted: ###sometimes, encoding won't be padded with an '=' at the end, so it can't be decoded. This encodes the plaintext with no encryption and add it to the end of the random string
            ciphertext = random + b64encode(plaintext.encode()).decode()
            ciphertext += str(len(b64encode(plaintext.encode()).decode())) + "-\!="
        else: ###ELSE INTERTWINE THE ENCRYPTED AND THE RANDOM
            ciphertext = self.intertwine(encrypted, random)
        return ciphertext.encode() 
        
    def encRoundOne(self, msg): ###ROUND ONE OF ENCRYPTION
        round1 = []
        for i in range(len(msg)):
            round1.append(msg[i] + self.nums_key[i]) ###adds each number of the msg and the corresponding number of the key
        return round1
        
    def encRoundTwo(self, msg): ###ROUND TWO OF ENCRYPTION
        round2 = []
        for i in range(len(msg)):
            round2.append(msg[i] + self.nums_key[::-1][i]) ###adds each number of msg and the inverted corresponding number of the key
        return round2
        
    def decrypter(self, ciphertext): ###DECRYPTS DATA
        if  ciphertext.decode().endswith("-\!="): ###IF CIPHERTEXT ENDS WITH THAT STRING, THEN THAT MEANS JUST DECODE THE LAST BIT OF THE STRING BY PULLING THE LENGTH AND ONLY DECODING UP TO THAT LENGTH
            cipher_rev = ciphertext.decode()[:-1]
            cipher_rev = cipher_rev[::-1]
            end, beginning = cipher_rev.split("=")[0], "".join(cipher_rev.partition("=")[1:])
            pattern = r"[0-9]"
            number = findall(pattern, end)
            plength = int("".join(number[::-1]))
            encrypted = beginning[:plength][::-1]
            plaintext = b64decode(encrypted.encode())
            return plaintext.decode()
        else: ###ELSE IT WAS ENCODED NORMALLY AND SHOULD BE DECRYPTED BY REVERSING ROUND ONE AND TWO
            ciphertext = ciphertext.decode()[11:] ###first it needs to cut off the random string
            encrypted = ciphertext[::2]
            chars_encrypted = b64decode(encrypted.encode()).decode()
            nums_encrypted = list(map(lambda x: ord(x), chars_encrypted))
            nums_pass = self.decRoundTwo(self.decRoundOne(nums_encrypted))
            plaintext = self.unpad("".join(list(map(lambda x: chr(x), nums_pass))))
            return plaintext
        
    def decRoundOne(self, msg): ###ROUND ONE OF DECRYPTION
        round1 = []
        for i in range(len(msg)):
            round1.append(abs(msg[i] - self.nums_key[::-1][i]))
        return round1
        
    def decRoundTwo(self, msg): ###ROUND TWO OF DECRYPTION
        ro
        
    @staticmethod
   
    def hideFile(filename): ###SETS ATTRIBUTES TO HIDDEN AND READ-ONLY
        subprocess.call("attrib +r +h " + filename)
    
    @staticmethod
    def showFile(filename): ###SETS ATTRIBUTES TO SHOWING AND READ AND WRITE
        subprocess.call("attrib -r -h " + filename)

class CSVHandler(): ###DOES EVERYTHING WITH THE CSV FILE
    
    def __init__(self): ###INTIALIZE VARIABLE FILENAME AND DATA
        os.chdir("C:\\")
        self.dirname = r"C:\SmartPass\bin"
        self.filename = self.dirname + r"\SmartPassLoginInformation.csv"
        CSVHandler.filename = self.filename
        self.secret_dirname = "\\"+ "\\" + ".\\" + r"C:\SmartPass\bin"
        self.secret_filename = self.secret_dirname + r"\con.csv"
        CSVHandler.secret_filename = self.secret_filename
        self.data = []
        if os.path.isfile(self.secret_filename) == os.path.isfile(self.filename) == False: ###this notation is needed to ensure that files aren't being made every single time an object for the class is made
            subprocess.call("mkdir " + self.secret_dirname, shell=True)
            with open(self.secret_filename, "w") as f: FileProperties.hideFile(self.secret_filename)
    
    def adder(self, description, username, password): ###ADDS TO FILE  
        self.description = description
        self.username = username
        self.password = password
        
        passwords = self.reader(None, None)[0] ###ADDS WHATEVER IS IN CSV FILE RIGHT NOW TO DATA, THEN ADDS NEW ENCRYPTED PASSWORD TO DATA AS WELL  
        for element in passwords: self.data.append([encrypt(element[0]), encrypt(element[1]), encrypt(element[2])])
        self.data.append([encrypt(description), encrypt(username), encrypt(password)])
        
        FileProperties.showFile(self.secret_filename)
        with open(self.secret_filename, "w", newline='') as f:
            writer = csv.writer(f)
            writer.writerows(self.data) ###rewrites csv file with data
        FileProperties.hideFile(self.secret_filename)
        
    def reader(self, line, description): ###READS WHOLE CSV FILE; IF LINE IS SPECIFIED AS SOMETHING OTHER THAN NONE, JUST READS PASSWORD CONTAINED IN THAT LINE
        with open(self.secret_filename, "r") as f:
            reader = csv.reader(f)
            i = 0
            if description == None and line == None:
                passwords = []
                for row in reader:
                    if row == []: continue ###without this, csv file would make unecessary and random empty rows 
                    else:
                        passwords.append([decrypt(row[0][2:-1].encode()), decrypt(row[1][2:-1].encode()), decrypt(row[2][2:-1].encode())])
                        i += 1
                return passwords, i
            elif line != None: ###if line has an value other than None, read that specific line
                for row in reader:
                    i += 1
                    if line == i:
                        return [decrypt(row[0][2:-1].encode()), decrypt(row[1][2:-1].encode()), decrypt(row[2][2:-1].encode())]
            elif description != None: ###if description has a value other than None, read from that description
                passwords = self.reader(None, None)[0]
                for element in passwords:
                    if description == element[0]:
                        return element
            
            else: raise ValueError("Arguments not inputted correctly") ###if for some reason none of the above statements are called, raise this error
    
    def deleter(self, line, description, username, password): ###DELETES EVERYTHING ON CSV FILE; IF LINE IS SPECIFIED AS SOMETHING OTHER THAN NONE, JUST DELETES PASSWORD CONTAINED IN THAT LINE; IF PASSWORD IS SPECIFIED AS SOMETHING OTHER THAN NONE, JUST DELETES PASSWORD
        passwords = self.reader(None, None)[0]
        if line == description == username == password == None: passwords = [] ###if no arguments specified, delete everything
        elif line != None: del passwords[line-1] ###delete the line specified
        elif description != None: ###look for the description and delete 
            for element in passwords:
                if description == element[0]:
                    passwords.remove(element)
        elif username != None: ###look for the username and delete
            for element in passwords:
                if username == element[1]:
                    passwords.remove(element)
        elif password != None: ###look for the password and delete
            for element in passwords:
                if password == element[2]:
                    passwords.remove(element)
        else: raise ValueError("Arguments not inputted correctly") ###if not going through if statements, arguments aren't inputted correctly
        
        for password in passwords: self.data.append([encrypt(password[0]), encrypt(password[1]), encrypt(password[2])]) ###REWRITES FILE WITH NEW DATA
        
        FileProperties.showFile(self.secret_filename)
        with open(self.secret_filename, "w", newline='') as f:
            writer = csv.writer(f)
            writer.writerows(self.data)
        FileProperties.hideFile(self.secret_filename)
        
    def prioritizer(self, line, description, username, password): ###ALLOWS FOR A SPECIFIC LINE, DESCRIPTION, USERNAME, OR PASSWORD TO BE PRIORITIZED TO BE AT THE TOP OF THE LIST
        passwords = self.reader(None, None)[0]
        if line != None: ###prioritize based on line number
          starred = passwords.pop(line-1)
          passwords.insert(0, starred)
        elif description != None: ###prioritize based on description
            i = 0
            for element in passwords:
                i += 1
                if description == element[0]: passwords.insert(0, passwords.pop(i-1))
        elif username != None: ###prioritize based on username
            i = 0
            for element in passwords:
                i += 1
                if username == element[1]: passwords.insert(0, passwords.pop(i-1))
        elif password != None: ###prioritize based on password
            i = 0
            for element in passwords:
                i += 1
                if password == element[2]: passwords.insert(0, passwords.pop(i-1))
        else: raise ValueError("Arguments not inputted correctly (One argument must be equal to something other than None)") ###all aruments are equal to None, which can't happen, so error is raised
          
        for password in passwords: self.data.append([encrypt(password[0]), encrypt(password[1]), encrypt(password[2])]) ###REWRITES FILE WITH NEW DATA
        
        FileProperties.showFile(self.secret_filename)
        with open(self.secret_filename, "w", newline='') as f:
            writer = csv.writer(f)
            writer.writerows(self.data)
        FileProperties.hideFile(self.secret_filename)    
            
            
c
    return handle.adder(description, username, password)
    
def
    createWindow.title("Save a New Login")
    createWindow.geometry(str(int(user32.GetSystemMetrics(0)/3))+'x'+str(int(user32.GetSystemMetrics(1)/3))) #sets screen size to a third of the monitor size
    windowSetup(createWindow)
    configGrid(createWindow,5,2)
    Label(createWindow,text="Save a Login",font=("Times New Roman",25)).grid(row=0,column=0,columnspan=3,padx=10,pady=0,sticky="W")
    Label(createWindow,text="Description:",font=("Calibri")).grid(row=1,column=0,sticky='W',padx=20)
    Label(createWindow,text="Username/Email:",font=("Calibri")).grid(row=2,column=0,sticky='W',padx=20)
    Label(createWindow,text="Password:",font=("Calibri")).grid(row=3,column=0,sticky='W',padx=20)
    e_description=Entry(createWindow,width=40)
    e_description.grid(row=1,column=1,sticky='W')
    e_username=Entry(createWindow,width=40)
    e_username.grid(row=2,column=1,sticky='W')
    e_password=Entry(createWindow,width=40,show='*')
    e_password.grid(row=3,column=1,sticky='W')
    b_showpassword=Button(createWindow,text="Show",width=5)
    b_showpassword.grid(row=3,column=1,sticky='E')
    def show(event):e_password.configure(show='')
    def hide(event):e_password.configure(show='*')
    b_showpassword.bind('<ButtonPress-1>',show)
    b_showpassword.bind('<ButtonRelease-1>',hide)
    c_prioritize=Checkbutton(createWindow,text="Prioritize (Most recent creation will have highest priority rank)",onvalue=1,offvalue=0,variable=priority)
    c_prioritize.grid(row=4,column=0,columnspan=3)
    l_descf=Label(createWindow,text="*Required Field",fg='red')
    l_descf.grid(row=1,column=2,sticky='W',padx=10)
    l_userf=Label(createWindow,text="*Required Field",fg='red')
    l_userf.grid(row=2,column=2,sticky='W',padx=10)
    l_passf=Label(createWindow,text="*Required Field",fg='red')
    l_passf.grid(row=3,column=2,sticky='W',padx=10)
    l_descf.grid_remove()
    l_userf.grid_remove()
    l_passf.grid_remove()
    Button(createWindow,text="OK",command=register,width=15).grid(row=5,column=1,sticky='E',padx=5,pady=10)
    Button(createWindow,text="Cancel",command=destroy_window,width=15).grid(row=5,column=2,sticky='W',padx=5,pady=10)
    createWindow.bind('<Return>',register)
    createWindow.bind('<Escape>',destroy_window)
    createWindow.resizable(False,False)
    createWindow.protocol("WM_DELETE_WINDOW",destroy_window)
    createWindow.mainloop()
    
def access_login(): #decrypts and displays all the user's logins in a file-directory like fashion
    desc=[] #list of descriptions ordered by priority
    abc=[] #list of descriptions ordered in abc order
    logins = read()[0]
    for login in logins:
        desc.append(login[0])
        abc.append(login[0])
    abc.sort()
    #create GUI Window
    accessWindow=Tk()
    configGrid(accessWindow,4,4)
    accessWindow.resizable(True,False)
    windowSetup(accessWindow)
    accessWindow.title("Access My Logins")
    accessWindow.geometry('1000x575')
    listmode=IntVar(accessWindow)
    listmode.set(1) #settings default to sorting data by priority 
    topLayer=Frame(accessWindow)
    topLayer.grid(row=0,rowspan=2,column=0,columnspan=5,sticky="NESW")
    configGrid(topLayer,2,5)
    canvas=Canvas(accessWindow)                              
    b_access_login.config(state='disabled')                   
    b_new_login.config(state='disabled')
    def destroy_window(*event): #function for handling window killing event
        accessWindow.destroy()
        try:
            b_access_login.config(state='normal')
            b_new_login.config(state='normal')
        except: pass
        
    def populate(frame,data): #populates the scroll frame with login data from the data file
        for widget in frame.winfo_children(): widget.destroy() #clears the frame before populating it
        if len(data)>0:
            b_deleteall.configure(state='normal')
            x=1
            for login in data:
                description=str(login)
                username=str(read(description=login)[1])
                password=str(read(description=login)[2])
                strength=getStrength(str(password))
                strengthlevel="Strong" if strength >= 21 else "Fair" if 11<strength<21 else "Weak" if strength<=11 else None
                Label(frame,text=str(data.index(login)+1),width=5,bg="light grey" if x==1 else "white",anchor='w').grid(row=data.index(login),column=0)
                Label(frame,text=description if len(description)<44 else description[:44]+' ...',width=40,bg="light grey" if x==1 else "white",anchor='w').grid(row=data.index(login),column=1)
                Label(frame,text=username if len(username)<44 else username[:44]+' ...',width=40,bg="light grey" if x==1 else "white",anchor='w').grid(row=data.index(login),column=2)
                Label(frame,text=password if len(password)<29 else password[:29]+' ...',width=30,bg="light grey" if x==1 else "white",anchor='w').grid(row=data.index(login),column=3)
                Label(frame,text=strengthlevel,width=15,
                    bg="light grey" if x==1 else "white",
                    fg='green' if strengthlevel=="Strong" else 'orange' if strengthlevel=="Fair" else 'red',
                    anchor='w').grid(row=data.index(login),column=4,sticky='EW')
                x=1 if x==0 else 0
        else:
            b_deleteall.configure(state='disabled')
            Label(frame,text="No Saved Logins" if len(desc)==0 else "No Results",font=("Calibri",15),anchor=CENTER,width=90,bg='light grey').grid(row=0,columnspan=5,sticky='EW')
        l_results.config(text="Results: "+str(len(data)))
    def configureFrame(canvas): #configures the canvas
        canvas.configure(scrollregion=canvas.bbox("all")) #CODE FROM http://effbot.org/tkinterbook/canvas.htm
    #display logins
    display=Frame(accessWindow,width=550,height=225)
    display.grid(row=3,column=0,columnspan=5,sticky="NSEW",padx=20)
    configGrid(display,0,4)
    scroll=Scrollbar(accessWindow,orient="vertical",command=canvas.yview)
    scroll.grid(row=2,column=4,sticky="NSE",padx=20)
    canvas.configure(yscrollcommand=scroll.set)
    def mousewheel(event):canvas.yview_scroll(int(-1*(event.delta/120)),"units") #CODE FROM https://stackoverflow.com/questions/17355902/python-tkinter-binding-mousewheel-to-scrollbar/37858368
    canvas.bind_all("<MouseWheel>",mousewheel)
    display.bind("<Configure>", lambda event, canvas=canvas: configureFrame(canvas))
   
    canvas.create_window((4,4),window=display) #code from https://stackoverflow.com/questions/29319445/tkinter-how-to-get-frame-in-canvas-window-to-expand-to-the-size-of-the-canvas
    
    Label(topLayer,text="Access My Logins",font=("Times New Roman",25)).grid(row=0,columnspan=10,padx=10,pady=10,sticky="NW")
    #Listing all data ordered either by priority or abc order
    r_priority=Radiobutton(topLayer,text="Sort all by\nPriority",variable=listmode,value=1,command=lambda:populate(frame=display,data=desc))
    r_priority.grid(row=1,column=3,sticky='E')
    r_abc=Radiobutton(topLayer,text="Sort all\nAlphabetically",variable=listmode,value=2,command=lambda:populate(frame=display,data=abc))
    r_abc.grid(row=1,column=4)
    #Listing results of a search
    def search(*event):
        listmode.set(0)
        searchdata=[]
        if len(str(e_search.get()))!=0:
            for login in desc:
                if str(e_search.get()).lower() in login.lower(): searchdata.append(login)
            populate(frame=display,data=searchdata)    
    l_search=Label(topLayer,text="Search: ",font=("Calibri"))
    l_search.grid(row=1,column=0,sticky='E',padx=10)
    e_search=Entry(topLayer,width=100)
    e_search.grid(row=1,column=1,sticky='EW')
    b_search=Button(topLayer,text="Search",command=search,width=7)
    b_search.grid(row=1,column=2,sticky='W')
    accessWindow.bind("<Return>",search)
    
    #labels
    labels=Frame(topLayer) #new fram topLayer
    labels.grid(row=2,column=0,columnspan=5,sticky="NEW",padx=20)
    configGrid(labels,0,4)
    Label(labels,text="#",width=5,anchor='w').grid(row=0,column=0)
    Label(labels,text="Description",width=40,anchor='w').grid(row=0,column=1)
    Label(labels,text="Username/Email",width=40,anchor='w').grid(row=0,column=2)
    Label(labels,text="Password",width=30,anchor='w').grid(row=0,column=3)
    Label(labels,text="Password\nStrength",width=9,anchor='w').grid(row=0,column=4)
    #bottom layer (close button and options to delete all logins button)
    def verifydelete():
        b_deleteall.configure(state="disabled")
        result=messagebox.askyesno("Delete All?","Are you sure you want to wipe all of your saved logins?")
        if result==True:
            delete()
            try:destroy_window()
            except: pass
        else: 
            try:b_deleteall.configure(state="normal")
            except: pass
    bottom=Frame(accessWindow)
    bottom.grid(row=3,column=0,columnspan=5,sticky="NSEW")
    Button(bottom,text="Close",command=destroy_window,width=10).pack(padx=10,pady=20,side=RIGHT)
    b_deleteall=Button(bottom,text="Delete All",command=verifydelete,width=10)
    b_deleteall.pack(pady=20,side=RIGHT)
    l_results=Label(bottom)
    l_results.pack(side=LEFT,padx=20)
    canvas.grid(row=2,column=0,columnspan=5,sticky="NSEW",padx=20)
    topLayer.tkraise()
    labels.tkraise()
    bottom.tkraise()
    populate(frame=display,data=desc)#initialize window with priority sorted data
    accessWindow.protocol("WM_DELETE_WINDOW",destroy_window)
    accessWindow.bind('<Escape>',destroy_window)
    accessWindow.mainloop()
    
def wipe(): #deletes all files/directories created by this program
    mainWindow.withdraw()
    result=messagebox.askyesno("Reset the Application?",
                               '''Are you sure you want to wipe all data?\nThis will perform a \"Factory Reset\" on this Application.
                               All app data will be lost\n(This will not uninstall the application)''')
    if result==True:
        messagebox.showwarning("Warning","For this action to execute successfully, please close File Explorer (Windows) or Finder (Mac)")
        FileHandler.makeVincible() #FileHandler class created by my partner
        shutil.rmtree(r'C:\SmartPass')
        os._exit(1)
    else: mainWindow.deiconify()
def importExport(option): #allows user to import/export the data file for cross device usage.
    mainWindow.withdraw()
    def destroy_window(*event): #handles window killing event
        mainWindow.deiconify()
        ie.destroy()
    bindirectory='C:\\SmartPass\\bin'
    source=r'C:\SmartPass\bin\SmartPassLoginInformation.csv'
    ie=Tk()
    ie.title("Copy Data File")
    windowSetup(ie)
    ie.geometry('650x275')
    ie.resizable(False,False)
    configGrid(ie,3,2)
    def copyfile(newdir): #copy the data to directory specified by user
        FileHandler.makeVincible(isHidden=True) #FileHandler class created by my partner; allows csv file to be moved
        shutil.copy(source,newdir)
        FileHandler.makeInvincible() #FileHandler class created by my partner
        destroy_window()
    def importfile(directory): #import the data file from directory specified by user
        try:
            FileHandler.makeVincible() #FileHandler class created by my partner
            os.remove(source)
        except: pass
        shutil.move(directory,bindirectory)
        FileHandler.makeInvincible() #FileHandler class created by my partner; disables all actions done to csv file
        destroy_window()
    def dialog(): #creates a GUI file dialog for a more user friendly way of finding a directory
        ie.withdraw()
        f_dir=filedialog.askdirectory() if option==1 else filedialog.askopenfilename(filetypes=[('SmartPassLoginInformation.csv','SmartPassLoginInformation.csv')]) #only file that will show up in search
        ie.deiconify()
        e_location.configure(state='normal')
        e_location.delete(0,END)
        e_location.insert(0,f_dir)
        e_location.configure(state='disabled')
        if len(str(e_location.get()))!=0:
            Button(ie,
                   text='Copy' if option==1 else 'Import',width=10,
                   command=lambda:copyfile(f_dir) if option==1 else importfile(f_dir)).grid(row=4,column=1,pady=10)
    Label(ie,text="Export Copy of Data File" if option==1 else "Import Data File",font=("Times New Roman",23)).grid(row=0,column=0,columnspan=2,padx=20,pady=10,sticky='NW')
    Label(ie,text='''This will place a copy of the data file into a specified destination.
          \nWe recommend saving the copy file to a flash drive and importing it using our software on another device.
          \nPlease select the destination folder in which to copy the data file.''' if option==1
          else '''Please locate the data file named "con.csv"
          \nThe file should be where you have previously saved it with this software on another device
          \nImporting a data file will overwrite all data previously saved by this device.''',
          font=("Calibri",10),anchor=CENTER).grid(row=1,column=0,columnspan=3,padx=20)
    e_location=Entry(ie,width=50,state='disabled')
    e_location.grid(row=3,column=0,sticky='E',pady=10)
    Button(ie,text='...',command=dialog).grid(row=3,column=1,sticky='W',pady=10)
    Button(ie,text='Cancel',command=destroy_window,width=10).grid(row=4,column=2,padx=5,pady=10)
    ie.protocol("WM_DELETE_WINDOW",destroy_window)
    ie.bind('<Escape>',destroy_window)
    ie.mainloop()
def deletefiles(): #gives user option to delete individual files (user info file or data file) [This is primarily used for testing purposes]
    fdelete=Tk()
    mainWindow.withdraw()
    def destroy_window(*event): #handles file killing event
        mainWindow.deiconify()
        fdelete.destroy()
    def execute(*event): #perform the action of deleting the files
        f_data=r'C:\SmartPass\bin\SmartPassLoginInformation.csv'
        result=messagebox.askyesno("Delete Selected Files?","Are you sure you want to delete these files?")
        if result==True:
            if v_loginf.get()==1:
                try: os.remove(r'C:\SmartPass\bin\~$uildf.txt')
                except: pass
            if v_dataf.get()==1:
                try:
                    FileHandler.makeVincible() #FileHandler class created by my partner (makes file movable)
                    os.remove(f_data)
                except: pass
        else: pass
        destroy_window()
    v_loginf=IntVar(fdelete)
    v_dataf=IntVar(fdelete)
    fdelete.title("Delete Files")
    windowSetup(fdelete)
    fdelete.geometry('350x150')
    fdelete.resizable(False,False)
    configGrid(fdelete,2,2)
    Label(fdelete,text='Delete Files',font=('Times New Roman',22)).grid(columnspan=2,padx=20,pady=10,sticky='NW')
    c_loginf=Checkbutton(fdelete,text="Info File \n('~$uildf.txt')",onvalue=1,offvalue=0,variable=v_loginf)
    c_loginf.grid(row=1,column=0,padx=5)
    c_dataf=Checkbutton(fdelete,text="Data File \n(File containing all login data)",onvalue=1,offvalue=0,variable=v_dataf)
    c_dataf.grid(row=1,column=1,padx=5,columnspan=2)
    Button(fdelete,text="Cancel",width=10,command=destroy_window).grid(row=2,column=2,padx=10,pady=10)
    Button(fdelete,text="Delete Files",width=10,command=execute).grid(row=2,column=1,pady=10,sticky='E')
    fdelete.mainloop()

#=====MAIN CODE=====#
editor_directory=os.getcwd() #set editor directory to current working directory
#attempt to create this directory if it does not exist already
try: os.mkdir('C:\\SmartPass')
except: pass
try:os.mkdir('C:\\SmartPass\\bin')
except: pass
bindirectory='C:\\SmartPass\\bin' #set bin directory to the directory that was just created
mainsetup() #run main setup defined above
mainWindow=Tk()

#variable declarations
t_resizable = IntVar(mainWindow)
t_resizable.set(0)

mainWindow.resizable(bool(t_resizable.get()),bool(t_resizable.get())) #update screen after default variables are set

#configures a 4x4 grid

configGrid(mainWindow,4,4) #function declared in setup.py
    
#Header and Version Info
version="SmartPass v1.0" #Any updates to name or version here will update everything else in the program
mainWindow.title(version)
mainWindow.geometry(str(int(user32.GetSystemMetrics(0)/3))+'x'+str(int(user32.GetSystemMetrics(1)/3))) #sets screen size to a third of the monitor size
welcomeLabel=Label(mainWindow,text=("Welcome to "+version),font=("Times New Roman",24)).grid(row=0,columnspan=5)
versionLabel=Label(mainWindow,text=version).grid(row=4,column=4)

#menu bar
menubar=Menu(mainWindow)

filemenu=Menu(menubar,tearoff=0)
filemenu.add_command(label="Wipe All Data",command=wipe)
filemenu.add_command(label="Delete Files",command=deletefiles)
filemenu.add_separator()
filemenu.add_command(label="Export Copy of Logins Data File",command=lambda:importExport(1))
filemenu.add_command(label="Import Logins from Existing File",command=lambda:importExport(2))
menubar.add_cascade(label="File",menu=filemenu)

optionsmenu=Menu(menubar,tearoff=0)
optionsmenu.add_checkbutton(label="Screen Resizable",onvalue=1,offvalue=0,variable=t_resizable,command=lambda: mainWindow.resizable(bool(t_resizable.get()),bool(t_resizable.get())))
optionsmenu.add_command(label="Reset Default Screen Size",command=lambda: mainWindow.geometry(str(int(user32.GetSystemMetrics(0)/3))+'x'+str(int(user32.GetSystemMetrics(1)/3))))
menubar.add_cascade(label="Options",menu=optionsmenu)

'''#EXPERIMENTAL [ABOUT MENU BAR] (WILL ADD IN LATER VERSIONS)
aboutmenu=Menu(menubar,tearoff=0)
aboutmenu.add_command(label="About the Software",command=lambda:[about_menu(selector=1),aboutmenu.entryconfig("About the Software",state='disabled')]) #FEATURES,FUNCTION,ETC. OF SOFTWARE
aboutmenu.add_command(label="Updates",command=lambda:[about_menu(selector=2),aboutmenu.entryconfig("Updates",state='disabled')]) #UPDATES
aboutmenu.add_separator()
aboutmenu.add_command(label="Help",command=lambda:[about_menu(selector=3),aboutmenu.entryconfig("Help",state='disabled')]) # TROUBLESHOOTING, HOW TO USE
menubar.add_cascade(label="About",menu=aboutmenu)
'''
mainWindow.config(menu=menubar)

#buttons
b_new_login=Button(mainWindow,text="Save New Login",command=new_login)
b_new_login.grid(row=1,columnspan=5,sticky="NWSE",padx=50) 
b_access_login=Button(mainWindow,text="Access My Logins",command=access_login)
b_access_login.grid(row=2,columnspan=5,sticky="NWSE",padx=50,pady=10)

windowSetup(mainWindow)
mainWindow.protocol("WM_DELETE_WINDOW",lambda:os._exit(1))
mainWindow.mainloop()

