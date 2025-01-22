from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('contas.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/pesquisa')
def pesquisa():
    return render_template('pesquisa.html')

@app.route('/pesquisa', methods=['POST'])
def pesquisar():
    chack = request.form['conta']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM contas WHERE codigo = ?', (chack,))
    conta = cursor.fetchone()
    conn.close()
    
    if conta:
        resultado = {
            'codigo': conta['codigo'],
            'nome': conta['nome'],
            'telefone': conta['telefone'],
            'saldo': conta['saldo'],
        }
    else:
        resultado = "codigo não encontrado"
    
    return render_template('pesquisa.html', resultado=resultado)

if __name__ == '__main__':
    app.run(debug=True)