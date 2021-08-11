import os

## 
const_root_plist = '''
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist>
	<array>
		<dict>
			<key>AR</key>
			<string>ar</string>
			<key>BubbleSize</key>
			<string>{width},{height}</string>
			<key>TextFontKey</key>
			<string>{fonts}</string>
		</dict>
	</array>
</plist>
'''

configuration_plist = "configuration.plist"

## 素材包 ar/res/arp 路径
ar_res_arp = os.path.join("ar", os.path.join("res", "arp"))

## 素材包 ar/res/bg.plist 路径
bg_plist = os.path.join("ar", os.path.join("res", "bg.plist"))
## 素材包 ar/res/ 路径下的 bg.plist 内容
const_bg_plist = '''
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist>
	<dict>
		<key>Tag</key>
		<string></string>
		<key>LoopCount</key>
		<integer>0</integer>
		<key>Nodes</key>
		<array>
			<dict>
				<key>Type</key>
				<string>Image</string>
				<key>LoopCount</key>
				<integer>0</integer>
				<key>Path</key>
				<string>{bg_file_name}</string>
				<key>FPS</key>
				<string>24.00</string>
			</dict>
		</array>
	</dict>
</plist>
'''

const_ar_common_text_v2='''
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist>
	<array>
		<dict>
			<key>Name</key>
			<string></string>
			<key>FacePart</key>
			<array>
				<dict>
					<key>Type</key>
					<string>MVCommonTextV2</string>
					<key>DrawLayerBorder</key>
					<integer>0</integer>
					<key>TextEnum</key>
					<integer>0</integer>
					<key>TextCommonStruct</key>
					<dict>
						<key>BGAnimation</key>
						<string>bg.plist</string>
						<key>BGThumbnailImage</key>
						<string>{bg_file_name}</string>
						<key>FGVAnimation</key>
						<string></string>
						<key>DefaultSize</key>
						<string>{width}, {height}</string>
                        {xml_text_piece_array_2_plist_lines}
					</dict>
				</dict>
			</array>
		</dict>
	</array>
</plist>
'''

const_plist_LayerStyleConfigs = '''
<key>LayerStyleConfigs</key>
<array>
	<dict>
		<key>LayerTag</key>
		<string>text</string>
		<key>LayerStyle</key>
		<integer>3</integer>
		<key>TextLayerConfig</key>
		<dict>
			<key>Enable</key>
			<integer>1</integer>
			<key>Editable</key>
			<integer>{editable}</integer>
		</dict>
	</dict>
</array>
'''

areas_format = ['c1', 'c3', 'c1c3']

dic_xml_format_2_plist_key = {
	'c1' 		: ["PLACE_BASE_1", "PLACE_BASE_EN_1"],
	'c3' 		: ["PLACE_BASE_3", "PLACE_BASE_EN_3"],
	'c1c3' 		: ["PLACE_BASE_5", "PLACE_BASE_EN_5"],

	## 10星期英文简称/Thu首字母大写其余小写   :61:星期英文简称/MON，全大写
	'E' 		: ["TIME_BASE_10", "TIME_BASE_61"],
	## 10星期英文简称/Thu首字母大写其余小写   :61:星期英文简称/MON，全大写
	'EE' 		: ["TIME_BASE_10", "TIME_BASE_61"],
	## 10星期英文简称/Thu首字母大写其余小写   :61:星期英文简称/MON，全大写
	'EEE' 		: ["TIME_BASE_10", "TIME_BASE_61"],

	## 28:首字母大写   29: 全大写
	'EEEE' 		: ["TIME_BASE_28", "TIME_BASE_29"],

	## 月份，数字
	'MM' 		: ["TIME_BASE_2"],
	## 60:月份英文简称，首字母大写后续小写  11:月份英文简称、全大写;  
	'MMM' 		: ["TIME_BASE_60", "TIME_BASE_11"],
	## 30:月份的英文全称、首字母大写     31:全大写
	'MMMM'		: ["TIME_BASE_30", "TIME_BASE_31"],
	## 日期，2个数字
	'dd' 		: ["TIME_BASE_3"],
	'yyyy'		: ["TIME_BASE_1"],
	'yyyy/MM/dd': ["TIME_BASE_12"],
	'yyyy.MM.dd': ["TIME_BASE_13"],
	'yyyy MM dd': ["TIME_BASE_14"],
	'yyyy-MM-dd': ["TIME_BASE_36"],
	'yyyyMMdd' 	: ["TIME_BASE_54"],
	'dd.MM.yyyy': ["TIME_BASE_55"],
	'yyyy/MM' 	: ["TIME_BASE_56"],
	'MM/dd' 	: ["TIME_BASE_57"],
	'MM.dd' 	: ["TIME_BASE_58"],

	'HH:mm' 	: ["TIME_BASE_48"],
	'HH:mm a' 	: ["TIME_BASE_49"],
	'MM dd HH:mm' : ["TIME_BASE_59"],
}


const_key_string 	= '''<key>{key}</key><string>{string}</string>'''
const_key_integer = '''<key>{key}</key><integer>{integer}</integer>'''

const_key_array 	= '''<key>{key}</key><array>{array}</array>'''
const_key_dict		= '''<key>{key}</key><dict>{dict}</dict>'''
const_dict 			= '''<dict>{dict}</dict>'''

def key_string(key, string):
	return const_key_string.format(key = key, string = string)

def key_integer(key, integer):
	return const_key_integer.format(key = key, integer = integer)

def key_array(key, array):
	return const_key_array.format(key = key, array = array)

def key_dict(key, dict):
	return const_key_dict.format(key = key, dict = dict)

def key_dict(dict):
    return const_dict.format(dict = dict)

def plist_input_flag(xml_format, xml_caseString, xml_language):
	if len(xml_format) == 0:
		return ""
	values = dic_xml_format_2_plist_key[xml_format]
	if len(values) == 0:
		raise Exception("Invalid xml format('%s')" % xml_format)
	elif len(values) == 1:
		return values[0]

	## 剩下的都是 values 长度为2
	if xml_format in areas_format:
		if xml_language == 'en_US':
			return values[1]
		else:
			return values[0]
	
	if xml_caseString == '1': ## 全大写
		return values[1]
	else:
		return values[0]
			