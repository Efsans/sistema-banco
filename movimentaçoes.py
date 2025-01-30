from flask import Flask, request, render_template # type: ignore
import sqlite3
import os

app=Flask(__name__)

def get():
    conn = sqlite3.connect('contas.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/transferir')
def transf():
    return render_template('transfer.html')

@app.route('/transferir', methods=['POST'])
def deposito():
    
    conn = get()
    cursor = conn.cursor()

    codigo1 = request.form['codigo1']
    codigo2 = request.form['codigo2']
    valor = float(request.form['valor'].replace(',', '.'))

    
    cursor.execute('SELECT * FROM  contas WHERE codigo = ?', (codigo1))
    cont1 = cursor.fetchone()
    

    
    cursor.execute('SELECT * FROM  contas WHERE codigo = ?', (codigo2))
    cont2 = cursor.fetchone()
    
    
    if not cont1:
        resultado="Conta de origem não encontrada."
        conn.close()
        return render_template('transfer.html', resultado=resultado)

    elif not cont2:
        resultado="Conta de destino não encontrada."
        conn.close()
        return render_template('transfer.html', resultado=resultado)

    saldo_origem = cont1[3]
    saldo_destino = cont2[3]
        #mensagem=f"Saldo na conta de origem {cont1[1]}: {saldo_origem:.2f}"
        #mensagem2= (f"Valor a ser transferido para {cont2[1]}: ").replace(',', '.')
        #return render_template('transfer.html', mensagem=mensagem, mensagem2=mensagem2)

        
    if valor == 0:
        resultado = "valor nulo trasação cancelada "
        return render_template('transfer.html', resultado=resultado)
    elif valor > saldo_origem:
        resultado = "Saldo insuficiente"
        return render_template('transfer.html', resultado=resultado)
    elif valor < 0:
        resultado = "coloque um valor valido"
        return render_template('transfer.html', resultado=resultado)
    elif valor < 10.00:
        resultado = "Valor mínimo para transação é 10,00"
            
          

    else:
             
        saldo_origem -= valor
        saldo_destino += valor

    
        cursor.execute('UPDATE contas SET saldo = ? WHERE codigo = ?', (saldo_origem, codigo1))
        cursor.execute('UPDATE contas SET saldo = ? WHERE codigo = ?', (saldo_destino, codigo2))
        conn.commit()
        conn.close()

        resultado = f"Transação de {valor:.2f} realizada com sucesso! Novo saldo na conta {cont1['nome']}: {saldo_origem:.2f}. Novo saldo na conta de destino {cont2['nome']}: {saldo_destino:.2f}"
        return render_template('transfer.html', resultado=resultado)
    
    #print(f"Transação de {transacao:.2f} realizada com sucesso!")
    #print(f"Novo saldo na conta de origem {cont1[1]}: {saldo_origem:.2f}")
    #print(f"Novo saldo na conta de destino {cont2[1]}: {saldo_destino:.2f}")



if __name__ == "__main__":
    app.run(debug=True)