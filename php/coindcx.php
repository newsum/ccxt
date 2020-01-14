<?php

namespace ccxt;

// PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
// https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

use Exception; // a common import

class coindcx extends Exchange {

    public function describe () {
        return array_replace_recursive(parent::describe (), array(
            'id' => 'coindcx',
            'name' => 'CoinDCX',
            'countries' => ['IN'], // india
            'urls' => array(
                'api' => array(
                    'general' => 'https://api.coindcx.com',
                    'public' => 'https://public.coindcx.com',
                    'private' => 'https://api.coindcx.com',
                ),
                'www' => 'https://coindcx.com/',
                'doc' => 'https://coindcx-official.github.io/rest-api/',
                'fees' => 'https://coindcx.com/fees',
            ),
            'version' => 'v1',
            'requiredCredentials' => array(
                'apiKey' => true,
                'secret' => true,
                'token' => false,
            ),
            'api' => array(
                'general' => array(
                    'get' => array(
                        'exchange/ticker',
                        'exchange/v1/markets',
                        'exchange/v1/markets_details',
                    ),
                ),
                'public' => array(
                    'get' => array(
                        'market_data/trade_history',
                        'market_data/orderbook',
                        'market_data/candles',
                    ),
                ),
                'private' => array(
                    'post' => array(
                        'exchange/v1/users/balances',
                        'exchange/v1/orders/create',
                        'exchange/v1/orders/status',
                        'exchange/v1/orders/active_orders',
                        'exchange/v1/orders/trade_history',
                        'exchange/v1/orders/cancel',
                        'exchange/v1/orders/cancel_all',
                    ),
                ),
            ),
            'has' => array(
                'fetchTicker' => 'emulated',
                'fetchTickers' => true,
                'fetchTrades' => true,
                'fetchOrderBook' => true,
                'fetchOHLCV' => true,
                'fetchBalance' => true,
                'fetchOrder' => true,
                'fetchOpenOrders' => true,
                'createLimitOrder' => true,
                'createMarketOrder' => true,
                'createOrder' => true,
                'cancelOrder' => true,
                'cancelAllOrders' => true,
                'editOrder' => false,
            ),
            'timeframes' => array(
                '1m' => '1m',
                '5m' => '5m',
                '15m' => '15m',
                '30m' => '30m',
                '1h' => '1h',
                '2h' => '2h',
                '4h' => '4h',
                '6h' => '6h',
                '8h' => '8h',
                '1d' => '1d',
                '3d' => '3d',
                '1w' => '1w',
                '1M' => '1M',
            ),
            'timeout' => 10000,
            'rateLimit' => 2000,
            'exceptions' => array(
                'Invalid Request.' => '\\ccxt\\BadRequest', // Yeah, with a dot at the end.
                'Invalid credentials' => '\\ccxt\\PermissionDenied',
                'Insufficient funds' => '\\ccxt\\InsufficientFunds',
                'Quantity too low' => '\\ccxt\\InvalidOrder',
                'Order not found' => '\\ccxt\\OrderNotFound',
            ),
        ));
    }

    public function fetch_markets ($params = array ()) {
        // answer example https://coindcx-official.github.io/rest-api/?javascript#markets-$details
        $details = $this->generalGetExchangeV1MarketsDetails ($params);
        $result = array();
        for ($i = 0; $i < count($details); $i++) {
            $market = $details[$i];
            $id = $this->safe_string($market, 'symbol');
            $quoteId = $this->safe_string($market, 'base_currency_short_name');
            $quote = $this->safe_currency_code($quoteId);
            $baseId = $this->safe_string($market, 'target_currency_short_name');
            $base = $this->safe_currency_code($baseId);
            $symbol = $base . '/' . $quote;
            $active = false;
            if ($market['status'] === 'active') {
                $active = true;
            }
            $precision = array(
                'amount' => $this->safe_integer($market, 'base_currency_precision'),
                'price' => $this->safe_integer($market, 'target_currency_precision'),
            );
            $limits = array(
                'amount' => array(
                    'min' => $this->safe_float($market, 'min_quantity'),
                    'max' => $this->safe_float($market, 'max_quantity'),
                ),
                'price' => array(
                    'min' => $this->safe_float($market, 'min_price'),
                    'max' => $this->safe_float($market, 'max_price'),
                ),
            );
            $result[] = array(
                'id' => $id,
                'symbol' => $symbol,
                'base' => $base,
                'quote' => $quote,
                'baseId' => $baseId,
                'quoteId' => $quoteId,
                'active' => $active,
                'precision' => $precision,
                'limits' => $limits,
                'info' => $market,
            );
        }
        return $result;
    }

