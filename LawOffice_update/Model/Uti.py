import string
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as tk_font
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer,Image,Table,TableStyle
from reportlab.pdfbase import pdfmetrics, ttfonts
from lxml import etree
from xml.etree import ElementTree as et
pdfmetrics.registerFont(TTFont('msyh', 'STSONG.TTF'))
import Model.Stage as stage
import window.StageUI as stage_ui


#判断字符串内容是否为数字
def check(a):
    if type(a) is not str:
        return False
    else:
        for i in a:
            if i not in string.digits:
                return False
        return True

#水平滚动条
class TreeListBox:
    def __init__(self, master, root, dict_group,stage_file,tree,container_tree):
        self.stage_file=stage_file
        self.tree = tree
        self.container_tree = container_tree
        self.master = master
        self.root = root
        self.setup_widget_tree()
        self.dict_group = dict_group
        self.level = 0
        self.build_tree(self.root, '')

    def setup_widget_tree(self):
        fr_x = tk.Frame(self.container_tree)
        fr_x.pack(side='bottom', fill='x')
        sb_x = tk.Scrollbar(fr_x, orient="horizontal", command=self.tree.xview)
        sb_x.pack(expand='yes', fill='x')
        self.tree.configure( xscrollcommand=sb_x.set)
        self.tree.pack(fill='both', expand='yes')



    def build_tree(self, parent, id_stroki):
        self.level += 1
        id = self.tree.insert(id_stroki, 'end', text=parent)
        # -----------------
        col_w = tk_font.Font().measure(parent)
        if col_w > 1000:
            col_w -= 400
        elif col_w > 500:
            col_w -= 200
        elif col_w > 300:
            col_w -= 100
        col_w = col_w + 25 * self.level
        if col_w > self.tree.column('#0', 'width'):
            self.tree.column('#0', width=col_w)
        # -----------------
        try:

            for element in sorted(self.dict_group[parent]):
                self.build_tree(element, id)
        except KeyError:
            pass
        self.level -= 1

#导出PDF
def exportPDF(title,id,user_dict,stage_file):
    story = []
    styles = getSampleStyleSheet()
    #导出标题和编号
    story.append(Paragraph(str(title) + ': ' + str(id), styles['Heading1']))

    # 打印用户信息
    com = [['', '', '', ''], ['Fee Earners', 'Admitted time', 'Title', 'Hourly Rate']]
    for i in user_dict:
        ss = []
        ss.append(i + '(' + str(user_dict[i][0]) + ')')
        ss.append(str(user_dict[i][1]))
        ss.append(str(user_dict[i][2]))
        ss.append('$' + str(user_dict[i][4] * 60))
        com.append(ss)
    component_table = Table(com, colWidths=[140, 140, 140, 140, 140])
    component_table.setStyle(TableStyle([
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('FONTNAME', (0, 0), (-1, -1), 'msyh'),
        ('GRID', (0, 2), (4, 0), 0.5, colors.black)
    ]))
    story.append(component_table)

    #打印单据数据
    tree = et.parse(stage_file)
    root = tree.getroot()
    bissdata1 = []

    for country in root.findall('stage'):
        story.append(Paragraph('', styles['title']))
        story.append(Paragraph('', styles['title']))
        story.append(Paragraph(
            str(country.attrib['id']) + ':' + str(country.attrib['name']) + '(' + str(country.attrib['date'] + ')'),
            styles['title']))
        for i in country:
            data = []
            data.append(i.attrib['id'])
            data.append('')
            data.append('')
            bissdata1.append(data)

            data2_bills = []

            for s in i:
                try:
                    data2 = []
                    data2.append('      ' + str(s.attrib['id']))
                    data2.append('')
                    data2.append('')
                    bissdata1.append(data2)
                except KeyError:
                    o = []
                    o.append(s.attrib['FeeEarners'])
                    o.append(s.attrib['Time'])
                    o.append(s.attrib['TotalMoney'])
                    data2_bills.append(o)

                data3_bills = []
                for k in s:
                    try:
                        data3 = []
                        data3.append('            ' + str(k.attrib['id']))
                        data3.append('')
                        data3.append('')
                        bissdata1.append(data3)
                    except KeyError:
                        o = []
                        o.append(k.attrib['FeeEarners'])
                        o.append(k.attrib['Time'])
                        o.append(k.attrib['TotalMoney'])
                        data3_bills.append(o)

                    data4_bills = []
                    for z in k:
                        try:
                            data4 = []
                            data4.append('             ' + str(z.attrib['id']))
                            data4.append('')
                            data4.append('')
                            bissdata1.append(data4)
                        except KeyError:
                            o = []
                            o.append(z.attrib['FeeEarners'])
                            o.append(z.attrib['Time'])
                            o.append(z.attrib['TotalMoney'])
                            data4_bills.append(o)
                    statistics(data4_bills, bissdata1)
                statistics(data3_bills, bissdata1)
            statistics(data2_bills, bissdata1)
        component_table12 = Table(bissdata1, colWidths=[80, 150, 220])
        story.append(component_table12)
        bissdata1.clear()
        bissdata1.append('')
    doc = SimpleDocTemplate('导出数据1.pdf')
    doc.build(story)

