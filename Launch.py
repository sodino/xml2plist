from xml.dom.minidom import parse
import xml.dom.minidom
import os

## 寻找老素材的地址
dir_old = "/Users/sodino/NativeProjects/textconfiguration/old"
## 记录所有的Tag名称
tags = {}

class TextXML:
    count = 0
    def read2parse_xml(self, path):
        dom_tree = xml.dom.minidom.parse(path)
        root_element = dom_tree.documentElement
        listAllNodes = [root_element]
        while len(listAllNodes) > 0:
            firstNode = listAllNodes[0]
            listAllNodes.remove(firstNode)

            if firstNode.childNodes.length > 0 :
                listAllNodes.extend(firstNode.childNodes)

            if firstNode.nodeType == xml.dom.Node.TEXT_NODE:
                continue
            tags[firstNode.nodeName] = ""






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
