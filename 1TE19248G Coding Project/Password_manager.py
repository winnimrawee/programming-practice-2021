import tkinter as tk                
from tkinter import font as tkfont  
import pickle as p
import random
import string
from tkinter.constants import CENTER


# Class for storing user data
class User:
    def __init__(self, usr, pwd):
        self.username = usr
        self.password = pwd
        self.accounts = {}
    
    def add_account(self, platform, username, password):
        if platform in self.accounts.keys():
            self.accounts[platform][username]= password
        else:
            self.accounts[platform] = {}
            self.accounts[platform][username]= password
        dict_file = open("save_users.pkl", "wb")
        p.dump(list_of_users, dict_file)
        dict_file.close()



        
def generate_password():
    length = random.randint(11, 16)
    lower = string.ascii_lowercase
    upper = string.ascii_uppercase
    num = string.digits
    symbols = string.punctuation
    all = lower + upper + num + symbols
    pass_word = "".join(random.sample(all,length))
    return pass_word


def clear_labels():
    for i in all_labels: 
        i.destroy()

def clear_buttons():
     for i in all_buttons:
        i.destroy()


# For deleting labels and some buttons when changing pages
global all_labels
all_labels=[]

global all_buttons
all_buttons = []


# Main application class
class Password_manager_app(tk.Tk):      # Main Program Class

    def __init__(self):
        tk.Tk.__init__(self)
        self.winfo_toplevel().title("Password Manager by Win")
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        
        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
      
        ## Create an instance for each page and store in dictionary
        self.frames = {}
        for F in (StartPage, Create_user, Log_in, after_log_in, Add_account, Access_account):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        ## Show a frame for the given page name 
        frame = self.frames[page_name]
        frame.tkraise()   # Show frame by bring it up front

        ## Removing labels and some buttons from previous page
        clear_labels()
        clear_buttons()
       
        #For adding Welcome Message after logging in (Only on log in page)
        if page_name == "after_log_in":
            label = tk.Label(self, text="Welcome, " + username_login+"!", font = self.title_font, anchor= 'n' )
            label.pack()
            label.place(relx= 0.5, y=35, anchor= CENTER)
            all_labels.append(label)

     
   





class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Welcome to Password Manager!", font=controller.title_font)
        label.pack(side="top", fill="x", pady=70, padx= 100)
        button1 = tk.Button(self, text="Create User",
                            command=lambda: controller.show_frame("Create_user"))
        button2 = tk.Button(self, text="Login with Existing User",
                            command=lambda: controller.show_frame("Log_in"), )
        button1.pack()
        button2.pack()
        empty_space = tk.Label(self, text = "\n")     ### Add empty space 
        empty_space.pack()
       





### Load user data from pickle file


try:
    dict_file = open("save_users.pkl", "rb")
    list_of_users = p.load(dict_file)
except:
    list_of_users = {}






