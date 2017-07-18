import requests
import json


class PyZen:
    # Referenced from:
    # https://en.bitcoin.it/wiki/Original_Bitcoin_client/API_calls_list
    # https://github.com/zcash/zcash/blob/master/doc/payment-api.md

    def __init__(self,
                 url='http://127.0.0.1:8231',
                 username='username',
                 password='password',
                 timeout=600,
                 id_='pyzen'):
        """
        Args:
            url: url to connect to the zen daemon
                (testnet port: 18231)
            username: rpc username
            password: rpc password
            timeout: timeout before getting a response (in seconds)
            testnet: Use the test network or nah
        """

        self.url = url
        self.username = username.encode('utf-8')
        self.password = password.encode('utf-8')
        self.timeout = timeout
        self.id_ = id_

    def _rpc_call(self, method, *args):
        """
        Communicate with the zen daemon via rpc
        """

        # Convert json data to string to
        # communicate via rpc
        data = json.dumps({
            'jsonrpc': '1.0',
            'method': method,
            'params': args,
            'id': self.id_
        })

        r = requests.post(self.url, auth=(self.username, self.password),
                          data=data, timeout=self.timeout)

        resp = json.loads(r.text)

        if resp['error']:
            raise Exception(str(resp['error']))

        return resp['result']

    def addnode(self, url, opt='add'):
        """
        Adds node to daemon

        Example call using curl:

        curl --user myusername --data-binary
        \'{ "jsonrpc": "1.0", "id":"curltest", "method": "addnode",
            "params": ["192.168.0.6:8233", "onetry"]
        }\' -H \'content-type: text/plain;\' http://127.0.0.1:8232/\n'}

        Args:
            url: Node url
            opt: <add|remove|onetry>
        """
        if opt is not 'add' or opt is not 'remove' or opt is not 'onetry':
            raise ValueError('addnode <node> <add/remove/onetry>')
        return self._rpc_call(url, 'add')

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

    def gettransaction(self, tid):
        """
        Returns an object about the given transaction

        Args:
            tid: transaction id
        """
        return self._rpc_call('gettransaction', tid)

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
