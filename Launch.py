from xml.dom.minidom import parse
import xml.dom.minidom
import os

## 寻找老素材的地址
dir_old = "/Users/sodino/NativeProjects/textconfiguration/old"
## 记录所有的Tag名称
tags = {}
## 记录所有的format格式
formats = {}

class TextXML:
    count = 0
    def read2parse_xml(self, path):
        dom_tree = xml.dom.minidom.parse(path)
        root_element = dom_tree.documentElement
        list_all_nodes = [root_element]
        while len(list_all_nodes) > 0:
            first_node = list_all_nodes[0]
            list_all_nodes.remove(first_node)

            if first_node.childNodes.length > 0 :
                list_all_nodes.extend(first_node.childNodes)

            if first_node.nodeType == xml.dom.Node.TEXT_NODE:
                continue
            tags[first_node.nodeName] = ""
            if first_node.nodeName == "format":
                if first_node.childNodes.length > 0:
                    ## 获取xml字段名对应的字段值
                    format_value = first_node.childNodes[0].data
                    formats[format_value] = ""






def findAllFile(base):
    for root, ds, fs in os.walk(base):
        for f in fs:
            if f.endswith("TextBubbleInfo.xml"):
                fullname = os.path.join(root, f)
                yield fullname


if __name__ == '__main__':
    ##  当前目录路径
    # current_path = os.getcwd()
    # test_xml = TextXML()
    # test_xml.read2parse_xml(current_path + "/TextBubbleInfo.xml")
    for i in findAllFile(dir_old) :
        test_xml = TextXML()
        test_xml.read2parse_xml(i)

    print("xml all tagNames are : " + str(tags.keys()))
    print("xml all formats are : " + str(formats.keys()))
