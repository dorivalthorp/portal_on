from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session
import requests
import psycopg2
import pandas
from datetime import datetime
import sys
sys.path.append("televendas")



def conecta_bd2():
    try:
        con2 = psycopg2.connect(
            user='a5solutions',
            password='@5s0lut10ns',
            host='18.230.44.138',
            port='5432',
            database='data_ims')
        return con2
    except psycopg2.Error as e:
        # Armazenar a URL da página original na sessão
        session['pagina_original'] = request.url
        return render_template('erro.html')


def conecta_bd():
    try:
        con = psycopg2.connect(
            user='postgres',
            password='gUnDiCITiOgy',
            host='172.172.0.25',
            port='5433',
            database='Televendas')
        return con
    except psycopg2.Error as e:
        # Armazenar a URL da página original na sessão
        session['pagina_original'] = request.url
        return render_template('erro.html')


def consulta_bd(sql):
    con = conecta_bd()
    cur = con.cursor()
    cur.execute(sql)
    temp = cur.fetchall()
    data = pandas.read_sql(sql, con)
    for i in range(0, len(temp)):
        temp[i] = tuple(temp[i])
    return data





televendas_bp = Blueprint("televendas", __name__, template_folder="templates", static_folder='static', static_url_path='/televendas/static')

@televendas_bp.route('/televendas')
def home_televendas():
    conn = conecta_bd()
    cursor = conn.cursor()

    cursor.execute(''' SELECT SUM(discados) AS soma_discados,
                    SUM(invalidos) AS soma_invalidos, 
                    CASE WHEN SUM(discados) > 0 THEN round((SUM(invalidos)/ SUM(discados) * 100), 0) ELSE 0 END AS soma_porcentagem_invalido
                    FROM public.originador_discagem''')
    
    rows = cursor.fetchall()

    if rows:
        soma_discados = rows[0][0]
        soma_porcentagem_invalido = rows[0][2]
        titulo = f'Painel Real Time Tahto - {soma_discados} / {soma_porcentagem_invalido}%'
    else:
        titulo = 'Painel Real Time Tahto - 0%'


    cursor.execute( ''' SELECT originador, qtd_consulta_total, qtd_bloqueio_total, ocupacao FROM public.liberacao_api order by qtd_consulta_total desc ''')
    rowsp = cursor.fetchall()


    
    return render_template("home.html", titulo=titulo, rowsp=rowsp, rows=rows)




@televendas_bp.route('/televendas/buscar', methods=['POST'])
def buscar_televendas():
    filtro = request.values.get('filtro').strip()
    conn = conecta_bd()
    cursor = conn.cursor()

    cursor.execute(''' SELECT SUM(discados) AS soma_discados,
                    SUM(invalidos) AS soma_invalidos, 
                    CASE WHEN SUM(discados) > 0 THEN round((SUM(invalidos)/ SUM(discados) * 100), 0) ELSE 0 END AS soma_porcentagem_invalido
                    FROM public.originador_discagem''')
    
    rows = cursor.fetchall()

    if rows:
        soma_discados = rows[0][0]
        soma_porcentagem_invalido = rows[0][2]
        titulo = f'Painel Real Time Tahto - {soma_discados} / {soma_porcentagem_invalido}%'
    else:
        titulo = 'Painel Real Time Tahto - 0%'


    if filtro == 'select':
        cursor.execute(f''' SELECT SUM(discados) AS soma_discados,
                    SUM(invalidos) AS soma_invalidos, 
                    CASE WHEN SUM(discados) > 0 THEN round((SUM(invalidos)/ SUM(discados) * 100), 0) ELSE 0 END AS soma_porcentagem_invalido
                    FROM public.originador_discagem where originador ilike '%{filtro}%' ''')
    
        rowsp = cursor.fetchall()

        if rowsp:
            soma_discados = rows[0][0]
            soma_porcentagem_invalido = rows[0][2]
            titulo = f'Painel Real Time Tahto - {soma_discados}K / {soma_porcentagem_invalido}%'
        else:
            titulo = 'Painel Real Time Tahto - 0%'
    
        return render_template("home.html", titulo=titulo, rows=rows, rowsp=rowsp)

    else:
        cursor.execute(f''' SELECT SUM(discados) AS soma_discados,
                    SUM(invalidos) AS soma_invalidos, 
                    CASE WHEN SUM(discados) > 0 THEN round((SUM(invalidos)/ SUM(discados) * 100), 0) ELSE 0 END AS soma_porcentagem_invalido
                    FROM public.originador_discagem  WHERE uf ilike '%{filtro}%' ''')
    
        rowsp = cursor.fetchall()

        if rowsp:
            soma_discados = rows[0][0]
            soma_porcentagem_invalido = rows[0][2]
            titulo = f'Painel Real Time Tahto - {soma_discados}K / {soma_porcentagem_invalido}%'
        else:
            titulo = 'Painel Real Time Tahto - 0%'

        return render_template("home.html", titulo=titulo, rows=rows, rowsp=rowsp)



