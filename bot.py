import time
import requests

print("BOT INICIANDO...")

def enviar_telegram(mensagem):
    token = "8436584198:AAGOmBcFjoPlZW_h9A3VBAhghFTu5sO-Yyw"
    chat_id = "5194672860"

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    requests.post(url, data={"chat_id": chat_id, "text": mensagem})

def monitorar():
    alvo_btc = 80000
    alvo_dolar = 6

    btc_alertado = False
    dolar_alertado = False

    while True:
        try:
            print("RODANDO...")

            btc = requests.get(
                "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT",
                timeout=5
            ).json()

            if "price" in btc:
             preco_btc = float(btc["price"])
            else:
             print("Erro ao pegar preço BTC:", btc)
            time.sleep(10)
            continue

            dolar = requests.get(
                "https://economia.awesomeapi.com.br/json/last/USD-BRL",
                timeout=5
            ).json()

            if "USDBRL" in dolar and "bid" in dolar["USDBRL"]:
             preco_dolar = float(dolar["USDBRL"]["bid"])
            else:
             print("Erro ao pegar preço do dólar:", dolar)
            time.sleep(10)
            continue
            print(f"BTC: {preco_btc} | Dólar: {preco_dolar}")

            if preco_btc >= alvo_btc and not btc_alertado:
                enviar_telegram(f"🚨 BTC bateu {preco_btc}")
                btc_alertado = True

            if preco_dolar >= alvo_dolar and not dolar_alertado:
                enviar_telegram(f"🚨 Dólar bateu {preco_dolar}")
                dolar_alertado = True

            time.sleep(15)

        except Exception as e:
            print(f"Erro: {e}")
            time.sleep(10)

monitorar()