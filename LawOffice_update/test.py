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

#打印单据数据


tree = et.parse("emplist.xml")
root = tree.getroot()
story = []
styles = getSampleStyleSheet()
bissdata1 = []
for country in root.findall('stage'):
    story.append(Paragraph(str(country.attrib['id']) + ':' + str(country.attrib['name']) + '(' + str(country.attrib['date'] + ')'),styles['title']))
    for i in country:
        bissdata = []
        data=[]
        data.append(i.attrib['id'])
        data.append('')
        data.append('')
        bissdata.append(data)
        component_table12 = Table(bissdata, colWidths=[150, 150, 150])
        story.append(component_table12)
        for s in i :
            data = []
            data.append('      '+str(s.attrib['id']))
            data.append('')
            data.append('')
            bissdata1.append(data)
            component_table12 = Table(bissdata1, colWidths=[150, 150, 150])
            story.append(component_table12)
            for k in s :
                bissdata1 = []
                try:
                    bissdata2 = []
                    data = []
                    data.append('      ' + str(k.attrib['id']))
                    data.append('')
                    data.append('')
                    bissdata1.append(data)
                    component_table12 = Table(bissdata2, colWidths=[150, 150, 150])
                    story.append(component_table12)
                except KeyError :
                    s_list = []
                    s_list.append(k.attrib['FeeEarners'])
                    s_list.append(k.attrib['Time'])
                    s_list.append(k.attrib['TotalMoney'])
                    bissdata1.append(s_list)



doc = SimpleDocTemplate('导出数据.pdf')
doc.build(story)

