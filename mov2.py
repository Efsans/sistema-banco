from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__)

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

    cursor.execute('SELECT * FROM contas WHERE codigo = ?', (codigo1,))
    conta1 = cursor.fetchone()

    cursor.execute('SELECT * FROM contas WHERE codigo = ?', (codigo2,))
    conta2 = cursor.fetchone()

    if not conta1:
        resultado = "Conta de origem não encontrada."
        conn.close()
        return render_template('transfer.html', resultado=resultado)
    elif not conta2:
        resultado = "Conta de destino não encontrada."
        conn.close()
        return render_template('transfer.html', resultado=resultado)

    saldo_origem = conta1['saldo']
    saldo_destino = conta2['saldo']

    if valor == 0:
        resultado = "Valor nulo, transação cancelada."
        return render_template('transfer.html', resultado=resultado)
    elif valor > saldo_origem:
        resultado = "Saldo insuficiente."
        return render_template('transfer.html', resultado=resultado)
    elif valor < 0:
        resultado = "Coloque um valor válido."
        return render_template('transfer.html', resultado=resultado)
    elif valor < 10.00:
        resultado = "Valor mínimo para transação é 10,00."
        return render_template('transfer.html', resultado=resultado)
    else:
        saldo_origem -= valor
        saldo_destino += valor

        cursor.execute('UPDATE contas SET saldo = ? WHERE codigo = ?', (saldo_origem, codigo1))
        cursor.execute('UPDATE contas SET saldo = ? WHERE codigo = ?', (saldo_destino, codigo2))
        conn.commit()
        conn.close()

        resultado = f"Transação de {valor:.2f} realizada com sucesso! Novo saldo na conta de origem ({conta1['nome']}): {saldo_origem:.2f}. Novo saldo na conta de destino ({conta2['nome']}): {saldo_destino:.2f}"
        return render_template('transfer.html', resultado=resultado)

if __name__ == '__main__':
    app.run(debug=True)