    public function fetch_tickers ($symbols = null, $params = array ()) {
        $this->load_markets();
        $response = $this->generalGetExchangeTicker ($params);
        $result = array();
        for ($i = 0; $i < count($response); $i++) {
            $ticker = $this->parse_ticker($response[$i]);
            // I found out that sometimes it returns tickers that aren't in the markets, so we should no add this to results
            if ($ticker === null) {
                continue;
            }
            $symbol = $ticker['symbol'];
            $result[$symbol] = $ticker;
        }
        return $result;
    }

    public function fetch_ticker ($symbol, $params = array ()) {
        $this->load_markets();
        $response = $this->generalGetExchangeTicker ($params);
        $market = $this->market ($symbol);
        $result = array();
        for ($i = 0; $i < count($response); $i++) {
            if ($response[$i]['market'] !== $market['id']) {
                continue;
            }
            $result = $this->parse_ticker($response[$i]);
            break;
        }
        return $result;
    }

    public function parse_ticker ($ticker) {
        $timestamp = $this->safe_timestamp($ticker, 'timestamp');
        $tickersMarket = $this->safe_string($ticker, 'market');
        if (!(is_array($this->markets_by_id) && array_key_exists($tickersMarket, $this->markets_by_id))) {
            return null;
        }
        $market = $this->markets_by_id[$tickersMarket];
        $last = $this->safe_float($ticker, 'last_price');
        return array(
            'symbol' => $market['symbol'],
            'info' => $ticker,
            'timestamp' => $timestamp,
            'datetime' => $this->iso8601 ($timestamp),
            'high' => $this->safe_float($ticker, 'high'),
            'low' => $this->safe_float($ticker, 'low'),
            'bid' => $this->safe_float($ticker, 'bid'),
            'bidVolume' => null,
            'ask' => $this->safe_float($ticker, 'ask'),
            'askVolume' => null,
            'vwap' => null,
            'open' => null,
            'close' => $last,
            'last' => $last,
            'previousClose' => null,
            'change' => $this->safe_float($ticker, 'change_24_hour'),
            'percentage' => null,
            'average' => null,
            'baseVolume' => $this->safe_float($ticker, 'volume'),
            'quoteVolume' => null,
        );
    }

    public function fetch_ohlcv ($symbol, $timeframe = '1m', $since = null, $limit = 500, $params = array ()) {
        // https://coindcx-official.github.io/rest-api/?shell#candles
        $this->load_markets();
        $market = $this->market ($symbol);
        $coindcxPair = $this->get_pair_from_info ($market);
        $coindcxTimeframe = $this->timeframes[$timeframe];
        if ($coindcxTimeframe === null) {
            throw new ExchangeError($this->id . ' has no "' . $timeframe . '" timeframe');
        }
        $request = array(
            'pair' => $coindcxPair,
            'interval' => $coindcxTimeframe,
            'limit' => $limit,
        );
        $response = $this->publicGetMarketDataCandles (array_merge($request, $params));
        return $this->parse_ohlcvs($response, $market, $timeframe, $since, $limit);
    }

    public function parse_ohlcv ($ohlcv, $market = null, $timeframe = '1m', $since = null, $limit = null) {
        return array(
            $this->safe_integer($ohlcv, 'time'),
            $this->safe_float($ohlcv, 'open'),
            $this->safe_float($ohlcv, 'high'),
            $this->safe_float($ohlcv, 'low'),
            $this->safe_float($ohlcv, 'close'),
            $this->safe_float($ohlcv, 'volume'),
        );
    }

    public function fetch_trades ($symbol, $since = null, $limit = 30, $params = array ()) {
        // https://coindcx-official.github.io/rest-api/?shell#trades
        $this->load_markets();
        $market = $this->market ($symbol);
        $coindcxPair = $this->get_pair_from_info ($market);
        $request = array(
            'pair' => $coindcxPair,
            'limit' => $limit,
        );
        $response = $this->publicGetMarketDataTradeHistory (array_merge($request, $params));
        return $this->parse_trades($response, $market, $since, $limit);
    }

    public function fetch_my_trades ($symbol = null, $since = null, $limit = 500, $params = array ()) {
        // https://coindcx-official.github.io/rest-api/?javascript#account-trade-history
        $this->load_markets();
        $request = array(
            'timestamp' => $this->milliseconds (),
            'limit' => $limit,
        );
        $response = $this->privatePostExchangeV1OrdersTradeHistory (array_merge($request, $params));
        return $this->parse_trades($response, null, $since, $limit);
    }

