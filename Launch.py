from xml.dom.minidom import parse
import xml.dom.minidom
import os

## 寻找老素材的地址
dir_old = "/Users/sodino/NativeProjects/textconfiguration/old"
## 记录所有的Tag名称
tags = {}
## 记录所有的format格式
formats = {}

class XmlFrameRect:
    ## xml中 <frameRect>的值 : >{{305,25},{105,575}}
    content         = ""

class XmlTextPiece:
    type            = 0
    text            = ""
    format          = ""
    language        = ""
    caseString      = ""
    editable        = True
    color           = ""

    isBold          = False
    isItalic        = False
    autoLineBreak   = False

    isVerticalText  = False
    align           = 0
    verticalAlign   = 0
    font            = ""

    showShadow      = False
    shadowColor     = ""
    ## <shadowOffset>{1.000000,1.000000}</shadowOffset>
    shadowOffset    = ""


class TextXML:
    resId                   = 0
    name                    = ""

    width                   = 0
    height                  = 0

    backgroundImagePath     = ""

    mirrorReverse           = 0
    textPieceArray          = []

    ## 当前xml的绝对路径
    __xml_path              = ""

    def __init__(self, xml_path):
        self.__xml_path = xml_path

    ## 收集所有关注的xml字段名或字段值
    def collect_all_infos(self, root_element):
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

    def parse_xml(self):
        dom_tree = xml.dom.minidom.parse(self.__xml_path)
        root_element = dom_tree.documentElement
        self.collect_all_infos(root_element)






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
    for xml_path in findAllFile(dir_old) :
        test_xml = TextXML(xml_path)
        test_xml.parse_xml()

    print("xml all tagNames are : " + str(tags.keys()))
    print("xml all formats are : " + str(formats.keys()))
