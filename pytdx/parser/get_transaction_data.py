from pytdx.parser.base import BaseParser
from pytdx.helper import get_datetime, get_volume, get_price
from collections import OrderedDict
import struct

class GetTransactionData(BaseParser):

    def setParams(self, market, code, start, count):
        if type(code) is str:
            code = code.encode("utf-8")
        pkg = bytearray.fromhex(u'0c 17 08 01 01 01 0e 00 0e 00 c5 0f')
        pkg.extend(struct.pack("<H6sHH", market, code, start, count))
        self.send_pkg = pkg

    def parseResponse(self, body_buf):
        pos = 0
        num = int.from_bytes(body_buf[:2])
        pos += 2
        ticks = []
        for i in range(num):
            ### ?? get_time
            # \x80\x03 = 14:56

            pos+=2
            price, pos = get_price(body_buf, pos)
            vol, pos = get_price(body_buf, pos)
            num, pos = get_price(body_buf, pos)
            buyorsell, pos = get_price(body_buf, pos)
            _, pos = get_price(body_buf, pos)

            tick = OrderedDict(
                [
                    ("price", price),
                    ("vol", vol),
                    ("num", num),
                    ("buyorsell", buyorsell)
                ]
            )

            ticks.append(tick)

        return ticks


