from xml.etree import ElementTree as et

def show_data(xml_file,value):
    tree = et.parse(xml_file)
    root = tree.getroot()
    number=0
    for country in root.iter(value):
        for i in country:
           i.attrib['id']
           number+=1
           try:
               for s in i:
                    s.attrib['id']
                    number+=1
           except KeyError :
               pass
    print(number)
show_data('asd.xml','Stage1')