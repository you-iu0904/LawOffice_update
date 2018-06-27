from xml.etree import ElementTree as et

tree = et.parse('asd.xml')
root = tree.getroot()

for country in root.findall('stage'):
    print(country.attrib['id'])
    for i in country:
       print(i.attrib['id'])
       if str(i.attrib['id']) == 'Stage1':
           for s in i:
               print(s.attrib['id'])
       else:
            pass