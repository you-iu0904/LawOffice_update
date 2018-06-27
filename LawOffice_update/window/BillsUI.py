from tkinter import ttk
import tkinter as tk


var_serialNum=''
var_user=''
var_incident=''
var_jobDate_y=''
var_jobDate_m=''
var_jobDate_d=''
var_serDate_hrs=''
var_serDate_mins=''
var_copying=''

var_filing=''
var_serving=''

users=[]
def bills_ui(bills_page):
    global users
    global var_serialNum
    global var_user
    global var_incident
    global var_jobDate_y
    global var_jobDate_m
    global var_jobDate_d
    global var_serDate_hrs
    global var_serDate_mins
    global var_copying
    global var_filing
    global var_serving

    var_serialNum=tk.StringVar()
    var_user = tk.StringVar()
    var_incident = tk.StringVar()
    var_jobDate_y = tk.StringVar()
    var_jobDate_m = tk.StringVar()
    var_jobDate_d = tk.StringVar()
    var_serDate_hrs = tk.StringVar()
    var_serDate_mins = tk.StringVar()
    var_copying = tk.StringVar()
    var_filing = tk.StringVar()
    var_serving = tk.StringVar()
    var_copying.set('0')
    var_filing.set('0')
    var_serving.set('0')
    var_serDate_hrs.set('0')
    var_serDate_mins.set('0')
    # 添加收据单_控件
    serialNum = tk.Entry(bills_page, textvariable=var_serialNum)
    user_la = tk.Label(bills_page, text="Fee Earners:")
    user_la.place(x=50, y=40)
    user_box = ttk.Combobox(bills_page, width=12, textvariable=var_user)
    user_box['values'] = users
    user_box['state']='readonly'
    user_box.place(x=150, y=40)

    incident_la = tk.Label(bills_page, text="Narrative:")
    incident_la.place(x=50, y=70)
    incident_entry = tk.Entry(bills_page, textvariable=var_incident)
    incident_entry.place(x=150, y=70)

    startDate_la = tk.Label(bills_page, text='Date:')
    startDate_la.place(x=50, y=100)
    startDate_la1=tk.Label(bills_page,text='Y:')
    startDate_la1.place(x=150,y=100)
    startDate_la2=tk.Label(bills_page,text='M:')
    startDate_la2.place(x=210,y=100)
    startDate_la3=tk.Label(bills_page,text='D:')
    startDate_la3.place(x=270,y=100)
    startDate_entry1 = tk.Entry(bills_page, width=5, textvariable=var_jobDate_y)
    startDate_entry1.place(x=170, y=100)
    startDate_entry2 = tk.Entry(bills_page, width=5, textvariable=var_jobDate_m)
    startDate_entry2.place(x=230, y=100)
    startDate_entry3 = tk.Entry(bills_page, width=5, textvariable=var_jobDate_d)
    startDate_entry3.place(x=290, y=100)

    serDate_la2 = tk.Label(bills_page, text='Working Hours:')
    serDate_la2.place(x=50, y=130)
    serDate_la3 = tk.Label(bills_page, text='Hsr:')
    serDate_la3.place(x=150, y=130)
    serDate_entry1 = tk.Entry(bills_page, width=5, textvariable=var_serDate_hrs)
    serDate_entry1.place(x=180, y=130)
    serDate_la4 = tk.Label(bills_page, text='Mins:')
    serDate_la4.place(x=220, y=130)
    serDate_entry2 = tk.Entry(bills_page, width=5, textvariable=var_serDate_mins)
    serDate_entry2.place(x=260, y=130)

    copying_la = tk.Label(bills_page, text='Copying:')
    copying_la.place(x=50, y=160)
    copying_entry = tk.Entry(bills_page, textvariable=var_copying)
    copying_entry.place(x=150, y=160)

    filing_la = tk.Label(bills_page, text='Filing:')
    filing_la.place(x=50, y=190)
    filing_entry = tk.Entry(bills_page, textvariable=var_filing)
    filing_entry.place(x=150, y=190)

    serving_la = tk.Label(bills_page, text='Serving:')
    serving_la.place(x=50, y=220)
    serving_entry = tk.Entry(bills_page, textvariable=var_serving)
    serving_entry.place(x=150, y=220)

