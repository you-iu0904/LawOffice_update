from xml.etree import ElementTree as et
import  xml.dom.minidom

treexml = et.parse('emplist.xml')
root = treexml.getroot()
for child in root:
    print(child.attrib)
    # for child1 in child:
    #     print(child1.attrib)
    #     for child2 in child1:
    #         try:
    #          child2.attrib['FeeEarners']
    #         except KeyError:
    #             print(child2.attrib)
    #         for  child3 in child2:
    #             try:
    #                 print(child3.attrib['FeeEarners'])
    #             except KeyError:
    #                 print(child3.attrib)
    print('-----------------')
    # print(str(child.attrib['id'])+':'+str(child.attrib['name'])+'('+str(child.attrib['date']+')'))
    # for i in child:
    #     print('    '+i.attrib['id'])