##################################################################################
#                                PRIMEIRA CAUTELAR                               #
##################################################################################


@televendas_bp.route('/televendas/buscarpcautelar', methods=['GET','POST'])
def buscarpcautelar_televendas():
    pesquisa = request.form.get('pesquisa').strip() 
    conn = conecta_bd()
    cursor = conn.cursor()

    cursor.execute(''' SELECT SUM(discados) AS soma_discados,
                    SUM(invalidos) AS soma_invalidos, 
                    CASE WHEN SUM(discados) > 0 THEN round((SUM(invalidos)/ SUM(discados) * 100), 0) ELSE 0 END AS soma_porcentagem_invalido
                    FROM public.originador_discagem''')
    
    rows = cursor.fetchall()

    if rows:
        soma_discados = rows[0][0]
        soma_porcentagem_invalido = rows[0][2]
        titulo = f'Painel Real Time Tahto - {soma_discados} / {soma_porcentagem_invalido}%'
    else:
        titulo = 'Painel Real Time Tahto - 0%'


    cursor.execute(f'''SELECT originador, qtd_consulta_total, qtd_bloqueio_total, ocupacao  
                    FROM public.liberacao_api WHERE originador ILIKE '%{pesquisa}%' 
                    order by qtd_consulta_total desc ''')
    
    rowsp = cursor.fetchall()

    return render_template("home.html", titulo=titulo, rows=rows, rowsp=rowsp)



##################################################################################
#                                SEGUNDA CAUTELAR                                #
##################################################################################


@televendas_bp.route('/televendas/segundacautelar')
def segundacautelar_televendas():
    originador = request.args.get('originador')
    conn = conecta_bd()
    cursor = conn.cursor()

    cursor.execute(''' SELECT SUM(discados) AS soma_discados,
                    SUM(invalidos) AS soma_invalidos, 
                    CASE WHEN SUM(discados) > 0 THEN round((SUM(invalidos)/ SUM(discados) * 100), 0) ELSE 0 END AS soma_porcentagem_invalido
                    FROM public.originador_discagem''')
    
    rows = cursor.fetchall()

    if rows:
        soma_discados = rows[0][0]
        soma_porcentagem_invalido = rows[0][2]
        titulo = f'Painel Real Time Tahto - {soma_discados} / {soma_porcentagem_invalido}%'
    else:
        titulo = 'Painel Real Time Tahto - 0%'

    cursor.execute("SELECT originador, discados, invalidos, porcentagem_invalido, qtd_consulta_total, tipo FROM public.originador_discagem ORDER BY porcentagem_invalido DESC NULLS LAST;")
    rowss = cursor.fetchall()

    # Substituir "None" por "-" e "compartilhado" por "40k" e "exclusivo" por "80k"
    rowss_with_dash_k = [
        (
            originador,
            discados,
            invalidos,
            f"{int(porcentagem_invalido)}%" if porcentagem_invalido is not None else "-",
            "-" if qtd_consulta_total is None else (int(qtd_consulta_total) if qtd_consulta_total.is_integer() else str(qtd_consulta_total)),
            "40k" if tipo == "compartilhado" else "80k"
        )
        for originador, discados, invalidos, porcentagem_invalido, qtd_consulta_total, tipo in rowss
    ]
    
    conn2 = conecta_bd2()
    cursor = conn2.cursor()

    data_por_originador = {}  # Dicionário para armazenar o datestart para cada originador

    for originador, _, _, _, _, _ in rowss:
        cursor.execute("SELECT ddd FROM a5solutions.originador WHERE originador = %s", (originador,))
        resultado = cursor.fetchone()

        resultado_formatado = ''
        if resultado:
            resultado_formatado = '|'.join(str(valor) for valor in resultado)

        cursor.execute(f''' SELECT datestart
                        FROM ingenium.cdr
                        WHERE called ~ '^99({resultado_formatado})'
                        ORDER BY datestart DESC
                        LIMIT 1; ''')

        resultado_cdr = cursor.fetchone()

        if resultado_cdr:
            datestart = resultado_cdr[0]
            data_por_originador[originador] = datestart  # Associa originador ao datestart

    conn2.close()

    return render_template("segundacautelar.html", titulo=titulo, rowss=rowss_with_dash_k, rows=rows, data_por_originador=data_por_originador)