def export(title,id,user_dict,stage_file):
    story = []
    styles = getSampleStyleSheet()
    # 导出标题和编号
    story.append(Paragraph(str(title) + ': ' + str(id), styles['Heading1']))

    # 打印用户信息
    com = [['', '', '', ''], ['Fee Earners', 'Admitted time', 'Title', 'Hourly Rate']]
    for i in user_dict:
        ss = []
        ss.append(i + '(' + str(user_dict[i][0]) + ')')
        ss.append(str(user_dict[i][1]))
        ss.append(str(user_dict[i][2]))
        ss.append('$' + str(user_dict[i][4] * 60))
        com.append(ss)
    component_table = Table(com, colWidths=[140, 140, 140, 140, 140])
    component_table.setStyle(TableStyle([
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('FONTNAME', (0, 0), (-1, -1), 'msyh'),
        ('GRID', (0, 2), (4, 0), 0.5, colors.black)
    ]))
    story.append(component_table)


    #打印单据数据
    tree = et.parse(stage_file)
    root = tree.getroot()
    bissdata1 = []
    for country in root.findall('stage'):
        story.append(Paragraph('', styles['title']))
        story.append(Paragraph('', styles['title']))
        story.append(Paragraph(str(country.attrib['id']) + ':' + str(country.attrib['name']) + '(' + str(country.attrib['date'] + ')'),
            styles['title']))
        bissdata = [['', '', '', '', ''], ['Date', 'Fee Earner', 'Hours', 'Narrative', 'Total']]
        for i in country:
            try:
                data = []
                data.append(i.attrib['Date'])
                data.append(i.attrib['FeeEarners'])
                data.append(i.attrib['Time'])
                data.append(i.attrib['Narrative'])
                data.append(i.attrib['TotalMoney'])

            except KeyError:
                pass
        component_table_bills = Table(bissdata, colWidths=[70, 70, 40, 290, 90])
        component_table_bills.setStyle(TableStyle([
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('FONTNAME', (0, 0), (-1, -1), 'msyh'),
            ('GRID', (0, 2), (4, 0), 0.5, colors.black)
        ]))
        story.append(component_table_bills)



    doc = SimpleDocTemplate('导出数据2.pdf')
    doc.build(story)
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
        datas.append('                   ' + '(  ' + str(i))
        datas.append('        '+str('-')+'      hr.      '+str(dic[i][0])+'      mins.' if dic[i][0]<60 else '        '+str(int(dic[i][0]) / 60)+'      hr.      '+str(int(int(dic[i][0]) %60))+'      mins.')
        datas.append('$' + str(dic[i][1]) + '  )')
        bissdata.append(datas)



#根据子节点返回父节点
def getIdName(stage_file,value):
    content = ""
    with open(stage_file, 'r') as f:
        content = f.read()
    xml = etree.fromstring(content)
    s = xml.findall('.//type[@id='+'"'+value+'"'+']...')
    return s[0].attrib['id']