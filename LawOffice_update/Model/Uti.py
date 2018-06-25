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
import os
import PyPDF2
import operator
from operator import itemgetter

pdfmetrics.registerFont(TTFont('msyh', 'STSONG.TTF'))
import Model.Stage as stage
import window.StageUI as stage_ui



# 排序_升序
def callBack(value,tree):
    date1 = []
    t = tree.get_children()
    for i in t:
        date1.append(tree.item(i, 'values'))
    items = tree.get_children()
    [tree.delete(item) for item in items]
    ss = {}
    content = []
    for s in date1:
        date2 = []
        date2.append(s[0])
        date2.append(s[1])
        date2.append(s[2])
        date2.append(int(s[3]))
        date2.append(s[4])
        date2.append(int(s[5]))
        date2.append(float(s[6]))
        ss[s[0]] = date2
    for i in ss.values():
        content.append(i)
    content.sort(key=operator.itemgetter(value), reverse=True)
    for s in content:
        tree.insert('', 0, values=(s[0], s[1], s[2], s[3], s[4], s[5], s[6]))

# 排序_降序
def callBack_order(value,tree):
    date1 = []
    t = tree.get_children()
    for i in t:
        date1.append(tree.item(i, 'values'))
    items = tree.get_children()
    [tree.delete(item) for item in items]
    ss = {}
    content = []
    for s in date1:
        date2 = []
        date2.append(s[0])
        date2.append(s[1])
        date2.append(s[2])
        date2.append(int(s[3]))
        date2.append(s[4])
        date2.append(int(s[5]))
        date2.append(float(s[6]))
        ss[s[0]] = date2
    for i in ss.values():
        content.append(i)
    content.sort(key=operator.itemgetter(value))
    for s in content:
        tree.insert('', 0, values=(s[0], s[1], s[2], s[3], s[4], s[5], s[6]))

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
    doc = SimpleDocTemplate(title+'1.pdf')
    doc.build(story)

