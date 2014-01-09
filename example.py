__author__ = '0xh3v3r1337'
from vircurex import *

#Your vircurex username
user = "user"
#A dictionary of secret keywords
secrets = {"get_balance": "", "create_order": "", "release_order": "", "delete_order": "", "read_order": "",
           "read_orders": "", "read_orderexecutions": "", "create_coupon": "", "redeem_coupon": ""}
test = Vircurex(user, secrets)
print(test.get_lowest_ask("BTC", "LTC"))