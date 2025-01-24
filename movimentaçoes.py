from flask import Flask, request, render_template # type: ignore
import sqlite3
import os

app=Flask(__name__)

def deposito():
    conn = sqlite3.connect('contas.db')
    cursor=conn.cursor()

    codigo1 = input("Digite o código da sua conta: ")
    codigo2 = input("Digite o código da conta de destino: ")

    if not os.path.exists('contas.db'):
        print("Arquivo não encontrado.")
        return

    
    cursor.execute('SELECT * FROM  contas WHERE codigo = ?', (codigo1))
    cont1 = cursor.fetchone()
    

    
    cursor.execute('SELECT * FROM  contas WHERE codigo = ?', (codigo2))
    cont2 = cursor.fetchone()
    
    
    if not cont1:
        print("Conta de origem não encontrada.")
        conn.close()
        return

    if not cont2:
        print("Conta de destino não encontrada.")
        conn.close()
        return

    saldo_origem = cont1[3]
    saldo_destino = cont2[3]
    while True:
        print(f"Saldo na conta de origem {cont1[1]}: {saldo_origem:.2f}")
        transacao = float(input(f"Valor a ser transferido para {cont2[1]}: ").replace(',', '.'))

        if transacao < 10.00:
            print("Valor mínimo para transação é 10,00")
            continue
        elif transacao > saldo_origem:
            print("Saldo insuficiente")
            continue
        elif transacao < 0:
            print("coloque um valor valido")
            continue
        elif transacao == 0:
            print("valor nulo trasação cancelada ")
            break
          

        else:
            break     

    saldo_origem -= transacao
    saldo_destino += transacao

    
    cursor.execute('UPDATE contas SET saldo = ? WHERE codigo = ?', (saldo_origem, codigo1))
    conn.commit()
    cursor.execute('UPDATE contas SET saldo = ? WHERE codigo = ?', (saldo_destino, codigo2))
    conn.commit()

    conn.close()

    print(f"Transação de {transacao:.2f} realizada com sucesso!")
    print(f"Novo saldo na conta de origem {cont1[1]}: {saldo_origem:.2f}")
    print(f"Novo saldo na conta de destino {cont2[1]}: {saldo_destino:.2f}")



if __name__ == "__main__":
    deposito()