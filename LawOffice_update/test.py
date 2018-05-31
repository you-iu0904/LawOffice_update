from xml.etree.ElementTree import ElementTree, Element




if __name__ == "__main__":
    # 1. 读取xml文件
    tree = read_xml("emplist.xml")

    # 2. 属性修改
    # A. 找到父节点
    nodes = find_nodes(tree, "stage")
    # # B. 通过属性准确定位子节点
    result_nodes = get_node_by_keyvalue(nodes, {"id": "Stage2"})

    # A.新建节点
    a = create_node("person", {"age": "15", "money": "200000"}, None)
    # B.插入到父节点之下
    add_child_node(result_nodes, a)
    # 6. 输出到结果文件
    write_xml(tree, "out.xml")



