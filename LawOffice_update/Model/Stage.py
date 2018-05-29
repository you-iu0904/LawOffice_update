import xml.dom.minidom
from xml.etree.ElementTree import ElementTree,Element
from xml.dom import Node

class Stage():
    def __init__(self,id,name,start_date_y,start_date_m,end_date_y,end_date_m):
        self.id = id  #编号
        self.name = name  #名称
        self.start_date_y=start_date_y  #开始年份
        self.start_date_m=start_date_m  #开始月份
        self.end_date_y=end_date_y  #结束月份
        self.end_date_m=end_date_m
    #保存数据
    def save(self,file):
        impl = xml.dom.minidom.getDOMImplementation()
        # 设置根结点data
        dom = impl.createDocument(None, 'data', None)
        root = dom.documentElement
        employee = dom.createElement('stage')

        # 添加属性
        employee.setAttribute("name", self.name)
        employee.setAttribute("date", str(self.start_date_y)+'/'+str(self.start_date_m)+'-'+str(self.end_date_y)+'/'+str(self.end_date_m))
        employee.setAttribute("id", 'Stage' + str(self.id))
        root.appendChild(employee)
        f = open(file, 'w')
        dom.writexml(f, addindent=' ', newl='\n')
        f.close()

class XmlDao():
    @staticmethod
    def openXml(filename):
        tree = ElementTree()
        tree.parse(filename)
        return tree
    @staticmethod
    def saveAs(tree,outfile):
        tree.write(outfile, encoding="utf-8",xml_declaration=True)
    @staticmethod
    def add_child_node(nodelist, element):
        '''给一个节点添加子节点
           nodelist: 节点列表
           element: 子节点'''
        for node in nodelist:
            node.append(element)
    @staticmethod
    def del_node_by_tagkeyvalue(nodelist, tag, kv_map):
        '''同过属性及属性值定位一个节点，并删除之
           nodelist: 父节点列表
           tag:子节点标签
           kv_map: 属性及属性值列表'''
        for parent_node in nodelist:
            children = parent_node.getchildren()
            for child in children:
                if child.tag == tag and XmlDao.if_match(child, kv_map):
                    parent_node.remove(child)
    @staticmethod
    def create_node(tag, property_map, content=''):
        '''新造一个节点
           tag:节点标签
           property_map:属性及属性值map
           content: 节点闭合标签里的文本内容
           return 新节点'''
        element = Element(tag, property_map)
        element.text = content
        return element
    @staticmethod
    def change_node_text(nodelist, text, is_add=False, is_delete=False):
        '''改变/增加/删除一个节点的文本
           nodelist:节点列表
           text : 更新后的文本'''
        for node in nodelist:
            if is_add:
                node.text += text
            elif is_delete:
                node.text = ""
            else:
                node.text = text
    @staticmethod
    def change_node_properties(nodelist, kv_map, is_delete=False):
        '''修改/增加 /删除 节点的属性及属性值
           nodelist: 节点列表
           kv_map:属性及属性值map'''
        for node in nodelist:
            for key in kv_map:
                if is_delete:
                    if key in node.attrib:
                        del node.attrib[key]
                else:
                    node.set(key, kv_map.get(key))
    @staticmethod
    def get_node_by_keyvalue(nodelist, kv_map):
        '''根据属性及属性值定位符合的节点，返回节点
           nodelist: 节点列表
           kv_map: 匹配属性及属性值map'''
        result_nodes = []
        for node in nodelist:
            if XmlDao.if_match(node, kv_map):
                result_nodes.append(node)
        return result_nodes
    @staticmethod
    def find_nodes(tree, path):
        '''查找某个路径匹配的所有节点
           tree: xml树
           path: 节点路径'''
        return tree.findall(path)
    @staticmethod
    def if_match(node, kv_map):
        '''判断某个节点是否包含所有传入参数属性
           node: 节点
           kv_map: 属性及属性值组成的map'''
        for key in kv_map:
            if node.get(key) != kv_map.get(key):
                return False
        return True

class FlagDao():
    def __init__(self,filename):
        if filename is None:
            self.__filename = filename
        else:
            self.__filename = filename
    #获取节点属性
    def getValueByName(self,id):
        tree = XmlDao.openXml(self.__filename)

        if tree is None:
            return None
        nodes = XmlDao.find_nodes(tree, 'stage')
        nodes = XmlDao.get_node_by_keyvalue(nodes, {'id':id})
        if len(nodes) > 0:
            return nodes[0].attrib['value']
        return None
    #设置节点
    def setValueByName(self,name,value):
        tree = XmlDao.openXml(self.__filename)
        if tree is None:
            return None
        nodes = XmlDao.find_nodes(tree, 'stage')
        nodes = XmlDao.get_node_by_keyvalue(nodes, {'name':name})
        if len(nodes) > 0:
            nodes[0].attrib['value'] = value
            XmlDao.saveAs(tree, self.__filename)
    #添加节点
    def addTag(self,name,date,id):
        tree = XmlDao.openXml(self.__filename)
        XmlDao.add_child_node([tree.getroot()],XmlDao.create_node('stage', {'date':date,'name':name,'id':id}))
        XmlDao.saveAs(tree, self.__filename)
    #删除节点
    def deleteTagByName(self,id):
        tree = XmlDao.openXml(self.__filename)
        XmlDao.del_node_by_tagkeyvalue([tree.getroot()], 'stage', {'id':id})
        XmlDao.saveAs(tree, self.__filename)


#点击stage获得相关数据
def show_data(path):
    dictAttr = {}
    d={}
    dom = xml.dom.minidom.parse(path)
    root = dom.documentElement
    for child in root.childNodes:
        if child.nodeType == Node.ELEMENT_NODE:
            listInfos = []
            for key in child.attributes.keys():
                attr = child.attributes[key]
                listInfos.append( attr.value)
            dictAttr[ attr.value]=listInfos
    for i in dictAttr.values():
        data=[]
        data.append(i[0])
        data.append(i[2])
        d[str(i[1])]=data
    return d