class Create_user(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        empty_space = tk.Label(self, text = "\n")     ### Add empty space 
        empty_space.pack()
        global username2, password2
        username2 = tk.Entry(self, width=30)
        username2.pack()
        username2.insert(0, "Enter Username...")  
        username2.bind('<FocusIn>', self.on_entry_click)
        username2.bind('<FocusOut>', self.on_focusout)
        password2 = tk.Entry(self, width=30)
        password2.pack()
        password2.insert(0, "Enter Password...")
        password2.bind('<FocusIn>', self.on_entry_click1)
        password2.bind('<FocusOut>', self.on_focusout1)
        username2.bind('<Return>',  lambda x=None: self.create_user(username2.get(),password2.get()))
        password2.bind('<Return>',  lambda x=None: self.create_user(username2.get(),password2.get()))
        button = tk.Button(self, text = 'Create user', command = lambda: self.create_user(username2.get(),password2.get()))
        button2 = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"), fg = 'red')
        button.pack()
        button2.pack()
    
    
    #### To make entry insert desappear on click ##########
    def on_entry_click(self, event):
        """function that gets called whenever entry is clicked"""
        if username2.get() == "Enter Username...":
            username2.delete(0, "end") # delete all the text in the entry
            username2.insert(0, '') #Insert blank for user input
    def on_focusout(self, event):
         if username2.get() == '':
            username2.insert(0, 'Enter Username...')
    def on_entry_click1(self, event):
        """function that gets called whenever entry is clicked"""
        if password2.get() == 'Enter Password...':
            password2.delete(0, "end") # delete all the text in the entry
            password2.insert(0, '') #Insert blank for user input
    def on_focusout1(self, event):
         if password2.get() == '':
            password2.insert(0, "Enter Password...")
    #####################################################
        

    def create_user(self, username, password):
        if username == 'Enter Username...' or username == "":
            clear_labels()
            clear_buttons()
            lbel1 = tk.Label(self, text = "              Please enter Username                \n\n\n", fg='orangered' )
            lbel1.pack()
            all_labels.append(lbel1)
        elif  password == "Enter Password..." or password == "":
            clear_labels()
            clear_buttons()
            lbel2 = tk.Label(self, text = "             Please enter Password              \n\n\n", fg='orangered' )
            lbel2.pack()
            all_labels.append(lbel2)
        else:
            try:
                username == list_of_users[username]
                clear_labels()
                clear_buttons()
                myLabel = tk.Label(self, text = "            This user has already been created               \n\n\n")
                myLabel.pack()
                myLabel.config(fg='orangered')
                all_labels.append(myLabel)

            except:
                list_of_users[username] = User(username,password)
                print(list_of_users)
                dict_file = open("save_users.pkl", "wb")
                p.dump(list_of_users, dict_file)
                dict_file.close()
                clear_labels()
                clear_buttons()
                global username_login
                username_login = username
                myLabel = tk.Label(self, text = "  User Created!  \n  Please click Next to continue  ")
                myLabel.pack()
                myLabel.config(fg='lime')
                all_labels.append(myLabel)
                button_next = tk.Button(self, text="Next",
                            command=lambda: self.controller.show_frame("after_log_in"))
                button_next.pack()
                all_buttons.append(button_next)
    











class Log_in(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        empty_space = tk.Label(self, text = "\n")     ### Add empty space 
        empty_space.pack()
        global username1, password1
        username1 = tk.Entry(self, width=30)
        username1.pack()
        username1.insert(0, "Enter Username...")
        username1.bind('<FocusIn>', self.on_entry_click)
        username1.bind('<FocusOut>', self.on_focusout)
        password1 = tk.Entry(self, width=30)
        password1.pack()
        password1.insert(0, "Enter Password...")
        password1.bind('<FocusIn>', self.on_entry_click1)
        password1.bind('<FocusOut>', self.on_focusout1)
        username1.bind('<Return>',  lambda x=None: self.log_in(username1.get(),password1.get()))
        password1.bind('<Return>',  lambda x=None: self.log_in(username1.get(),password1.get()))
        button = tk.Button(self, text = 'Log in', command = lambda: self.log_in(username1.get(),password1.get()))
        button2 = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"), fg = 'red')
        button.pack()
        button2.pack()

    #### To make entry insert desappear on click ##########
    def on_entry_click(self, event):
        """function that gets called whenever entry is clicked"""
        if username1.get() == 'Enter Username...':
            username1.delete(0, "end") # delete all the text in the entry
            username1.insert(0, '') #Insert blank for user input
    def on_focusout(self, event):
         if username1.get() == '':
            username1.insert(0, 'Enter Username...')
    def on_entry_click1(self, event):
        """function that gets called whenever entry is clicked"""
        if password1.get() == 'Enter Password...':
            password1.delete(0, "end") # delete all the text in the entry
            password1.insert(0, '') #Insert blank for user input
    def on_focusout1(self, event):
         if password1.get() == '':
            password1.insert(0, "Enter Password...")


    def log_in(self,username, password):
        if username == 'Enter Username...' or username == "":
            clear_labels()
            lbel1 = tk.Label(self, text = "           Please enter Username            \n\n", fg='orangered' )
            lbel1.pack()
            all_labels.append(lbel1)
        elif  password == "Enter Password..." or password == "":
            clear_labels()
            lbel2 = tk.Label(self, text = "           Please enter Password            \n\n", fg='orangered' )
            lbel2.pack()
            all_labels.append(lbel2)
        else:
            if list_of_users == {}:
                clear_labels()
                myLabel = tk.Label(self,text = 'There are no user created', fg='orangered')
                myLabel.pack()
                all_labels.append(myLabel)

            else:
                global username_login
                username_login = username
                try:
                    check = list_of_users[username_login].username
                    if check == username_login:
                        pw = password
                        if list_of_users[username_login].password == pw: 
                            clear_labels()
                            clear_buttons()
                            myLabel3 = tk.Label(self,text = '      Log in successful. Please click Next       ', fg = 'lime')
                            myLabel3.pack() 
                            all_labels.append(myLabel3) 
                            button_next = tk.Button(self, text="Next",
                                command=lambda: self.controller.show_frame("after_log_in"))
                            button_next.pack()
                            all_buttons.append(button_next)
                        else:
                            clear_labels()
                            clear_buttons()
                            myLabel1 = tk.Label(self,text = '         Password is incorrect, try again         \n\n')
                            myLabel1.pack()
                            myLabel1.config(fg='orangered')
                            all_labels.append(myLabel1)
                
                except:
                    clear_labels()
                    clear_buttons()
                    myLabel2 = tk.Label(self,text = 'Username does not exist, please try again\n\n')
                    myLabel2.pack()
                    myLabel2.config(fg='orangered')
                    all_labels.append(myLabel2)












class after_log_in(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        empty_space = tk.Label(self, text = "\n\n\n")     ### Add empty space for Welcome Text
        empty_space.pack()
        button_3 = tk.Button(self, text= "Add new account",
                           command=lambda: self.controller.show_frame("Add_account"))
        button_4 = tk.Button(self, text= "Access added accounts",
                           command=lambda: self.controller.show_frame("Access_account"))
        button_back = tk.Button(self, text="Logout",
                           command=lambda: controller.show_frame("Log_in"), fg='red')
        button_3.pack()
        button_4.pack()
        button_back.pack()

       
    









class Add_account(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        empty_space = tk.Label(self, text = "\n")     ### Add empty space 
        empty_space.pack()
        global entry_platform, entry_username
        entry_platform = tk.Entry(self, width=30)
        entry_platform.pack()
        entry_platform.insert(0, "Enter platform name...")
        entry_platform.bind('<FocusIn>', self.on_entry_click)  
        entry_platform.bind('<FocusOut>', self.on_focusout)
        entry_username = tk.Entry(self, width=30)
        entry_username.pack()
        entry_username.insert(0, "Enter username for that platform...")
        entry_username.bind('<FocusIn>', self.on_entry_click1)
        entry_username.bind('<FocusOut>', self.on_focusout1)
        entry_platform.bind('<Return>',  lambda x=None: self.add_account(entry_platform.get(), entry_username.get(), generate_password()))
        entry_username.bind('<Return>',  lambda x=None: self.add_account(entry_platform.get(), entry_username.get(), generate_password()))
        add_entry = tk.Button(self, text = "Add account",
                            command=lambda: self.add_account(entry_platform.get(), entry_username.get(), generate_password()))
        button_back1 = tk.Button(self, text="Back",
                           command=lambda: controller.show_frame("after_log_in"), fg='red')
        add_entry.pack()
        button_back1.pack()



    #### To make entry insert desappear on click ##########
    def on_entry_click(self, event):
        """function that gets called whenever entry is clicked"""
        if entry_platform.get() == 'Enter platform name...':
            entry_platform.delete(0, "end") # delete all the text in the entry
            entry_platform.insert(0, '') #Insert blank for user input
    def on_focusout(self, event):
         if entry_platform.get() == '':
            entry_platform.insert(0, 'Enter platform name...')
    def on_entry_click1(self, event):
        """function that gets called whenever entry is clicked"""
        if entry_username.get() == 'Enter username for that platform...':
            entry_username.delete(0, "end") # delete all the text in the entry
            entry_username.insert(0, '') #Insert blank for user input
    def on_focusout1(self, event):
         if entry_username.get() == '':
            entry_username.insert(0, "Enter username for that platform...")


    # for copying password
    def copy(self, text):
        self.clipboard_clear()
        self.clipboard_append(text)
        
    def add_account(self, platform, username, password):
        if platform == 'Enter platform name...' or platform == "":
            clear_labels()
            clear_buttons()
            lbel1 = tk.Label(self, text = "            Please enter platform name             \n\n\n\n", fg='orangered' )
            lbel1.pack()
            all_labels.append(lbel1)
        elif  username == "Enter username for that platform..." or username == "":
            clear_labels()
            clear_buttons()
            lbel2 = tk.Label(self, text = "             Please enter username for the platform entered              \n\n\n\n", fg='orangered' )
            lbel2.pack()
            all_labels.append(lbel2)
        else:
            try:
                if username in list_of_users[username_login].accounts[platform].keys():
                    clear_buttons()
                    clear_labels()
                    lbl = tk.Label(self, text= "        Username already added for this platform         \n\n\n\n", fg='orangered')
                    lbl.pack()
                    all_labels.append(lbl)
                else:
                    clear_buttons()
                    clear_labels()
                    list_of_users[username_login].add_account(platform, username, password)
                    myLabel6 = tk.Label(self, text = "             Account Added Successfully             \nThe randomly generated password is: ", fg='lime')
                    myLabel6.pack()
                    all_labels.append(myLabel6)
                    pwd = tk.Label(self, text = password)
                    pwd.pack()
                    all_labels.append(pwd)
                    copy_button = tk.Button(self, text = "Copy password", command = lambda: self.copy(password))
                    copy_button.pack()
                    all_buttons.append(copy_button)
            except:
                clear_buttons()
                clear_labels()
                list_of_users[username_login].add_account(platform, username, password)
                myLabel6 = tk.Label(self, text = "           Account Added Successfully           \nThe randomly generated password is: ", fg='lime')
                myLabel6.pack()
                all_labels.append(myLabel6)
                pwd = tk.Label(self, text = password)
                pwd.pack()
                all_labels.append(pwd)
                copy_button = tk.Button(self, text = "Copy password", command = lambda: self.copy(password))
                copy_button.pack()
                all_buttons.append(copy_button)
                










class Access_account(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        access_button = tk.Button(self, text = "Click to show available platforms", command= lambda: self.get_platform_buttons())
        button_back2 = tk.Button(self, text="Back",
                           command=lambda: controller.show_frame("after_log_in"),fg='red')
        access_button.pack()
        button_back2.pack()

    def get_platform_buttons(self):
        if list_of_users[username_login].accounts == {}:
            nlabel = tk.Label(self, text = '\nThere is no account added. Please add accounts first', fg='orangered')
            nlabel.pack()
            all_labels.append(nlabel)

        else:
            for platform in list_of_users[username_login].accounts:
                self.create_button(platform)
    
    global platform_buttons
    platform_buttons={}

    def create_button(self, platform):
        s = tk.Button(self, text= str(platform),command= lambda platform=platform: self.get_accounts(platform))
        s.pack()
        platform_buttons[platform] = s
        all_buttons.append(s)
    

    def get_accounts(self, platform):
        if platform in list_of_users[username_login].accounts:
            label1 = tk.Label(self, text = '\nAccounts for '+ platform + ' are: \n')
            label1.pack()
            label1.config(fg='light sky blue')
            all_labels.append(label1)
            for i,j in list_of_users[username_login].accounts[platform].items():
                label = tk.Label(self, text = 'username:  '+i+'\npassword:  '+j)
                label.pack()
                all_labels.append(label)
                bt1 = tk.Button(self, text= 'Copy username', command= lambda i=i: self.copy(i))
                bt1.pack()
                all_buttons.append(bt1)
                bt2 = tk.Button(self, text= 'Copy password', command= lambda j=j: self.copy(j))
                bt2.pack()
                all_buttons.append(bt2)
                bt3 = tk.Button(self, text= 'Delete account', fg = 'red')
                bt3.pack()
                bt3.config(command= lambda i=i, platform= platform, bt1=bt1, bt2=bt2, bt3=bt3, label = label, label1 = label1: self.delete_account(platform, i, bt1, bt2, bt3,  label, label1))
                all_buttons.append(bt3)
        
    
    def delete_account(self, platform, username, bt1, bt2, bt3, label, label1):
        if len(list_of_users[username_login].accounts[platform]) == 1:
            del list_of_users[username_login].accounts[platform]
            label1.destroy()
            platform_buttons[platform].pack_forget()
            if len(list_of_users[username_login].accounts)==0:
                nlabel = tk.Label(self, text = '\nThere is no account added. Please add accounts first', fg='orangered')
                nlabel.pack()
                all_labels.append(nlabel)

        else:
            del list_of_users[username_login].accounts[platform][username]
        dict_file = open("save_users.pkl", "wb")
        p.dump(list_of_users, dict_file)
        dict_file.close()
        bt1.destroy()
        bt2.destroy()
        label.destroy()
        bt3.pack_forget()
    
    def copy(self, text):
        self.clipboard_clear()
        self.clipboard_append(text)





# Run using mainloop()    
if __name__ == "__main__":
    app = Password_manager_app()
    app.mainloop()
    







