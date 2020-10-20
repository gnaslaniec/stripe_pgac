import psycopg2

class OperacoesBD(object):
    
    # Conexão com o banco de dados RDS
    def conexao_bd_rds(conf):
        con = psycopg2.connect(
            database=conf['db_rds']['database'],
            user=conf['db_rds']['user'],
            password=conf['db_rds']['password'],
            host=conf['db_rds']['host'],
            port=conf['db_rds']['port']
        )
        cur = con.cursor()
        return con, cur

    def atualiza_saldo(connection,cursor,valor,id_usuario):
        # Captura o saldo atual do usuário
        cursor.execute("""select saldo_centavos from usuario where id = %s""", (id_usuario,))
        saldo = cursor.fetchone()
        # Soma o saldo atual do usuário com o valor que foi comprado
        saldo_centavos = saldo[0] + int(valor)
        # Formata e salva o valor em reais
        saldo_real = float(saldo_centavos) / 100
        # Atualiza o saldo no banco
        cursor.execute("""update usuario set saldo_centavos = %s where id = %s""", (saldo_centavos,id_usuario))
        cursor.execute("""update usuario set saldo = %s where id = %s""", (saldo_real,id_usuario))
        connection.commit()

    def retorna_saldo_usuario_reais(cursor, id_usuario):
        cursor.execute("""select round(saldo,2) from usuario where id = %s""", (id_usuario,))
        saldo = cursor.fetchone()
        if saldo != None:
            return saldo[0]
        else:
            return False