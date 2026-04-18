import time
import requests
import os

print("BOT INICIANDO...")

def enviar_telegram(mensagem):
    token = os.getenv("8436584198:AAGOmBcFjoPlZW_h9A3VBAhghFTu5sO-Yyw")
    chat_id = os.getenv("5194672860")

    if not token or not chat_id:
        print("Erro: TOKEN ou CHAT_ID não definidos")
        return

    url = f"https://api.telegram.org/bot{token}/sendMessage"

    try:
        requests.post(url, data={
            "chat_id": chat_id,
            "text": mensagem
        }, timeout=5)
    except Exception as e:
        print("Erro ao enviar Telegram:", e)


def pegar_preco_btc():
    # 🔹 Tenta CoinGecko primeiro
    try:
        btc = requests.get(
            "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd",
            timeout=5
        ).json()

        if "status" in btc and btc["status"].get("error_code") == 429:
            print("⚠️ Rate limit CoinGecko, tentando Binance...")
            raise Exception("Rate limit")

        if "bitcoin" in btc and "usd" in btc["bitcoin"]:
            return btc["bitcoin"]["usd"]

    except:
        pass

    # 🔹 Fallback: Binance
    try:
        btc = requests.get(
            "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT",
            timeout=5
        ).json()

        if "price" in btc:
            return float(btc["price"])
        else:
            print("Erro Binance:", btc)

    except Exception as e:
        print("Erro geral BTC:", e)

    return None


def pegar_preco_dolar():
    try:
        dolar = requests.get(
            "https://open.er-api.com/v6/latest/USD",
            timeout=5
        ).json()

        if "rates" in dolar and "BRL" in dolar["rates"]:
            return float(dolar["rates"]["BRL"])
        else:
            print("Erro Dólar:", dolar)

    except Exception as e:
        print("Erro ao pegar dólar:", e)

    return None


def monitorar():
    alvo_btc = 80000
    alvo_dolar = 6

    btc_alertado = False
    dolar_alertado = False

    while True:
        try:
            print("RODANDO...")

            preco_btc = pegar_preco_btc()
            preco_dolar = pegar_preco_dolar()

            if preco_btc is None or preco_dolar is None:
                print("Erro ao obter preços, tentando novamente...")
                time.sleep(60)
                continue

            print(f"BTC: {preco_btc} | Dólar: {preco_dolar}")

            # 🔔 Alertas
            if preco_btc >= alvo_btc and not btc_alertado:
                enviar_telegram(f"🚨 BTC bateu {preco_btc}")
                btc_alertado = True

            if preco_dolar >= alvo_dolar and not dolar_alertado:
                enviar_telegram(f"🚨 Dólar bateu {preco_dolar}")
                dolar_alertado = True

            time.sleep(60)  

        except Exception as e:
            print("Erro geral:", e)
            time.sleep(60)


monitorar()