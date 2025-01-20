import html
from flask import Flask, request, render_template_string
import os

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


pag = '''
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>Cadastro de Conta</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        .container {
            width: 300px;
            margin: 50px auto;
            padding: 20px;
            background-image: linear-gradient(50deg, rgb(255, 247, 247), rgb(255, 255, 255));
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.8);
            text-align: center;
        }
        body {
            font-family: Arial, sans-serif;
            background-image: linear-gradient(10deg, rgb(255, 255, 255), rgb(241, 233, 233));
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            height: 100vh;
         }
         h2 {
            margin-bottom: 20px;
            color: rgb(0, 0, 0);
        }
        input {
            width: 100%;
            padding: 8px;
            margin-bottom: 20px;
            border: 1px solid #ccc;
            border-radius: 5px;
        }
        button {
            background-color: #ac0606;
            color: rgb(237, 212, 212);
            padding: 10px 20px;
            border-color: white; 
            border-radius: 10px;
            cursor: pointer;
        }
        button:hover {
            background-color: #000000;
        }
        .mensagem {
            margin-top: 20px;
            padding: 10px;
            background-color: #d4edda;
            border: 1px solid #c3e6cb;
            border-radius: 5px;
            color: #155724;
            text-align: center;
        }
    </style>
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery.mask/1.14.16/jquery.mask.min.js"></script>
    <script>
        $(document).ready(function(){
            $('#deposito').mask('#.##0,00', {reverse: true});
            $('#tele').mask('(00) 00000-0000');
        });
    </script>
</head>
<body>
    <div class="container">
        <h2><b>Cadastro de Conta</b></h2>
        {% if mensagem %}
        <div class="mensagem">
            <p>{{ mensagem|safe }}</p>
        </div>
        {% endif %}
        <form action="/cadastrar" method="post">
            <label for="name">Nome Completo:<b>*</b></label>
            <input type="text" id="name" name="name" required placeholder="nome completo"><br>
            <label for="tele">Número de Telefone:<b>*</b></label>
            <input type="tel" min="0" id="tele" name="tele" required placeholder="(xx) xxxxx-xxxx"><br>
            <label for="deposito">Valor inicial de deposito:</label>
            <input type="text" id="deposito" name="deposito" placeholder="digite o valor do deposito" step="0.01" min="0.0"><br>
            <button type="submit">Cadastrar</button>
        </form>
    </div>
</body>
</html>
'''


@app.route('/')
def cadastro():
    return render_template_string(pag)

@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    nome = request.form['name']
    telefone = request.form['tele']
    telefone=int(telefone.replace(")", "").replace("-", "").replace("(", "").replace(" ", ""))
    saldo = request.form['deposito']
    if not saldo:
        saldo = '000'
    else:
        saldo = saldo.replace(".", "").replace(",", "")
        saldo = int(saldo)    


    
    numero_gerado = gerar_numero_sequencial()
    
    with open("contas", "a") as arquiv:
        line = "%s\t%s\t%d\t%d" % (numero_gerado, nome, telefone, saldo)
        arquiv.write(f"{line}\n")
    
    mensagem = f"Cadastro feito com sucesso! Número da conta: {numero_gerado}. Guarde bem esse número :)"
    return render_template_string(pag, mensagem=mensagem)

if __name__ == '__main__':
    app.run(debug=True)