import hashlib
import sys
from bitcoin.rpc import RawProxy


def swapHex(data):
    newHex = ""
    for i in range(0, len(data)/2):
        byte = data[2*i] + data[2*i+1]
        newHex = byte + newHex
    return newHex


def main():
    p = RawProxy()

    blockheight = int(sys.argv[1])

    blockhash = p.getblockhash(blockheight)

    block = p.getblock(blockhash)

    header_hex = (swapHex(block["versionHex"]) +
                  swapHex(block["previousblockhash"]) +
                  swapHex(block["merkleroot"]) +
                  swapHex('{:08x}'.format(block["time"])) +
                  swapHex(block["bits"]) +
                  swapHex('{:08x}'.format(block["nonce"])))

    header_bin = header_hex.decode('hex')

    hash = hashlib.sha256(hashlib.sha256(header_bin).digest()).digest()

    print hash[::-1].encode('hex_codec')
    print block["hash"]


if __name__ == '__main__':
    main()
