import re
from datetime import datetime
from difflib import SequenceMatcher

def is_chinese(c):
    '''https://stackoverflow.com/questions/1366068/whats-the-complete-range-for-chinese-characters-in-unicode'''
    if u'\u4E00' <= c < u'\u9FFF' or \
       u'\u3400' <= c < u'\u4DBF' or \
       u'\u20000' <= c < u'\u2A6DF' or \
       u'\u2A700' <= c < u'\u2B73F' or \
       u'\u2B740' <= c < u'\u2B81F' or \
       u'\u2B820' <= c < u'\u2CEAF':
        return True
    else:
        return False

# def is_chinese_punctuation(c):
#     arr = [
#         u'\u3002',u'\uFF1F',u'\uFF01',u'\u3010',u'\u3011',u'\uFF0C',u'\u3001',u'\uFF1B',
#         u'\uFF1A',u'\u300C',u'\u300D',u'\u300E',u'\u300F',u'\u2019',u'\u201C',u'\u201D',
#         u'\u2018',u'\uFF08',u'\uFF09',u'\u3014',u'\u3015',u'\u2026',u'\u2013',u'\uFF0E',
#         u'\u2014',u'\u300A',u'\u300B',u'\u3008',u'\u3009'
#     ]
#     return c in arr

# def is_english_punctuation(c):
#     arr = [
#         '!', '"', '#', '$', '%', '&',
#         "'", '(', ')', '*', '+', ',', '-', 
#         '.', '/', ':', ';', '<', '=', '>', 
#         '?', '@', '[', '\\', ']', '\^', '_', 
#         '`', '{', '|', '}', '~'
#     ]
#     return c in arr

def is_chinese_char(char):
    """
    判断一个字符是否是中文字符
    """
    # 中文字符的 Unicode 范围
    ranges = [
        (0x4E00, 0x9FFF),  # 基本汉字
        (0x3400, 0x4DBF),  # 扩展 A
        (0x20000, 0x2A6DF),  # 扩展 B
        (0x2A700, 0x2B73F),  # 扩展 C
        (0x2B740, 0x2B81F),  # 扩展 D
        (0x2B820, 0x2CEAF),  # 扩展 E
        (0xF900, 0xFAFF),    # 兼容汉字
        (0x2F800, 0x2FA1F),  # 兼容扩展
    ]

    # 将字符转换为 Unicode 编码
    code = ord(char)

    # 检查字符是否在任何一个范围内
    for start, end in ranges:
        if start <= code <= end:
            return True
    return False

def is_chinese_punctuation(char):
    """
    判断一个字符是否是中文标点符号
    """
    # 中文标点符号的 Unicode 范围 https://symbl.cc/cn/unicode-table/#cjk-symbols-and-punctuation
    ranges = [
        (0x3000, 0x3003),
        (0x3008, 0x3011),
        (0x3013, 0x301F),
        # 全角标点
        (0xFF00, 0xFF0F),
        (0xFF1A, 0xFF20),
        (0xFF3B, 0xFF40),
        (0xFF5B, 0xFF64),
    ]

    # 将字符转换为 Unicode 编码
    code = ord(char)

    # 检查字符是否在任何一个范围内
    for start, end in ranges:
        if start <= code <= end:
            return True
    return False

def is_english_punctuation(char):
    """
    判断一个字符是否是英文标点符号
    """
    # 英文标点符号的 Unicode 范围
    ranges = [
        (0x0020, 0x002F),  # 空格和基本标点
        (0x003A, 0x0040),  # :;<=>?@
        (0x005B, 0x0060),  # [\]^_`
        (0x007B, 0x007E),  # {|}~
    ]

    # 将字符转换为 Unicode 编码
    code = ord(char)

    # 检查字符是否在任何一个范围内
    for start, end in ranges:
        if start <= code <= end:
            return True
    return False

def is_digit(char):
    """
    判断一个字符是否是数字
    """
    ranges = [
        (0x0030, 0x0039),  # 拉丁数字（ASCII 0-9）
        (0xFF10, 0xFF19),  # 全角数字（全角 0-9）
    ]

    # 将字符转换为 Unicode 编码
    code = ord(char)

    # 检查字符是否在任何一个范围内
    for start, end in ranges:
        if start <= code <= end:
            return True
    return False

