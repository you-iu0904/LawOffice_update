import tkinter as tk
var_username=''
var_acronym=''
var_sex=''
var_post=''
var_ReauthenticationTime=''
var_charge=''

#增加用户UI
def user_ui(adduser_page):
    global var_username
    global var_acronym
    global var_sex
    global var_post
    global var_ReauthenticationTime
    global var_charge

    var_username = tk.StringVar()
    var_acronym = tk.StringVar()
    var_sex = tk.IntVar()
    var_post = tk.StringVar()
    var_ReauthenticationTime = tk.StringVar()
    var_charge = tk.StringVar()

    username_la = tk.Label(adduser_page, text="Fee Earners:")
    username_la.place(x=50, y=40)
    username_entry = tk.Entry(adduser_page, textvariable=var_username)
    username_entry.place(x=130, y=40)
    acronym_la = tk.Label(adduser_page, text="Initials:")
    acronym_la.place(x=50, y=70)
    acronym_entry = tk.Entry(adduser_page, textvariable=var_acronym)
    acronym_entry.place(x=130, y=70)
    sex_la = tk.Label(adduser_page, text='Sex:')
    sex_la.place(x=50, y=100)
    sex_man = tk.Radiobutton(adduser_page, text='男', value=1, variable=var_sex)
    sex_man.place(x=130, y=100)
    sex_woman = tk.Radiobutton(adduser_page, text='女', value=2, variable=var_sex)
    sex_woman.place(x=180, y=100)
    post_la = tk.Label(adduser_page, text='Title:')
    post_la.place(x=50, y=130)
    numberChosen = tk.Entry(adduser_page, textvariable=var_post)
    numberChosen.place(x=130, y=130)
    ReauthenticationTime_la = tk.Label(adduser_page, text='Admitted Time:')
    ReauthenticationTime_la.place(x=50, y=160)
    ReauthenticationTime_entry = tk.Entry(adduser_page, textvariable=var_ReauthenticationTime)
    ReauthenticationTime_entry.place(x=145, y=160)
    charge_la = tk.Label(adduser_page, text='Hourly Rate:')
    charge_la.place(x=50, y=190)
    charge_entry = tk.Entry(adduser_page, textvariable=var_charge)
    charge_entry.place(x=130, y=190)