def export(title,id,user_dict,stage_file):
    nums = 0
    totaltime = 0.0
    totalMoney = 0.0
    story = []
    styles = getSampleStyleSheet()
    total = [['', '', ''], ['Fee Earner', 'Total time(Hrs)', 'Total']]
    story1=[]
    normalStyle = styles['Normal']
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

    suminn_time = []
    suminn_moeny = []
    for country in root.findall('stage'):
        stage_total = []
        moeny = 0.0
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
                bissdata.append(data)
                stage_total.append(data)
            except KeyError:
                pass
            for s in i:
                try:
                    data = []
                    data.append(s.attrib['Date'])
                    data.append(s.attrib['FeeEarners'])
                    data.append(s.attrib['Time'])
                    data.append(s.attrib['Narrative'])
                    data.append(s.attrib['TotalMoney'])
                    bissdata.append(data)
                    stage_total.append(data)
                except KeyError:
                    pass
                for k in s:
                    try:
                        data = []
                        data.append(k.attrib['Date'])
                        data.append(k.attrib['FeeEarners'])
                        data.append(k.attrib['Time'])
                        data.append(k.attrib['Narrative'])
                        data.append(k.attrib['TotalMoney'])
                        bissdata.append(data)
                        stage_total.append(data)
                    except KeyError:
                        pass
                    for p in k:
                        try:
                            data = []
                            data.append(p.attrib['Date'])
                            data.append(p.attrib['FeeEarners'])
                            data.append(p.attrib['Time'])
                            data.append(p.attrib['Narrative'])
                            data.append(p.attrib['TotalMoney'])
                            bissdata.append(data)
                            stage_total.append(data)
                        except KeyError:
                            pass
                        for t in p:
                            try:
                                data = []
                                data.append(t.attrib['Date'])
                                data.append(t.attrib['FeeEarners'])
                                data.append(t.attrib['Time'])
                                data.append(t.attrib['Narrative'])
                                data.append(t.attrib['TotalMoney'])
                                bissdata.append(data)
                                stage_total.append(data)
                            except KeyError:
                                pass
                            for y in t:
                                try:
                                    data = []
                                    data.append(y.attrib['Date'])
                                    data.append(y.attrib['FeeEarners'])
                                    data.append(y.attrib['Time'])
                                    data.append(y.attrib['Narrative'])
                                    data.append(y.attrib['TotalMoney'])
                                    bissdata.append(data)
                                    stage_total.append(data)
                                except KeyError:
                                    pass
                                for o in y:
                                    try:
                                        data = []
                                        data.append(o.attrib['Date'])
                                        data.append(o.attrib['FeeEarners'])
                                        data.append(o.attrib['Time'])
                                        data.append(o.attrib['Narrative'])
                                        data.append(o.attrib['TotalMoney'])
                                        bissdata.append(data)
                                        stage_total.append(data)
                                    except KeyError:
                                        pass
        result_time = {}
        result_money = {}
        l = []
        for d in stage_total:
            result_time[d[1]] = round(float(result_time.get(d[1], 0)) + float(d[2]), 2)
            result_money[d[1]] = round(float(result_money.get(d[1], 0)) + float(d[4]), 1)
        l.append(result_time)
        l.append(result_money)

        for y in result_time:
            data = []
            data.append(y)
            data.append(result_time[y])
            suminn_time.append(data)
        for y2 in result_money:
            data = []
            data.append(y2)
            data.append(result_money[y2])
            suminn_moeny.append(data)
        dic = {}
        for _ in l:
            for k, v in _.items():
                dic.setdefault(k, []).append(v)
        money_list = [['', '', ''], ['Fee Earners', 'Hours', 'Total']]
        for ss in dic:
            totaltime += dic[ss][0]
            totalMoney += dic[ss][1]
            s = []
            s.append(ss)
            s.append(str(dic[ss][0]))
            s.append('$' + str(dic[ss][1]))
            money_list.append(s)
            moeny += dic[ss][1]
        moeny_o = []
        moeny_o.append('')
        moeny_o.append('')
        moeny_o.append('TOTAL:$' + str(moeny))
        money_list.append(moeny_o)
        li = ['', '', '']
        money_list.append(li)
        money_list1 = [['Stage Summary:', '', '']]

        component_table_bills = Table(bissdata, colWidths=[70, 70, 40, 290, 90])
        component_table_bills.setStyle(TableStyle([
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('FONTNAME', (0, 0), (-1, -1), 'msyh'),
            ('GRID', (0, 2), (4, 0), 0.5, colors.black)
        ]))

        story.append(component_table_bills)
        story.append(Paragraph('———————————————————————————————', normalStyle))
        component_tablel2 = Table(money_list, colWidths=[180, 180, 180])
        component_tablel2.setStyle(TableStyle([
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('FONTNAME', (0, 0), (-1, -1), 'msyh'),
            ('GRID', (0, 2), (3, 0), 0.5, colors.black)
        ]))
        component_tablel3 = Table(money_list1, colWidths=[180, 180, 180])
        component_tablel3.setStyle(TableStyle([
            ('FONTSIZE', (0, 0), (-1, -1), 20),
            ('FONTNAME', (0, 0), (-1, -1), 'msyh'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),  # 字体大小
        ]))
        story.append(component_tablel3)
        story.append(component_tablel2)

        nums += 1
        doc = SimpleDocTemplate('PDF/导出数据' + str(nums) + '.pdf')
        doc.build(story)

    p = []
    result_time = dict()
    for data in suminn_time:
        result_time[data[0]] = float(result_time.get(data[0], 0)) + float(data[1])
    result_money = dict()
    for data in suminn_moeny:
        result_money[data[0]] = float(result_money.get(data[0], 0)) + float(data[1])
    sum = []
    sum.append(result_time)
    sum.append(result_money)
    dic1 = {}
    for _ in sum:
        for k, v in _.items():
            dic1.setdefault(k, []).append(v)
    for i in dic1:
        value = []
        value.append(i)
        value.append(round(dic1[i][0], 2))
        value.append('$' + str(dic1[i][1]))
        total.append(value)
    tota2 = []

    p.append('')
    p.append('Total: ' + str(round(totaltime, 2)))
    p.append('$' + str(round(totalMoney, 2)))
    tota2.append(p)
    summ = [['Summary: ', '', '']]
    component_tablel4 = Table(summ, colWidths=[180, 180, 180])
    component_tablel3 = Table(total, colWidths=[180, 180, 180])
    component_tablel5 = Table(tota2, colWidths=[180, 180, 180])
    component_tablel3.setStyle(TableStyle([
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('FONTNAME', (0, 0), (-1, -1), 'msyh'),
        ('GRID', (0, 2), (2, 0), 0.5, colors.black)
    ]))
    story1.append(component_tablel4)
    story1.append(component_tablel3)
    story1.append(Paragraph('———————————————————————————————', normalStyle))
    story1.append(component_tablel5)
    doc1 = SimpleDocTemplate(os.getcwd() + '/PDF/导出数据' + str(nums + 1) + '.pdf')
    doc1.build(story1)
    path = os.getcwd() + '/PDF'  # 文件夹目录
    files = os.listdir(path)  # 得到文件夹下的所有文件名称
    s = []
    for file in files:  # 遍历文件夹
        s.append(file)
    merger = PyPDF2.PdfFileMerger()
    for filename in s:
        merger.append(PyPDF2.PdfFileReader(os.getcwd() + '/PDF' + '/' + filename))
        os.remove(os.getcwd() + '/PDF' + '/' + filename)
    merger.write(title+'2.pdf')




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
# getIdName('asd.xml',)