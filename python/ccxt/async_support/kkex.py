# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.async_support.base.exchange import Exchange
from ccxt.base.errors import ArgumentsRequired
from ccxt.base.errors import InvalidOrder
from ccxt.base.errors import OrderNotFound


class kkex(Exchange):

    def describe(self):
        return self.deep_extend(super(kkex, self).describe(), {
            'id': 'kkex',
            'name': 'KKEX',
            'countries': ['CN', 'US', 'JP'],
            'version': 'v2',
            'has': {
                'CORS': False,
                'fetchBalance': True,
                'fetchTickers': True,
                'fetchOrders': True,
                'fetchOpenOrders': True,
                'fetchClosedOrders': True,
                'fetchMyTrades': True,
                'fetchOHLCV': True,
                'createMarketOrder': True,
                'fetchOrder': True,
            },
            'timeframes': {
                '1m': '1min',
                '5m': '5min',
                '15m': '15min',
                '30m': '30min',
                '1h': '1hour',
                '4h': '4hour',
                '12h': '12hour',
                '1d': '1day',
                '1w': '1week',
                '1M': '1month',
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/47401462-2e59f800-d74a-11e8-814f-e4ae17b4968a.jpg',
                'api': {
                    'public': 'https://kkex.com/api/v1',
                    'private': 'https://kkex.com/api/v2',
                    'v1': 'https://kkex.com/api/v1',
                },
                'www': 'https://kkex.com',
                'doc': 'https://kkex.com/api_wiki/cn/',
                'fees': 'https://intercom.help/kkex/fee',
            },
            'api': {
                'public': {
                    'get': [
                        'exchange_rate',
                        'products',
                        'assets',
                        'tickers',
                        'ticker',
                        'depth',
                        'trades',
                        'kline',
                    ],
                },
                'private': {
                    'post': [
                        'profile',
                        'trade',
                        'batch_trade',
                        'cancel_order',
                        'cancel_all_orders',
                        'order_history',
                        'userinfo',
                        'order_info',
                        'orders_info',
                    ],
                },
                'v1': {
                    'post': [
                        'process_strategy',
                    ],
                },
            },
            'fees': {
                'trading': {
                    'tierBased': False,
                    'percentage': True,
                    'taker': 0.002,
                    'maker': 0.002,
                },
                'funding': {
                    'tierBased': False,
                    'percentage': False,
                    'withdraw': {},
                    'deposit': {},
                },
            },
            'options': {
                'lastNonceTimestamp': 0,
            },
        })

    async def fetch_markets(self, params={}):
        tickers = await self.publicGetTickers(params)
        tickers = tickers['tickers']
        products = await self.publicGetProducts(params)
        products = products['products']
        markets = []
        for k in range(0, len(tickers)):
            keys = list(tickers[k].keys())
            markets.append(keys[0])
        result = []
        for i in range(0, len(markets)):
            id = markets[i]
            market = markets[i]
            baseId = ''
            quoteId = ''
            precision = {}
            limits = {}
            for j in range(0, len(products)):
                p = products[j]
                if p['mark_asset'] + p['base_asset'] == market:
                    quoteId = p['base_asset']
                    baseId = p['mark_asset']
                    price_scale_str = str(p['price_scale'])
                    scale = len(price_scale_str) - 1
                    precision = {
                        'price': scale,
                        'amount': scale,
                    }
                    limits = {
                        'amount': {
                            'min': max(self.safe_float(p, 'min_bid_size'), self.safe_float(p, 'min_ask_size')),
                            'max': min(self.safe_float(p, 'max_bid_size'), self.safe_float(p, 'max_ask_size')),
                        },
                        'price': {
                            'min': self.safe_float(p, 'min_price'),
                            'max': self.safe_float(p, 'max_price'),
                        },
                    }
                    limits['cost'] = {
                        'min': self.safe_float(p, 'min_bid_amount'),
                        'max': self.safe_float(p, 'max_bid_amount'),
                    }
            base = self.safe_currency_code(baseId)
            quote = self.safe_currency_code(quoteId)
            symbol = base + '/' + quote
            result.append({
                'id': id,
                'symbol': symbol,
                'base': base,
                'quote': quote,
                'baseId': baseId,
                'quoteId': quoteId,
                'active': True,
                'precision': precision,
                'limits': limits,
                'info': market,
            })
        return result

    def parse_ticker(self, ticker, market=None):
        timestamp = self.safe_timestamp(ticker, 'date')
        symbol = None
        if market is not None:
            symbol = market['symbol']
        last = self.safe_float(ticker, 'last')
        return {
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': self.safe_float(ticker, 'high'),
            'low': self.safe_float(ticker, 'low'),
            'bid': self.safe_float(ticker, 'buy'),
            'bidVolume': None,
            'ask': self.safe_float(ticker, 'sell'),
            'askVolume': None,
            'vwap': None,
            'open': None,
            'close': last,
            'last': last,
            'previousClose': None,
            'change': None,
            'percentage': None,
            'average': None,
            'baseVolume': self.safe_float(ticker, 'vol'),
            'quoteVolume': None,
            'info': ticker,
        }

    async def fetch_ticker(self, symbol, params={}):
        await self.load_markets()
        market = self.markets[symbol]
        request = {
            'symbol': market['id'],
        }
        response = await self.publicGetTicker(self.extend(request, params))
        ticker = self.extend(response['ticker'], self.omit(response, 'ticker'))
        return self.parse_ticker(ticker, market)

    async def fetch_tickers(self, symbols=None, params={}):
        await self.load_markets()
        response = await self.publicGetTickers(params)
        #
        #     {   date:    1540350657,
        #       tickers: [{ENUBTC: {sell: "0.00000256",
        #                               buy: "0.00000253",
        #                              last: "0.00000253",
        #                               vol: "138686.828804",
        #                              high: "0.00000278",
        #                               low: "0.00000253",
        #                              open: "0.0000027"      }},
        #                  {ENUEOS: {sell: "0.00335",
        #                               buy: "0.002702",
        #                              last: "0.0034",
        #                               vol: "15084.9",
        #                              high: "0.0034",
        #                               low: "0.003189",
        #                              open: "0.003189"  }}           ],
        #        result:    True                                          }
        #
        tickers = self.safe_value(response, 'tickers')
        result = {}
        for i in range(0, len(tickers)):
            ids = list(tickers[i].keys())
            id = ids[0]
            market = self.safe_value(self.markets_by_id, id)
            if market is not None:
                symbol = market['symbol']
                ticker = self.extend(tickers[i][id], self.omit(response, 'tickers'))
                result[symbol] = self.parse_ticker(ticker, market)
        return result

    async def fetch_order_book(self, symbol, limit=None, params={}):
        await self.load_markets()
        request = {
            'symbol': self.market_id(symbol),
        }
        if limit is not None:
            request['size'] = limit
        response = await self.publicGetDepth(self.extend(request, params))
        return self.parse_order_book(response)

    def parse_trade(self, trade, market=None):
        timestamp = self.safe_integer(trade, 'date_ms')
        datetime = self.iso8601(timestamp)
        price = self.safe_float(trade, 'price')
        amount = self.safe_float(trade, 'amount')
        cost = None
        if price is not None:
            if amount is not None:
                cost = amount * price
        symbol = None
        if market is not None:
            symbol = market['symbol']
        id = self.safe_string(trade, 'tid')
        type = None
        side = self.safe_string(trade, 'type')
        return {
            'info': trade,
            'id': id,
            'timestamp': timestamp,
            'datetime': datetime,
            'symbol': symbol,
            'order': None,
            'type': type,
            'side': side,
            'takerOrMaker': None,
            'price': price,
            'amount': amount,
            'cost': cost,
            'fee': None,
        }

    async def fetch_trades(self, symbol, since=None, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
        }
        response = await self.publicGetTrades(self.extend(request, params))
        return self.parse_trades(response, market, since, limit)

    async def fetch_balance(self, params={}):
        await self.load_markets()
        response = await self.privatePostUserinfo(params)
        balances = self.safe_value(response, 'info')
        result = {'info': response}
        funds = self.safe_value(balances, 'funds')
        free = self.safe_value(funds, 'free', {})
        freezed = self.safe_value(funds, 'freezed', {})
        currencyIds = list(free.keys())
        for i in range(0, len(currencyIds)):
            currencyId = currencyIds[i]
            code = self.safe_currency_code(currencyId)
            account = self.account()
            account['free'] = self.safe_float(free, currencyId)
            account['used'] = self.safe_float(freezed, currencyId)
            result[code] = account
        return self.parse_balance(result)

    async def fetch_order(self, id, symbol=None, params={}):
        if not symbol:
            raise ArgumentsRequired(self.id + ' fetchOrder requires a symbol argument')
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'order_id': id,
            'symbol': market['id'],
        }
        response = await self.privatePostOrderInfo(self.extend(request, params))
        if response['result']:
            return self.parse_order(response['order'], market)
        raise OrderNotFound(self.id + ' order ' + id + ' not found')

    def parse_ohlcv(self, ohlcv, market=None, timeframe='1m', since=None, limit=None):
        return [
            int(ohlcv[0]),
            float(ohlcv[1]),
            float(ohlcv[2]),
            float(ohlcv[3]),
            float(ohlcv[4]),
            float(ohlcv[5]),
        ]

    async def fetch_ohlcv(self, symbol, timeframe='1m', since=None, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
            'type': self.timeframes[timeframe],
        }
        if since is not None:
            # since = self.milliseconds() - self.parse_timeframe(timeframe) * limit * 1000
            request['since'] = int(since / 1000)
        if limit is not None:
            request['size'] = limit
        response = await self.publicGetKline(self.extend(request, params))
        #
        #     [
        #         [
        #             "1521072000000",
        #             "0.000002",
        #             "0.00003",
        #             "0.000002",
        #             "0.00003",
        #             "3.106889"
        #         ],
        #         [
        #             "1517356800000",
        #             "0.1",
        #             "0.1",
        #             "0.00000013",
        #             "0.000001",
        #             "542832.83114"
        #         ]
        #     ]
        #
        return self.parse_ohlcvs(response, market, timeframe, since, limit)

    def parse_order_status(self, status):
        statuses = {
            '-1': 'canceled',
            '0': 'open',
            '1': 'open',
            '2': 'closed',
            '3': 'open',
            '4': 'canceled',
        }
        return self.safe_string(statuses, status, status)

    def parse_order(self, order, market=None):
        #
        #     {
        #         "status": 2,
        #         "source": "NORMAL",
        #         "amount": "10.852019",
        #         "create_date": 1523938461036,
        #         "avg_price": "0.00096104",
        #         "order_id": "100",
        #         "price": "0.00096105",
        #         "type": "buy",
        #         "symbol": "READBTC",
        #         "deal_amount": "10.852019"
        #     }
        #
        symbol = None
        if market is not None:
            symbol = market['symbol']
        side = self.safe_string(order, 'side')
        if side is None:
            side = self.safe_string(order, 'type')
        timestamp = self.safe_integer(order, 'create_date')
        id = self.safe_string_2(order, 'order_id', 'id')
        status = self.parse_order_status(self.safe_string(order, 'status'))
        price = self.safe_float(order, 'price')
        amount = self.safe_float(order, 'amount')
        filled = self.safe_float(order, 'deal_amount')
        average = self.safe_float(order, 'avg_price')
        average = self.safe_float(order, 'price_avg', average)
        remaining = None
        cost = None
        if filled is not None:
            if amount is not None:
                remaining = amount - filled
            if average is not None:
                cost = average * filled
        return {
            'id': id,
            'clientOrderId': None,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'lastTradeTimestamp': None,
            'status': status,
            'symbol': symbol,
            'average': average,
            'type': 'limit',
            'side': side,
            'price': price,
            'cost': cost,
            'amount': amount,
            'filled': filled,
            'remaining': remaining,
            'fee': None,
            'info': order,
            'trades': None,
        }

    async def create_order(self, symbol, type, side, amount, price=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
            'type': side,
        }
        if type == 'market':
            # for market buy it requires the amount of quote currency to spend
            if side == 'buy':
                if self.options['createMarketBuyOrderRequiresPrice']:
                    if price is None:
                        raise InvalidOrder(self.id + " createOrder() requires the price argument with market buy orders to calculate total order cost(amount to spend), where cost = amount * price. Supply a price argument to createOrder() call if you want the cost to be calculated for you from price and amount, or, alternatively, add .options['createMarketBuyOrderRequiresPrice'] = False to supply the cost in the amount argument(the exchange-specific behaviour)")
                    else:
                        request['amount'] = self.cost_to_precision(symbol, float(amount) * float(price))
                request['price'] = self.cost_to_precision(symbol, amount)
            else:
                request['amount'] = self.amount_to_precision(symbol, amount)
            request['type'] += '_' + type
        else:
            request['amount'] = self.amount_to_precision(symbol, amount)
            request['price'] = self.price_to_precision(symbol, price)
        response = await self.privatePostTrade(self.extend(request, params))
        id = self.safe_string(response, 'order_id')
        return {
            'info': response,
            'id': id,
            'datetime': None,
            'timestamp': None,
            'lastTradeTimestamp': None,
            'status': 'open',
            'symbol': symbol,
            'type': type,
            'side': side,
            'price': price,
            'cost': None,
            'amount': amount,
            'filled': None,
            'remaining': None,
            'trades': None,
            'fee': None,
            'clientOrderId': None,
            'average': None,
        }

    async def cancel_order(self, id, symbol=None, params={}):
        if symbol is None:
            raise ArgumentsRequired(self.id + ' cancelOrder requires a symbol argument')
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'order_id': id,
            'symbol': market['id'],
        }
        return await self.privatePostCancelOrder(self.extend(request, params))

    async def fetch_orders(self, symbol=None, since=None, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
        }
        if limit is not None:
            request['page_length'] = limit  # 20 by default
        response = await self.privatePostOrderHistory(self.extend(request, params))
        return self.parse_orders(response['orders'], market, since, limit)

    async def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        request = {
            'status': 0,
        }
        return await self.fetch_orders(symbol, since, limit, self.extend(request, params))

    async def fetch_closed_orders(self, symbol=None, since=None, limit=None, params={}):
        request = {
            'status': 1,
        }
        return await self.fetch_orders(symbol, since, limit, self.extend(request, params))

    def nonce(self):
        return self.milliseconds()

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        url = self.urls['api'][api] + '/' + path
        if api == 'public':
            url += '?' + self.urlencode(params)
            headers = {'Content-Type': 'application/json'}
        else:
            self.check_required_credentials()
            nonce = self.nonce()
            signature = self.extend({
                'nonce': nonce,
                'api_key': self.apiKey,
            }, params)
            signature = self.urlencode(self.keysort(signature))
            signature += '&secret_key=' + self.secret
            signature = self.hash(self.encode(signature), 'md5')
            signature = signature.upper()
            body = self.extend({
                'api_key': self.apiKey,
                'sign': signature,
                'nonce': nonce,
            }, params)
            body = self.urlencode(body)
            headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        return {'url': url, 'method': method, 'body': body, 'headers': headers}
