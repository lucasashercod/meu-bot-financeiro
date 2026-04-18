import time
import requests

def enviar_telegram(mensagem):
    token = "8782584663:AAFfCuBzf_YwDP4_Lmfut9HOyBmUq_NKIQA"
    chat_id = "5194672860"

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    requests.post(url, data={"chat_id": chat_id, "text": mensagem})

def monitorar():
    alvo_btc = 80000
    alvo_dolar = 6

    while True:
        try:
            btc = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT").json()
            preco_btc = float(btc["price"])

            dolar = requests.get("https://economia.awesomeapi.com.br/json/last/USD-BRL").json()
            preco_dolar = float(dolar["USDBRL"]["bid"])

            print(f"BTC: {preco_btc} | Dólar: {preco_dolar}")

            if preco_btc >= alvo_btc:
                enviar_telegram(f"🚨 BTC bateu {preco_btc}")

            if preco_dolar >= alvo_dolar:
                enviar_telegram(f"🚨 Dólar bateu {preco_dolar}")

            time.sleep(10)

        except:
            time.sleep(10)

monitorar()