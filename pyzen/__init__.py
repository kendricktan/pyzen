# 2017-07-18
# Author: Kendrick Tan
# LICENSE: MIT


import binascii
import json

from jsonrpc_requests import Server, TransportError, ProtocolError


class PyZen:
    # Referenced from:
    # https://en.bitcoin.it/wiki/Original_Bitcoin_client/API_calls_list
    # https://github.com/zcash/zcash/blob/master/doc/payment-api.md

    def __init__(self,
                 host='127.0.0.1',
                 port=8231,
                 username='username',
                 password='password',):
        """
        Args:
            host: host specified in ~/.zen/zen.conf
            port: port specified in ~/.zen/zen.conf
            username: rpc username
            password: rpc password
        """
        self._rpc_server = Server(
            'http://{}:{}'.format(host, str(port)), auth=(username, password))

    def _rpc_call(self, method, *args):
        """
        Communicate with the zen daemon via rpc
        """
        resp = self._rpc_server.send_request(method, False, args)
        return resp

    def addnode(self, host, opt='add'):
        """
        Adds node to daemon

        Args:
            host: Node host
            opt: <add|remove|onetry>
        """
        if opt is not 'add' or opt is not 'remove' or opt is not 'onetry':
            raise ValueError('addnode <node> <add/remove/onetry>')
        return self._rpc_call(host, 'add')

    """ Block info """

    def getblock(self, bhash):
        """
        Returns information about the
        block with the given hash

        Args:
            bhash: block hash
        """
        return self._rpc_call('getblock', bhash)

    def getblockhash(self, index):
        """
        Returns hash of block in best-block-chain
        at <index>; index 0 is the genesis block

        Argrs:
            index: hash no.
        """
        return self._rpc_call('getblockhash', index)

    def getbestblockhash(self):
        """
        Gets the best (tip) block in the longest blockchain
        A.k.a gets the latest block
        """
        return self._rpc_call('getbestblockhash')

    def getbestnblock(self, n):
        """
        Gets the n best (tip) block
        A.k.a gets the N lastest block

        Args:
            n: number of blocks from tip to retrieve
        """
        lastblockhash = self.getbestblockhash()

        last = self.getblock(lastblockhash)
        blocks = [last]
        for i in range(n):
            if not 'previousblockhash' in last:
                break
            last = self.getblock(last['previousblockhash'])
            blocks.append(last)

        return blocks

    def getblockcount(self):
        return self._rpc_call('getblockcount')

    """ Network info  """

    def getinfo(self):
        return self._rpc_call('getinfo')

    def getpeerinfo(self):
        return self._rpc_call('getpeerinfo')

    def getdifficulty(self):
        return self._rpc_call('getdifficulty')

    def getmininginfo(self):
        return self._rpc_call('getmininginfo')

    def getconnectioncount(self):
        return self._rpc_call('getconnectioncount')

    """ Transactional info """

    def gettx(self, txid):
        """
        Returns the decoded transaction

        Args:
            txid: transaction id
        """
        try:
            raw = self._rpc_call('getrawtransaction', txid)
            return self._rpc_call('decoderawtransaction', raw)
        except (TransportError, ProtocolError) as e:
            return None

    def gettxs(self, txids):
        """
        Returns a list of decoded transactions

        Args:
            txids: A list of transaction ids
        """
        txs = []

        for i in txids:
            t = self.gettx(i)

            if t is None:
                continue

            txs.append(t)

        return txs

    """ Wallet information """
    """
        Anything beyond this section isn't necessary to make
        an explorer. Maybe an online wallet? I dunnoe lol
    """

    def getnewaddress(self):
        return self._rpc_call('getnewaddress')

    def getreceivedbyaccount(self, minconf=1):
        """
        Returns total amount received by addresses in
        account with at least <minconf> confirmations

        Args:
            minconf: minimum confirmations
        """
        return self._rpc_call('getreceivedbyaccount', '', minconf)

    def getbalance(self, minconf=1):
        """
        Args:
            minconf: Only include transactions confirmed at least this
                     many times
        """
        return self._rpc_call('getbalance', minconf)

    def getaddressesbyaccount(self, minconf=1):
        """
        Returns total amount in wallet with minconf confirmations

        Args:
            minconf: minimum confirmations
        """
        return self._rpc_call('getaddressesbyaccount', '', minconf)

    def getreceivedbyaddress(self, address, minconf=1):
        """
        Returns the amount received by <address> in transactions
        with at least <minconf> confirmations. Only for local wallet.

        Args:
            address: t address
            minconf: minimum confirmations
        """
        return self._rpc_call('getreceivedbyaddress', address, minconf)

    def z_getoperationresult(self):
        return self._rpc_call('z_getoperationresult')

    def z_getnewaddress(self):
        return self._rpc_call('z_getnewaddress')

    def z_listaddresses(self):
        return self._rpc_call('z_listaddresses')

    def z_listreceivedbyaddress(self, address):
        """
        List what transactions received by address
        Args:
            address: z address
        """
        return self._rpc_call('z_listreceivedbyaddress', address)
