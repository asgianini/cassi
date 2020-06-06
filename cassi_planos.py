#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 24 17:37:46 2020

@author: 08679507733
"""

from utils import busca_pagina, gera_msg_erro, grava_msg_erro, conecta_banco


def grava_plano(id_plano, nome, ans, tipo, status):
    '''Grava um plano no banco de dados
    
    Parameters
    ----------
    nome : string
        Nome do plano.
    ans : string
        Número do plano na ANS.
    tipo : string
        Tipo do plano (empresarial, individual etc).
    status : string
        Status do plano (ativo, inativo etc).

    Returns
    -------
    msg_erro : string
        Mensagem de rro formatada.
    '''
    erro = 0
    msg_erro = None    
    try:
        con = conecta_banco()
        cursor = con.cursor()
        sql = 'INSERT INTO tb_plano (id_plano, nm_plano, cd_ans, tp_plano, st_plano) '
        sql += 'VALUES (%s, %s, %s, %s, %s)'
        cursor.execute(sql, (id_plano, nome, ans, tipo, status))
        con.commit()
        con.close()
    except Exception as e:
        erro = 1
        msg_erro = gera_msg_erro(e, 'Falhou na gravação do plano: ' + nome)
        
    return erro, msg_erro

def busca_plano(id_plano = None):
    '''Busca UFs no banco de dados
    
    Parameters
    ----------
    id_plano : int
        Identificador do plano (opcional).

    Returns
    -------
    erro : string
        Indicador de erro.
    msg_erro : string
        Mensagem de erro formatada.
    ufs : list
        Lista de UFs.
    '''
    erro = 0
    msg_erro = None
    ufs = None
    try:
        con = conecta_banco()
        cursor = con.cursor()
        sql = 'SELECT id_plano, nm_plano, cd_ans, tp_plano, st_plano from tb_plano'
        if id_plano is not None:
            sql += ' where id_plano = ' + str(id_plano)
        cursor.execute(sql)
        ufs = cursor.fetchall()
        con.close()
    except Exception as e:
        erro = 1
        msg_erro = gera_msg_erro(e, 'Falhou na consulta do plano: ' + str(id_plano))
        
    return erro, msg_erro, ufs



def carrega_plano():
    URL = 'https://www.redecredenciada.mobi/mobile-guia/v2/ws-plano.php'
    parametros = {'id_operadora':19, 'formatacao_texto':2, 'conv_id':'',
                  'default_label_sessao_outros_planos':'Outros planos', 
                  'default_label_sessao_meus_planos':'Meu plano'}
    tipo = 'html'
    metodo = 'get'
    
    plano = None
    
    
    # Chamada da função para criar um BS a partir de uma url
    while True:
        try:
            erro, msg_erro, bs = busca_pagina(URL, tipo, parametros, metodo)
            break
        except Exception as e:
            print(e)
            print(parametros)
            continue
    
    if erro:
        # Salva log de erro
        grava_msg_erro(msg_erro)
        return
    
    try:
        planos = bs.find_all('li')
    except Exception as e:
        msg_erro = gera_msg_erro(e, 'Falhou no bs.find_all')
        grava_msg_erro(msg_erro)
        return
    
    
    if not planos:
        msg_erro = gera_msg_erro(None, 'Falhou no bs.find_all')
        grava_msg_erro(msg_erro)
        return


    for plano in planos:
        
        try:
            id_plano = plano.find('div').get('data-id')
            nome = plano.find('div').get('data-nome')
            ans = plano.find('em').text.split('|')[0].strip().split(':')[1].strip()
            tipo = plano.find('em').text.split('|')[1].strip()
            status = plano.find('strong').text.strip()
        except Exception as e:
            msg_erro = gera_msg_erro(e, 'Falhou na busca de atributos')
            grava_msg_erro(msg_erro)
            return
        
        erro, msg_erro = grava_plano(id_plano, nome, ans, tipo, status)
        if erro:
            grava_msg_erro(msg_erro)
            return 