    public function parse_trade ($trade, $market = null) {
        $timestamp = $this->safe_integer_2($trade, 'T', 'timestamp');
        $symbol = null;
        if ($market === null) {
            $marketId = $this->safe_string_2($trade, 's', 'symbol');
            $market = $this->safe_value($this->markets_by_id, $marketId);
        }
        if ($market !== null) {
            $symbol = $market['symbol'];
        }
        $takerOrMaker = null;
        if (is_array($trade) && array_key_exists('m', $trade)) {
            $takerOrMaker = $trade['m'] ? 'maker' : 'taker';
        }
        $price = $this->safe_float_2($trade, 'p', 'price');
        $amount = $this->safe_float_2($trade, 'q', 'quantity');
        return array(
            'id' => $this->safe_string($trade, 'id'),
            'info' => $trade,
            'timestamp' => $timestamp,
            'datetime' => $this->iso8601 ($timestamp),
            'symbol' => $symbol,
            'order' => null,
            'type' => null,
            'takerOrMaker' => $takerOrMaker,
            'side' => $this->safe_string($trade, 'side'),
            'price' => $price,
            'amount' => $amount,
            'cost' => $price * $amount,
            'fee' => $this->safe_float($trade, 'fee_amount'),
        );
    }

    public function fetch_order_book ($symbol, $limit = null, $params = array ()) {
        // https://coindcx-official.github.io/rest-api/?shell#order-book
        $this->load_markets();
        $market = $this->market ($symbol);
        $coindcxPair = $this->get_pair_from_info ($market);
        $request = array(
            'pair' => $coindcxPair,
        );
        $response = $this->publicGetMarketDataOrderbook (array_merge($request, $params));
        return $this->parse_order_book($response);
    }

    public function parse_bids_asks ($bidasks, $priceKey = null, $amountKey = null) {
        $priceKeys = is_array($bidasks) ? array_keys($bidasks) : array();
        $parsedData = array();
        for ($i = 0; $i < count($priceKeys); $i++) {
            $amountKey = $priceKeys[$i];
            $price = floatval ($amountKey);
            $amount = floatval ($bidasks[$amountKey]);
            $parsedData[] = [$price, $amount];
        }
        return $parsedData;
    }

    public function fetch_balance ($params = array ()) {
        // https://coindcx-official.github.io/rest-api/?javascript#get-balances
        $this->load_markets();
        $request = array(
            'timestamp' => $this->milliseconds (),
        );
        $response = $this->privatePostExchangeV1UsersBalances (array_merge($request, $params));
        $result = array( 'info' => $response );
        for ($i = 0; $i < count($response); $i++) {
            $balance = $response[$i];
            $currencyId = $this->safe_string($balance, 'currency');
            $code = $this->safe_currency_code($currencyId);
            if (!(is_array($result) && array_key_exists($code, $result))) {
                $account = $this->account ();
                $account['free'] = $this->safe_float($balance, 'balance');
                $account['used'] = $this->safe_float($balance, 'locked_balance');
                $account['total'] = $this->sum ($account['free'], $account['used']);
                $result[$code] = $account;
            }
        }
        return $this->parse_balance($result);
    }

    public function fetch_order ($id, $symbol = null, $params = array ()) {
        // https://coindcx-official.github.io/rest-api/?javascript#account-trade-history
        $this->load_markets();
        $request = array(
            'id' => $id,
        );
        $response = $this->privatePostExchangeV1OrdersStatus (array_merge($request, $params));
        return $this->parse_order($response);
    }

    public function fetch_open_orders ($symbol = null, $since = null, $limit = null, $params = array ()) {
        $this->load_markets();
        $market = $this->market ($symbol);
        $request = array(
            'market' => $this->safe_value($market, 'id'),
            'timestamp' => $this->milliseconds (),
        );
        $response = $this->privatePostExchangeV1OrdersActiveOrders (array_merge($request, $params));
        $orders = $this->safe_value($response, 'orders', array());
        return $this->parse_orders($orders, $market, $since, $limit);
    }

    public function create_order ($symbol, $type, $side, $amount, $price = null, $params = array ()) {
        // https://coindcx-official.github.io/rest-api/?javascript#new-order
        $this->load_markets();
        $market = $this->market ($symbol);
        $marketInfo = $this->safe_value($market, 'info');
        $orderType = 'limit_order';
        if ($type === 'market') {
            $orderType = 'market_order';
        }
        $request = array(
            'market' => $this->safe_value($marketInfo, 'symbol'),
            'total_quantity' => $amount,
            'side' => $side,
            'order_type' => $orderType,
            'timestamp' => $this->milliseconds (),
        );
        if ($orderType === 'limit_order') {
            $request['price_per_unit'] = $price;
        }
        $response = $this->privatePostExchangeV1OrdersCreate (array_merge($request, $params));
        $orders = $this->safe_value($response, 'orders', array());
        return $this->parse_order($orders[0], $market);
    }

    public function cancel_order ($id, $symbol = null, $params = array ()) {
        $this->load_markets();
        $request = array(
            'id' => $id,
            'timestamp' => $this->milliseconds (),
        );
        return $this->privatePostExchangeV1OrdersCancel (array_merge($request, $params));
    }

