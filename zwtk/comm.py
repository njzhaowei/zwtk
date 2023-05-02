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