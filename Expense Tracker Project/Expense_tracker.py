import random
import tkinter as tk
from tkinter import PhotoImage
import tkinter.font as tkfont
from tkinter import ttk
from tkmacosx import Button
from tkcalendar import DateEntry
from datetime import date
import requests
from bs4 import BeautifulSoup as bs
import pickle
from tkinter import W
import matplotlib.pyplot as plt
import numpy as np


today = date.today()
today_date = today.strftime("%B %d, 20%y")
current_month = today.strftime("%m/%y")

list_of_months = [
    "01/21",
    "02/21",
    "03/21",
    "04/21",
    "05/21",
    "06/21",
    "07/21",
    "08/21",
    "09/21",
    "10/21",
    "11/21",
    "12/21",
    "01/22",
    "02/22",
    "03/22",
    "04/22",
    "05/22",
    "06/22",
    "07/22",
    "08/22",
    "09/22",
    "10/22",
    "11/22",
    "12/22",
]



class Monthly_data:
    def __init__(self, month_year):
        self.month = month_year
        self.income = {}
        self.expense = {}
        self.table_Data = []
        self.income_sum = 0
        self.expense_sum = 0

    def get_sum_income(self):
        in_total = 0
        for i in self.income.values():
            in_total += sum(i)
        self.income_sum = in_total
        return in_total

    def get_sum_expense(self):
        ex_total = 0
        for i in self.expense.values():
            ex_total += sum(i)
        self.expense_sum = ex_total
        return ex_total

    def get_month_net(self):
        x = self.get_sum_income() - self.get_sum_expense()
        return x


all_labels = []


def destroy_labels():
    for x in all_labels:
        x.destroy()



def previous_month(i):
    return list_of_months[i-1]


def next_month(i):

    return list_of_months[i+1]


class SampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.font2 = tkfont.Font(family="Century", size=30, weight="bold")
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for page in (Home, Income, Expense, Summary, Covid_19):
            page_name = page.__name__
            frame = page(parent=container, controller=self)
            frame.config(bg="lightcyan")
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("Home")

    def show_frame(self, page_name):
        # Show a frame for the given page name
        frame = self.frames[page_name]
        ## For Fixing a weird bug where title disappears in Summary Page
        if page_name == 'Summary':
            month_label = tk.Label(frame, text="Summary: \nCurrent Month " + current_month, font=self.font2,
                                   bg="lightcyan", fg='steelblue4')
            month_label.place(x=319, y=40)
            all_labels.append(month_label)

        frame.tkraise()


try:
    a_file = open("monthly_data.pkl", "rb")
    a_file = project_data = pickle.load(a_file)
    print("pickle loaded")
except:
    project_data = {}
    for month in list_of_months:
        project_data[month] = Monthly_data(month)
    a_file = open("monthly_data.pkl", "wb")
    pickle.dump(project_data, a_file)
    print("pickle created")
    print(project_data)


def save_file():
    a_file = open("monthly_data.pkl", "wb")
    a_file = pickle.dump(project_data, a_file)



def update_label_position(label, x, y, text):
    if len(text) == 1:
        label.place(x=x, y=y)
    if len(text) > 1:
        label.place(x=(x - (10 * len(text))), y=y)


btnState = False


