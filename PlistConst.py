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