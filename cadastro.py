from flask import Flask, request, render_template
import os
import re

app = Flask(__name__)

def gerar_numero_sequencial(arquivo="contas"):
    if not os.path.exists(arquivo):
        with open(arquivo, "w") as f:
            pass
    with open("contas", "r") as l:
        linhas = l.readlines()
        if not linhas:
            return "000001"
        ultima_linha = linhas[-1].strip()
        numeroF = int(ultima_linha.split("\t")[0])
        numeroF += 1
        numero = f"{numeroF:06d}"
        return numero
        

@app.route('/')
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
    
    numero_gerado = gerar_numero_sequencial()
    
    with open("contas", "a") as arquiv:
        linha = "%s\t%s\t%s\t%d" % (numero_gerado, nome, telefone, saldo)
        arquiv.write(f"{linha}\n")
    
    mensagem = f"Cadastro feito com sucesso! Número da conta: {numero_gerado}. por falta de tempo e conhecimento, não foi possível implementar a funcionalidade de login. Guarde bem esse número para que voce possa usar bem a sua conta no nosso alegre Banco :) XD :V"
    return render_template('cadastro.html', mensagem=mensagem)

if __name__ == '__main__':
    app.run(debug=True)