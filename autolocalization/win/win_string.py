# encoding: utf-8
import re
import sys
import os
import random
import io
from xpinyin import Pinyin
from xml.etree import ElementTree as ET

reload(sys)
sys.setdefaultencoding('utf-8')
print_type = sys.getfilesystemencoding()

xml_path = 'D:/app/src/main/res/values/strings.xml'
main_path = 'D:/app/src/main'
app_context = 'X.appContext.'

crt_ss = []
names = {}
b = ''
root = None
updateTree = None


# 查询某个文件中的中文
def start_find_chinese(file_path, skipxml):
    suffix = os.path.splitext(file_path)[1]
    if cmp(suffix, '.java') != 0 and cmp(suffix, '.xml') != 0:
        return
    r = []
    with open(file_path, 'rb') as infile:
        for line in infile.readlines():
            content = line.strip().decode('utf-8', 'ignore')
            p2 = re.compile('.+?"(.+?)"')  # 取每行中双引号内的内容
            str_array = p2.findall(content)
            # 再取出引号中包含中文的字符串
            zh = []
            for s in str_array:
                if check_contain_chinese(s):
                    zh.append(s)
            for s in zh:
                if skipxml:
                    if s in crt_ss:
                        # 如果存在了就直接使用@string/xxx替换xml中的内容,使用R.string.xxx来替换java中内容
                        change_text(file_path, s)
                    else:
                        # 如果不存在则需要添加到string.xml中，并设置value的key
                        modifyxml(xml_path, s)
                        # 再使用@string/xxx替换xml中的内容,使用R.string.xxx来替换java中内容
                        change_text(file_path, s)
                        # 添加新的value到crt_ss中，以免xml中重复
                        crt_ss.append(s)
                else:
                    if len(str_array) != 0:
                        name = str_array[0]
                        names.update({s.decode('utf-8'): name})
                r.append(s)
    return r


# 判断字符串中是否有中文
def check_contain_chinese(check_str):
    for ch in check_str.decode('utf-8'):
        if u'\u4e00' <= ch <= u'\u9fa5':
            return True
    return False


# 替换内容
def change_text(file_path, name):
    suffix = os.path.splitext(file_path)[1]
    xml_name = names[name.decode('utf-8')]
    change_content = ''
    if cmp(suffix, '.java') == 0:
        if 'Fragment' in file_path or 'Activity' in file_path:
            change_content = 'getString(R.string.'
        else:
            change_content = app_context + 'getString(R.string.'
        string_switch(file_path, '"' + name + '"', change_content + xml_name + ")")
    elif cmp(suffix, '.xml') == 0:
        string_switch(file_path, name, "@string/" + xml_name)
    print 'change success!'


# 定义一个函数，带有4个参数
# x 表示要更新的文件名称
# y 表示要被替换的内容
# z 表示 替换后的内容
# s 默认参数为 1 表示只替换第一个匹配到的字符串
# 如果参数为 s = 'g' 则表示全文替换
def string_switch(x, y, z, s=1):
    with io.open(x, "r", encoding="utf-8") as f:
        # readlines以列表的形式将文件读出
        lines = f.readlines()
    with io.open(x, "w", encoding="utf-8") as f_w:
        # 定义一个数字，用来记录在读取文件时在列表中的位置
        n = 0
        # 默认选项，只替换第一次匹配到的行中的字符串
        if s == 1:
            for line in lines:
                if y in line:
                    line = line.replace(y, z)
                    f_w.write(line)
                    n += 1
                    break
                f_w.write(line)
                n += 1
            # 将剩余的文本内容继续输出
            for i in range(n, len(lines)):
                f_w.write(lines[i])
        # 全局匹配替换
        elif s == 'g':
            for line in lines:
                if y in line:
                    line = line.replace(y, z)
                f_w.write(line)


# 遍历文件夹内的所有文件，并输出其中的中文
def find_file_chinese(path):
    result = []
    files = os.listdir(path)
    for file in files:
        if not file.startswith("."):
            file_path = path + "/" + file
            if not os.path.isdir(file_path):
                if cmp(file_path, xml_path) != 0:
                    sub_file = start_find_chinese(file_path, True)
                    if sub_file:
                        result.append(sub_file)
            else:
                child = find_file_chinese(file_path)
                if child:
                    result.append(child)
    return result


# 修改xml文件
def modifyxml(path, text):
    try:
        global b
        global root
        global updateTree
        if root is None:
            # 读取待修改文件
            updateTree = ET.parse(path)
            root = updateTree.getroot()
        # 创建新节点并添加为root的子节点
        newEle = ET.Element("string")
        name = ''
        if b == '':
            print '是否自动生成name n/y?'.decode('utf-8').encode(print_type)
            b = raw_input()[0:1]
        if b == 'y':
            # 自动生成名字
            name = createRandomString(text, 3)
        else:
            # 手动输入名字
            print text.decode('utf-8') + ": 输入名称".decode('utf-8')
            # input(提示字符串)，函数阻塞程序，并提醒用户输入字符串
            name = raw_input()
        newEle.attrib = {"name": name}
        newEle.text = text.decode('utf-8')
        root.append(newEle)
        # 更新名字得字典
        names.update({text.decode('utf-8'): name})
        # 写回原文件
        updateTree.write(path, 'utf-8')
    except IndentationError as identifier:
        print identifier


# 随机字符串
def createRandomString(str, lens):
    raw = ""
    range1 = range(58, 97)
    i = 0
    while i < lens:
        seed = random.randint(48, 122)
        if seed in range1:
            continue
        if raw == "" and seed < 97:
            continue
        raw += chr(seed)
        i += 1
    if len(str) > 4:
        str = str[0:3]
    raw = chinese2py(str).replace("：",'').replace(':', '').replace('，', '').replace('【', '').replace('/', '').replace('／', '').strip() + "_" + raw
    return raw


# 汉字转拼音
def chinese2py(str):
    p = Pinyin()
    return p.get_pinyin(str, '')


# find_file_chinese的中文是否在string.xml中存在
def handle_text():
    # xml现有得字符串
    global crt_ss
    crt_ss = start_find_chinese(xml_path, False)
    find_file_chinese(main_path)


# start to find
if __name__ == '__main__':
    handle_text()
