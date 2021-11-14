# -*- coding: utf-8 -*-
import requests
import json
import psycopg2

host = "192.168.10.39"
port = "5432"
user = "postgres"
password = "gsspostgres"
database = "gss_elecciones"
fuente = """host=%s port=%s user=%s password=%s dbname=%s""" % (
    host, port, user, password, database)

#TOKEN = "1945790969:AAHiuXZ7lj6l09xwFSqeVNW2G_aqsgpOB8o"
TOKEN = "1978519504:AAGVzxbRVlmFeDW8zkjxHcbL9cs7h4H9Hhw"
CHAT_ID = [239672335, 1214971500, 827637342, 666228594]


def buscar_nombre(cedbus) -> str:
    try:
        nombres = ""
        sentencia = "select votante from" + ' "Personas"' + \
            ".vw_rep where cedula=%s"
        conexion = psycopg2.connect(fuente)
        puntero = conexion.cursor()
        puntero.execute(sentencia, (cedbus,))
        valores = puntero.fetchone()
        nombres = str(valores[0]).title()
        print(nombres)
        puntero.close()
        conexion.close()
        return nombres
    except psycopg2.Error as e:
        print(e)
    except UnicodeDecodeError as uni:
        print(uni)


def main():
     try:
         url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
         sentencia = "select * from" + ' "Telegram_Bot"' + \
             ".tg_users"
         conexion = psycopg2.connect(fuente)
         puntero = conexion.cursor()
         puntero.execute(sentencia)
         valores = puntero.fetchall()
         for registros in valores:
             mensaje = "Saludos Camarada\n" + str(buscar_nombre(
                 int(registros[2])))+"\nDesde la Gran Sala Situacional del PSUV Zulia"
             parametros = {"chat_id": int(registros[1]), "text": mensaje}
             respuesta = requests.post(url, data=parametros)
             if respuesta.status_code == 200:
                 salida = json.loads(respuesta.text)
     except psycopg2.Error as e:
         print(e)


# def main():
#     try:
#         url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
#         sentencia = "select * from" + ' "Telegram_Bot"' + \
#             ".tg_users"
#         parse = 'HTML'
#         conexion = psycopg2.connect(fuente)
#         puntero = conexion.cursor()
#         puntero.execute(sentencia)
#         valores = puntero.fetchall()
#         for registros in valores:
#             print(registros[1])
#             mensaje = 'Este es el <b><a href="http://t.me/GssPsuvZulia_Bot">link</a></b> del bot de la Gran Sala Situacional del PSUV Zulia'
#             parametros = {"chat_id": int(
#                 registros[1]), "text": mensaje, "parse_mode": parse}
#             respuesta = requests.post(url, data=parametros)
#             if respuesta.status_code == 200:
#                 salida = json.loads(respuesta.text)
#     except psycopg2.Error as e:
#         print(e)


if __name__ == '__main__':
    main()