class Home(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.topFrame = tk.Frame(self, bg="lightcyan", height=60, width=200)
        self.topFrame.place(x=0, y=0)
        self.navIcon = PhotoImage(file="menu.png")
        self.closeIcon = PhotoImage(file="close.png")
        self.circle = PhotoImage(file="circle_medium.png")
        self.font = tkfont.Font(family="Segoe Script", size=20)
        self.font_bold = tkfont.Font(family="Century", size=20, weight="bold")
        self.font2 = tkfont.Font(family="Century", size=30, weight="bold")
        self.font3 = tkfont.Font(family="Century", size=40, weight="bold")
        date_label = tk.Label(
            self.topFrame, text=today_date, font=self.font, bg="lightcyan"
        )
        date_label.place(x=70, y=18)
        date_label = tk.Label(
            self, text="Current Month at a Glance", font=self.font2, bg="lightcyan", fg='steelblue4'
        )
        date_label.place(x=260, y=70)
        tk.Label(self, image=self.circle, bg="lightcyan").place(x=270, y=170)
        tk.Label(self, text="Expense", bg="lightcyan", font=self.font).place(
            x=80, y=230
        )
        tk.Label(self, text="Total", bg="white", font=self.font).place(x=420, y=230)
        tk.Label(self, text="Income", bg="lightcyan", font=self.font).place(
            x=700, y=230
        )
        project_data[current_month].get_sum_income()
        project_data[current_month].get_sum_expense()
        global total_expense_label, total_income_label, net_label
        total_expense_label = tk.Label(
            self,
            text=project_data[current_month].expense_sum,
            fg="red",
            bg="lightcyan",
            font=self.font3,
        )
        update_label_position(
            total_expense_label, 110, 320, str(project_data[current_month].expense_sum)
        )
        total_income_label = tk.Label(
            self,
            text=project_data[current_month].income_sum,
            fg="green",
            bg="lightcyan",
            font=self.font3,
        )
        update_label_position(
            total_income_label, 720, 320, str(project_data[current_month].income_sum)
        )
        net_label = tk.Label(
            self,
            text=project_data[current_month].get_month_net(),
            fg="grey",
            bg="white",
            font=self.font3,
        )
        update_label_position(
            net_label, 430, 320, str(project_data[current_month].get_month_net())
        )
        self.navRoot = tk.Frame(self, bg="lightblue", height=1000, width=200)
        self.navRoot.place(x=-200, y=0)
        tk.Label(
            self.navRoot, bg="skyblue", fg="white", height=3, width=300, padx=0
        ).place(x=0, y=0)
        tk.Label(
            self.navRoot, text="Menu", fg="white", bg="skyblue", font=self.font
        ).place(x=50, y=20)
        self.navbarBtn = Button(
            self.topFrame,
            image=self.navIcon,
            activebackground="lightblue",
            bd=0,
            padx=-15,
            command=self.switch,
            borderless=True,
        )
        self.navbarBtn.place(x=10, y=10)
        self.y = 80
        self.menu_buttons = ["Home", "Income", "Expense", "Summary", "Covid_19"]
        for i in range(5):
            Button(
                self.navRoot,
                text=self.menu_buttons[i],
                font="BahnschriftLight 15",
                bg="white",
                fg="orange",
                activebackground="lightblue",
                activeforeground="darkorange",
                borderless=True,
                command=lambda x=i: [
                    controller.show_frame(self.menu_buttons[x]),
                    self.switch(),
                ],
            ).place(x=25, y=self.y)
            self.y += 40
        self.closeBtn = Button(
            self.navRoot,
            image=self.closeIcon,
            bg="white",
            activebackground="skyblue",
            command=self.switch,
            borderless=True,
            padx=-15,
        )
        self.closeBtn.place(x=150, y=10)

    def switch(self):
        global btnState
        if btnState is True:
            # create animated Navbar closing:
            for x in range(301):
                self.navRoot.place(x=-(10 * x), y=0)
                self.topFrame.update()

            # resetting widget colors:
            self.topFrame.config(bg="lightcyan")

            # turning button OFF:
            btnState = False
        else:
            # make root dim:
            self.topFrame.config(bg="lightcyan")

            # created animated Navbar opening:
            for x in range(-300, 0):
                self.navRoot.place(x=10 * x, y=0)
                self.topFrame.update()

            # turing button ON:
            btnState = True


class Income(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.topFrame = tk.Frame(self, bg="lightcyan", height=60, width=100)
        self.topFrame.place(x=0, y=0)
        self.navIcon = PhotoImage(file="menu.png")
        self.closeIcon = PhotoImage(file="close.png")
        self.font = tkfont.Font(family="Century", size=20)
        self.font_bold = tkfont.Font(family="Century", size=20, weight="bold")
        self.font2 = tkfont.Font(family="Century", size=30, weight="bold")
        self.font3 = tkfont.Font(family="Century", size=40, weight="bold")
        date_label = tk.Label(self, text="Add Income", font=self.font2, bg="lightcyan", fg='steelblue4')
        date_label.place(x=360, y=40)
        income_label = tk.Label(
            self, text="Income Amount:", font=self.font, bg="lightcyan"
        )
        income_label.place(x=200, y=100)
        income_entry = tk.Entry(self)
        income_entry.place(x=500, y=105)
        date_label2 = tk.Label(self, text=" Date:", font=self.font, bg="lightcyan")
        date_label2.place(x=200, y=150)
        date_entry2 = DateEntry(self, bg="lightcyan")
        date_entry2.place(x=500, y=155)
        add_btn = Button(
            self,
            text="Add Income",
            borderless=True,
            command=lambda: self.add_income(date_entry2.get(), income_entry.get()),
        )
        add_btn.place(x=500, y=200)
        self.navRoot = tk.Frame(self, bg="lightblue", height=1000, width=200)
        self.navRoot.place(x=-200, y=0)
        tk.Label(
            self.navRoot, bg="skyblue", fg="white", height=3, width=300, padx=0
        ).place(x=0, y=0)
        tk.Label(
            self.navRoot, text="Menu", fg="white", bg="skyblue", font=self.font
        ).place(x=50, y=20)
        self.navbarBtn = Button(
            self.topFrame,
            image=self.navIcon,
            activebackground="lightblue",
            bd=0,
            padx=-15,
            command=self.switch,
            borderless=True,
        )
        self.navbarBtn.place(x=10, y=10)
        self.y = 80
        self.menu_buttons = ["Home", "Income", "Expense", "Summary", "Covid_19"]
        for i in range(5):
            Button(
                self.navRoot,
                text=self.menu_buttons[i],
                font="BahnschriftLight 15",
                bg="white",
                fg="orange",
                activebackground="lightblue",
                activeforeground="darkorange",
                borderless=True,
                command=lambda x=i: [
                    controller.show_frame(self.menu_buttons[x]),
                    self.switch(),
                ],
            ).place(x=25, y=self.y)
            self.y += 40
        self.closeBtn = Button(
            self.navRoot,
            image=self.closeIcon,
            bg="white",
            activebackground="skyblue",
            command=self.switch,
            borderless=True,
            padx=-15,
        )
        self.closeBtn.place(x=150, y=10)

    def add_income(self, date, amount):
        destroy_labels()
        try:
            amount_int = int(amount)
            date_split = date.split("/")
            income_month_year = str(month_key[date_split[0]]) + "/" + str(date_split[2])
            total_income_label.config(
                text=project_data[income_month_year].get_sum_income() + amount_int
            )
            if income_month_year == current_month:
                net_label.config(
                    text=project_data[income_month_year].get_month_net() + amount_int
                )
                summary_table.insert(parent='', index='end', iid=random.randint(60000, 600000),
                                     values=('income', date, '', amount))
            if date in project_data[income_month_year].income:
                project_data[income_month_year].income[date].append(amount_int)
                project_data[income_month_year].table_Data.append(('income', date, '', amount))
                save_file()
            else:
                project_data[income_month_year].income[date] = [amount_int]
                project_data[income_month_year].table_Data.append(('income', date, '', amount))
                save_file()
            project_data[current_month].get_sum_income()
            add_income_label = tk.Label(self, text='Income Successfully Added', fg='green', bg='lightcyan')
            add_income_label.place(x=500, y=230)
            all_labels.append(add_income_label)
            update_label_position(
                total_income_label, 720, 320, str(project_data[current_month].income_sum))
            update_label_position(
                net_label, 430, 320, str(project_data[current_month].get_month_net()))
        except:
            error_label = tk.Label(self, text="Please enter numbers only", fg="red", bg="lightcyan")
            error_label.place(x=500, y=230)
            all_labels.append(error_label)


    def switch(self):
        global btnState
        if btnState is True:
            # create animated Navbar closing:
            for x in range(301):
                self.navRoot.place(x=-(10 * x), y=0)
                self.topFrame.update()

            # resetting widget colors:
            self.topFrame.config(bg="lightcyan")

            # turning button OFF:
            btnState = False
        else:
            # make root dim:
            self.topFrame.config(bg="lightcyan")

            # created animated Navbar opening:
            for x in range(-300, 0):
                self.navRoot.place(x=10 * x, y=0)
                self.topFrame.update()

            # turing button ON:
            btnState = True


month_key = {
    "1": "01",
    "2": "02",
    "3": "03",
    "4": "04",
    "5": "05",
    "6": "06",
    "7": "07",
    "8": "08",
    "9": "09",
    "10": "10",
    "11": "11",
    "12": "12",
}


class Expense(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.font = tkfont.Font(family="Century", size=20)
        self.topFrame = tk.Frame(self, bg="lightcyan", height=60, width=100)
        self.topFrame.place(x=0, y=0)
        self.font_bold = tkfont.Font(family="Century", size=20, weight="bold")
        self.font2 = tkfont.Font(family="Century", size=30, weight="bold")
        self.font3 = tkfont.Font(family="Century", size=40, weight="bold")
        date_label = tk.Label(self, text="Add Expense", font=self.font2, bg="lightcyan", fg='steelblue4')
        date_label.place(x=360, y=40)
        tk.Label(self, text="Date:", font=self.font, bg="lightcyan").place(x=200, y=100)
        date = DateEntry(self, bg="lightcyan")
        date.place(x=500, y=105)
        tk.Label(self, text="Category:", font=self.font, bg="lightcyan").place(
            x=200, y=150
        )
        categories = ttk.Combobox(self)

        global categories_data
        try:
            b_file = open("categories.pkl", "rb")
            categories_data = pickle.load(b_file)
            print("categories loaded")
        except:
            categories_data = ["Food", "Home", "Groceries", "Social life", "Transportation", "Apparel", "Health", "Education"]
            b_file = open("categories.pkl", "wb")
            b_file = pickle.dump(categories_data, b_file)
            print("categories created")
            print(categories_data)

        categories["values"] = categories_data
        categories.place(x=500, y=155)
        tk.Label(self, text="Price:", font=self.font, bg="lightcyan").place(
            x=200, y=200
        )
        price = tk.Entry(self, selectborderwidth=0)
        price.place(x=500, y=200)
        Button(
            self,
            text="Add Expense",
            borderless=True,
            command=lambda: self.add_expense(date.get(), categories.get(), price.get()),
        ).place(x=500, y=250)

        self.navIcon = PhotoImage(file="menu.png")
        self.closeIcon = PhotoImage(file="close.png")

        self.navRoot = tk.Frame(self, bg="lightblue", height=1000, width=200)
        self.navRoot.place(x=-200, y=0)
        tk.Label(
            self.navRoot, bg="skyblue", fg="white", height=3, width=300, padx=0
        ).place(x=0, y=0)
        tk.Label(
            self.navRoot, text="Menu", fg="white", bg="skyblue", font=self.font
        ).place(x=50, y=20)
        self.navbarBtn = Button(
            self.topFrame,
            image=self.navIcon,
            activebackground="lightblue",
            bd=0,
            padx=-15,
            command=self.switch,
            borderless=True,
        )
        self.navbarBtn.place(x=10, y=10)
        self.y = 80
        self.menu_buttons = ["Home", "Income", "Expense", "Summary", "Covid_19"]
        for i in range(5):
            Button(
                self.navRoot,
                text=self.menu_buttons[i],
                font="BahnschriftLight 15",
                bg="white",
                fg="orange",
                activebackground="lightblue",
                activeforeground="darkorange",
                borderless=True,
                command=lambda x=i: [
                    controller.show_frame(self.menu_buttons[x]),
                    self.switch(),
                ],
            ).place(x=25, y=self.y)
            self.y += 40
        self.closeBtn = Button(
            self.navRoot,
            image=self.closeIcon,
            bg="white",
            activebackground="skyblue",
            command=self.switch,
            borderless=True,
            padx=-15,
        )
        self.closeBtn.place(x=150, y=10)


    def add_expense(self, date, category, price):
        destroy_labels()
        try:
            price_int = int(price)
            if category not in categories_data:
                categories_data.append(category)
                b_file = open("categories.pkl", "wb")
                b_file = pickle.dump(categories_data, b_file)
            date_split = date.split("/")
            expense_month_year = str(month_key[date_split[0]]) + "/" + str(date_split[2])
            if expense_month_year == current_month:
                total_expense_label.config(
                    text=str(project_data[expense_month_year].get_sum_expense() + price_int)
                )
                net_label.config(
                    text=project_data[expense_month_year].get_month_net() - price_int
                )
                summary_table.insert(parent='', index='end', iid=random.randint(100, 6000),
                                     values=('expense', date, category, price))
            if category in project_data[expense_month_year].expense.keys():
                project_data[expense_month_year].expense[category].append(price_int)
                project_data[expense_month_year].table_Data.append(('expense', date, category, price))
                save_file()
            else:
                project_data[expense_month_year].expense[category] = [price_int]
                project_data[expense_month_year].table_Data.append(('expense', date, category, price))
                save_file()
            project_data[current_month].get_sum_expense()
            project_data[current_month].get_month_net()
            add_expense_label = tk.Label(self, text="Expense Successfully Added", fg="green", bg="lightcyan")
            add_expense_label.place(x=500, y=280)
            all_labels.append(add_expense_label)
            update_label_position(
                total_expense_label, 110, 320, str(project_data[current_month].expense_sum))
            update_label_position(
                net_label, 430, 320, str(project_data[current_month].get_month_net()))
        except:
            error_expense = tk.Label(self, text="Please enter numbers only", fg="red", bg="lightcyan")
            error_expense.place(x=500, y=280)
            all_labels.append(error_expense)


    def switch(self):
        global btnState
        if btnState is True:
            # create animated Navbar closing:
            for x in range(301):
                self.navRoot.place(x=-(10 * x), y=0)
                self.topFrame.update()

            # resetting widget colors:
            self.topFrame.config(bg="lightcyan")

            # turning button OFF:
            btnState = False
        else:
            # make root dim:
            self.topFrame.config(bg="lightcyan")

            # created animated Navbar opening:
            for x in range(-300, 0):
                self.navRoot.place(x=10 * x, y=0)
                self.topFrame.update()

            # turing button ON:
            btnState = True


class Summary(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.topFrame = tk.Frame(self, bg="lightcyan", height=60, width=100)
        self.topFrame.place(x=0, y=0)
        self.navIcon = PhotoImage(file="menu.png")
        self.closeIcon = PhotoImage(file="close.png")
        self.font = tkfont.Font(family="Century", size=20, weight="bold")
        self.click = 0
        self.font2 = tkfont.Font(family="Century", size=30, weight="bold")

        self.navRoot = tk.Frame(self, bg="lightblue", height=1000, width=200)
        self.navRoot.place(x=-200, y=0)
        tk.Label(
            self.navRoot, bg="skyblue", fg="white", height=3, width=300, padx=0
        ).place(x=0, y=0)
        tk.Label(
            self.navRoot, text="Menu", fg="white", bg="skyblue", font=self.font
        ).place(x=50, y=20)
        self.navbarBtn = Button(
            self.topFrame,
            image=self.navIcon,
            activebackground="lightblue",
            bd=0,
            padx=-15,
            command=self.switch,
            borderless=True,
        )
        self.navbarBtn.place(x=10, y=10)
        self.y = 80
        self.menu_buttons = ["Home", "Income", "Expense", "Summary", "Covid_19"]
        for i in range(5):
            Button(
                self.navRoot,
                text=self.menu_buttons[i],
                font="BahnschriftLight 15",
                bg="white",
                fg="orange",
                activebackground="lightblue",
                activeforeground="darkorange",
                borderless=True,
                command=lambda x=i: [
                    controller.show_frame(self.menu_buttons[x]),
                    self.switch(),
                ],
            ).place(x=25, y=self.y)
            self.y += 40
        self.closeBtn = Button(
            self.navRoot,
            image=self.closeIcon,
            bg="white",
            activebackground="skyblue",
            command=self.switch,
            borderless=True,
            padx=-15,
        )
        self.closeBtn.place(x=150, y=10)
        #month_label = tk.Label(self, text="Summary: \nCurrent Month " + current_month, font=self.font2, bg="lightcyan")
        #month_label.place(x=319, y=40)
        #all_labels.append(month_label)
        global summary_table
        table_x = 200
        table_y = 140

        summary_table = ttk.Treeview(self)
        vsb = ttk.Scrollbar(self, orient="vertical", command=summary_table.yview)
        vsb.place(x=table_x+480, y=table_y, height=210)

        summary_table.configure(yscrollcommand=vsb.set)
        summary_table['columns'] = ('Type', 'Date', 'Category', 'Amount')
        summary_table.column('#0', width=0, minwidth=0)
        summary_table.column('Type', anchor=W, width=120, minwidth=25)
        summary_table.column('Date', anchor=W, width=120)
        summary_table.column('Category', anchor=W, width=120)
        summary_table.column('Amount', anchor=W, width=120)
        summary_table.heading('Type', text='Type', anchor=W)
        summary_table.heading('Date', text='Data', anchor=W)
        summary_table.heading('Category', text='Category', anchor=W)
        summary_table.heading('Amount', text='Amount', anchor=W)
        iid=0
        for c in project_data[current_month].table_Data:
            summary_table.insert(parent='', index='end', iid=iid, values=c)
            iid+=1
        summary_table.place(x=table_x, y=table_y)
        Button(self, text=' < ',borderless=True , command=lambda: self.destroy_and_create_table_previous(list_of_months.index(current_month)), width=60).place(x=300, y=360)
        Button(self, text=' > ',borderless=True, command=lambda: self.destroy_and_create_table_next(list_of_months.index(current_month)), width=60).place(x=540, y=360)
        Button(self, text='Delete Selected', command=lambda: self.delete(), borderless=True, width=120, fg='red').place(x=390, y=360)

        Button(self, text=' Pie Graph',
               command=lambda: self.show_pie_graph(), width=200, borderless=True, bg='lightblue').place(x=350, y=420)
        Button(self, text='Expenses by Month',
               command=lambda: self.show_line_graph(), width=200, borderless=True, bg='lightblue').place(x=350, y=450)
        Button(self, text='Analysis by Month',
               command=lambda: self.show_bar_graph(), width=200, borderless=True, bg='lightblue').place(x=350, y=480)


    def destroy_and_create_table_previous(self, index):
        self.click = self.click - 1
        destroy_labels()
        if self.click == 0:
            month_label = tk.Label(self, text="Summary: \nCurrent Month " + current_month, font=self.font2,
                                   bg="lightcyan", fg='steelblue4')
            month_label.place(x=319, y=40)
            all_labels.append(month_label)
        else:
            month_label = tk.Label(self, text="           Summary: \n      " + list_of_months[index + self.click], font=self.font2, bg="lightcyan", fg='steelblue4')
            month_label.place(x=320, y=40)
            all_labels.append(month_label)
        print(self.click)
        for data in summary_table.get_children():
            summary_table.delete(data)
        iid = 0
        for c in project_data[list_of_months[index + self.click]].table_Data:
            summary_table.insert(parent='', index='end', iid=iid, values=c)
            iid += 1

    def destroy_and_create_table_next(self, index):
        self.click += 1
        print(self.click)
        destroy_labels()
        if self.click == 0:
            month_label = tk.Label(self, text="Summary: \nCurrent Month " + current_month, font=self.font2,
                                   bg="lightcyan", fg='steelblue4')
            month_label.place(x=319, y=40)
            all_labels.append(month_label)
        else:
            month_label = tk.Label(self, text="           Summary: \n      " + list_of_months[index + self.click],
                                   font=self.font2, bg="lightcyan", fg='steelblue4')
            month_label.place(x=320, y=40)
        for data in summary_table.get_children():
            summary_table.delete(data)
        iid = 0
        for c in project_data[list_of_months[index + self.click]].table_Data:
            summary_table.insert(parent='', index='end', iid=iid, values=c)
            iid += 1

    def delete(self):
        selected_item = summary_table.selection()[0]  ## get selected item
        item_text = summary_table.item(selected_item)
        if item_text['values'][0] == 'expense':
            if len(project_data[list_of_months[list_of_months.index(current_month) + self.click]].expense[item_text['values'][2]]) == 1:
                del project_data[list_of_months[list_of_months.index(current_month) + self.click]].expense[
                item_text['values'][2]]
                print('deleted key')
                print(project_data[list_of_months[list_of_months.index(current_month) + self.click]].expense)
            else:
                project_data[list_of_months[list_of_months.index(current_month) + self.click]].expense[item_text['values'][2]].remove(item_text['values'][3])
                print(project_data[list_of_months[list_of_months.index(current_month) + self.click]].expense)

            save_file()
            if list_of_months[list_of_months.index(current_month) + self.click] == current_month:
                total_expense_label.config(text=project_data[current_month].get_sum_expense())
                net_label.config(text=project_data[current_month].get_month_net())
                update_label_position(
                    total_expense_label, 110, 320, str(project_data[current_month].expense_sum))
                update_label_position(
                    net_label, 430, 320, str(project_data[current_month].get_month_net()))
        if item_text['values'][0] == 'income':
            print(project_data[list_of_months[list_of_months.index(current_month) + self.click]].income)
            project_data[list_of_months[list_of_months.index(current_month) + self.click]].income[
                item_text['values'][1]].remove(item_text['values'][3])
            save_file()
            if list_of_months[list_of_months.index(current_month) + self.click] == current_month:
                total_income_label.config(text=project_data[current_month].get_sum_income())
                net_label.config(text=project_data[current_month].get_month_net())
                update_label_position(
                    total_income_label, 720, 320, str(project_data[current_month].income_sum))
                update_label_position(
                    net_label, 430, 320, str(project_data[current_month].get_month_net()))
        print(project_data[current_month].table_Data)
        print(len(project_data[list_of_months[list_of_months.index(current_month) + self.click]].table_Data))
        table_data_2 = project_data[list_of_months[list_of_months.index(current_month) + self.click]].table_Data.copy()
        c = 0
        del_count = 0
        while True:
            if del_count == 1:
                break
            if table_data_2[c] == (item_text['values'][0], item_text['values'][1], item_text['values'][2], str(item_text['values'][3])):
                del project_data[list_of_months[list_of_months.index(current_month) + self.click]].table_Data[c]
                save_file()
                del_count+=1
            c+=1
        summary_table.delete(selected_item)


    def show_pie_graph(self):
        display_month = list_of_months[list_of_months.index(current_month) + self.click]
        labels = []
        sizes = []
        for c in project_data[display_month].expense.keys():
            labels.append(c)
        for v in project_data[display_month].expense.values():
            y = sum(v)/project_data[display_month].get_sum_expense()
            sizes.append(y)
        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
                shadow=True, startangle=90)
        ax1.axis('equal')
        fig1.show()

    def show_line_graph(self):
        months = []
        total_expense = []
        for a in list_of_months:
            z = project_data[a].get_sum_expense()
            if z > 1:
                months.append(a)
                total_expense.append(z)
        fig1, ax1 = plt.subplots()
        ax1.set_title('Expenses by Month')
        ax1.set_xlabel('Month')
        ax1.set_ylabel('Total Expense')
        ax1.plot(months, total_expense)
        fig1.show()

    def show_bar_graph(self):
        months = []
        total_expense = []
        total_income = []
        for a in list_of_months:
            z = project_data[a].get_sum_expense()
            b = project_data[a].get_sum_income()
            if z > 1 or b > 1:
                months.append(a)
                total_expense.append(z)
                total_income.append(b)
        x = np.arange(len(months))
        width = 0.35
        fig, ax = plt.subplots()
        rects1 = ax.bar(x - width / 2, total_income, width, label='Income')
        rects2 = ax.bar(x + width / 2, total_expense, width, label='Expense')
        ax.set_ylabel('Amount')
        ax.set_title('Income/Expense by Month')
        ax.set_xticks(x)
        ax.set_xticklabels(months)
        ax.legend()
        ax.bar_label(rects1, padding=3)
        ax.bar_label(rects2, padding=3)

        fig.tight_layout()

        fig.show()


    def switch(self):
        global btnState
        if btnState is True:
            # create animated Navbar closing:
            for x in range(301):
                self.navRoot.place(x=-(10 * x), y=0)
                self.topFrame.update()

            # resetting widget colors:
            self.topFrame.config(bg="lightcyan")

            # turning button OFF:
            btnState = False
        else:
            # make root dim:
            self.topFrame.config(bg="lightcyan")

            # created animated Navbar opening:
            for x in range(-300, 0):
                self.navRoot.place(x=10 * x, y=0)
                self.topFrame.update()

            # turing button ON:
            btnState = True


class Covid_19(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.topFrame = tk.Frame(self, bg="lightcyan", height=60, width=100)
        self.topFrame.place(x=0, y=0)
        self.navIcon = PhotoImage(file="menu.png")
        self.closeIcon = PhotoImage(file="close.png")
        self.font = tkfont.Font(family="Century", size=20, weight="bold")
        self.navRoot = tk.Frame(self, bg="lightblue", height=1000, width=200)
        self.navRoot.place(x=-200, y=0)
        self.retrieve_data = False

        tk.Label(
            self.navRoot, bg="skyblue", fg="white", height=3, width=300, padx=0
        ).place(x=0, y=0)
        tk.Label(
            self.navRoot, text="Menu", fg="white", bg="skyblue", font=self.font
        ).place(x=50, y=20)
        self.navbarBtn = Button(
            self.topFrame,
            image=self.navIcon,
            activebackground="lightblue",
            bd=0,
            padx=-15,
            command=self.switch,
            borderless=True,
        )
        self.navbarBtn.place(x=10, y=10)
        self.y = 80
        self.menu_buttons = ["Home", "Income", "Expense", "Summary", "Covid_19"]
        for i in range(5):
            Button(
                self.navRoot,
                text=self.menu_buttons[i],
                font="BahnschriftLight 15",
                bg="white",
                fg="orange",
                activebackground="lightblue",
                activeforeground="darkorange",
                borderless=True,
                command=lambda x=i: [
                    controller.show_frame(self.menu_buttons[x]),
                    self.switch(),
                ],
            ).place(x=25, y=self.y)
            self.y += 40
        self.closeBtn = Button(
            self.navRoot,
            image=self.closeIcon,
            bg="white",
            activebackground="skyblue",
            command=self.switch,
            borderless=True,
            padx=-15,
        )
        self.closeBtn.place(x=150, y=10)
        tk.Label(
            self,
            bg="lightcyan",
            text="Check Covid-19 Information by Country",
            font=self.font,
        ).place(x=250, y=50)
        input = tk.Entry(self, text="Enter Country Name")
        input.place(x=350, y=100)
        go = Button(
            self, text="Check", command=lambda: self.get_corona_info(input.get()), borderless=True
        )
        go.place(x=395, y=150)

    def get_corona_info(self, country_input):
        if self.retrieve_data == False:
            url = "https://www.worldometers.info/coronavirus/"
            r = requests.get(url)
            htmlcontent = r.content
            soup = bs(htmlcontent, "html.parser")
            country = soup.find_all("a", class_="mt_a")[:120]
            names = [
                "sno",
                "Country",
                "Totalcases",
                "NewCases",
                "TotalDeaths",
                "NewDeaths",
                "TotalRecovered",
                "NewRecovered",
                "ActiveCases",
                "Serious",
                "TotCases/1M pop",
                "Deaths/1M pop",
                "TotalTests",
                "Tests/1M pop",
            ]
            tbody = soup.find_all("tbody")[0]
            country_info = [
                a.string if a.string is not None else ""
                for i in tbody.find_all("tr")[8:]
                for a in i.find_all("td")[:14]
            ]
            self.covid_info = {
                x: {y: z for y, z in zip(names, country_info[ind * len(names) :])}
                for ind, x in enumerate([i.string for i in country])
            }
            self.retrieve_data = True

        # country_input = input("Please insert country name: ")
        try:
            destroy_labels()
            data_info = (
                "Total case:   "
                + str(self.covid_info[country_input]["Totalcases"])
                + "\nNew case:   "
                + str(self.covid_info[country_input]["NewCases"])
                + "\nNew Deaths:   "
                + str(self.covid_info[country_input]["NewDeaths"])
                + "\nTotal Recovered:   "
                + str(self.covid_info[country_input]["TotalRecovered"])
                + "\nNew Recovered:   "
                + str(self.covid_info[country_input]["NewRecovered"])
                + "\nActive cases:   "
                + str(self.covid_info[country_input]["ActiveCases"])
            )
            output = tk.Label(
                self, text=data_info, bg="lightcyan", font=("Haveltica", 15)
            )
            output.place(x=360, y=200)
            all_labels.append(output)
        except:
            destroy_labels()
            error = tk.Label(self, text="Error", fg="red", bg="lightcyan")
            error.place(x=425, y=180)
            all_labels.append(error)

    def switch(self):
        global btnState
        if btnState is True:
            # create animated Navbar closing:
            for x in range(301):
                self.navRoot.place(x=-(10 * x), y=0)
                self.topFrame.update()

            # resetting widget colors:
            self.topFrame.config(bg="lightcyan")

            # turning button OFF:
            btnState = False
        else:
            # make root dim:
            self.topFrame.config(bg="lightcyan")

            # created animated Navbar opening:
            for x in range(-300, 0):
                self.navRoot.place(x=10 * x, y=0)
                self.topFrame.update()

            # turing button ON:
            btnState = True


if __name__ == "__main__":
    app = SampleApp()
    app.minsize(900, 600)
    app.title("Expense Manager by Win")
    app.mainloop()
