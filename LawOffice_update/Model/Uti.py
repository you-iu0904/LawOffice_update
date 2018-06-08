import string
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as tk_font
import window.index
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
        # self.tree.bind("<Double-Button-1>", self.trefun)
        # self.tree.bind("<<TreeviewSelect>>", self.choice)
        # self.tree.bind("<Button-3>", self.right_key)


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