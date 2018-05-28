import xml.dom.minidom
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
        employee.setAttribute("id", 'Stage'+str(self.id))
        employee.setAttribute("name", self.name)
        employee.setAttribute("date", str(self.start_date_y)+'/'+str(self.start_date_m)+'-'+str(self.end_date_y)+'/'+str(self.end_date_m))
        root.appendChild(employee)

        f = open(file, 'a')
        dom.writexml(f, addindent=' ', newl='\n')
        f.close()