@televendas_bp.route('/televendas/buscarscautelar', methods=['GET', 'POST'])
def buscarscautelar_televendas():
    pesquisa = request.form.get('pesquisa').strip()
    conn = conecta_bd()
    cursor = conn.cursor()

    cursor.execute(''' SELECT SUM(discados) AS soma_discados,
                    SUM(invalidos) AS soma_invalidos, 
                    CASE WHEN SUM(discados) > 0 THEN round((SUM(invalidos)/ SUM(discados) * 100), 0) ELSE 0 END AS soma_porcentagem_invalido
                    FROM public.originador_discagem''')
    
    rows = cursor.fetchall()

    if rows:
        soma_discados = rows[0][0]
        soma_porcentagem_invalido = rows[0][2]
        titulo = f'Painel Real Time Tahto - {soma_discados} / {soma_porcentagem_invalido}%'
    else:
        titulo = 'Painel Real Time Tahto - 0%'

    cursor.execute(f''' SELECT 
                        originador,
                        discados,
                        invalidos,
                        CASE
                            WHEN porcentagem_invalido IS NULL THEN '-'
                            ELSE porcentagem_invalido::text
                        END AS porcentagem_invalido,
                        CASE
                            WHEN qtd_consulta_total IS NULL THEN '-'
                            ELSE qtd_consulta_total::text
                        END AS qtd_consulta_total,
                        CASE
                            WHEN tipo = 'compartilhado' THEN '40k'
                            WHEN tipo = 'exclusivo' THEN '80k'
                            ELSE tipo
                        END AS tipo
                    FROM 
                        public.originador_discagem 
                    WHERE 
                        originador ILIKE '%{pesquisa}%'
                    ORDER BY 
                        porcentagem_invalido DESC NULLS LAST;
                      ''')

    rowss = cursor.fetchall()

    rowss_with_percentages = [
    (
        originador,
        discados,
        invalidos,
        f"{int(float(porcentagem_invalido))}%" if porcentagem_invalido != '-' else '-',
        "-" if qtd_consulta_total == '-' else qtd_consulta_total,
        "40k" if tipo == "compartilhado" else "80k"
    )
    for originador, discados, invalidos, porcentagem_invalido, qtd_consulta_total, tipo in rowss
]

    data_por_originador = {}  # Dicionário para armazenar o datestart para cada originador

    conn2 = conecta_bd2()
    cursor = conn2.cursor()

    for originador, _, _, _, _, _ in rowss:
        cursor.execute("SELECT ddd FROM a5solutions.originador WHERE originador = %s", (originador,))
        resultado = cursor.fetchone()

        resultado_formatado = ''
        if resultado:
            resultado_formatado = '|'.join(str(valor) for valor in resultado)

        cursor.execute(f''' SELECT datestart
                        FROM ingenium.cdr
                        WHERE called ~ '^99({resultado_formatado})'
                        ORDER BY datestart DESC
                        LIMIT 1; ''')

        resultado_cdr = cursor.fetchone()

        if resultado_cdr:
            datestart = resultado_cdr[0]
            data_por_originador[originador] = datestart  # Associa originador ao datestart

    conn2.close()

    return render_template("segundacautelar.html", titulo=titulo, rows=rows, rowss=rowss_with_percentages, data_por_originador=data_por_originador)




def consultar_originador(originador):
    conn2 = conecta_bd2()
    cursor = conn2.cursor()

    cursor.execute(f''' SELECT faixa FROM a5solutions.originador WHERE originador = '{originador}' ''')
    resultado = cursor.fetchone()

    conn2.close()

    if resultado:
        return resultado[0]
    else:
        return None

@televendas_bp.route('/televendas/obterResultado', methods=['GET'])
def obter_resultado():
    originador = request.args.get('originador')

    # Consultar o originador localmente
    resultado = consultar_originador(originador)

    if resultado:
        return jsonify({'resultado': resultado})
    else:
        return jsonify({'resultado': 'Nenhum resultado encontrado'}), 404





# Rota para a página de erro
@televendas_bp.route('/televendas/erro-conexao')
def erro_conexao():
    # Verificar se a URL da página original está armazenada na sessão
    if 'pagina_original' in session:
        pagina_original = session.pop('pagina_original')
        return render_template('erro.html', pagina_original=pagina_original)
    else:
        # Caso a URL não esteja armazenada na sessão, redirecionar para a home
        return render_template('erro.html', pagina_original='/televendas')