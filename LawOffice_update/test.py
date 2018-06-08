



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



