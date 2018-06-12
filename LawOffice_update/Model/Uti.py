import string
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as tk_font
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer,Image,Table,TableStyle
from reportlab.pdfbase import pdfmetrics, ttfonts
pdfmetrics.registerFont(TTFont('msyh', 'STSONG.TTF'))
import Model.Stage as stage
import window.StageUI as stage_ui
from xml.etree import ElementTree as et

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
    treexml = et.parse(stage_file)
    root = treexml.getroot()

    for child in root:
        data_list=[]
        story.append(Paragraph(str(child.attrib['id'])+':'+str(child.attrib['name'])+'('+str(child.attrib['date']+')'),styles['title']))
        bissdata = [['', '', '']]

        for child1 in child:
            data=[]
            data.append(str(child1.attrib['id']))
            bissdata.append(data)
            for child2 in child1:
                try:
                    data = []
                    data.append('      '+str(child2.attrib['id']))
                    bissdata.append(data)
                except KeyError :
                    s_list = []
                    bissdata1 = []
                    s_list.append(child2.attrib['FeeEarners'])
                    s_list.append(child2.attrib['Time'])
                    s_list.append(child2.attrib['TotalMoney'])
                    data_list.append(s_list)
                    text(data_list, bissdata1)
                    component_table12 = Table(bissdata1, colWidths=[150, 150, 150])
                    story.append(component_table12)

            component_table11 = Table(bissdata, colWidths=[150, 150, 150])
            story.append(component_table11)

        # component_table12 = Table(bissdata1, colWidths=[50, 40, 75,75, 75, 75,60])
        # story.append(component_table12)




    doc = SimpleDocTemplate('导出数据.pdf')
    doc.build(story)

def text(data_list,bissdata):
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
        data = []
        data.append('      ' + '(  ' + str(i))
        data.append('')
        data.append(str(0)+'      hr.      '+str(dic[i][0])+'      mins.' if dic[i][0]<60 else str(int(dic[i][0]) / 60)+'      hr.      '+str(int(int(dic[i][0]) %60))+'      mins.')
        data.append('')
        data.append('$' + str(dic[i][1]) + '  )')
        data.append('')
        data.append('')
    bissdata.append(data)

