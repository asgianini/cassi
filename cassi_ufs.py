# -*- coding: utf-8 -*-
"""
Created on Sun May 24 14:42:30 2020

@author: asgia
"""

from utils import busca_pagina, gera_msg_erro, grava_msg_erro, conecta_banco
from cassi_planos import busca_plano

def grava_uf(id_plano, cd_uf, sg, nome, codigo_IBGE):
    '''Grava uma UF no banco de dados
    
    Parameters
    ----------
    id : int
        identificador da UF.
    sg : string
        Sigla da UF.
    nome : string
        Nome da UF.
    codigo_IBGE : string
        Código da UF no IBGE.

    Returns
    -------
    msg_erro : string
        Mensagem de erro formatada.
    '''
    erro = 0
    msg_erro = None    
    try:
        con = conecta_banco()
        cursor = con.cursor()
        sql = 'INSERT INTO tb_uf (id_plano, cd_uf, sg_uf, nm_uf, cd_IBGE) '
        sql += 'VALUES (%s, %s, %s, %s, %s)'
        cursor.execute(sql, (id_plano, cd_uf, sg, nome, codigo_IBGE))
        con.commit()
        con.close()
    except Exception as e:
        erro = 1
        msg_erro = gera_msg_erro(e, 'Falhou na gravação da uf')
        
    return erro, msg_erro

def busca_uf(id_uf = None):
    '''Busca UFs no banco de dados
    
    Parameters
    ----------
    id_uf : int
        Identificador da UF (opcional).

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
        sql = 'SELECT id_uf, id_plano, cd_uf, sg_uf, nm_uf, cd_ibge from tb_uf'
        if id_uf is not None:
            sql += ' where id_uf = ' + str(id_uf)
        cursor.execute(sql)
        ufs = cursor.fetchall()
        con.close()
    except Exception as e:
        erro = 1
        msg_erro = gera_msg_erro(e, 'Falhou na consulta da UF')
        
    return erro, msg_erro, ufs


def carrega_uf():
    erro, msg_erro, planos = busca_plano()
    
    if erro:
        # Salva log de erro
        grava_msg_erro(msg_erro)
        return
    
    for plano in planos:
        id_plano = plano[0]
    
        URL = 'https://www.redecredenciada.mobi/mobile-guia/v2/ws-estado-unico.php'
        parametros = {'true':'' , 'id_operadora':19, 'id_plano': id_plano,
                      '_':'1590356909735'}
        tipo = 'json'
        metodo = 'get'
        
        
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
            for uf in bs['estados']:
                cd_uf = uf['id']
                sg = uf['uf']
                nome = uf['nome']
                codigo_IBGE = uf['codigo_IBGE']
                
                erro, msg_erro = grava_uf(id_plano, cd_uf, sg, nome, codigo_IBGE)
                
                if erro:
                    grava_msg_erro(msg_erro)
                    return
                
        except Exception as e:
            msg_erro = gera_msg_erro(e, 'Falhou na busca de estados')
            grava_msg_erro(msg_erro)
            return
    

