from operator import itemgetter
from tkinter import *
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox
import pickle
import logging
import datetime
import tkinter.filedialog
import re
import docx
import os
from win32com import client
from docx.shared import Cm
import operator
import string
import PyPDF2
import os
import window.UserUI as user_ui
import window.StageUI as satge_ui
import window.BillsUI as bills_ui
from reportlab.pdfgen.canvas import Canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer,Image,Table,TableStyle
from reportlab.pdfbase import pdfmetrics, ttfonts
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))
pdfmetrics.registerFont(TTFont('msyh', 'STSONG.TTF'))


def indexUI():
    window = tk.Tk()
    window.title("xxx律师所")
    window.geometry('690x600')
    window.resizable(False, False)

    # 添加用户
    def addUser():
        pass

    # 添加用户页面_清空按钮
    def cancels():
        pass

    # 添加Stage
    def addstageDate():
        stage2=tree_stage.insert("", 0,text=satge_ui.var_stageID.get())

    # 修改stage
    def updateStageDate():
        pass

    # 删除Stage
    def removeStageDate():
        pass

    # 添加收据单_添加当前层按钮
    def confirms():
        pass
    # 添加收据单_添加下一层
    value=''
    def confirm_next():
        global value
        tree_stage.insert(value,0,text=bills_ui.var_bills_type.get())
    # 删除单据
    def removeBills():
        pass
    # 修改单据
    def updateBills():
        pass
    # 添加单据页面_清空按钮
    def cancel():
        pass

    # 导入用户文件
    def input_user():
        pass

    # 导入单据文件
    def input_receipts():
        pass

    # 导出docx
    def docxui():
        pass

    # 导出PDF
    def pdfui():
        pass

    # 显示全部数据
    def overall_data():
        pass

    # 退出
    def exita():
        pass
    #选择stage节点

    def trefun(event):
        global value
        value = event.widget.selection()
    def raise_frame(frame):
        frame.tkraise()
    def billsUI():
        raise_frame(bills_page)
    def userUI():
        raise_frame(adduser_page)
    def stageUI():
        raise_frame(stage_page)

    bills_page = Frame(window, width=500, height=320)
    adduser_page = Frame(window, width=500, height=320)
    stage_page = Frame(window, width=500, height=320)
    rests_page=Frame(window, width=500, height=320)

    billsUI1 = tk.Button(bills_page, text='Event', width=8, command=billsUI, borderwidth=1).place(x=5,y=0)
    userUI1  = tk.Button(bills_page, text='FeeEarner', width=8, command=userUI, borderwidth=1).place(x=80,y=0)
    stageUI1 = tk.Button(bills_page, text='Stage', width=8, command=stageUI, borderwidth=1).place(x=155,y=0)

    billsUI1 = tk.Button(adduser_page, text='Event', width=8, command=billsUI, borderwidth=1).place(x=5,y=0)
    userUI1  = tk.Button(adduser_page, text='FeeEarner', width=8, command=userUI, borderwidth=1).place(x=80,y=0)
    stageUI1 = tk.Button(adduser_page, text='Stage', width=8, command=stageUI, borderwidth=1).place(x=155,y=0)

    billsUI1 = tk.Button(stage_page, text='Event', width=8, command=billsUI, borderwidth=1).place(x=5,y=0)
    userUI1  = tk.Button(stage_page, text='FeeEarner', width=8, command=userUI, borderwidth=1).place(x=80,y=0)
    stageUI1 = tk.Button(stage_page, text='Stage', width=8, command=stageUI, borderwidth=1).place(x=155,y=0)

    for frame in (bills_page, adduser_page, stage_page,rests_page):
        frame.grid(row=0, column=0, sticky='news')

    raise_frame(bills_page)
    user_ui.user_ui(adduser_page)#添加用户UI
    satge_ui.stage_ui(stage_page)#添加StageUI
    bills_ui.bills_ui(bills_page)#添加收据单UI


    #添加用户页面按钮
    addUser = tk.Button(adduser_page, text='添 加', width=5, command=addUser)
    addUser.place(x=160, y=240)
    cancel = tk.Button(adduser_page, text='清 空', width=5, command=cancels)
    cancel.place(x=220, y=240)

    #添加Stage页面按钮
    addstageDate = tk.Button(stage_page, text='添 加', width='5', command=addstageDate)
    updateStageDate = tk.Button(stage_page, text='修改', width='5', command=updateStageDate)
    removeStageDate = tk.Button(stage_page, text='删除', width='5', command=removeStageDate)
    addstageDate.place(x=200, y=190)
    updateStageDate.place(x=255, y=190)
    removeStageDate.place(x=310, y=190)

    #添加单据页面按钮
    confirm = tk.Button(bills_page, text='添加当前层', width=8, command=confirms)
    confirm.place(x=120, y=275)
    confirm_next=tk.Button(bills_page,text='添加下一层',width=8,command=confirm_next)
    confirm_next.place(x=200,y=275)
    removeBills = tk.Button(bills_page, text='删 除', width=6, command=removeBills)
    updateBills = tk.Button(bills_page, text='修 改', width=6, command=updateBills)
    cancel_i = tk.Button(bills_page, text='清 空', width=6, command=cancel)
    cancel_i.place(x=280, y=275)

    #用户列表
    lbUserss = tk.Listbox(window, height=9, width=24)
    lbUserss.place(x=530, y=0)



    #stage
    tree_stage = ttk.Treeview(window,height=8)
    vbar = ttk.Scrollbar(window, orient=VERTICAL, command=tree_stage.yview)
    myid = tree_stage.insert("", 0, 'Stage1', text='Stage1', values='1')
    myidx1 = tree_stage.insert(myid, 0, text='conference within stage1', values='2')
    myidx2 = tree_stage.insert(myid, 1,  text='with client  ', values='3')
    tree_stage.bind("<<TreeviewSelect>>", trefun)
    tree_stage.place(x=530, y=166)


    # 导航条
    men = tk.Menu(window)
    usermenu = tk.Menu(men, tearoff=0)
    men.add_cascade(label='功能', menu=usermenu)
    usermenu.add_command(label='导入用户数据', command=input_user)
    usermenu.add_command(label='导入单据数据', command=input_receipts)
    usermenu.add_command(label='导出DOCX', command=docxui)
    usermenu.add_command(label='导出PDF', command=pdfui)
    usermenu.add_command(label='显示全部数据', command=overall_data)
    exitemenu = tk.Menu(men, tearoff=0)
    men.add_cascade(label='退出', menu=exitemenu)
    exitemenu.add_command(label='退出', command=exita)
    window.config(menu=men)

    # 显示单据的全部信息
    tree = ttk.Treeview(window, show="headings", height=13)
    tree["columns"] = ('ID', 'Fee Earners', 'Date', 'Billable MIns', 'Title', 'Rests', 'Total')
    tree.column('ID', width=60, anchor="center")
    tree.column('Fee Earners', width=80, anchor="center")
    tree.column('Date', width=92, anchor="center")
    tree.column('Billable MIns', width=92, anchor="center")
    tree.column('Title', width=210, anchor="center")
    tree.column('Rests', width=82, anchor="center")
    tree.column('Total', width=82, anchor="center")
    tree.column('ID', width=60, anchor="center")
    tree.column('Fee Earners', width=80, anchor="center")
    tree.column('Date', width=92, anchor="center")
    tree.column('Billable MIns', width=92, anchor="center")
    tree.column('Title', width=210, anchor="center")
    tree.column('Rests', width=82, anchor="center")
    tree.column('Total', width=82, anchor="center")

    tree.heading('ID', text='ID')
    tree.heading('Fee Earners', text='Fee Earners')
    tree.heading('Date', text='Date')
    tree.heading('Billable MIns', text='Billable MIns')
    tree.heading('Title', text='Title')
    tree.heading('Rests', text='Rests')
    tree.heading('Total', text='Total')
    tree.place(x=0, y=315)

    window.mainloop()
