from xml.dom.minidom import parse
import xml.dom.minidom
import os
import shutil
import PlistConst
import PlistIO

## 寻找老素材的地址
# dir_old = "/Users/sodino/NativeProjects/textconfiguration/old/"
dir_old = "/Users/sodino/IdeaProjects/xml2plist/test/"
## 转换为plist后的存储路径，要以 / 结尾
dir_plist = "/Users/sodino/IdeaProjects/xml2plist/new_plist/"

XML_NAME = "TextBubbleInfo.xml"

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
    
    def __init__(self, content):
        ## xml中 <frameRect>的值 : >{{305,25},{105,575}}
        self.content = content
        tmp = content.replace("{", "").replace("}", "")
        values = tmp.split(',')
        self.x = values[0]
        self.y = values[1]
        self.width = values[2]
        self.height = values[3]

    def __str__(self):
        return "[x,y=%s,%s, w,h=%s,%s]" %(self.x, self.y, self.width, self.height)

    def plist_content(self):
        value = PlistConst.key_string("Rectangle", 
                                "%s,%s,%s,%s" 
                                %(self.x, self.y, self.width, self.height)
                            )
        return value

class XmlTextPiece:
    def __init__(self):
        self.type            = ""
        self.text            = ""
        self.format          = ""
        self.language        = ""
        self.caseString      = ""
        self.editable        = ""
        self.color           = ""

        self.isBold          = ""
        self.isItalic        = ""
        self.autoLineBreak   = ""

        self.isVerticalText  = ""
        self.align           = ""
        self.verticalAlign   = ""
        self.font            = ""

        self.showShadow      = ""
        self.shadowColor     = ""
        ## <shadowOffset>{1.000000,1.000000}</shadowOffset>
        self.shadowOffset    = ""
        self.frameRect       = ""
        self.maxTextHeight   = ""

    def __str__(self):
        value = "type=%s text='%s' format='%s' color='%s' frameRect:%s"\
                % (self.type, self.text, self.format, self.color, self.frameRect)

        return value

    def text_color_orgba(self):
        if len(self.color) == 0:
            ## color无值的情况，只有三个素材  10130375 10110488 10110434，都被‘禁用’了
            return ""
        elif len(self.color) != 9:
            ## 不符合格式
            return ""
        
        ## 将 #11AA33FF转为 ORGBA格式 :  100, 17, 170, 51, 255 (10进制)
        r = self.color[1:3]
        g = self.color[3:5]
        b = self.color[5:7]
        a = self.color[7:9]
        int_r = int(r, base=16)
        int_g = int(g, base=16)
        int_b = int(b, base=16)
        int_a = int(a, base=16)
        ## 100 为默认值
        value = "100, %d, %d, %d, %d" %(int_r, int_g, int_b, int_a)
        ## print("test --> %s to %s" %(self.color, value))
        return value

    def text_input_flag(self):
        if len(self.format) == 0:
            return ""
        return ""

    def text_horizontal_and_justify(self):
        XML_LEFT = '0'
        XML_CENTER = '1'
        XML_RIGHT = '2'

        ALIGN_LEFT = 0x01
        ALIGN_HCENTER = 0x02
        ALIGN_RIGHT = 0x04
        ALIGN_TOP = 0x10
        ALIGN_VCENTER = 0x20
        ALIGN_BOTTOM = 0x40

        
        justify = ALIGN_VCENTER | ALIGN_HCENTER
        
        horizontal = 1 ## 1 : 文字为水平排列； 0 : 文字竖排，即‘对联’的竖排
        if self.isVerticalText.lower() == 'true':
            horizontal = 0
            align = ALIGN_VCENTER
            if self.verticalAlign == XML_LEFT:
                align = ALIGN_TOP
            elif self.verticalAlign == XML_RIGHT:
                align = ALIGN_BOTTOM
            else:
                align = ALIGN_VCENTER
            justify = ALIGN_HCENTER | align
        else:
            align = ALIGN_HCENTER
            if self.align == XML_LEFT:
                align = ALIGN_LEFT
            elif self.align == XML_RIGHT:
                align = ALIGN_RIGHT
            else:
                align = ALIGN_HCENTER
            justify = ALIGN_VCENTER | align

        line  = PlistConst.key_integer("Horizontal", horizontal)
        line += PlistConst.key_integer("Justify", justify)
        return line


    def generate_plist_line(self):
        ## RenderMode
        line = ""
        line += PlistConst.key_integer("RenderMode", "0")
        line += PlistConst.key_string("TextString", self.text)
        line += PlistConst.key_string("FontLibrary", self.font)
        line += PlistConst.key_string("Size", self.maxTextHeight)
        line += PlistConst.key_string("ORGBA", self.text_color_orgba())

        line += self.frameRect.plist_content()
        line += self.text_horizontal_and_justify()

        bold = "0"
        if self.isBold.lower() == 'true':
            bold = "1"
        line += PlistConst.key_string("Bold", bold)
        
        italic = "0"
        if self.isItalic.lower() == "true":
            italic = "1"
        line += PlistConst.key_string("Italic", italic)

        wrap = 1 ## 是否自动换行
        if self.autoLineBreak.lower() == "false":
            wrap = 0
        line += PlistConst.key_integer("Wrap", wrap)

        editable = 1 ## 默认可编辑
        input_flag = PlistConst.plist_input_flag(self.format, self.caseString, self.language)
        if len(input_flag) > 0:
            line += PlistConst.key_string("InputFlag", input_flag)
            editable = 0 ## 有format就不可编辑

        ## 下划线：默认值，原xml中无此定义
        line += PlistConst.key_integer("Underline", 0)
        ## 删除线：默认值，原xml中无此定义
        line += PlistConst.key_integer("StrikeThrough", 0)
        ## 字间距：默认值，原xml中无此定义
        line += PlistConst.key_integer("Spacing", 0)
        ## 行间距：默认值，原xml中无此定义
        line += PlistConst.key_integer("LineSpacing", 0)
        ## 文字从左至右：默认值，原xml中无此定义
        line += PlistConst.key_integer("LeftToRight", 1)
        ## 是否自动缩放：默认值，原xml中无此定义
        line += PlistConst.key_integer("Shrink", 1)

        line += PlistConst.const_plist_LayerStyleConfigs.format(editable = editable)

        result = PlistConst.key_dict(dict = line)
        print("test --> line : %s" %result)

        return result


