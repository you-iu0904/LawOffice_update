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
serialNumber = 0
num = 0
num1 = 0
num2 = 0

value = ''
valueobj = ''

def indexUI(user_file,bills_file,stage_file):

    global num
    global num1
    global num2
    global serialNumber
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

    tree_total = ttk.Treeview(window, show="headings", height=13)
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
        tree_stage = ttk.Treeview(window, height=7)
        treexml = et.parse(Stage_file)
        root = treexml.getroot()
        for child in root:
            myid=tree_stage.insert("", num, text=child.attrib['id'])
            num+=1
            for i in child:
                myidx1 = tree_stage.insert(myid, num1, text=i.attrib['id'])
                num1+=1
                try:
                    for s in i:
                        myidx2 = tree_stage.insert(myidx1, num2, text=s.attrib['id'])
                        num2+=1
                except KeyError:
                    pass
    except Exception as e:
        pass

    #页面加载时将单据的数据添tree_total列表中
    try:
        dom = xml.dom.minidom.parse(stage_file)
        root = dom.documentElement
        bb = root.getElementsByTagName('bills')
        for i in range(len(bb)):
            tree_total.insert('', serialNumber, values=(bb[i].getAttribute('serialNumber'),bb[i].getAttribute('FeeEarners'),
                                             bb[i].getAttribute('Date'),
                                             bb[i].getAttribute('Time'),
                                             bb[i].getAttribute('Narrative'),
                                             bb[i].getAttribute('Other'),
                                             bb[i].getAttribute('TotalMoney')
                                             )
                              )
            serialNumber=bb[i].getAttribute('serialNumber')
    except Exception:
        pass


    # 添加用户
    def addUser():
        sex = '男' if int(user_ui.var_sex.get()) == 1 else '女'
        if  (user_ui.var_username.get() =='') | (user_ui.var_acronym.get()=='') | (sex=='') | (user_ui.var_charge.get()==''):
            tk.messagebox.showinfo(title='提示',message='请填写相关数据，再进行添加!')
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
                start_month = '0' + stage_ui.var_stageStartDate_m.get() if len(str(stage_ui.var_stageStartDate_m.get()))==1 else stage_ui.var_stageStartDate_m.get()
                end_month = '0' + stage_ui.var_stage_endDate_m.get() if len(str(stage_ui.var_stage_endDate_m.get())) == 1 else stage_ui.var_stage_endDate_m.get()
                flagDao = stage.FlagDao(stage_file)
                flagDao.addTag(stage_ui.var_stageName.get(),str(stage_ui.var_stageStartDate_y.get())+'/'+
                                          start_month+'-'+
                                          str(stage_ui.var_stage_endDate_y.get())+'/'+
                                           end_month,
                                         'Stage' + str(stage_ui.var_stageID.get())
                               )
                tree_stage.insert("", num, text='Stage' + stage_ui.var_stageID.get())
                tk.messagebox.showinfo(title='提示',message='添加成功!')
                wipe_data()#清空数据
            except xml.parsers.expat.ExpatError as e:
                    stage_obj=stage.Stage(stage_ui.var_stageID.get(),
                                          stage_ui.var_stageName.get(),
                                          stage_ui.var_stageStartDate_y.get(),
                                          '0' + stage_ui.var_stageStartDate_m.get() if len(str(stage_ui.var_stageStartDate_m.get()))==1 else stage_ui.var_stageStartDate_m.get(),
                                          stage_ui.var_stage_endDate_y.get(),
                                        '0' + stage_ui.var_stage_endDate_m.get() if len(str(stage_ui.var_stage_endDate_m.get())) == 1 else stage_ui.var_stage_endDate_m.get()
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
            flagDao = stage.FlagDao(stage_file)
            flagDao.deleteTagByName('Stage'+str(stage_ui.var_stageID.get()))
            dom = xml.dom.minidom.parse(stage_file)
            start_month = '0' + stage_ui.var_stageStartDate_m.get() if len(
                str(stage_ui.var_stageStartDate_m.get())) == 1 else stage_ui.var_stageStartDate_m.get()
            end_month = '0' + stage_ui.var_stage_endDate_m.get() if len(
                str(stage_ui.var_stage_endDate_m.get())) == 1 else stage_ui.var_stage_endDate_m.get()
            flagDao = stage.FlagDao(stage_file)
            flagDao.addTag(stage_ui.var_stageName.get(), str(stage_ui.var_stageStartDate_y.get()) + '/' +
                           start_month + '-' +
                           str(stage_ui.var_stage_endDate_y.get()) + '/' +
                           end_month,
                           'Stage' + str(stage_ui.var_stageID.get())
                           )
            tk.messagebox.showinfo(title='提示', message='修改成功!')
            wipe_data()  # 清空数据

    # 显示单据
    def show_bills():
        try:
            global serialNumber
            items = tree_total.get_children()
            [tree_total.delete(item) for item in items]
            dom = xml.dom.minidom.parse(stage_file)
            root = dom.documentElement
            bb = root.getElementsByTagName('bills')
            for i in range(len(bb)):
                tree_total.insert('', bb[i].getAttribute('serialNumber'), values=(bb[i].getAttribute('serialNumber'), bb[i].getAttribute('FeeEarners'),
                                                            bb[i].getAttribute('Date'),
                                                            bb[i].getAttribute('Time'),
                                                            bb[i].getAttribute('Narrative'),
                                                            bb[i].getAttribute('Other'),
                                                            bb[i].getAttribute('TotalMoney')
                                                            )
                                  )
                serialNumber =bb[i].getAttribute('serialNumber')
        except Exception:
            pass

    # 显示stage
    def show_stage_data():
        num=0
        num1=0
        num2 = 0
        try:
            items = tree_stage.get_children()
            [tree_stage.delete(item) for item in items]
            treexml = et.parse(Stage_file)
            root = treexml.getroot()
            for child in root:
                myid = tree_stage.insert("", num, text=child.attrib['id'])
                num+=1
                for i in child:
                    myidx1 = tree_stage.insert(myid, num1, text=i.attrib['id'])
                    num1+=1
                    for s in i:
                        myidx2 = tree_stage.insert(myidx1, num2, text=s.attrib['id'])
                        num2+=1
        except Exception as e:
            pass

    # 删除Stage
    def removeStageDate():
        flagDao = stage.FlagDao(stage_file)
        flagDao.deleteTagByName('Stage'+str(stage_ui.var_stageID.get()))
        items = tree_stage.get_children()
        [tree_stage.delete(item) for item in items]
        show_stage_data()
        tk.messagebox.showinfo(title='提示',message='删除成功!')
        wipe_data()

    # 添加收据单
    def confirms():
        global value
        global  valueobj
        global serialNumber

        if value=='' :
            tk.messagebox.showinfo(title='提示',message='请选择节点,再进行添加!')
        elif bills_ui.var_user.get()=='':
            tk.messagebox.showinfo(title='提示',message='请选择律师!')
        elif bills_ui.var_incident.get()=='':
            tk.messagebox.showinfo(title='提示',message='请填写Narrative!')
        elif bills_ui.var_jobDate_y.get()=='' or bills_ui.var_jobDate_m.get()=='' or bills_ui.var_jobDate_d.get()=='':
            tk.messagebox.showinfo(title='提示',message='请填写工作日期!')
        elif bills_ui.var_serDate_hrs.get()=='' and bills_ui.var_serDate_mins.get()=='':
            tk.messagebox.showinfo(title='提示',message='请填写服务时间!')
        elif uti.check(bills_ui.var_jobDate_y.get()) == False or uti.check(bills_ui.var_jobDate_m.get()) == False or uti.check(bills_ui.var_jobDate_d.get()) == False:
            tk.messagebox.showinfo(title='提示',message='工作日期只能填写数字!')
        elif uti.check(bills_ui.var_serDate_hrs.get()) == False or uti.check(bills_ui.var_serDate_mins.get()) == False:
            tk.messagebox.showinfo(title='提示',message='服务时间只能填写数字!')
        elif len(bills_ui.var_jobDate_y.get())<4 or int(bills_ui.var_jobDate_m.get())>12 or int(bills_ui.var_jobDate_d.get())>31:
            tk.messagebox.showinfo(title='提示',message='工作日期格式错误,请重新填写!')
        elif uti.check(bills_ui.var_copying.get())== False :
            tk.messagebox.showinfo(title='提示',message='Copying只能填写数字,请重新填写!')
        elif uti.check(bills_ui.var_filing.get())== False:
            tk.messagebox.showinfo(title='提示',message='Filing只能填写数字,请重新填写!')
        elif uti.check(bills_ui.var_serving.get())== False:
            tk.messagebox.showinfo(title='提示',message='Serving只能填写数字,请重新填写!')
        else:
            rates = user_dict[bills_ui.var_user.get()][4]
            ms = user_dict[bills_ui.var_user.get()][1]
            if int(bills_ui.var_jobDate_y.get())<int(ms):
                tk.messagebox.showinfo(title='提示',message='工作日期不能小于该律师认证日期!')
            else:
                date_y = bills_ui.var_jobDate_y.get()
                date_m = '0'+str(bills_ui.var_jobDate_m.get()) if len(bills_ui.var_jobDate_m.get())==1 else bills_ui.var_jobDate_m.get()
                date_d = '0'+str(bills_ui.var_jobDate_d.get()) if len(bills_ui.var_jobDate_d.get())==1 else bills_ui.var_jobDate_d.get()
                time = (int(bills_ui.var_serDate_hrs.get())*60)+int(bills_ui.var_serDate_mins.get())
                money = float(int(time)*float(rates))+int(bills_ui.var_copying.get())+int(bills_ui.var_filing.get())+int(bills_ui.var_serving.get())
                tree = stage.read_xml(stage_file)
                nodes = stage.find_nodes(tree, ".//")
                result_nodes = stage.get_node_by_keyvalue(nodes, {"id": value})
                a = stage.create_node("bills", {'serialNumber':str(int(serialNumber)+1),
                                                'FeeEarners':bills_ui.var_user.get(),
                                                'Narrative':bills_ui.var_incident.get(),
                                                'Date':date_y+'-'+date_m+'-'+date_d,
                                                'Time':str(time),
                                                'Other':str(int(bills_ui.var_copying.get())+int(bills_ui.var_filing.get())+int(bills_ui.var_serving.get())),
                                                'TotalMoney':str(money)
                                                },
                                      None)
                tree_total.insert('', int(serialNumber)+1, values=(str(int(serialNumber)+1), bills_ui.var_user.get(),
                                           date_y + '-' + date_m + '-' + date_d,
                                           str(time), bills_ui.var_incident.get(),
                                           int(bills_ui.var_copying.get()) + int(bills_ui.var_filing.get()) + int(bills_ui.var_serving.get()),
                                           str(money)
                                          )
                            )

                # 插入到父节点之下
                stage.add_child_node(result_nodes, a)
                #添加xml
                stage.write_xml(tree, stage_file)
                tk.messagebox.showinfo(title='提示',message='添加成功!')
                cancel_bills()
                int(serialNumber)+1

    # 添加收据单_添加下一层
    def confirm_next():
        global value
        global valueobj
        if value=='' or valueobj=='':
            tk.messagebox.showinfo(title='提示',message='请选择节点再进行添加!')
        else:
            tree = stage.read_xml(stage_file)
            nodes = stage.find_nodes(tree, ".//")
            result_nodes = stage.get_node_by_keyvalue(nodes, {"id": value})
            a = stage.create_node("type", {'id':bills_ui.var_bills_type.get()}, None)
            # 插入到父节点之下
            stage.add_child_node(result_nodes, a)
            #添加xml
            stage.write_xml(tree, stage_file)
            tree_stage.insert(valueobj,0,text=bills_ui.var_bills_type.get())
            tk.messagebox.showinfo(title='提示',message='添加成功!')
            value=''
            valueobj=''

    # 删除单据
    def removeBills():
        global serialNumber
        tree = stage.read_xml(stage_file)
        del_parent_nodes = stage.find_nodes(tree, ".//")
        # 准确定位子节点并删除之
        target_del_node = stage.del_node_by_tagkeyvalue(del_parent_nodes, 'bills', {"serialNumber": bills_ui.var_serialNum.get()})
        stage.write_xml(tree, stage_file)
        tk.messagebox.showinfo(title='提示', message='删除成功!')
        show_bills()
        int(serialNumber)-1
        billsUI()
        bills_ui.var_serialNum==''

    # 修改单据
    def updateBills():

        if bills_ui.var_user.get() == '':
            tk.messagebox.showinfo(title='提示', message='请选择律师!')
        elif bills_ui.var_incident.get() == '':
            tk.messagebox.showinfo(title='提示', message='请填写Narrative!')
        elif bills_ui.var_jobDate_y.get() == '' or bills_ui.var_jobDate_m.get() == '' or bills_ui.var_jobDate_d.get() == '':
            tk.messagebox.showinfo(title='提示', message='请填写工作日期!')
        elif bills_ui.var_serDate_hrs.get() == '' and bills_ui.var_serDate_mins.get() == '':
            tk.messagebox.showinfo(title='提示', message='请填写服务时间!')
        elif uti.check(bills_ui.var_jobDate_y.get()) == False or uti.check(
                bills_ui.var_jobDate_m.get()) == False or uti.check(bills_ui.var_jobDate_d.get()) == False:
            tk.messagebox.showinfo(title='提示', message='工作日期只能填写数字!')
        elif uti.check(bills_ui.var_serDate_hrs.get()) == False or uti.check(bills_ui.var_serDate_mins.get()) == False:
            tk.messagebox.showinfo(title='提示', message='服务时间只能填写数字!')
        elif len(bills_ui.var_jobDate_y.get()) < 4 or int(bills_ui.var_jobDate_m.get()) > 12 or int(
                bills_ui.var_jobDate_d.get()) > 31:
            tk.messagebox.showinfo(title='提示', message='工作日期格式错误,请重新填写!')
        elif uti.check(bills_ui.var_copying.get()) == False:
            tk.messagebox.showinfo(title='提示', message='Copying只能填写数字,请重新填写!')
        elif uti.check(bills_ui.var_filing.get()) == False:
            tk.messagebox.showinfo(title='提示', message='Filing只能填写数字,请重新填写!')
        elif uti.check(bills_ui.var_serving.get()) == False:
            tk.messagebox.showinfo(title='提示', message='Serving只能填写数字,请重新填写!')
        else:
            rates = user_dict[bills_ui.var_user.get()][4]
            ms = user_dict[bills_ui.var_user.get()][1]
            if int(bills_ui.var_jobDate_y.get()) < int(ms):
                tk.messagebox.showinfo(title='提示', message='工作日期不能小于该律师认证日期!')
            else:
                date_y = bills_ui.var_jobDate_y.get()
                date_m = '0' + str(bills_ui.var_jobDate_m.get()) if len(
                    bills_ui.var_jobDate_m.get()) == 1 else bills_ui.var_jobDate_m.get()
                date_d = '0' + str(bills_ui.var_jobDate_d.get()) if len(
                    bills_ui.var_jobDate_d.get()) == 1 else bills_ui.var_jobDate_d.get()
                time = (int(bills_ui.var_serDate_hrs.get()) * 60) + int(bills_ui.var_serDate_mins.get())
                money = float(int(time) * float(rates)) + int(bills_ui.var_copying.get()) + int(
                    bills_ui.var_filing.get()) + int(bills_ui.var_serving.get())

                tree = stage.read_xml(stage_file)
                nodes = stage.find_nodes(tree, ".//")
                result_nodes = stage.get_node_by_keyvalue(nodes, {"serialNumber":bills_ui.var_serialNum.get()})
                stage.change_node_properties(result_nodes,{"Date":str(date_y)+'-'+str(date_m)+'-'+str(date_d),
                                                           'FeeEarners':bills_ui.var_user.get(),



                                                           'Narrative':bills_ui.var_incident.get(),
                                                           'Other':str(int(bills_ui.var_copying.get())+int(bills_ui.var_filing.get())+int(bills_ui.var_serving.get())),
                                                           'Time': str(time),
                                                           'TotalMoney':str(money)
                                                           }
                                             )
                stage.write_xml(tree, stage_file)
                tk.messagebox.showinfo(title='提示',message='修改成功!')
                billsUI()
                show_bills()


    #双击控制台将单据数据显示控件中
    def trefun_total(event):
        billsUI()
        iids = tree_total.selection()
        data_list=[]
        for i in iids:
            data_list.append(tree_total.item(i, 'values'))
        for o in data_list:
            bills_ui.var_serialNum.set(o[0])
            bills_ui.var_user.set(o[1])
            bills_ui.var_incident.set(o[4])
            bills_ui.var_jobDate_y.set(o[2].replace('-', '')[:4])
            bills_ui.var_jobDate_m.set(o[2].replace('-', '')[4:6])
            bills_ui.var_jobDate_d.set(o[2].replace('-', '')[6:8])
            if float(o[3])<60:
                bills_ui.var_serDate_mins.set(o[3])
            else:
                bills_ui.var_serDate_hrs.set(int(float(o[3])/60))
                bills_ui.var_serDate_mins.set(int(float(o[3]))%60)

        confirm.place_forget()
        confirm_next.place_forget()
        updateBills.place(x=120, y=275)
        removeBills.place(x=200, y=275)
        cancel_i.place(x=280, y=275)

    # 添加单据页面_清空按钮
    def cancel_bills():
        bills_ui.var_serialNum.set('')
        bills_ui.var_user.set('')
        bills_ui.var_incident.set('')
        bills_ui.var_jobDate_y.set('')
        bills_ui.var_jobDate_m.set('')
        bills_ui.var_jobDate_d.set('')
        bills_ui.var_serDate_hrs.set('0')
        bills_ui.var_serDate_mins.set('0')
        bills_ui.var_copying.set('0')
        bills_ui.var_filing.set('0')
        bills_ui.var_serving.set('0')
        bills_ui.var_bills_type.set('')

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

    def choice (event):
        global value
        global valueobj
        valueobj=event.widget.selection()
        for idx in valueobj:
            value=tree_stage.item(idx)["text"]

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

    #查看节点的数据
    def trefun(event):
        stageUI()
        data=stage.show_data(stage_file)
        values = event.widget.selection()
        for idx in values:
            stage_ui.var_stageID.set(tree_stage.item(idx)["text"][5:])
            stage_ui.var_stageName.set(data[tree_stage.item(idx)["text"]][2])
            stage_ui.var_stageStartDate_y.set(data[tree_stage.item(idx)["text"]][0][:4])
            stage_ui.var_stageStartDate_m.set(data[tree_stage.item(idx)["text"]][0][5:7])
            stage_ui.var_stage_endDate_y.set(data[tree_stage.item(idx)["text"]][0][8:12])
            stage_ui.var_stage_endDate_m.set(data[tree_stage.item(idx)["text"]][0][13:])

    #删除子节点
    def delete_node():
        global value
        if value=='':
            tk.messagebox.showinfo(title='提示',message='请选择节点,再进行删除!')
        else:
            tree = stage.read_xml(stage_file)
            del_parent_nodes = stage.find_nodes(tree, ".//")
            # 准确定位子节点并删除之
            target_del_node = stage.del_node_by_tagkeyvalue(del_parent_nodes,'type' ,{"id": value})
            stage.write_xml(tree, stage_file)
            tk.messagebox.showinfo(title='提示',message='删除成功!')
            show_stage_data()
            value = ''
            valueobj = ''

    #修改子节点弹出修改窗口
    def update_node():
        if value=='':
            tk.messagebox.showinfo(title='提示',message='请选择节点,再进行修改!')
        else:
            # 确定_修改子节点
            def confirm_add_node():
                # 1. 读取xml文件
                global value
                tree = stage.read_xml(stage_file)
                nodes = stage.find_nodes(tree, ".//")
                result_nodes = stage.get_node_by_keyvalue(nodes, {"id": value})
                stage.change_node_properties(result_nodes, {"id":var_update_node.get()})
                stage.write_xml(tree, stage_file)
                tk.messagebox.showinfo(title='提示',message='修改成功!')
                var_update_node.set('')
                root.destroy()
                show_stage_data()
                value=''
                valueobj=''

            # 取消_修改子节点
            def cancel_add_node():
                root.destroy()
                value=''
                valueobj=''

            root = tk.Toplevel(window)
            root.geometry('270x100')
            update_la = tk.Label(root, text='Type:').place(x=20, y=20)
            update_en = tk.Entry(root, textvariable=var_update_node)
            update_en.place(x=70, y=20)
            confirm = tk.Button(root,command=confirm_add_node,text='确定',width=5)
            confirm.place(x=50,y=60)
            cancel = tk.Button(root,command=cancel_add_node,text='取消',width=5)
            cancel.place(x=100,y=60)
            root.resizable(False, False)
            root.mainloop()

    def raise_frame(frame):
        frame.tkraise()

    def billsUI():
        raise_frame(bills_page)
        cancels()#清空用户页面控件数据
        wipe_data()#清空Stgae页面控件数据
        cancel_bills()  # 清空单据页面控件数据
        confirm.place(x=120,y=275)
        confirm_next.place(x=205, y=275)
        updateBills.place_forget()
        removeBills.place_forget()
        cancel_i.place(x=290, y=275)
    def userUI():
        raise_frame(adduser_page)
        cancels()#清空用户页面控件数据
        wipe_data()#清空Stgae页面控件数据
        cancel_bills()  # 清空单据页面控件数据
        confirm.place(x=120,y=275)
        confirm_next.place(x=205, y=275)
        updateBills.place_forget()
        removeBills.place_forget()
        cancel_i.place(x=290, y=275)

    def stageUI():
        raise_frame(stage_page)
        cancels()   #清空用户页面控件数据
        wipe_data() #清空Stgae页面控件数据
        cancel_bills()  #清空单据页面控件数据
        confirm.place(x=120,y=275)
        confirm_next.place(x=205, y=275)
        updateBills.place_forget()
        removeBills.place_forget()
        cancel_i.place(x=290, y=275)

    var_update_node = tk.StringVar()    #修改节点的数据
    #鼠标右键菜单
    def _right_key(event):
        menubar = Menu(window, tearoff=False)
        menubar.add_command(label='修改',command = update_node)
        menubar.add_command(label='删除',command = delete_node)
        menubar.post(event.x_root, event.y_root)

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
    confirm = tk.Button(bills_page, text='添加收据', width=8, command=confirms)
    confirm.place(x=120, y=275)
    confirm_next=tk.Button(bills_page,text='添加下一层',width=8,command=confirm_next)
    confirm_next.place(x=205,y=275)
    removeBills = tk.Button(bills_page, text='删 除', width=6, command=removeBills)
    updateBills = tk.Button(bills_page, text='修 改', width=6, command=updateBills)
    cancel_i = tk.Button(bills_page, text='清 空', width=6, command=cancel_bills)
    cancel_i.place(x=290, y=275)

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
    tree_stage.bind("<Double-Button-1>", trefun)
    tree_stage.bind("<<TreeviewSelect>>", choice)
    tree_stage.place(x=530, y=166)
    tree_stage.bind("<Button-3>", _right_key)

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

    tree_total["columns"] = ('ID', 'Fee Earners', 'Date', 'Billable MIns', 'Title', 'Rests', 'Total')
    tree_total.bind('<<TreeviewSelect>>',trefun_total)
    tree_total.column('ID', width=60, anchor="center")
    tree_total.column('Fee Earners', width=80, anchor="center")
    tree_total.column('Date', width=92, anchor="center")
    tree_total.column('Billable MIns', width=92, anchor="center")
    tree_total.column('Title', width=210, anchor="center")
    tree_total.column('Rests', width=82, anchor="center")
    tree_total.column('Total', width=82, anchor="center")
    tree_total.column('ID', width=60, anchor="center")
    tree_total.column('Fee Earners', width=80, anchor="center")
    tree_total.column('Date', width=92, anchor="center")
    tree_total.column('Billable MIns', width=92, anchor="center")
    tree_total.column('Title', width=210, anchor="center")
    tree_total.column('Rests', width=82, anchor="center")
    tree_total.column('Total', width=82, anchor="center")

    tree_total.heading('ID', text='ID')
    tree_total.heading('Fee Earners', text='Fee Earners')
    tree_total.heading('Date', text='Date')
    tree_total.heading('Billable MIns', text='Billable MIns')
    tree_total.heading('Title', text='Title')
    tree_total.heading('Rests', text='Rests')
    tree_total.heading('Total', text='Total')
    tree_total.place(x=0, y=333)

    window.mainloop()
