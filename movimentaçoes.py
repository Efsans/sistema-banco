from flask import Flask, request, render_template # type: ignore
import sqlite3
import os

app=Flask(__name__)

@app.route('/transferir')
def transf():
    return render_template('transfer.html')

@app.route('/transferir', methods=['POST'])
def deposito():
    conn = sqlite3.connect('contas.db')
    cursor=conn.cursor()

    codigo1 = request.form['codigo1']
    codigo2 = request.form['codigo2']

    if not os.path.exists('contas.db'):
        resultado= "Arquivo não encontrado."
        return render_template('transfer.html', resultado=resultado)

    
    cursor.execute('SELECT * FROM  contas WHERE codigo = ?', (codigo1))
    cont1 = cursor.fetchone()
    

    
    cursor.execute('SELECT * FROM  contas WHERE codigo = ?', (codigo2))
    cont2 = cursor.fetchone()
    
    
    if not cont1:
        resultado="Conta de origem não encontrada."
        conn.close()
        return render_template('transfer.html', resultado=resultado)

    if not cont2:
        resultado="Conta de destino não encontrada."
        conn.close()
        return render_template('transfer.html', resultado=resultado)

    saldo_origem = cont1[3]
    saldo_destino = cont2[3]
    while True:
        mensagem=f"Saldo na conta de origem {cont1[1]}: {saldo_origem:.2f}"
        mensagem2= (f"Valor a ser transferido para {cont2[1]}: ").replace(',', '.')
        return render_template('transfer.html', mensagem=mensagem, mensagem2=mensagem2)
        
        transacao = request.form('valor')

        
        if transacao == 0:
            print("valor nulo trasação cancelada ")
            continue
        elif transacao > saldo_origem:
            print("Saldo insuficiente")
            continue
        elif transacao < 0:
            print("coloque um valor valido")
            continue
        elif transacao < 10.00:
            print("Valor mínimo para transação é 10,00")
            
          

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
    app.run(debug=True)