def hasdigit(s):
    m = re.compile(r'\d')
    return bool(m.search(s))

def rmexblank(txt):
    '''
    删除多余空格, 英文保留一个空格, 中文则不保留空格
    '''
    s = txt.strip()
    rtn = []
    for i,c in enumerate(s):
        if c.isspace():
            prev_char = rtn[-1] if len(rtn)>0 else ''
            next_char = s[i+1]
            if any([next_char.isspace(), is_chinese(next_char), is_chinese_punctuation(next_char)]):
                # 当前是空格，若后接空格或中文则不留
                continue
            elif not is_chinese(next_char) and any([is_chinese(prev_char), is_chinese_punctuation(prev_char)]):
                # 当前是空格，若前接非中文且后接中文则不留
                continue
            else:
                rtn.append(c)
        else:
            rtn.append(c)
    return ''.join(rtn)

def inner_trim(value, replace=''):
    if isinstance(value, str):
        TABSSPACE = re.compile(r'[\s\t]+')
        # remove tab and white space
        value = re.sub(TABSSPACE, replace, value)
        value = ''.join(value.splitlines())
        return value.strip()
    return ''

class ReplaceSequence(object):
    def __init__(self):
        self.actions = []

    def append(self, pattern, replace_with=None):
        self.actions.append( (pattern, replace_with or '') )
        return self

    def replace(self, string):
        if not string:
            return ''
        mutatedString = string
        for pattern, replace_with in self.actions:
            mutatedString = mutatedString.replace(pattern, replace_with)
        return mutatedString

def find_datestr(s):
    arr = []
    rtn = []
    
    _arr = re.findall(r'(?:\D)([12]\d{3}-\d{1,2}-\d{1,2})(?:\D)*', s)
    _arr = ['%s-%s-%s'%(a.split('-')[0], a.split('-')[1].rjust(2,'0'), a.split('-')[2].rjust(2,'0')) for a in _arr]
    arr.extend(_arr)

    _arr = re.findall(r'(?:\D)([12]\d{3}/\d{1,2}/\d{1,2})(?:\D)*', s)
    _arr = ['%s-%s-%s'%(a.split('/')[0], a.split('/')[1].rjust(2,'0'), a.split('/')[2].rjust(2,'0')) for a in _arr]
    arr.extend(_arr)

    _arr = re.findall(r'(?:\D)([12]\d{3}\d{2}\d{2})(?:\D)*', s)
    _arr = ['%s-%s-%s'%(a[:4], a[4:6], a[6:]) for a in _arr]
    arr.extend(_arr)
    for i,a in enumerate(arr):
        try:
            datetime.strptime(a, '%Y-%m-%d')
            rtn.append(a)
        except Exception:
            arr[i] = None
    arr = [o for o in arr if o]
            
    #TODO update re, get rid of this if
    if len(arr) == 0:
        _arr = re.findall(r'(?:\D)([12]\d{3}-\d{1,2})(?:\D)*', s)
        _arr = ['%s-%s'%(a.split('-')[0], a.split('-')[1].rjust(2,'0')) for a in _arr]
        arr.extend(_arr)

        _arr = re.findall(r'(?:\D)([12]\d{3}/\d{1,2})(?:\D)*', s)
        _arr = ['%s-%s'%(a.split('/')[0], a.split('/')[1].rjust(2,'0')) for a in _arr]
        arr.extend(_arr)
        
        _arr = re.findall(r'(?:\D)([12]\d{3}\d{2})(?:\D)*', s)
        _arr = ['%s-%s'%(a[:4], a[4:6]) for a in _arr]
        arr.extend(_arr)
        for a in arr:
            try:
                datetime.strptime(a, '%Y-%m')
                rtn.append(a)
            except Exception:
                pass
    for i,r in enumerate(rtn):
        year = int(r.split('-')[0])
        if year < 1949:
            rtn[i] = None
    rtn = [r for r in rtn if r]
    return rtn

def similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()

def unicode_represent(s):
    u = ''
    for c in s:
        u += r'\u{}'.format(ord(c))
    return u