    public function cancel_all_orders ($symbol = null, $params = array ()) {
        $this->load_markets();
        $market = $this->market ($symbol);
        $request = array(
            'market' => $this->safe_value($market, 'id'),
            'timestamp' => $this->milliseconds (),
        );
        return $this->privatePostExchangeV1OrdersCancelAll (array_merge($request, $params));
    }

    public function parse_order_status ($status) {
        $statuses = array(
            'init' => 'open',
            'open' => 'open',
            'partially_filled' => 'open',
            'filled' => 'closed',
            'rejected' => 'rejected',
            'canceled' => 'canceled',
            'partially_cancelled' => 'canceled',
        );
        return $this->safe_string($statuses, $status, $status);
    }

    public function parse_order ($order, $market = null) {
        $id = $this->safe_string($order, 'id');
        $timestamp = $this->parse_date($this->safe_string($order, 'created_at'));
        if ($timestamp === null) {
            $timestamp = $this->safe_integer($order, 'created_at');
        }
        $lastTradeTimestamp = $this->parse_date($this->safe_string($order, 'updated_at'));
        if ($lastTradeTimestamp === null) {
            $lastTradeTimestamp = $this->safe_integer($order, 'updated_at');
        }
        $orderStatus = $this->safe_string($order, 'status');
        $status = $this->parse_order_status($orderStatus);
        $marketId = $this->safe_string($market, 'symbol');
        if ($market === null) {
            $market = $this->safe_value($this->markets_by_id, $marketId);
        }
        $symbol = null;
        $quoteSymbol = null;
        $fee = null;
        if ($market !== null) {
            $symbol = $this->safe_string($market, 'symbol');
            $quoteSymbol = $this->safe_string($market, 'quote');
            if ($quoteSymbol !== null) {
                $fee = array(
                    'currency' => $quoteSymbol,
                    'rate' => $this->safe_float($order, 'fee'),
                    'cost' => $this->safe_float($order, 'fee_amount'),
                );
            }
        }
        $type = $this->safe_string($order, 'order_type');
        if ($type === 'market_order') {
            $type = 'market';
        } else if ($type === 'limit_order') {
            $type = 'limit';
        }
        return array(
            'id' => $id,
            'datetime' => $this->iso8601 ($timestamp),
            'timestamp' => $timestamp,
            'lastTradeTimestamp' => $lastTradeTimestamp,
            'status' => $status,
            'symbol' => $symbol,
            'type' => $type,
            'side' => $this->safe_string($order, 'side'),
            'price' => $this->safe_float_2($order, 'price', 'price_per_unit'),
            'amount' => $this->safe_float($order, 'total_quantity'),
            'filled' => null,
            'remaining' => null,
            'cost' => null,
            'trades' => null,
            'fee' => $fee,
            'info' => $order,
        );
    }

    public function get_pair_from_info ($market) {
        $marketInfo = $this->safe_value($market, 'info');
        $coindcxPair = $this->safe_string($marketInfo, 'pair');
        if ($coindcxPair === null) {
            throw new ExchangeError($this->id . ' has no pair (look at $market\'s info) value for ' . $market['symbol']);
        }
        return $coindcxPair;
    }

    public function sign ($path, $api = 'public', $method = 'GET', $params = array (), $headers = null, $body = null) {
        $base = $this->urls['api'][$api];
        $request = '/' . $this->implode_params($path, $params);
        $url = $base . $request;
        $query = $this->omit ($params, $this->extract_params($path));
        if ($method === 'GET') {
            if ($query) {
                $suffix = '?' . $this->urlencode ($query);
                $url .= $suffix;
            }
        }
        if ($api === 'private') {
            $this->check_required_credentials();
            $body = $this->json ($query);
            $signature = $this->hmac ($this->encode ($body), $this->encode ($this->secret));
            $headers = array(
                'X-AUTH-APIKEY' => $this->apiKey,
                'X-AUTH-SIGNATURE' => $signature,
            );
        }
        return array( 'url' => $url, 'method' => $method, 'body' => $body, 'headers' => $headers );
    }

    public function handle_errors ($code, $reason, $url, $method, $headers, $body, $response, $requestHeaders, $requestBody) {
        if (!$response) {
            return;
        }
        if ($code >= 400) {
            $feedback = $this->id . ' ' . $body;
            $message = $this->safe_string($response, 'message');
            if ($message !== null) {
                $this->throw_exactly_matched_exception($this->exceptions, $message, $feedback);
            }
            $this->throw_exactly_matched_exception($this->httpExceptions, (string) $code, $feedback);
            throw new ExchangeError($feedback); // unknown $message
        }
    }
}