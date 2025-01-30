from flask import Flask, request, render_template
import sqlite3
import re

app = Flask(__name__)

def get():
    conn = sqlite3.connect('contas.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def menu():
    return render_template('menu.html')

@app.route('/pesquisa')
def pesquisa():
    return render_template('pesquisa.html')

@app.route('/pesquisa', methods=['POST'])
def pesquisar():
    chack = request.form['conta']
    conn = get()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM contas WHERE codigo = ?', (chack,))
    conta = cursor.fetchone()
    conn.close()
    
    if conta:
        resultado = {
            'codigo': conta['codigo'],
            'nome': conta['nome'],
            'telefone': conta['telefone'],
            'saldo': f"{conta['saldo'] / 100:.2f}".replace('.', ','),
        }
    else:
        resultado = "codigo não encontrado"
    
    return render_template('pesquisa.html', resultado=resultado)

def gerar_numero_sequencial():
    conn = get()
    cursor = conn.cursor()
    cursor.execute('SELECT MAX(codigo) FROM contas')
    max_codigo = cursor.fetchone()[0]
    conn.close()
    if max_codigo is None:
        return str('000001')
    else:
        max_codigo = int(max_codigo)
        return f"{int(max_codigo) + 1:06d}"

@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    nome = request.form['name']
    telefone = request.form['tele']
    telefone = re.sub(r'\D', '', telefone)
    saldo = request.form['deposito']
    if not saldo:
        saldo = '000'
    else:
        saldo = saldo.replace(',', '').replace('.', '')
        saldo = int(saldo)
    
    while True:
        numero_gerado = str(gerar_numero_sequencial())
        conn = get()
        cursor = conn.cursor()
        cursor.execute('SELECT 1 FROM contas WHERE codigo = ?', (numero_gerado,))
        if cursor.fetchone() is None:
            break
        conn.close()
    
    cursor.execute('INSERT INTO contas (codigo, nome, telefone, saldo) VALUES (?, ?, ?, ?)', (numero_gerado, nome, telefone, saldo))
    conn.commit()
    conn.close()
    
    mensagem = f"Cadastro feito com sucesso! Número da conta: {numero_gerado}." #Guarde bem esse número pois por falta de conhecimento e tempo não foi emplementado sistema de login, então para que você possa usar bem a sua conta no nosso banco anote o numero. :) XD :v"
    return render_template('cadastro.html', mensagem=mensagem)

@app.route("/mov")
def menu_mov():
    return render_template('menu_mov.html')

@app.route('/transferir')
def transf():
    return render_template('transfer.html')

@app.route('/transferir', methods=['POST'])
def transferir():
    conn = get()
    cursor = conn.cursor()

    codigo1 = request.form['codigo1']
    codigo2 = request.form['codigo2']
    valor = request.form['valor']
    valor = valor.replace('.', '').replace(',', '.')
    valor = float(valor) * 100  # Convertendo para centavos

    cursor.execute('SELECT * FROM contas WHERE codigo = ?', (codigo1,))
    cont1 = cursor.fetchone()

    cursor.execute('SELECT * FROM contas WHERE codigo = ?', (codigo2,))
    cont2 = cursor.fetchone()

    if not cont1:
        resultado = "Conta de origem não encontrada."
        conn.close()
        return render_template('transfer.html', resultado=resultado)
    elif not cont2:
        resultado = "Conta de destino não encontrada."
        conn.close()
        return render_template('transfer.html', resultado=resultado)

    saldo_origem = cont1['saldo']
    saldo_destino = cont2['saldo']

    if valor == 0:
        resultado = "Valor nulo, transação cancelada."
        return render_template('transfer.html', resultado=resultado)
    elif valor > saldo_origem:
        resultado = "Saldo insuficiente."
        return render_template('transfer.html', resultado=resultado)
    elif valor < 0:
        resultado = "Coloque um valor válido."
        return render_template('transfer.html', resultado=resultado)
    elif valor < 1000: 
        resultado = "Valor mínimo para transação é 10,00."
        return render_template('transfer.html', resultado=resultado)
    else:
        saldo_origem -= valor
        saldo_destino += valor

        cursor.execute('UPDATE contas SET saldo = ? WHERE codigo = ?', (saldo_origem, codigo1))
        cursor.execute('UPDATE contas SET saldo = ? WHERE codigo = ?', (saldo_destino, codigo2))
        conn.commit()
        conn.close()

        resultado = f"Transação de {valor / 100:.2f} realizada com sucesso! Novo saldo na conta de origem ({cont1['nome']}): {saldo_origem / 100:.2f}. Novo saldo na conta de destino ({cont2['nome']}): {saldo_destino / 100:.2f}"
        return render_template('transfer.html', resultado=resultado)
    

@app.route('/deposito')
def depositar():
    return render_template('depositar.html')

@app.route('/deposito', methods=['POST'])
def realizar_deposito():
    conn = get()
    cursor = conn.cursor()

    conta = request.form['conta']
    valor = request.form['valor']
    valor = valor.replace('.', '').replace(',', '.')
    valor = float(valor) * 100  

    cursor.execute('SELECT * FROM contas WHERE codigo = ?', (conta,))
    cont = cursor.fetchone()

    if not cont:
        mensagem = "Conta não encontrada."
        conn.close()
        return render_template('depositar.html', mensagem=mensagem)

    saldo = cont['saldo']
    saldo += valor

    cursor.execute('UPDATE contas SET saldo = ? WHERE codigo = ?', (saldo, conta))
    conn.commit()
    conn.close()

    mensagem = f"Depósito de {valor / 100:.2f} realizado com sucesso! Novo saldo: {saldo / 100:.2f}"
    return render_template('depositar.html', mensagem=mensagem)

@app.route('/sacar')
def sacar():
    return render_template('sacar.html')

@app.route('/sacar', methods=['POST'])
def realizar_saque():
    conn = get()
    cursor = conn.cursor()

    conta = request.form['conta']
    valor = request.form['valor']
    valor = valor.replace('.', '').replace(',', '.')
    valor = float(valor) * 100  # Convertendo para centavos

    cursor.execute('SELECT * FROM contas WHERE codigo = ?', (conta,))
    cont = cursor.fetchone()

    if not cont:
        mensagem = "Conta não encontrada."
        conn.close()
        return render_template('sacar.html', mensagem=mensagem)

    saldo = cont['saldo']
    saldo -= valor

    cursor.execute('UPDATE contas SET saldo = ? WHERE codigo = ?', (saldo, conta))
    conn.commit()
    conn.close()

    mensagem = f"Saque de {valor / 100:.2f} realizado com sucesso! Novo saldo: {saldo / 100:.2f}"
    return render_template('sacar.html', mensagem=mensagem)

if __name__ == '__main__':
    app.run(debug=True)