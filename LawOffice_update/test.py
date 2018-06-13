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
pdfmetrics.registerFont(TTFont('msyh', 'STSONG.TTF'))
import Model.Stage as stage
import window.StageUI as stage_ui
from xml.etree import ElementTree as et

def test(data_list,bissdata):
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
        datas.append('      ' + '(  ' + str(i))
        datas.append(str(0)+'      hr.      '+str(dic[i][0])+'      mins.' if dic[i][0]<60 else str(int(dic[i][0]) / 60)+'      hr.      '+str(int(int(dic[i][0]) %60))+'      mins.')
        datas.append('$' + str(dic[i][1]) + '  )')
        bissdata.append(datas)


#打印单据数据
tree = et.parse("emplist.xml")
root = tree.getroot()
story = []
styles = getSampleStyleSheet()
bissdata1 = []
s_list = []
s_list1 = []
cs=[]
for country in root.findall('stage'):
    story.append(Paragraph(str(country.attrib['id']) + ':' + str(country.attrib['name']) + '(' + str(country.attrib['date'] + ')'),styles['title']))
    for i in country:
        data=[]
        data.append(i.attrib['id'])
        data.append('')
        data.append('')
        bissdata1.append(data)
        for s in i :
            try:
                data2 = []
                data2.append('      '+str(s.attrib['id']))
                data2.append('')
                data2.append('')
                bissdata1.append(data2)
            except KeyError:
                data2 = []
                data2.append('           (' + str(s.attrib['FeeEarners']))
                data2.append(str(0) + '      hr.      ' + str(s.attrib['Time']) + '      mins.' if int(s.attrib['Time']) < 60 else str(int(int(s.attrib['Time']) / 60)) + '      hr.      ' + str(int(int(s.attrib['Time']) % 60)) + '      mins.')
                data2.append('$ ' + str(s.attrib['TotalMoney']) + ')')
                bissdata1.append(data2)
            for k in s :
                try:
                    data3 = []
                    data3.append('      ' + str(k.attrib['id']))
                    data3.append('')
                    data3.append('')
                    bissdata1.append(data)
                except KeyError :
                    data3=[]
                    data3.append('           ('+str(k.attrib['FeeEarners']))
                    data3.append(str(0) + '      hr.      ' + str(k.attrib['Time']) + '      mins.' if int(k.attrib['Time']) < 60 else str(int(int(k.attrib['Time']) / 60)) + '      hr.      ' + str(int(int(k.attrib['Time']) % 60)) + '      mins.')
                    data3.append('$ '+str(k.attrib['TotalMoney'])+')')
                    bissdata1.append(data3)

    component_table12 = Table(bissdata1, colWidths=[80, 150, 220])
    story.append(component_table12)
    bissdata1.clear()
    bissdata1.append('')

doc = SimpleDocTemplate('导出数据.pdf')
doc.build(story)