class TextXML:
    def __init__(self, xml_path):
        ## 当前xml的绝对路径
        self._xml_path          = xml_path
        self.textPieceArray     = []
        self.resId              = ""

        self.width              = ""
        self.height             = ""

        self.backgroundImagePath= ""
        self.mirrorReverse      = ""

    def __str__(self):
        return "resId(%s) [w, h]=[%s, %s] bg=%s" %(self.resId, self.width, self.height, self.backgroundImagePath)

    def fonts(self):
        values = ""
        dict = {}
        for piece in self.textPieceArray:
            font = piece.font
            if font in dict:
                continue
            suffix = ""
            if len(dict) > 0:
                suffix = ","
            values = values + suffix + font
            dict[piece.font] = ""

        return values

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
            elif 'maxTextHeight' == node.tagName:
                xPiece.maxTextHeight = xml_node_value(node)
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

        e_textPieceArray = root_element.getElementsByTagName("textPieceArray")
        self.read_textPieceArray(e_textPieceArray)


    def read_xml(self):
        dom_tree = xml.dom.minidom.parse(self._xml_path)
        root_element = dom_tree.documentElement
        self.collect_all_infos(root_element)
        self.read_tag_values(root_element)


class TextPlist:
    def __init__(self, xml):
        self.xml = xml

    def generate_plist_lines(self):
        lines = ""
        xml_text_piece_array = self.xml.textPieceArray
        for piece in xml_text_piece_array:
            lines += piece.generate_plist_line()

        new_content = PlistConst.key_array("Lines", lines)
        return new_content

    def generate_plist_content(self):
        plist_lines = self.generate_plist_lines()

        template = PlistConst.const_ar_common_text_v2
        new_content = template.format(width = self.xml.width,
                                    height = self.xml.height,
                                    bg_file_name = self.xml.backgroundImagePath,
                                    xml_text_piece_array_2_plist_lines = plist_lines)
        return new_content

    

