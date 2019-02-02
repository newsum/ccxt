# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.base.exchange import Exchange
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import PermissionDenied
from ccxt.base.errors import InsufficientFunds
from ccxt.base.errors import InvalidAddress
from ccxt.base.errors import InvalidOrder
from ccxt.base.errors import OrderNotFound
from ccxt.base.errors import InvalidNonce


class cobinhood (Exchange):

    def describe(self):
        return self.deep_extend(super(cobinhood, self).describe(), {
            'id': 'cobinhood',
            'name': 'COBINHOOD',
            'countries': ['TW'],
            'rateLimit': 1000 / 10,
            'version': 'v1',
            'has': {
                'fetchCurrencies': True,
                'fetchTickers': True,
                'fetchOHLCV': True,
                'fetchOpenOrders': True,
                'fetchClosedOrders': True,
                'fetchOrderTrades': True,
                'fetchOrder': True,
                'fetchDepositAddress': True,
                'createDepositAddress': True,
                'fetchDeposits': True,
                'fetchWithdrawals': True,
                'withdraw': True,
                'fetchMyTrades': True,
                'editOrder': True,
            },
            'requiredCredentials': {
                'apiKey': True,
                'secret': False,
            },
            'timeframes': {
                # the first two don't seem to work at all
                '1m': '1m',
                '5m': '5m',
                '15m': '15m',
                '30m': '30m',
                '1h': '1h',
                '3h': '3h',
                '6h': '6h',
                '12h': '12h',
                '1d': '1D',
                '1w': '7D',
                '2w': '14D',
                '1M': '1M',
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/35755576-dee02e5c-0878-11e8-989f-1595d80ba47f.jpg',
                'api': 'https://api.cobinhood.com',
                'www': 'https://cobinhood.com',
                'doc': 'https://cobinhood.github.io/api-public',
            },
            'api': {
                'system': {
                    'get': [
                        'info',
                        'time',
                        'messages',
                        'messages/{message_id}',
                    ],
                },
                'admin': {
                    'get': [
                        'system/messages',
                        'system/messages/{message_id}',
                    ],
                    'post': [
                        'system/messages',
                    ],
                    'patch': [
                        'system/messages/{message_id}',
                    ],
                    'delete': [
                        'system/messages/{message_id}',
                    ],
                },
                'public': {
                    'get': [
                        'market/fundingbook/precisions/{currency_id}',
                        'market/fundingbooks/{currency_id}',
                        'market/tickers',
                        'market/currencies',
                        'market/quote_currencies',
                        'market/trading_pairs',
                        'market/orderbook/precisions/{trading_pair_id}',
                        'market/orderbooks/{trading_pair_id}',
                        'market/stats',
                        'market/tickers',  # fetchTickers
                        'market/tickers/{trading_pair_id}',
                        'market/trades/{trading_pair_id}',
                        'market/trades_history/{trading_pair_id}',
                        'market/trading_pairs',
                        'chart/candles/{trading_pair_id}',
                        'system/time',
                    ],
                },
                'private': {
                    'get': [
                        'funding/auto_offerings',
                        'funding/auto_offerings/{currency_id}',
                        'funding/funding_history',
                        'funding/fundings',
                        'funding/loans',
                        'funding/loans/{loan_id}',
                        'trading/orders/{order_id}',
                        'trading/orders/{order_id}/trades',
                        'trading/orders',
                        'trading/order_history',
                        'trading/positions',
                        'trading/positions/{trading_pair_id}',
                        'trading/positions/{trading_pair_id}/claimable_size',
                        'trading/trades',
                        'trading/trades/{trade_id}',
                        'trading/volume',
                        'wallet/balances',
                        'wallet/ledger',
                        'wallet/limits/withdrawal',
                        'wallet/generic_deposits',
                        'wallet/generic_deposits/{generic_deposit_id}',
                        'wallet/generic_withdrawals',
                        'wallet/generic_withdrawals/{generic_withdrawal_id}',
                        # older endpoints
                        'wallet/deposit_addresses',
                        'wallet/deposit_addresses/iota',
                        'wallet/withdrawal_addresses',
                        'wallet/withdrawal_frozen',
                        'wallet/withdrawals/{withdrawal_id}',
                        'wallet/withdrawals',
                        'wallet/deposits/{deposit_id}',
                        'wallet/deposits',
                    ],
                    'patch': [
                        'trading/positions/{trading_pair_id}',
                    ],
                    'post': [
                        'funding/auto_offerings',
                        'funding/fundings',
                        'trading/check_order',
                        'trading/orders',
                        # older endpoints
                        'wallet/deposit_addresses',
                        'wallet/transfer',
                        'wallet/withdrawal_addresses',
                        'wallet/withdrawals',
                        'wallet/withdrawals/fee',
                    ],
                    'put': [
                        'funding/fundings/{funding_id}',
                        'trading/orders/{order_id}',
                    ],
                    'delete': [
                        'funding/auto_offerings/{currency_id}',
                        'funding/fundings/{funding_id}',
                        'funding/loans/{loan_id}',
                        'trading/orders/{order_id}',
                        'trading/positions/{trading_pair_id}',
                        'wallet/generic_withdrawals/{generic_withdrawal_id}',
                        'wallet/withdrawal_addresses/{wallet_id}',
                    ],
                },
            },
            'fees': {
                'trading': {
                    'maker': 0.0,
                    'taker': 0.0,
                },
            },
            'precision': {
                'amount': 8,
                'price': 8,
            },
            'exceptions': {
                'insufficient_balance': InsufficientFunds,
                'invalid_order_size': InvalidOrder,
                'invalid_nonce': InvalidNonce,
                'unauthorized_scope': PermissionDenied,
                'invalid_address': InvalidAddress,
                'parameter_error': OrderNotFound,
            },
            'commonCurrencies': {
                'SMT': 'SocialMedia.Market',
                'MTN': 'Motion Token',
            },
        })

    def fetch_currencies(self, params={}):
        response = self.publicGetMarketCurrencies(params)
        currencies = response['result']['currencies']
        result = {}
        for i in range(0, len(currencies)):
            currency = currencies[i]
            id = currency['currency']
            code = self.common_currency_code(id)
            minUnit = self.safe_float(currency, 'min_unit')
            result[code] = {
                'id': id,
                'code': code,
                'name': currency['name'],
                'active': True,
                'fiat': False,
                'precision': self.precision_from_string(currency['min_unit']),
                'limits': {
                    'amount': {
                        'min': minUnit,
                        'max': None,
                    },
                    'price': {
                        'min': minUnit,
                        'max': None,
                    },
                    'deposit': {
                        'min': minUnit,
                        'max': None,
                    },
                    'withdraw': {
                        'min': minUnit,
                        'max': None,
                    },
                },
                'funding': {
                    'withdraw': {
                        'fee': self.safe_float(currency, 'withdrawal_fee'),
                    },
                    'deposit': {
                        'fee': self.safe_float(currency, 'deposit_fee'),
                    },
                },
                'info': currency,
            }
        return result

    def fetch_markets(self, params={}):
        response = self.publicGetMarketTradingPairs()
        markets = response['result']['trading_pairs']
        result = []
        for i in range(0, len(markets)):
            market = markets[i]
            id = market['id']
            baseId, quoteId = id.split('-')
            base = self.common_currency_code(baseId)
            quote = self.common_currency_code(quoteId)
            symbol = base + '/' + quote
            precision = {
                'amount': 8,
                'price': self.precision_from_string(market['quote_increment']),
            }
            active = self.safe_value(market, 'is_active', True)
            result.append({
                'id': id,
                'symbol': symbol,
                'base': base,
                'quote': quote,
                'baseId': baseId,
                'quoteId': quoteId,
                'active': active,
                'precision': precision,
                'limits': {
                    'amount': {
                        'min': self.safe_float(market, 'base_min_size'),
                        'max': self.safe_float(market, 'base_max_size'),
                    },
                    'price': {
                        'min': None,
                        'max': None,
                    },
                    'cost': {
                        'min': None,
                        'max': None,
                    },
                },
                'info': market,
            })
        return result

    def parse_ticker(self, ticker, market=None):
        symbol = None
        if market is None:
            marketId = self.safe_string(ticker, 'trading_pair_id')
            if marketId in self.markets_by_id:
                market = self.markets_by_id[marketId]
            else:
                baseId, quoteId = marketId.split('-')
                base = self.common_currency_code(baseId)
                quote = self.common_currency_code(quoteId)
                symbol = base + '/' + quote
        if market is not None:
            symbol = market['symbol']
        timestamp = self.safe_integer(ticker, 'timestamp')
        last = self.safe_float(ticker, 'last_trade_price')
        return {
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': self.safe_float(ticker, '24h_high'),
            'low': self.safe_float(ticker, '24h_low'),
            'bid': self.safe_float(ticker, 'highest_bid'),
            'bidVolume': None,
            'ask': self.safe_float(ticker, 'lowest_ask'),
            'askVolume': None,
            'vwap': None,
            'open': None,
            'close': last,
            'last': last,
            'previousClose': None,
            'change': self.safe_float(ticker, 'percentChanged24hr'),
            'percentage': None,
            'average': None,
            'baseVolume': self.safe_float(ticker, '24h_volume'),
            'quoteVolume': self.safe_float(ticker, 'quote_volume'),
            'info': ticker,
        }

    def fetch_ticker(self, symbol, params={}):
        self.load_markets()
        market = self.market(symbol)
        response = self.publicGetMarketTickersTradingPairId(self.extend({
            'trading_pair_id': market['id'],
        }, params))
        ticker = response['result']['ticker']
        return self.parse_ticker(ticker, market)

    def fetch_tickers(self, symbols=None, params={}):
        self.load_markets()
        response = self.publicGetMarketTickers(params)
        tickers = response['result']['tickers']
        result = []
        for i in range(0, len(tickers)):
            result.append(self.parse_ticker(tickers[i]))
        return self.index_by(result, 'symbol')

    def fetch_order_book(self, symbol, limit=None, params={}):
        self.load_markets()
        request = {
            'trading_pair_id': self.market_id(symbol),
        }
        if limit is not None:
            request['limit'] = limit  # 100
        response = self.publicGetMarketOrderbooksTradingPairId(self.extend(request, params))
        return self.parse_order_book(response['result']['orderbook'], None, 'bids', 'asks', 0, 2)

    def parse_trade(self, trade, market=None):
        symbol = None
        if market:
            symbol = market['symbol']
        timestamp = trade['timestamp']
        price = self.safe_float(trade, 'price')
        amount = self.safe_float(trade, 'size')
        cost = price * amount
        # you can't determine your side from maker/taker side and vice versa
        # you can't determine if your order/trade was a maker or a taker based
        # on just the side of your order/trade
        # https://github.com/ccxt/ccxt/issues/4300
        # side = 'sell' if (trade['maker_side'] == 'bid') else 'buy'
        side = None
        return {
            'info': trade,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': symbol,
            'id': trade['id'],
            'order': None,
            'type': None,
            'side': side,
            'price': price,
            'amount': amount,
            'cost': cost,
            'fee': None,
        }

    def fetch_trades(self, symbol, since=None, limit=50, params={}):
        self.load_markets()
        market = self.market(symbol)
        response = self.publicGetMarketTradesTradingPairId(self.extend({
            'trading_pair_id': market['id'],
            'limit': limit,  # default 20, but that seems too little
        }, params))
        trades = response['result']['trades']
        return self.parse_trades(trades, market, since, limit)

    def parse_ohlcv(self, ohlcv, market=None, timeframe='5m', since=None, limit=None):
        return [
            # they say that timestamps are Unix Timestamps in seconds, but in fact those are milliseconds
            ohlcv['timestamp'],
            float(ohlcv['open']),
            float(ohlcv['high']),
            float(ohlcv['low']),
            float(ohlcv['close']),
            float(ohlcv['volume']),
        ]

    def fetch_ohlcv(self, symbol, timeframe='1m', since=None, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        #
        # they say in their docs that end_time defaults to current server time
        # but if you don't specify it, their range limits does not allow you to query anything
        #
        # they also say that start_time defaults to 0,
        # but most calls fail if you do not specify any of end_time
        #
        # to make things worse, their docs say it should be a Unix Timestamp
        # but with seconds it fails, so we set milliseconds(somehow it works that way)
        #
        endTime = self.milliseconds()
        request = {
            'trading_pair_id': market['id'],
            'timeframe': self.timeframes[timeframe],
            'end_time': endTime,
        }
        if since is not None:
            request['start_time'] = since
        response = self.publicGetChartCandlesTradingPairId(self.extend(request, params))
        ohlcv = response['result']['candles']
        return self.parse_ohlcvs(ohlcv, market, timeframe, since, limit)

    def fetch_balance(self, params={}):
        self.load_markets()
        response = self.privateGetWalletBalances(params)
        result = {'info': response}
        balances = response['result']['balances']
        for i in range(0, len(balances)):
            balance = balances[i]
            currency = balance['currency']
            if currency in self.currencies_by_id:
                currency = self.currencies_by_id[currency]['code']
            account = {
                'used': float(balance['on_order']),
                'total': float(balance['total']),
            }
            account['free'] = float(account['total'] - account['used'])
            result[currency] = account
        return self.parse_balance(result)

    def parse_order_status(self, status):
        statuses = {
            'filled': 'closed',
            'rejected': 'closed',
            'partially_filled': 'open',
            'pending_cancellation': 'open',
            'pending_modification': 'open',
            'open': 'open',
            'new': 'open',
            'queued': 'open',
            'cancelled': 'canceled',
            'triggered': 'triggered',
        }
        if status in statuses:
            return statuses[status]
        return status

    def parse_order(self, order, market=None):
        #
        #     {
        #         'completed_at': None,
        #         'eq_price': '0',
        #         'filled': '0',
        #         'id': '88426800-beae-4407-b4a1-f65cef693542',
        #         'price': '0.00000507',
        #         'side': 'bid',
        #         'size': '3503.6489',
        #         'source': 'exchange',
        #         'state': 'open',
        #         'timestamp': 1535258403597,
        #         'trading_pair_id': 'ACT-BTC',
        #         'type': 'limit',
        #     }
        #
        symbol = None
        if market is None:
            marketId = self.safe_string_2(order, 'trading_pair', 'trading_pair_id')
            market = self.safe_value(self.markets_by_id, marketId)
        if market is not None:
            symbol = market['symbol']
        timestamp = self.safe_integer(order, 'timestamp')
        price = self.safe_float(order, 'price')
        average = self.safe_float(order, 'eq_price')
        amount = self.safe_float(order, 'size')
        filled = self.safe_float(order, 'filled')
        remaining = None
        cost = None
        if filled is not None and average is not None:
            cost = average * filled
        elif average is not None:
            cost = average * amount
        if amount is not None:
            if filled is not None:
                remaining = amount - filled
        status = self.parse_order_status(self.safe_string(order, 'state'))
        side = self.safe_string(order, 'side')
        if side == 'bid':
            side = 'buy'
        elif side == 'ask':
            side = 'sell'
        return {
            'id': self.safe_string(order, 'id'),
            'datetime': self.iso8601(timestamp),
            'timestamp': timestamp,
            'lastTradeTimestamp': None,
            'status': status,
            'symbol': symbol,
            'type': self.safe_string(order, 'type'),  # market, limit, stop, stop_limit, trailing_stop, fill_or_kill
            'side': side,
            'price': price,
            'cost': cost,
            'average': average,
            'amount': amount,
            'filled': filled,
            'remaining': remaining,
            'trades': None,
            'fee': None,
            'info': order,
        }

    def create_order(self, symbol, type, side, amount, price=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        side = 'ask' if (side == 'sell') else 'bid'
        request = {
            'trading_pair_id': market['id'],
            'type': type,  # market, limit, stop, stop_limit
            'side': side,
            'size': self.amount_to_precision(symbol, amount),
        }
        if type != 'market':
            request['price'] = self.price_to_precision(symbol, price)
        response = self.privatePostTradingOrders(self.extend(request, params))
        order = self.parse_order(response['result']['order'], market)
        id = order['id']
        self.orders[id] = order
        return order

    def edit_order(self, id, symbol, type, side, amount, price, params={}):
        self.load_markets()
        response = self.privatePutTradingOrdersOrderId(self.extend({
            'order_id': id,
            'price': self.price_to_precision(symbol, price),
            'size': self.amount_to_precision(symbol, amount),
        }, params))
        return self.parse_order(self.extend(response, {
            'id': id,
        }))

    def cancel_order(self, id, symbol=None, params={}):
        self.load_markets()
        response = self.privateDeleteTradingOrdersOrderId(self.extend({
            'order_id': id,
        }, params))
        return self.parse_order(self.extend(response, {
            'id': id,
        }))

    def fetch_order(self, id, symbol=None, params={}):
        self.load_markets()
        response = self.privateGetTradingOrdersOrderId(self.extend({
            'order_id': str(id),
        }, params))
        return self.parse_order(response['result']['order'])

    def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        self.load_markets()
        result = self.privateGetTradingOrders(params)
        orders = self.parse_orders(result['result']['orders'], None, since, limit)
        if symbol is not None:
            return self.filter_by_symbol_since_limit(orders, symbol, since, limit)
        return self.filter_by_since_limit(orders, since, limit)

    def fetch_closed_orders(self, symbol=None, since=None, limit=None, params={}):
        self.load_markets()
        result = self.privateGetTradingOrderHistory(params)
        orders = self.parse_orders(result['result']['orders'], None, since, limit)
        if symbol is not None:
            return self.filter_by_symbol_since_limit(orders, symbol, since, limit)
        return self.filter_by_since_limit(orders, since, limit)

    def fetch_order_trades(self, id, symbol=None, since=None, limit=None, params={}):
        self.load_markets()
        response = self.privateGetTradingOrdersOrderIdTrades(self.extend({
            'order_id': id,
        }, params))
        market = None if (symbol is None) else self.market(symbol)
        return self.parse_trades(response['result']['trades'], market)

    def fetch_my_trades(self, symbol=None, since=None, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {}
        if symbol is not None:
            request['trading_pair_id'] = market['id']
        response = self.privateGetTradingTrades(self.extend(request, params))
        return self.parse_trades(response['result']['trades'], market, since, limit)

    def create_deposit_address(self, code, params={}):
        self.load_markets()
        currency = self.currency(code)
        # 'ledger_type' is required, see: https://cobinhood.github.io/api-public/#create-new-deposit-address
        ledgerType = self.safe_string(params, 'ledger_type', 'exchange')
        request = {
            'currency': currency['id'],
            'ledger_type': ledgerType,
        }
        response = self.privatePostWalletDepositAddresses(self.extend(request, params))
        address = self.safe_string(response['result']['deposit_address'], 'address')
        tag = self.safe_string(response['result']['deposit_address'], 'memo')
        self.check_address(address)
        return {
            'currency': code,
            'address': address,
            'tag': tag,
            'info': response,
        }

    def fetch_deposit_address(self, code, params={}):
        self.load_markets()
        currency = self.currency(code)
        response = self.privateGetWalletDepositAddresses(self.extend({
            'currency': currency['id'],
        }, params))
        #
        #     {success:    True,
        #        result: {deposit_addresses: [{      address: "abcdefg",
        #                                         blockchain_id: "eosio",
        #                                            created_at:  1536768050235,
        #                                              currency: "EOS",
        #                                                  memo: "12345678",
        #                                                  type: "exchange"      }]} }
        #
        addresses = self.safe_value(response['result'], 'deposit_addresses', [])
        address = None
        tag = None
        if len(addresses) > 0:
            address = self.safe_string(addresses[0], 'address')
            tag = self.safe_string_2(addresses[0], 'memo', 'tag')
        self.check_address(address)
        return {
            'currency': code,
            'address': address,
            'tag': tag,
            'info': response,
        }

    def withdraw(self, code, amount, address, tag=None, params={}):
        self.load_markets()
        currency = self.currency(code)
        request = {
            'currency': currency['id'],
            'amount': amount,
            'address': address,
        }
        if tag is not None:
            request['memo'] = tag
        response = self.privatePostWalletWithdrawals(self.extend(request, params))
        return {
            'id': None,
            'info': response,
        }

    def fetch_deposits(self, code=None, since=None, limit=None, params={}):
        self.load_markets()
        if code is None:
            raise ExchangeError(self.id + ' fetchDeposits() requires a currency code arguemnt')
        currency = self.currency(code)
        request = {
            'currency': currency['id'],
        }
        response = self.privateGetWalletDeposits(self.extend(request, params))
        return self.parseTransactions(response['result']['deposits'], currency)

    def fetch_withdrawals(self, code=None, since=None, limit=None, params={}):
        self.load_markets()
        if code is None:
            raise ExchangeError(self.id + ' fetchWithdrawals() requires a currency code arguemnt')
        currency = self.currency(code)
        request = {
            'currency': currency['id'],
        }
        response = self.privateGetWalletWithdrawals(self.extend(request, params))
        return self.parseTransactions(response['result']['withdrawals'], currency)

    def parse_transaction_status(self, status):
        statuses = {
            'tx_pending_two_factor_auth': 'pending',
            'tx_pending_email_auth': 'pending',
            'tx_pending_approval': 'pending',
            'tx_approved': 'pending',
            'tx_processing': 'pending',
            'tx_pending': 'pending',
            'tx_sent': 'pending',
            'tx_cancelled': 'canceled',
            'tx_timeout': 'failed',
            'tx_invalid': 'failed',
            'tx_rejected': 'failed',
            'tx_confirmed': 'ok',
        }
        return statuses[status] if (status in list(statuses.keys())) else status

    def parse_transaction(self, transaction, currency=None):
        timestamp = self.safe_integer(transaction, 'created_at')
        code = None
        if currency is None:
            currencyId = self.safe_string(transaction, 'currency')
            if currencyId in self.currencies_by_id:
                currency = self.currencies_by_id[currencyId]
            else:
                code = self.common_currency_code(currencyId)
        if currency is not None:
            code = currency['code']
        id = None
        withdrawalId = self.safe_string(transaction, 'withdrawal_id')
        depositId = self.safe_string(transaction, 'deposit_id')
        type = None
        address = None
        if withdrawalId is not None:
            type = 'withdrawal'
            id = withdrawalId
            address = self.safe_string(transaction, 'to_address')
        elif depositId is not None:
            type = 'deposit'
            id = depositId
            address = self.safe_string(transaction, 'from_address')
        additionalInfo = self.safe_value(transaction, 'additional_info', {})
        tag = self.safe_string(additionalInfo, 'memo')
        return {
            'info': transaction,
            'id': id,
            'txid': self.safe_string(transaction, 'txhash'),
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'address': address,
            'tag': tag,  # refix it properly
            'type': type,
            'amount': self.safe_float(transaction, 'amount'),
            'currency': code,
            'status': self.parse_transaction_status(transaction['status']),
            'updated': None,
            'fee': {
                'cost': self.safe_float(transaction, 'fee'),
                'rate': None,
            },
        }

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        url = self.urls['api'] + '/' + self.version + '/' + self.implode_params(path, params)
        query = self.omit(params, self.extract_params(path))
        headers = {}
        if api == 'private':
            self.check_required_credentials()
            # headers['device_id'] = self.apiKey
            headers['nonce'] = str(self.nonce())
            headers['Authorization'] = self.apiKey
        if method == 'GET':
            query = self.urlencode(query)
            if len(query):
                url += '?' + query
        else:
            headers['Content-type'] = 'application/json charset=UTF-8'
            body = self.json(query)
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def handle_errors(self, code, reason, url, method, headers, body, response):
        if code < 400 or code >= 600:
            return
        if body[0] != '{':
            raise ExchangeError(self.id + ' ' + body)
        feedback = self.id + ' ' + self.json(response)
        errorCode = self.safe_value(response['error'], 'error_code')
        if method == 'DELETE' or method == 'GET':
            if errorCode == 'parameter_error':
                if url.find('trading/orders/') >= 0:
                    # Cobinhood returns vague "parameter_error" on fetchOrder() and cancelOrder() calls
                    # for invalid order IDs as well as orders that are not "open"
                    raise InvalidOrder(feedback)
        exceptions = self.exceptions
        if errorCode in exceptions:
            raise exceptions[errorCode](feedback)
        raise ExchangeError(feedback)

    def nonce(self):
        return self.milliseconds()
