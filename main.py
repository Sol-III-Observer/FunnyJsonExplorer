import sys
import explorer
import json

def help(): # 帮助信息
    print('')
    print('')
    print('  -h : Display this help message')

def load_icon(name):
    with open("icon-family.json", 'r', encoding='utf-8') as f:
        icons = json.load(f)
        if name in icons:
            return icons[name]
        else:
            return None

if __name__ == '__main__':
    if len(sys.argv) == 1 or '-h' in sys.argv:
        help() # 展示帮助信息
        sys.exit(0)
    i = 1
    file = ""
    style = ""
    icon_name = ""
    while i < len(sys.argv):
        # 读取参数
        if sys.argv[i] == '-f':
            file = sys.argv[i + 1]
            i += 1
        elif sys.argv[i] == '-s':
            style = sys.argv[i + 1]
            i += 1
        elif sys.argv[i] == '-i':
            icon_name = sys.argv[i + 1]
            i += 1
        i += 1
    if file == "":
        print('Please specify the file path')
        sys.exit(0)
    if style == "":
        print('Please specify the style')
        sys.exit(0)
    if icon_name == "":
        print('Please specify the icon family')
        sys.exit(0)

    icon = load_icon(icon_name)
    if icon is None:
        print('Icon family not found')
        sys.exit(0)
    if style not in ['tree', 'rectangle']:
        print('Style not found')
        sys.exit(0)
    
    explorer = explorer.Explorer()
    explorer.load(file)
    explorer.print(style, icon)