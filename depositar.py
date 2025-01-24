import sqlite3
import os

def depositar():

  conn = sqlite3.connect('contas.db')
  cursor=conn.cursor()

  conta = input("numero da conta: ")

  if not os.path.exists('contas.db'):
        print("Arquivo não encontrado.")
        return
  cursor.execute("SELECT * FROM contas WHERE codigo =?", (conta))
  cont = cursor.fetchone()

  if not cont:
        print("Conta de origem não encontrada.")
        conn.close()
        return

  saldo = cont[3]

  print(f"saldo atual {cont[3]}")
  deposito=int(input(f"valor para depositar para {cont[1]}:  "))
  

  saldo += deposito

  cursor.execute('UPDATE contas SET saldo= ? WHERE codigo = ?', (saldo, conta))
  conn.commit()
  conn.close()


  print(f"valor atual {saldo}")
  return 


if __name__ == "__main__":
  depositar()