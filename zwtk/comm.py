import time
import sys, os

def print_duration(method):
    """Prints out the runtime duration of a method in seconds

    .. code-block:: python
        :linenos:

        @print_duration
        def test_func():
            pass

        test_func()

    """
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        print('%s cost %2.2f second(s)' % (method.__name__, te - ts))
        return result
    return timed

def waitkey():
    """ Wait for a key press on the console and return it. """
    result = None
    if os.name == 'nt':
        import msvcrt
        result = msvcrt.getch()
    else:
        import termios
        fd = sys.stdin.fileno()
        oldterm = termios.tcgetattr(fd)
        newattr = termios.tcgetattr(fd)
        newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
        termios.tcsetattr(fd, termios.TCSANOW, newattr)
        try:
            result = sys.stdin.read(1)
        except IOError:
            pass
        finally:
            termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
    return result

def parse_args_to_dict(start_idx=1):
    """将命令行中 key=value 格式的参数解析为字典"""
    args_dict = {}
    # 从第start_idx个参数开始遍历
    for arg in sys.argv[start_idx:]:
        if '=' in arg:
            key, value = arg.split('=', 1)  # 只分割第一个等号
            # 尝试将值转换为合适类型
            try:
                # 处理布尔值
                if value.lower() == 'true':
                    args_dict[key] = True
                elif value.lower() == 'false':
                    args_dict[key] = False
                # 处理整数
                elif value.isdigit():
                    args_dict[key] = int(value)
                # 处理浮点数
                elif value.replace('.', '', 1).isdigit():
                    args_dict[key] = float(value)
                else:
                    args_dict[key] = value  # 保持字符串
            except:
                args_dict[key] = value  # 转换失败时保持原始字符串
        else:
            # 处理没有等号的标志参数（视为布尔值True）
            args_dict[arg] = True
    return args_dict