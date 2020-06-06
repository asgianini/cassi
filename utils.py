# -*- coding: utf-8 -*-
"""
Created on Sun May 24 19:00:27 2020

@author: asgia
"""
import requests
from bs4 import BeautifulSoup
import inspect
import psycopg2
from unicodedata import normalize



def remover_acentos(txt):
    return normalize('NFKD', txt).encode('ASCII', 'ignore').decode('ASCII')

def gera_msg_erro(e, msg):
    '''Gera uma mensagem formatada de erro
    
    Parameters
    ----------
    e : Exception Object
        Exceção gerada com o erro.
    msg : string
        Mensagem de erro.

    Returns
    -------
    msg_erro : string
        Mensagem de rro formatada.
    '''
    if hasattr(e, 'message'):
        exception = e.message
    else:
        exception = e
    msg_erro = '####################################################################\n'
    msg_erro += msg + '\n'
    msg_erro += 'Função: ' + str(inspect.stack()[1][3]) + '\n'
    msg_erro += str(exception)
    
    return msg_erro

def grava_msg_erro(erro):
    # Fazer função para gravar o erro no banco
    print(erro)


def busca_pagina(URL, tipo, parametros, metodo='get'):
    erro = 0
    msg_erro = None
    bs = None
    
    # Busca páginas html
    if (tipo == 'html'):    
        if (metodo == 'get'):
            try:
                pagina = requests.get(url = URL, params = parametros)
            except Exception as e:
                erro = 1
                msg_erro = gera_msg_erro(e, 'Falhou no requests.get')

        else:
            try:
                pagina = requests.post(url = URL, params = parametros)
            except Exception as e:
                erro = 1
                msg_erro = gera_msg_erro(e, 'Falhou no requests.post')
        
        if erro:
            return erro, msg_erro, None
        
        # Cria um objeto Beautiful Soup com a pagina
        try:
            bs = BeautifulSoup(pagina.text, 'html.parser', from_encoding='UTF-8')
        except Exception as e:
            erro = 1
            msg_erro = gera_msg_erro(e, 'Falhou na criação do objeto Beautiful Soup')
        
        return erro, msg_erro, bs
        
    # Busca páginas json    
    elif (tipo == 'json'):
        if (metodo == 'get'):
            try:
                pagina = requests.get(url = URL, params = parametros)
            except Exception as e:
                erro = 1
                msg_erro = gera_msg_erro(e, 'Falhou no requests.get')

        else:
            try:
                pagina = requests.post(url = URL, params = parametros)
            except Exception as e:
                erro = 1
                msg_erro = gera_msg_erro(e, 'Falhou no requests.post')
        
        if erro:
            return erro, msg_erro, None
        
        # Extraindo os dados no formato json
        try:            
            bs = pagina.json()
        except Exception as e:
            erro = 1
            msg_erro = gera_msg_erro(e, 'Falhou na criação do objeto Beautiful Soup')
        
        return erro, msg_erro, bs


def conecta_banco():
    '''Conecta ao banco de dados
    
    Parameters
    ----------

    Returns
    -------
    connection : objeto de conexão
        Objeto de conexão com o banco de dados.
    '''
    connection = psycopg2.connect(user = "postgres",
                                  password = "admin",
                                  host = "127.0.0.1",
                                  port = "5432",
                                  database = "db_cassi")
    return connection