# 一个文字素材包解压后的目录结构
# AUGUST 
#     |-- configuration.plist
#     |-- ar
#         |-- configuration.plist
#         |-- res
#             |-- bg.plist
#             |-- bg.png                  ## 缩略图，对文字需求来说可以省略
#             |-- arp
#                 |-- bg.png

class Converter:
    
    ## 清除存储目录
    def clear_target_directory(self):
        if os.path.exists(dir_plist):
            shutil.rmtree(dir_plist)
            os.makedirs(dir_plist)
            print("clear and recreate target directory : %s" % dir_plist)
        else:
            os.makedirs(dir_plist)
            print("create a new target directory : %s" % dir_plist)

    
    def create_target_directory(self, xml_path):
        suffix = xml_path.replace(dir_old, "").replace(XML_NAME, "")
        new_dir_path = dir_plist + suffix
        # 创建新文件夹的目录 
        os.makedirs(new_dir_path)
        print("new_dir_path : " + new_dir_path)
        return new_dir_path

    ## 创建素材包根目录下第一个 configuration.plist 
    def create_root_plist(self, dir, text_xml):
        template = PlistConst.const_root_plist
        new_content = template.format(width = text_xml.width, 
                                        height = text_xml.height,
                                        fonts = text_xml.fonts())
        file_plist_path = os.path.join(dir, PlistConst.configuration_plist)
        PlistIO.write(file_plist_path, new_content)
        
    def create_bg_plist(self, dir, text_xml):
        template = PlistConst.const_bg_plist
        new_content = template.format(bg_file_name = text_xml.backgroundImagePath)
        file_plist_path = os.path.join(dir, PlistConst.bg_plist)
        PlistIO.write(file_plist_path, new_content)

    def copy_bg_file(self, dir, text_xml):
        xml_dir = os.path.dirname(text_xml._xml_path)
        file_bg_path = os.path.join(xml_dir, text_xml.backgroundImagePath)
        if os.path.exists(file_bg_path) == False:
            print("Error!! Can't find bg file. res<%s> bg=%s" %(text_xml.resId, text_xml.backgroundImagePath))
        new_bg_path = os.path.join(dir, os.path.join(PlistConst.ar_res_arp, text_xml.backgroundImagePath))
        ## print("test --> new_bg_path %s" %new_bg_path)
        PlistIO.copy_file(file_bg_path, new_bg_path)

    def create_text_plist(self, dir, text_xml):
        file_plist_path = os.path.join(dir, os.path.join("ar", PlistConst.configuration_plist))
        text_plist = TextPlist(text_xml)
        new_content = text_plist.generate_plist_content()
        PlistIO.write(file_plist_path, new_content)


    def convert2plist(self, text_xml):
        target_dir_path = self.create_target_directory(text_xml._xml_path)
        self.create_root_plist(target_dir_path, text_xml)
        self.create_bg_plist(target_dir_path, text_xml)
        self.copy_bg_file(target_dir_path, text_xml)
        self.create_text_plist(target_dir_path, text_xml)
            


    def findAllFile(self, base_path):
        for root, ds, fs in os.walk(base_path):
            for f in fs:
                if f.endswith(XML_NAME):
                    fullname = os.path.join(root, f)
                    yield fullname

    def start(self):
        ##  当前目录路径
        # current_path = os.getcwd()
        # test_xml = TextXML()
        # test_xml.read2parse_xml(current_path + "/TextBubbleInfo.xml")
        for xml_path in self.findAllFile(dir_old) :
            text_xml = TextXML(xml_path)
            text_xml.read_xml()
            converter.convert2plist(text_xml)


if __name__ == '__main__':
    converter = Converter()
    ## 清空、重建一下存储目录
    converter.clear_target_directory()

    converter.start()
    

    print("xml all tagNames are : " + str(tags.keys()))
    print("xml all formats are : " + str(formats.keys()))
