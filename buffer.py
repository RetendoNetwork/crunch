import struct


class Buffer:
    def __init__(self, *slices):
        self.buf = bytearray()
        self.off = 0
        self.boff = 0

        if len(slices) == 1:
            self.buf = bytearray(slices[0])
        elif len(slices) > 1:
            for s in slices:
                self.buf.extend(s)

        self.refresh()

    def read_bit(self, off):
        if off > (self.bcap - 1):
            raise Exception("BufferOverreadError")
        if off < 0:
            raise Exception("BufferUnderreadError")

        return (self.buf[off // 8] >> (7 - (off % 8))) & 1

    def read_bit_next(self):
        out = self.read_bit(self.boff)
        self.seek_bit(1, True)
        return out

    def read_bits(self, off, n):
        out = 0
        for i in range(n):
            out = (out << 1) | self.read_bit(off + i)
        return out

    def read_bits_next(self, n):
        out = self.read_bits(self.boff, n)
        self.seek_bit(n, True)
        return out

    def set_bit(self, off):
        if off > (self.bcap - 1):
            raise Exception("BufferOverwriteError")
        if off < 0:
            raise Exception("BufferUnderwriteError")

        self.buf[off // 8] |= (1 << (7 - (off % 8)))

    def set_bit_next(self):
        self.set_bit(self.boff)
        self.seek_bit(1, True)

    def clear_bit(self, off):
        if off > (self.bcap - 1):
            raise Exception("BufferOverwriteError")
        if off < 0:
            raise Exception("BufferUnderwriteError")

        self.buf[off // 8] &= ~(1 << (7 - (off % 8)))

    def clear_bit_next(self):
        self.clear_bit(self.boff)
        self.seek_bit(1, True)

    def set_bits(self, off, data, n):
        for i in range(n):
            if (data >> (n - i - 1)) & 1 == 0:
                self.clear_bit(off + i)
            else:
                self.set_bit(off + i)

    def set_bits_next(self, data, n):
        self.set_bits(self.boff, data, n)
        self.seek_bit(n, True)

    def flip_bit(self, off):
        if off > (self.bcap - 1):
            raise Exception("BufferOverwriteError")
        if off < 0:
            raise Exception("BufferUnderwriteError")

        self.buf[off // 8] ^= (1 << (7 - (off % 8)))

    def flip_bit_next(self):
        self.flip_bit(self.boff)
        self.seek_bit(1, True)

    def clear_all_bits(self):
        for i in range(len(self.buf)):
            self.buf[i] = 0

    def set_all_bits(self):
        for i in range(len(self.buf)):
            self.buf[i] = 0xFF

    def flip_all_bits(self):
        for i in range(len(self.buf)):
            self.buf[i] ^= 0xFF

    def seek_bit(self, off, relative):
        if relative:
            self.boff += off
        else:
            self.boff = off

    def after_bit(self, *off):
        if len(off) == 0:
            return self.bcap - self.boff - 1
        return self.bcap - off[0] - 1

    def align_bit(self):
        self.boff = self.off * 8

    def write_bytes(self, off, data):
        if (off + len(data)) > self.cap:
            raise Exception("BufferOverwriteError")
        if off < 0:
            raise Exception("BufferUnderwriteError")

        self.buf[off:off + len(data)] = data

    def write_bytes_next(self, data):
        self.write_bytes(self.off, data)
        self.seek_byte(len(data), True)

    def write_byte(self, off, data):
        self.write_bytes(off, [data])

    def write_byte_next(self, data):
        self.write_bytes(self.off, [data])
        self.seek_byte(1, True)

    def read_bytes(self, off, n):
        if (off + n) > self.cap:
            raise Exception("BufferOverreadError")
        if off < 0:
            raise Exception("BufferUnderreadError")

        return self.buf[off:off + n]

    def read_bytes_next(self, n):
        out = self.read_bytes(self.off, n)
        self.seek_byte(n, True)
        return out

    def read_byte(self, off):
        return self.read_bytes(off, 1)[0]

    def read_byte_next(self):
        out = self.read_bytes(self.off, 1)[0]
        self.seek_byte(1, True)
        return out

    def seek_byte(self, off, relative):
        if relative:
            self.off += off
        else:
            self.off = off

    def after_byte(self, *off):
        if len(off) == 0:
            return self.cap - self.off - 1
        return self.cap - off[0] - 1

    def align_byte(self):
        self.off = self.boff // 8

    def truncate_left(self, n):
        if n < 0:
            raise Exception("BufferInvalidByteCountError")

        self.buf = self.buf[n:]
        self.refresh()

    def truncate_right(self, n):
        if n < 0:
            raise Exception("BufferInvalidByteCountError")

        self.buf = self.buf[:self.cap - n]
        self.refresh()

    def grow(self, n):
        if n < 0:
            raise Exception("BufferInvalidByteCountError")

        if n <= len(self.buf) - self.cap:
            self.buf = self.buf[:self.cap + n]
        else:
            self.buf.extend(bytearray(n))
        self.refresh()

    def refresh(self):
        self.cap = len(self.buf)
        self.bcap = self.cap * 8

    def reset(self):
        self.buf = bytearray()
        self.off = 0
        self.boff = 0
        self.cap = 0
        self.bcap = 0

    def bytes(self):
        return bytes(self.buf)

    def byte_capacity(self):
        return self.cap

    def bit_capacity(self):
        return self.bcap

    def byte_offset(self):
        return self.off

    def bit_offset(self):
        return self.boff