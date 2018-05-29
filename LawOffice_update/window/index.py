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
import Model.Uti as uti
import window.UserUI as user_ui #用户页面
import window.StageUI as stage_ui #Stage页面
import window.BillsUI as bills_ui #单据页面
from reportlab.pdfgen.canvas import Canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer,Image,Table,TableStyle
from reportlab.pdfbase import pdfmetrics, ttfonts
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from xml.etree import ElementTree as et
import  xml.dom.minidom
pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))
pdfmetrics.registerFont(TTFont('msyh', 'STSONG.TTF'))
import Model.Attorney as attorney
import Model.Stage as stage

User_file=''
Bills_file=''
Stage_file=''
def indexUI(user_file,bills_file,stage_file):
    window = tk.Tk()
    window.title("xxx律师所")
    window.geometry('690x600')
    window.resizable(False, False)

    bills_page = Frame(window, width=500, height=320)
    adduser_page = Frame(window, width=500, height=320)
    stage_page = Frame(window, width=500, height=320)
    rests_page=Frame(window, width=500, height=320)

    User_file=user_file
    Bills_file=bills_file
    Stage_file=stage_file

    lbUserss = tk.Listbox(window, height=9, width=24)

    user_dict={}
    #页面加载时将数据添加到user_dict字典中
    user_obj=open(User_file,'r')
    user_data=user_obj.readlines()
    for dic in user_data:
        user_dict=eval(dic)
        for i in user_dict.keys():
            lbUserss.insert('end',i)
            bills_ui.users.append(i)
            bills_ui.bills_ui(bills_page)

    try:
        #页面加载完成时将数据添加到stage列表中
        tree_stage = ttk.Treeview(window, height=8)
        treexml = et.parse(Stage_file)
        root = treexml.getroot()
        num=0
        num1=0
        num2=0
        for child in root:
            myid=tree_stage.insert("", num, text=child.attrib['id'])
            num+=1
            for i in child:
                myidx1 = tree_stage.insert(myid, num1, text=i.text)
                num1+=1
                for s in i:
                    myidx2 = tree_stage.insert(myidx1, num2, text=s.text)
                    num2+=1
    except Exception as e:
        pass


    # 添加用户
    def addUser():
        sex = '男' if int(user_ui.var_sex.get()) == 1 else '女'
        if  (user_ui.var_username.get() =='') | (user_ui.var_acronym.get()=='') | (sex=='') | (user_ui.var_charge.get()==''):
            tk.messagebox.showinfo(title='提示',message='请填写相关数据，再进行添加!')
        elif  len(user_ui.var_ReauthenticationTime.get())<4:
            tk.messagebox.showinfo(title='提示',message='请输入正确的认证时间!')
        elif uti.check(user_ui.var_ReauthenticationTime.get())!=True:
            tk.messagebox.showinfo(title='提示',message='认证时间错误,请重新输入!')
        elif uti.check(user_ui.var_charge.get())!=True:
            tk.messagebox.showinfo(title='提示',message='收费标准错误,请重新输入!')
        else:
            ss=attorney.Attorney(
                user_ui.var_username.get(),
                user_ui.var_acronym.get(),
                sex,
                user_ui.var_post.get(),
                user_ui.var_ReauthenticationTime.get(),
                float(user_ui.var_charge.get())/60)
            bills_ui.users.append(user_ui.var_username.get())#将添加的用户添加到单据页面用户下拉列表框
            bills_ui.bills_ui(bills_page)
            ss.save(User_file,user_dict)#将数据保存到txt文件中
            tk.messagebox.showinfo(title='提示',message='添加成功!')
            lbUserss.insert('end',user_ui.var_username.get())
            cancels()

    # 添加用户页面_清空按钮
    def cancels():
        user_ui.var_username.set('')
        user_ui.var_acronym.set('')
        user_ui.var_sex.set(0)
        user_ui.var_post.set('')
        user_ui.var_ReauthenticationTime.set('')
        user_ui.var_charge.set('')

    #修改用户
    def updateUser():
        sex='男' if int(user_ui.var_sexs.get()) == 1 else '女'
        if  (user_ui.var_usernames.get() =='') | (user_ui.var_acronyms.get()=='')  | (sex=='') |(user_ui.var_charges.get()==''):
            tk.messagebox.showinfo(title='提示',message='请填写相关数据，再进行添加!')
        elif  len(user_ui.var_ReauthenticationTimes.get())<4:
            tk.messagebox.showinfo(title='提示',message='请输入正确的认证时间!')
        elif uti.check(user_ui.var_ReauthenticationTimes.get())!=True:
            tk.messagebox.showinfo(title='提示',message='认证时间错误,请重新输入!')
        else:
            user_dict[user_ui.var_usernames.get()][0] = user_ui.var_acronyms.get()
            user_dict[user_ui.var_usernames.get()][1] =  user_ui.var_ReauthenticationTimes.get()
            user_dict[user_ui.var_usernames.get()][2] = user_ui.var_posts.get()
            user_dict[user_ui.var_usernames.get()][3] = sex
            user_dict[user_ui.var_usernames.get()][4] = float(user_ui.var_charges.get())/60
            fileobj = open(user_file, 'w',encoding="gbk")
            fileobj.write(str(user_dict))
            fileobj.close()
            tk.messagebox.showinfo(title='提示', message='修改成功!')
            user_ui.clear_data()
            userUI()
    #删除用户
    def removeUser():
        user_dict.pop(user_ui.var_usernames.get())
        fileobj = open(user_file, 'w')
        fileobj.write(str(user_dict))
        fileobj.close()
        bills_ui.users.remove(str(user_ui.var_usernames.get()))
        bills_ui.bills_ui(bills_page)
        user_ui.clear_data()
        lbUserss.delete(0, 'end')
        for i in user_dict :
            lbUserss.insert('end',i)
        userUI()
        tk.messagebox.showinfo(title='提示',message='删除成功!')

    #显示用户信息
    def show_user(event):
        raise_frame(rests_page)
        callUpdateUser()


    # 添加Stage
    def addstageDate():
        if stage_ui.var_stageID.get() == '':
            tk.messagebox.showinfo(title='提示', message='请填写编号!')

        elif uti.check(stage_ui.var_stageID.get()) != True:
            tk.messagebox.showinfo(title='提示', message='编号只能为数字!')

        elif stage_ui.var_stageID.get() == '':
            tk.messagebox.showinfo(title='提示', message='请填写名称!')

        elif stage_ui.var_stageStartDate_y.get() == '' or stage_ui.var_stageStartDate_m.get() == '' or stage_ui.var_stage_endDate_y.get() == '' or stage_ui.var_stage_endDate_m.get() == '':
            tk.messagebox.showinfo(title='提示', message='请填写日期!')

        elif uti.check(stage_ui.var_stageStartDate_y.get()) != True or uti.check(
                stage_ui.var_stageStartDate_m.get()) != True or uti.check(
                stage_ui.var_stage_endDate_y.get()) != True or uti.check(stage_ui.var_stage_endDate_m.get()) != True:
            tk.messagebox.showinfo(title='提示', message='日期只能填写数字,请重新填写!')

        elif len(stage_ui.var_stageStartDate_y.get()) < 4 or int(stage_ui.var_stageStartDate_m.get()) > 12 or len(
                stage_ui.var_stage_endDate_y.get()) < 4 or int(stage_ui.var_stage_endDate_m.get()) > 12:
            tk.messagebox.showinfo(title='提示', message='日期格式错误请重新填写!')

        elif int(stage_ui.var_stageStartDate_y.get() + ('0' + stage_ui.var_stageStartDate_m.get() if len(
                stage_ui.var_stageStartDate_m.get()) == 1 else stage_ui.var_stageStartDate_m.get())) > int(
            stage_ui.var_stage_endDate_y.get() + ('0' + stage_ui.var_stage_endDate_m.get() if len(
                stage_ui.var_stage_endDate_m.get()) == 1 else stage_ui.var_stage_endDate_m.get())):
            tk.messagebox.showinfo(title='提示', message='开始时间不能大于结束时间!')

        else:
            try:
                dom = xml.dom.minidom.parse(stage_file)
                flagDao = stage.FlagDao(stage_file)
                flagDao.addTag('Stage'+str(stage_ui.var_stageID.get()),stage_ui.var_stageID.get(),str(stage_ui.var_stageStartDate_y.get())+'/'+
                                          str(stage_ui.var_stageStartDate_m.get())+'-'+
                                          str(stage_ui.var_stage_endDate_y.get())+'/'+
                                          str(stage_ui.var_stage_endDate_m.get()))
                tree_stage.insert("", num, text='Stage' + stage_ui.var_stageID.get())
                tk.messagebox.showinfo(title='提示',message='添加成功!')
                wipe_data()#清空数据
            except xml.parsers.expat.ExpatError as e:
                    stage_obj=stage.Stage(stage_ui.var_stageID.get(),
                                          stage_ui.var_stageName.get(),
                                          stage_ui.var_stageStartDate_y.get(),
                                          stage_ui.var_stageStartDate_m.get(),
                                          stage_ui.var_stage_endDate_y.get(),
                                          stage_ui.var_stage_endDate_m.get()
                                          )
                    stage_obj.save(stage_file)
                    tree_stage.insert("", num,text='Stage'+stage_ui.var_stageID.get())
                    tk.messagebox.showinfo(title='提示', message='添加成功!')
                    wipe_data()  # 清空数据
    def wipe_data():
        stage_ui.var_stageID.set('')
        stage_ui.var_stageName.set('')
        stage_ui.var_stageStartDate_y.set('')
        stage_ui.var_stageStartDate_m.set('')
        stage_ui.var_stage_endDate_y.set('')
        stage_ui.var_stage_endDate_m.set('')

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


    # 将值赋值到相关控件中
    def callUpdateUser():
        try:
            user = lbUserss.get(lbUserss.curselection())
            user_ui.var_usernames.set(user)
            user_ui.var_acronyms.set(user_dict[user][0])
            user_ui.var_posts.set(user_dict[user][2])
            user_ui.var_ReauthenticationTimes.set(user_dict[user][1])
            user_ui.var_charges.set(round(float(user_dict[user][4]) * 60, 2))
            sex= 1 if user_dict[user][3]== '男' else 2
            user_ui.var_sexs.set(sex)
        except Exception as e:
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



    billsUI1 = tk.Button(bills_page, text='Event', width=8, command=billsUI, borderwidth=1).place(x=5,y=0)
    userUI1  = tk.Button(bills_page, text='FeeEarner', width=8, command=userUI, borderwidth=1).place(x=80,y=0)
    stageUI1 = tk.Button(bills_page, text='Stage', width=8, command=stageUI, borderwidth=1).place(x=155,y=0)

    billsUI1 = tk.Button(adduser_page, text='Event', width=8, command=billsUI, borderwidth=1).place(x=5,y=0)
    userUI1  = tk.Button(adduser_page, text='FeeEarner', width=8, command=userUI, borderwidth=1).place(x=80,y=0)
    stageUI1 = tk.Button(adduser_page, text='Stage', width=8, command=stageUI, borderwidth=1).place(x=155,y=0)

    billsUI1 = tk.Button(stage_page, text='Event', width=8, command=billsUI, borderwidth=1).place(x=5,y=0)
    userUI1  = tk.Button(stage_page, text='FeeEarner', width=8, command=userUI, borderwidth=1).place(x=80,y=0)
    stageUI1 = tk.Button(stage_page, text='Stage', width=8, command=stageUI, borderwidth=1).place(x=155,y=0)

    billsUI1 = tk.Button(rests_page, text='Event', width=8, command=billsUI, borderwidth=1).place(x=5,y=0)
    userUI1  = tk.Button(rests_page, text='FeeEarner', width=8, command=userUI, borderwidth=1).place(x=80,y=0)
    stageUI1 = tk.Button(rests_page, text='Stage', width=8, command=stageUI, borderwidth=1).place(x=155,y=0)

    for frame in (bills_page, adduser_page, stage_page,rests_page):
        frame.grid(row=0, column=0, sticky='news')

    raise_frame(bills_page)
    user_ui.user_ui(adduser_page)#添加用户UI
    stage_ui.stage_ui(stage_page)#添加StageUI
    bills_ui.bills_ui(bills_page)#添加收据单UI
    user_ui.show_user(rests_page)

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
    lbUserss.place(x=530, y=0)
    lbUserss.bind('<Button-1>', show_user)

    #显示用户页面按钮
    updateUser = tk.Button(rests_page, text='修改', width=5, command=updateUser)
    removeUser = tk.Button(rests_page, text='删除', width=5, command=removeUser)
    removeUser.place(x=160, y=220)
    updateUser.place(x=240, y=220)

    #stage
    vbar = ttk.Scrollbar(window, orient=VERTICAL, command=tree_stage.yview)
    # myid = tree_stage.insert("", 0, 'Stage1', text='Stage1', values='1')
    # myidx1 = tree_stage.insert(myid, 0, text='conference within stage1', values='2')
    # myidx2 = tree_stage.insert(myid, 1,  text='with client  ', values='3')
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
