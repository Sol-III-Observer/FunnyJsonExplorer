import sys

def help(): # 帮助信息
    print('')
    print('')
    print('  -h : Display this help message')

if __name__ == '__main__':
    if len(sys.argv) == 1 or '-h' in sys.argv:
        help() # 展示帮助信息
        sys.exit(0)
    i = 1
    file = ""
    style = ""
    icon = ""
    while i < len(sys.argv):
        # 读取参数
        if sys.argv[i] == '-f':
            file = sys.argv[i + 1]
            i += 1
        elif sys.argv[i] == '-s':
            style = sys.argv[i + 1]
            i += 1
        elif sys.argv[i] == '-i':
            icon = sys.argv[i + 1]
            i += 1
        i += 1
    if file == "":
        print('Please specify the file path')
        sys.exit(0)
    if style == "":
        print('Please specify the style')
        sys.exit(0)
    if icon == "":
        print('Please specify the icon family')
        sys.exit(0)