import datetime
import json
import requests
import time

transacoes = []
def salvar_dados():
    with open("dados.json", "w") as f:
        json.dump(transacoes, f, default=str)

def adicionar_transacao():
    tipo = input("Tipo (entrada/saida): ").lower()
    valor = float(input("Valor: "))
    descricao = input("Descrição: ")
    data = datetime.datetime.now()    

    transacoes.append({
        "tipo": tipo,
        "valor": valor,
        "descricao": descricao,
        "data": data
    })
    salvar_dados()
    print("Transação adicionada com sucesso!\n")

def ver_preco_bitcoin():
    url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
    
    try:
        resposta = requests.get(url)
        dados = resposta.json()
        
        preco = dados["price"]
        print(f"Preço do Bitcoin: $ {preco}")
    
    except:
        print("Erro ao buscar preço. Verifique sua conexão.")

def ver_resumo():
    entradas = sum(t["valor"] for t in transacoes if t["tipo"] == "entrada")
    saidas = sum(t["valor"] for t in transacoes if t["tipo"] == "saida")
    saldo = entradas - saidas

    print("\n===== RESUMO =====")
    print(f"Entradas: R$ {entradas:.2f}")
    print(f"Saídas: R$ {saidas:.2f}")
    print(f"Saldo: R$ {saldo:.2f}\n")

def alerta_bitcoin():
    alvo = float(input("Digite o preço alvo: "))

    print("Monitorando preço do Bitcoin... (Ctrl + C para parar)\n")

    while True:
        try:
            url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
            resposta = requests.get(url)
            dados = resposta.json()
            preco = float(dados["price"])

            print(f"Preço atual: $ {preco}")

            if preco >= alvo:
                mensagem = f"🚨 Bitcoin atingiu o preço alvo: $ {preco}"
                print(mensagem)
                enviar_telegram(mensagem)
                break

            time.sleep(5)  # espera 5 segundos antes de verificar de novo

        except:
            print("Erro ao buscar preço...")
            time.sleep(5)

            
def ver_preco_dolar():
    url = "https://economia.awesomeapi.com.br/json/last/USD-BRL"
    
    try:
        resposta = requests.get(url)
        dados = resposta.json()
        
        preco = dados["USDBRL"]["bid"]
        print(f"Preço do Dólar: R$ {preco}")
    
    except:
        print("Erro ao buscar preço do dólar.")   

def enviar_telegram(mensagem):
    token = "8436584198:AAGOmBcFjoPlZW_h9A3VBAhghFTu5sO-Yyw"
    chat_id = "5194672860"
    
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    
    requests.post(url, data={
        "chat_id": chat_id,
        "text": mensagem
    })         

def alerta_dolar():
    alvo = float(input("Digite o preço alvo do dólar: "))

    print("Monitorando dólar... (Ctrl + C para parar)\n")

    while True:
        try:
            url = "https://economia.awesomeapi.com.br/json/last/USD-BRL"
            resposta = requests.get(url)
            dados = resposta.json()

            preco = float(dados["USDBRL"]["bid"])

            print(f"Preço atual do dólar: R$ {preco}")

            if preco >= alvo:
                mensagem = f"🚨 Dólar atingiu o preço alvo: R$ {preco}"
                print(mensagem)
                enviar_telegram(mensagem)
                break

            time.sleep(5)

        except:
            print("Erro ao buscar preço do dólar...")
            time.sleep(5)

def menu():
    while True:
        print("1 - Adicionar transação")
        print("2 - Ver resumo")
        print("3 - Sair")
        print("4 - Ver preço do Bitcoin")
        print("5 - Alerta de preço Bitcoin")
        print("6 - Ver preço do Dólar")
        print("7 - Alerta de preço do Dólar")

        opcao = input("Escolha: ")

        if opcao == "1":
            adicionar_transacao()
        elif opcao == "2":
            ver_resumo()
        elif opcao == "3":
            break
        elif opcao == "4":
            ver_preco_bitcoin()
        elif opcao == "5":
            alerta_bitcoin()    
        elif opcao == "6":
            ver_preco_dolar()
        elif opcao == "7":
            alerta_dolar()
        else:
             print("Opção inválida\n")
             


menu()