
from bitcoin.rpc import RawProxy

import sys


def main():
    p = RawProxy()

    txid = sys.argv[1]

    raw_tx = p.getrawtransaction(txid)

    decoded_tx = p.decoderawtransaction(raw_tx)

    # calculate output value
    output_value = 0

    for tx in decoded_tx["vout"]:
        output_value += tx["value"]

    # calculate input value
    input_value = 0

    for tx in decoded_tx["vin"]:
        raw_input_tx = p.getrawtransaction(tx["txid"])
        decoded_input_tx = p.decoderawtransaction(raw_input_tx)
        n = tx["vout"]
        trans = {}
        for _trans in decoded_input_tx["vout"]:
            if _trans["n"] == n:
                trans = _trans
        input_value += trans["value"]

    print "Transaction fee: {}".format(input_value-output_value)


if __name__ == '__main__':
    main()
