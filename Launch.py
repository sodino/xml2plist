from xml.dom.minidom import parse
import xml.dom.minidom
import os

## 寻找老素材的地址
dir_old = "/Users/sodino/NativeProjects/textconfiguration/old"
## 记录所有的Tag名称
tags = {}
## 记录所有的format格式
formats = {}

def xml_node_value(node):
    if node.childNodes.length == 0:
        return ''
    else:
        value = node.childNodes[0].data
        return value

def xml_elements_value(elements):
    value = elements[0].childNodes[0].data
    return value

class XmlFrameRect:
    ## xml中 <frameRect>的值 : >{{305,25},{105,575}}
    content         = ""

    x               = ""
    y               = ""
    width           = ""
    height          = ""

    def __init__(self, content):
        self.content = content
        tmp = content.replace("{", "").replace("}", "")
        values = tmp.split(',')
        self.x = values[0]
        self.y = values[1]
        self.width = values[2]
        self.height = values[3]

    def __str__(self):
        return "[x,y=%s,%s, w,h=%s,%s]" %(self.x, self.y, self.width, self.height)

class XmlTextPiece:
    type            = ""
    text            = ""
    format          = ""
    language        = ""
    caseString      = ""
    editable        = ""
    color           = ""

    isBold          = ""
    isItalic        = ""
    autoLineBreak   = ""

    isVerticalText  = ""
    align           = ""
    verticalAlign   = ""
    font            = ""

    showShadow      = ""
    shadowColor     = ""
    ## <shadowOffset>{1.000000,1.000000}</shadowOffset>
    shadowOffset    = ""
    frameRect       = ""

    def __str__(self):
        value = "type=%s text='%s' format='%s' color='%s' frameRect:%s"\
                % (self.type, self.text, self.format, self.color, self.frameRect)

        return value


class TextXML:
    resId                   = ""

    width                   = ""
    height                  = ""

    backgroundImagePath     = ""

    mirrorReverse           = ""
    textPieceArray          = []

    ## 当前xml的绝对路径
    __xml_path              = ""

    def __init__(self, xml_path):
        self.__xml_path = xml_path

    def __str__(self):
        return "resId(%s) [w, h]=[%s, %s] bg=%s" %(self.resId, self.width, self.height, self.backgroundImagePath)

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
                    format_value = xml_node_value(first_node)
                    formats[format_value] = ""

    def read_textPiece(self, textPiece):
        nodes = textPiece.childNodes
        xPiece = XmlTextPiece()
        for node in nodes:
            if node.nodeType == xml.dom.Node.TEXT_NODE:
                continue
            if 'type' == node.tagName:
                xPiece.type = xml_node_value(node)
            elif 'text' == node.tagName:
                xPiece.text = xml_node_value(node)
            elif 'format' == node.tagName:
                xPiece.format = xml_node_value(node)
            elif 'language' == node.tagName:
                xPiece.language = xml_node_value(node)
            elif 'caseString' == node.tagName:
                xPiece.caseString = xml_node_value(node)
            elif 'editable' == node.tagName:
                xPiece.editable = xml_node_value(node)
            elif 'color' == node.tagName:
                xPiece.color = xml_node_value(node)
            elif 'isBold' == node.tagName:
                xPiece.isBold = xml_node_value(node)
            elif 'isItalic' == node.tagName:
                xPiece.isItalic = xml_node_value(node)
            elif 'autoLineBreak' == node.tagName:
                xPiece.autoLineBreak = xml_node_value(node)
            elif 'isVerticalText' == node.tagName:
                xPiece.isVerticalText = xml_node_value(node)
            elif 'align' == node.tagName:
                xPiece.align = xml_node_value(node)
            elif 'verticalAlign' == node.tagName:
                xPiece.verticalAlign = xml_node_value(node)
            elif 'font' == node.tagName:
                xPiece.font = xml_node_value(node)
            elif 'showShadow' == node.tagName:
                xPiece.showShadow = xml_node_value(node)
            elif 'shadowColor' == node.tagName:
                xPiece.shadowColor = xml_node_value(node)
            elif 'shadowOffset' == node.tagName:
                xPiece.shadowOffset = xml_node_value(node)
            elif 'frameRect' == node.tagName:
                tmpValue = xml_node_value(node)
                xPiece.frameRect = XmlFrameRect(tmpValue)

        self.textPieceArray.append(xPiece)



    def read_textPieceArray(self, textPieceArray):
        array = textPieceArray[0]
        for textPiece in array.childNodes:
            if textPiece.nodeType == xml.dom.Node.TEXT_NODE:
                continue
            self.read_textPiece(textPiece)

    def read_tag_values(self, root_element):
        e_resId = root_element.getElementsByTagName("resId")
        self.resId = xml_elements_value(e_resId)

        e_width = root_element.getElementsByTagName("width")
        self.width = xml_elements_value(e_width)

        e_height = root_element.getElementsByTagName("height")
        self.height = xml_elements_value(e_height)

        e_backgroundImagePath = root_element.getElementsByTagName("backgroundImagePath")
        self.backgroundImagePath = xml_elements_value(e_backgroundImagePath)

        e_mirrorReverse = root_element.getElementsByTagName("mirrorReverse")
        self.mirrorReverse = xml_elements_value(e_mirrorReverse)

        print(self)

        e_textPieceArray = root_element.getElementsByTagName("textPieceArray")
        self.read_textPieceArray(e_textPieceArray)


    def parse_xml(self):
        dom_tree = xml.dom.minidom.parse(self.__xml_path)
        root_element = dom_tree.documentElement
        self.collect_all_infos(root_element)
        self.read_tag_values(root_element)
        for text in self.textPieceArray:
            print(text)






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
