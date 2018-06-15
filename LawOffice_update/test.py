from xml.etree import ElementTree as et
import string
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as tk_font
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer,Image,Table,TableStyle
from reportlab.pdfbase import pdfmetrics, ttfonts
import  xml.dom.minidom
import os
import PyPDF2
pdfmetrics.registerFont(TTFont('msyh', 'STSONG.TTF'))
import Model.Stage as stage
import window.StageUI as stage_ui
from xml.etree import ElementTree as et

#统计单据
def statistics(data_list,bissdata):
    result_time = {}
    result_money = {}
    for d in data_list:
        result_time[d[0]] = round(float(result_time.get(d[0], 0)) + float(d[1]), 2)
        result_money[d[0]] = round(float(result_money.get(d[0], 0)) + float(d[2]), 1)
    l = []
    l.append(result_time)
    l.append(result_money)
    dic = {}
    for _ in l:
        for k, v in _.items():
            dic.setdefault(k, []).append(v)
    for i in dic:
        datas = []
        datas.append('            ' + '(  ' + str(i))
        datas.append(str(0)+'      hr.      '+str(dic[i][0])+'      mins.' if dic[i][0]<60 else str(int(dic[i][0]) / 60)+'      hr.      '+str(int(int(dic[i][0]) %60))+'      mins.')
        datas.append('$' + str(dic[i][1]) + '  )')
        bissdata.append(datas)


#打印单据数据
tree = et.parse("emplist.xml")
root = tree.getroot()
story = []
styles = getSampleStyleSheet()
bissdata1 = []
nums = 0
for country in root.findall('stage'):
    story.append(Paragraph('',styles['title']))
    story.append(Paragraph('', styles['title']))
    story.append(Paragraph(str(country.attrib['id']) + ':' + str(country.attrib['name']) + '(' + str(country.attrib['date'] + ')'),styles['title']))
    for i in country:
        data=[]
        data.append(i.attrib['id'])
        data.append('')
        data.append('')
        bissdata1.append(data)
        data2_bills = []
        for s in i :
            try:
                data2 = []
                data2.append('      '+str(s.attrib['id']))
                data2.append('')
                data2.append('')
                bissdata1.append(data2)
            except KeyError:
                o = []
                o.append(s.attrib['FeeEarners'])
                o.append(s.attrib['Time'])
                o.append(s.attrib['TotalMoney'])
                data2_bills.append(o)

            data3_bills=[]
            for k in s :
                try:
                    data3 = []
                    data3.append('      ' + str(k.attrib['id']))
                    data3.append('')
                    data3.append('')
                    bissdata1.append(data3)
                except KeyError :
                    o=[]
                    o.append(k.attrib['FeeEarners'])
                    o.append(k.attrib['Time'])
                    o.append(k.attrib['TotalMoney'])
                    data3_bills.append(o)

                data4_bills = []
                for z in k:
                    try:
                        data4 = []
                        data4.append('      ' + str(z.attrib['id']))
                        data4.append('')
                        data4.append('')
                        bissdata1.append(data4)
                    except KeyError:
                        o = []
                        o.append(z.attrib['FeeEarners'])
                        o.append(z.attrib['Time'])
                        o.append(z.attrib['TotalMoney'])
                        data4_bills.append(o)
                test(data4_bills, bissdata1)
            test(data3_bills, bissdata1)
        test(data2_bills, bissdata1)

    component_table12 = Table(bissdata1, colWidths=[80, 150, 220])
    story.append(component_table12)
    bissdata1.clear()
    bissdata1.append('')

doc = SimpleDocTemplate('导出数据.pdf')
doc.build(story)



