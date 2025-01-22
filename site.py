from flask import Flask, request, render_template
import os
import re
import sqlite3

app = Flask(__name__)

def get():
    banco = sqlite3.connect('contas.db')
    banco.row_factory = sqlite3.Row

    return banco

@app.route('/')
def menu():
    return render_template('menu.html')

@app.route('/pesquisa')
def pesquisa():
    return render_template('pesquisa.html')

@app.route('/pesquisa', methods=['POST'])
def pesquisar(arquivo="contas"):
    chack = request.form['conta']
    resultado = None
    if os.path.exists(arquivo):
        with open(arquivo, "r") as l:
            for lido in l:
                codigo = lido[:6]
                if codigo == chack:
                    dados = lido.strip().split('\t')
                    resultado = {
                        'codigo': dados[0],
                        'nome': dados[1],
                        'telefone': dados[2],
                        'saldo': dados[3] if len(dados) > 3 else '0,00',
                    }
                    break
            else:
                resultado = "codigo não encontrado"
    else:
        resultado = "arquivo não encontrado"
    return render_template('pesquisa.html', resultado=resultado)

def gerar_numero_sequencial():
    conn = get()
    cursor=conn.cursor()
    cursor.execute('SELECT MAX(codigo) FROM contas')
    cod = cursor.fetchone()[0]
    conn.close()
    if cod is None:
        return "000001"
    else:
        return f"{int(cod) + 1:06d}"

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
        conn = get()
        cursor = conn.cursor()
        cursor.execute('SELECT 1 FROM contas WHERE codigo = printf("%06d", ?)', (numero_gerado,))
        if cursor.fetchone() is None:
            break
        
    
    """ with open("contas", "a") as arquiv:
        linha = "%s\t%s\t%s\t%d" % (numero_gerado, nome, telefone, saldo)
        arquiv.write(f"{linha}\n") """
    
    
    
    cursor.execute('INSERT INTO contas (codigo, nome, telefone, saldo) VALUES (printf("%06d", ?), ?, ?, ?)', (numero_gerado, nome, telefone, saldo))
    conn.commit()
    conn.close()
    
    
    
    mensagem = f"Cadastro feito com sucesso! Número da conta: {numero_gerado}. Guarde bem esse número poi por falta de tempo e conhecimento, não foi possível implementar a funcionalidade de login. Por isso o numero é necessario para usar bem a sua conta no nosso banco :) XD :V"
    return render_template('cadastro.html', mensagem=mensagem)

if __name__ == '__main__':
    app.run(debug=True)