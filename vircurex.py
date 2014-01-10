import time
import json
import urllib.parse
import urllib.request
import hashlib
import random


class Vircurex:
    domain = "https://vircurex.com"

    @staticmethod
    def simple_request(command, **params):
        global domain

        url = "{}/api/{}.json?{}".format(Vircurex.domain, command, urllib.parse.urlencode(params))
        #blocks python scripts for some reason
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        data = urllib.request.urlopen(req).read().decode('utf-8')
        return json.loads(data)

    @staticmethod
    def secure_request(user, secret, command, tokenparams, **params):
        global domain
        t = time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime())
        txid = "{}-{}".format(t, random.randint(0, 1 << 31))
        txid_bytes = txid.encode('utf-8')
        txid = hashlib.sha256(txid_bytes).hexdigest()
        #token computation
        #vp = [command] + map(lambda x:params[x],tokenparams)
        vp = [command] + [params[x] for x in tokenparams]
        token_input = "{};{};{};{};{}".format(secret, user, t, txid, ';'.join(map(str, vp)))
        token_input_bytes = token_input.encode('utf-8')
        token = hashlib.sha256(token_input_bytes).hexdigest()
        #cbuilding request
        reqp = {"account": user, "id": txid, "token": token, "timestamp": t}
        reqp.update(params)
        url = "{}/api/{}.json?{}".format(Vircurex.domain, command, urllib.parse.urlencode(reqp))
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        data = urllib.request.urlopen(req).read().decode('utf-8')
        return json.loads(data)

    def __init__(self, user=None, secrets={}):
        self.user = user
        self.secrets = secrets

        #trade API

    def get_balance(self, currency):
        return Vircurex.secure_request(self.user, self.secrets["get_balance"], "get_balance", ["currency"],
                                       currency=currency)

    def get_balances(self):
        return Vircurex.secure_request(self.user, self.secrets["get_balance"], "get_balances", [])

    def create_order(self, ordertype, amount, currency1, unitprice, currency2):
        return Vircurex.secure_request(self.user, self.secrets["create_order"], "create_order",
                                       ["ordertype", "amount", "currency1", "unitprice", "currency2"],
                                       ordertype=ordertype, amount=amount, currency1=currency1, unitprice=unitprice,
                                       currency2=currency2)

    def release_order(self, orderid):
        return Vircurex.secure_request(self.user, self.secrets["release_order"], "release_order", ["orderid"],
                                       orderid=orderid)

    def delete_order(self, orderid, otype):
        return Vircurex.secure_request(self.user, self.secrets["delete_order"], "delete_order", ["orderid", "otype"],
                                       orderid=orderid, otype=otype)

    def read_order(self, orderid, otype):
        return Vircurex.secure_request(self.user, self.secrets["read_order"], "read_order", ["orderid"],
                                       orderid=orderid,
                                       otype=otype)

    def read_orders(self, otype):
        return Vircurex.secure_request(self.user, self.secrets["read_orders"], "read_orders", [], otype=otype)

    def read_orderexecutions(self, orderid):
        return Vircurex.secure_request(self.user, self.secrets["read_orderexecutions"], "read_orderexecutions",
                                       ["orderid"], orderid=orderid)

    def create_coupon(self, amount, currency):
        return Vircurex.secure_request(self.user, self.secrets["create_coupon"], "create_coupon",
                                       ["amount", "currency"],
                                       amount=amount, currency=currency)

    def redeem_coupon(self, coupon):
        return Vircurex.secure_request(self.user, self.secrets["redeem_coupon"], "redeem_coupon", ["coupon"],
                                       coupon=coupon)

        ##info API

    def get_lowest_ask(self, base, alt):
        return Vircurex.simple_request("get_lowest_ask", base=base, alt=alt)

    def get_highest_bid(self, base, alt):
        return Vircurex.simple_request("get_highest_bid", base=base, alt=alt)

    def get_last_trade(self, base, alt):
        return Vircurex.simple_request("get_last_trade", base=base, alt=alt)

    def get_volume(self, base, alt):
        return Vircurex.simple_request("get_volume", base=base, alt=alt)

    def get_info_for_currency(self):
        return Vircurex.simple_request("get_info_for_currency")

    def get_info_for_1_currency(self, base, alt):
        return Vircurex.simple_request("get_info_for_1_currency", base=base, alt=alt)

    def orderbook(self, base, alt):
        return Vircurex.simple_request("orderbook", base=base, alt=alt)

    def orderbook_alt(self, alt):
        return Vircurex.simple_request("orderbook_alt", alt=alt)

    def trades(self, base, alt, since):
        return Vircurex.simple_request("trades", base=base, alt=alt, since=since)

    def get_currency_info(self):
        return Vircurex.simple_request("get_currency_info")