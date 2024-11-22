from buffer import Buffer


def main():
    buff = Buffer()
    buff.grow(12)
    buff.write_bytes_next("hello world !")
    print(str(buff.bytes))