from buffer import Buffer
from minibuf import MiniBuffer


def main():
    buff = Buffer()
    buff.grow(8 * 4) # Size
    buff.write_f64_be_next([69.0, -21.0, -42.42, 3.621])
    print(buff.bytes())
    buff.seek_byte(0x00, False)
    print(buff.read_f64_be_next(4))