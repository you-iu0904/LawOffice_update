import xml.dom.minidom
def GenerateXml():
    impl = xml.dom.minidom.getDOMImplementation()
    # 设置根结点data
    dom = impl.createDocument(None, 'data', None)
    root = dom.documentElement
    employee = dom.createElement('stage')

    #添加属性
    employee.setAttribute("id", "stage1")
    employee.setAttribute("name", "pre action stage")
    employee.setAttribute("date", "2010/11-2011/6")
    root.appendChild(employee)

    #添加子节点
    typeE=dom.createElement('type')
    typeT=dom.createTextNode('Conference within stage1')
    typeE.appendChild(typeT)
    employee.appendChild(typeE)


    #添加子节点
    typeE2=dom.createElement('type')
    typeT2=dom.createTextNode('Communication within stage1')
    typeE2.appendChild(typeT2)
    employee.appendChild(typeE2)

    #添加子节点
    typeE3=dom.createElement('type')
    typeT3=dom.createTextNode('Attending')
    typeE3.appendChild(typeT3)
    employee.appendChild(typeE3)

    #添加子节点
    typeE4=dom.createElement('type')
    typeT4=dom.createTextNode('Perusing and considering')
    typeE4.appendChild(typeT4)
    employee.appendChild(typeE4)


    f = open('emplist.xml', 'w')
    dom.writexml(f, addindent=' ', newl='\n')
    f.close()
GenerateXml()