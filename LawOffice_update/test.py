import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as tk_font
from xml.etree import ElementTree as et

class TreeListBox:
    def __init__(self, master, root, dict_group):
        self.master = master
        self.root = root
        self.dict_group = dict_group
        self.level = 0
        self.setup_widget_tree()
        self.build_tree(self.root, '')

    def setup_widget_tree(self):
        container_tree = tk.Frame(self.master, width=250, height=300)
        container_tree.propagate(False)
        container_tree.pack(side="left", fill='y')
        self.tree = ttk.Treeview(container_tree, show="tree", selectmode='browse')
        fr_y = tk.Frame(container_tree)
        fr_y.pack(side='right', fill='y')
        tk.Label(fr_y, borderwidth=1, relief='raised', font="Arial 8").pack(side='bottom', fill='x')
        sb_y = tk.Scrollbar(fr_y, orient="vertical", command=self.tree.yview)
        sb_y.pack(expand='yes', fill='y')
        fr_x = tk.Frame(container_tree)
        fr_x.pack(side='bottom', fill='x')
        sb_x = tk.Scrollbar(fr_x, orient="horizontal", command=self.tree.xview)
        sb_x.pack(expand='yes', fill='x')
        self.tree.configure(yscrollcommand=sb_y.set, xscrollcommand=sb_x.set)
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

if __name__ == '__main__':
    treexml = et.parse('emplist.xml')
    root = treexml.getroot()
    d_dict = {}
    node = []

    for child in root:
        s = []
        data = child.attrib['id']
        node.append(data)
        for i in child:
            data1 = i.attrib['id']
            s.append(data1)
            d_dict[data] = s

    d_dict['Nomenclature'] = node

    root = tk.Tk()
    myTest = TreeListBox(root, 'Nomenclature', d_dict)
    root.mainloop()



