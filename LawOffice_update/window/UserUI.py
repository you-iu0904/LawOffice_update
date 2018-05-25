import tkinter as tk

var_username=''
var_acronym=''
var_sex=''
var_post=''
var_ReauthenticationTime=''
var_charge=''

var_usernames=''
var_acronyms=''
var_sexs=''
var_posts=''
var_ReauthenticationTimes=''
var_charges=''

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

#显示用户的详细信息
def show_user(rests_page):
    global var_usernames
    global var_acronyms
    global var_sexs
    global var_posts
    global var_ReauthenticationTimes
    global var_charges

    var_usernames = tk.StringVar()
    var_acronyms = tk.StringVar()
    var_sexs = tk.IntVar()
    var_posts = tk.StringVar()
    var_ReauthenticationTimes = tk.StringVar()
    var_charges = tk.StringVar()

    usernmae_la2 = tk.Label(rests_page, text="Fee Earners:")
    username_entry2 = tk.Entry(rests_page, textvariable=var_usernames, state='disabled')
    acronym_la2 = tk.Label(rests_page, text="Initials:")
    acronym_entry2 = tk.Entry(rests_page, textvariable=var_acronyms)
    sex_la2 = tk.Label(rests_page, text='Sex:')
    sex_man2 = tk.Radiobutton(rests_page, text='男', value=1, variable=var_sexs)
    sex_woman2 = tk.Radiobutton(rests_page, text='女', value=2, variable=var_sexs)
    post_la2 = tk.Label(rests_page, text='Title:')
    numberChosen2 = tk.Entry(rests_page, textvariable=var_posts)
    ReauthenticationTime_la2 = tk.Label(rests_page, text='Admitted Time:')
    ReauthenticationTime_entry2 = tk.Entry(rests_page, textvariable=var_ReauthenticationTimes)
    charge_la2 = tk.Label(rests_page, text='Hourly Rate:')
    charge_entry2 = tk.Entry(rests_page, textvariable=var_charges)

    usernmae_la2.place(x=50, y=35)
    username_entry2.place(x=145, y=35)
    acronym_la2.place(x=50, y=65)
    acronym_entry2.place(x=145, y=65)
    sex_la2.place(x=50, y=95)
    sex_man2.place(x=145, y=95)
    sex_woman2.place(x=180, y=95)
    post_la2.place(x=50, y=125)
    numberChosen2.place(x=145, y=125)
    ReauthenticationTime_la2.place(x=50, y=155)
    ReauthenticationTime_entry2.place(x=145, y=155)
    charge_la2.place(x=50, y=185)
    charge_entry2.place(x=145, y=185)

def clear_data():
    var_usernames.set('')
    var_acronyms.set('')
    var_sexs.set('')
    var_posts.set('')
    var_ReauthenticationTimes.set('')
    var_charges.set('')


