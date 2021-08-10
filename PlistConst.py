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


const_key_string 	= '''<key>{key}</key><string>{string}</string>'''
const_key_integer = '''<key>{key}</key><integer>{integer}</integer>'''

const_key_array 	= '''<key>{key}</key><array>{array}</array>'''
const_key_dict	= '''<key>{key}</key><dict>{dict}</dict>'''

def key_string(key, string):
	return const_key_string.format(key = key, string = string)

def key_integer(key, integer):
	return const_key_integer.format(key = key, integer = integer)

def key_array(key, array):
	return const_key_array.format(key = key, array = array)

def key_dict(key, dict):
	return const_key_dict.format(key = key, dict = dict)