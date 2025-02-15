from flask import Flask, request, render_template
import sqlite3
import re

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('contas.db')
    conn.row_factory = sqlite3.Row
    return conn

def gerar_numero_sequencial():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT MAX(codigo) FROM contas')
    max_codigo = cursor.fetchone()[0]
    conn.close()
    if max_codigo is None:
        return "000001"
    else:
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
        numero_gerado = gerar_numero_sequencial()
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT 1 FROM contas WHERE codigo = ?', (numero_gerado,))
        if cursor.fetchone() is None:
            break
        conn.close()
    
    cursor.execute('INSERT INTO contas (codigo, nome, telefone, saldo) VALUES (?, ?, ?, ?)', (numero_gerado, nome, telefone, saldo))
    conn.commit()
    conn.close()
    
    mensagem = f"Cadastro feito com sucesso! Número da conta: {numero_gerado}. Guarde bem esse número para que você possa usar bem a sua conta no nosso banco."
    return render_template('cadastro.html', mensagem=mensagem)

if __name__ == '__main__':
    app.run(debug=True)