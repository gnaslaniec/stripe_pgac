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
        cursor.execute("""select saldo from usuario where id = %s""", (id_usuario,))
        saldo = cursor.fetchone()
        # Soma o saldo atual do usuário com o valor que foi comprado
        saldo_atualizado = saldo[0] + valor
        cursor.execute("""update usuario set saldo = %s where id = %s""", (saldo_atualizado,id_usuario))
        connection.commit()