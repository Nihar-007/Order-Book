from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

def get_binance_order_book(coin_id):
    url = f"https://www.binance.com/api/v3/depth?symbol={coin_id}USDT&limit=1000"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        return {}

@app.route('/', methods=['GET', 'POST'])
def order_book():
    coin_id = None
    bids = []
    asks = []

    if request.method == 'POST':
        coin_id = request.form.get('coin_id')
        coin_id = coin_id.upper()

        if coin_id:
            data = get_binance_order_book(coin_id)
            
            if data:
                bids_data = data.get('bids', [])
                asks_data = data.get('asks', [])
                
                for bid in bids_data:
                    price = float(bid[0])
                    volume = float(bid[1])
                    total = price * volume  
                    bids.append({
                        'volume': volume,
                        'price': price,
                        'total': total
                    })

                for ask in asks_data:
                    price = float(ask[0])
                    volume = float(ask[1])
                    total = price * volume  
                    asks.append({
                        'volume': volume,
                        'price': price,
                        'total': total
                    })

                # for i in asks:
                #     print(i['price'])
                # print(asks)
    return render_template('index.html', coin_id=coin_id, bids=bids, asks=asks)

@app.route('/update/<coin_id>')
def order_book_polling(coin_id):
    data = get_binance_order_book(coin_id.upper())
    bids = []
    asks = []

    if data:
        bids_data = data.get('bids', [])
        asks_data = data.get('asks', [])
        
        for bid in bids_data:
            price = float(bid[0])
            volume = float(bid[1])
            total = price * volume
            bids.append({
                'volume': volume,
                'price': price,
                'total': total
            })

        for ask in asks_data:
            price = float(ask[0])
            volume = float(ask[1])
            total = price * volume
            asks.append({
                'volume': volume,
                'price': price,
                'total': total
            })

    return jsonify({'bids': bids, 'asks': asks})


if __name__ == '__main__':
    app.run(debug=True)