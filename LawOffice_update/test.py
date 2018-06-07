# import Model.Stage as stage
# import xml.dom.minidom
# from xml.etree.ElementTree import ElementTree,Element
# from xml.dom import Node
#
#
# def read_xml(in_path):
#     '''''读取并解析xml文件
#        in_path: xml路径
#        return: ElementTree'''
#     tree = ElementTree()
#     tree.parse(in_path)
#     return tree
#
# def find_nodes(tree, path):
#     '''''查找某个路径匹配的所有节点
#        tree: xml树
#        path: 节点路径'''
#     return tree.findall(path)
#
#
# def write_xml(tree, out_path):
#     '''''将xml文件写出
#        tree: xml树
#        out_path: 写出路径'''
#     tree.write(out_path, encoding="utf-8", xml_declaration=True)
#
#
# def if_match(node, kv_map):
#     '''''判断某个节点是否包含所有传入参数属性
#        node: 节点
#        kv_map: 属性及属性值组成的map'''
#     for key in kv_map:
#         if node.get(key) != kv_map.get(key):
#             return False
#     return True
#
# def del_node_by_tagkeyvalue(nodelist, tag, kv_map):
#     for parent_node in nodelist:
#         children = parent_node.getchildren()
#         for child in children:
#             if child.tag == tag and if_match(child, kv_map):
#                 parent_node.remove(child)
# def change_node_properties(nodelist, kv_map, is_delete=False):
#     '''''修改/增加 /删除 节点的属性及属性值
#        nodelist: 节点列表
#        kv_map:属性及属性值map'''
#     for node in nodelist:
#         for key in kv_map:
#             if is_delete:
#                 if key in node.attrib:
#                     del node.attrib[key]
#             else:
#                 node.set(key, kv_map.get(key))
# def get_node_by_keyvalue(nodelist, kv_map):
#     '''''根据属性及属性值定位符合的节点，返回节点
#        nodelist: 节点列表
#        kv_map: 匹配属性及属性值map'''
#     result_nodes = []
#     for node in nodelist:
#         if if_match(node, kv_map):
#             result_nodes.append(node)
#     return result_nodes
#
#
# if __name__ == "__main__":
#     # 1. 读取xml文件
#     tree = read_xml("emplist.xml")
#     nodes = find_nodes(tree, ".//")
#     result_nodes =get_node_by_keyvalue(nodes, {"serialNumber":'4'})
#     stage.change_node_properties(result_nodes, {"Date":'2018-07-21','Time':'123'})
#     stage.write_xml(tree, "emplist.xml")
#
# from tkinter import *
#
#
#
# root = Tk()
#
# lb = Listbox(root)
# # 水平方向滚动
# S1 = Scrollbar(root, orient=HORIZONTAL)
#
# S1.pack(side=BOTTOM, fill=X)
# lb['xscrollcommand'] = S1.get()
# for i in range(100):
#     lb.insert(END, i)
# lb.pack(side=TOP)
# S1['command'] = lb.yview
# root.mainloop()

from tkinter import *
from tkinter import ttk

root = Tk()

tree = ttk.Treeview(root)

tree["columns"]=("one","two")
tree.column("one", width=0 )
tree.column("two", width=0)
# tree.heading("one", text="coulmn A")
# tree.heading("two", text="column B")

# tree.insert("" , 0,    text="Line 1)

id2 = tree.insert("", 1, "dir2", text="Dir 2")
tree.insert(id2, "end", "dir 2", text="sub dir 2")

##alternatively:
tree.insert("", 3, "dir3", text="Dir 3")
tree.insert("dir3", 3, text=" sub dir 3")

tree.pack()
root.mainloop()