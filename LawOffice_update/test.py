from lxml import etree
def getIdName(stage_file,value):
    content = ""
    with open(stage_file, 'r') as f:
        content = f.read()
    xml = etree.fromstring(content)
    s = xml.findall('.//type[@id='+'"'+value+'"'+']...')
    return s[0].attrib['id']
print(getIdName('asd.xml','asd'))