import mysql
import mysql.connector
import pandas as pd

def conexao(query):
    conn = mysql.connector.connect(
    host= "127.0.0.1",
    port= "3306",
    user= "root",
    password= "senai@134",
    db= "bd_carro"
    )

    dataframe = pd.read_sql(query, conn)

    #executa a consulta sql e armazena o resulta em um dataframe

    conn.close()

    return dataframe