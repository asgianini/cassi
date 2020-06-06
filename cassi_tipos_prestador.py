# -*- coding: utf-8 -*-
"""
Created on Mon May 25 13:44:28 2020

@author: asgia
"""

from utils import busca_pagina, gera_msg_erro, grava_msg_erro, conecta_banco
from cassi_planos import busca_plano

def grava_tipo_prestador(id_plano, cd_tipo_prestador, nm_tipo_prestador):
    '''Grava uma UF no banco de dados
    
    Parameters
    ----------
    id_tipo_prestador : int
        Identificador do Tipo Prestador.
    id_plano: int
        Identificador do plano.
    nm_tipo_prestador : string
        Nome do Tipo prestador.

    Returns
    -------
    erro : int
       Flag de erro. 
    msg_erro : string
        Mensagem de erro formatada.
    '''
    erro = 0
    msg_erro = None    
    try:
        con = conecta_banco()
        cursor = con.cursor()
        sql = 'INSERT INTO tb_tipo_prestador (id_plano, cd_tipo_prestador, nm_tipo_prestador) '
        sql += 'VALUES (%s, %s, %s)'
        cursor.execute(sql, (id_plano, cd_tipo_prestador, nm_tipo_prestador))
        con.commit()
        con.close()
    except Exception as e:
        erro = 1
        msg_erro = gera_msg_erro(e, 'Falhou na gravação do tipo prestador: ' + nm_tipo_prestador + ' (' + str(cd_tipo_prestador) + ')')
        
    return erro, msg_erro


def busca_tipo_prestador(id_tipo_prestador = None, id_plano = None, cd_tipo_prestador = None):
    '''Busca Tipos Prestador no banco de dados
    
    Parameters
    ----------
    id_tipo_prestador : int
        Identificador do Tipo Prestador (opcional).
    cd_tipo_prestador_bairro : int
        Código do Tipo Prestador (opcional).
    
    Returns
    -------
    erro : string
        Indicador de erro.
    msg_erro : string
        Mensagem de erro formatada.
    bairros : list
        Lista de Bairros.
    '''
    erro = 0
    msg_erro = None
    tipos_prestador = None
    try:
        con = conecta_banco()
        cursor = con.cursor()
        sql = 'SELECT id_tipo_prestador, id_plano, cd_tipo_prestador, nm_tipo_prestador'
        sql += ' from tb_tipo_prestador where 1 = 1'
        if id_tipo_prestador is not None:
            sql += ' and id_tipo_prestador = ' + str(id_tipo_prestador)
        if id_plano is not None:
            sql += ' and id_plano = ' + str(id_plano)
        if cd_tipo_prestador is not None:
            sql += ' and cd_tipo_prestador = ' + str(cd_tipo_prestador)
        cursor.execute(sql)
        tipos_prestador = cursor.fetchall()
        con.close()
    except Exception as e:
        erro = 1
        msg_erro = gera_msg_erro(e, 'Falhou na consulta do Tipo Prestador: ' + str(id_tipo_prestador))
        
    return erro, msg_erro, tipos_prestador

def carrega_tipo_prestador():
    erro, msg_erro, planos = busca_plano()
    
    if erro:
        # Salva log de erro
        grava_msg_erro(msg_erro)
        return
    
    for plano in planos:
        id_plano = plano[0]
        
        URL = 'https://www.redecredenciada.mobi/mobile-guia/v2/ws-tipo-prestador.php'
        parametros = {'id_operadora':19, 'id_cidade': '',  
                      'id_plano': id_plano, 'id_estado': '', 'bairro': '',
                      'formatacao_texto':'2', '_': '1590376516866',
                      'force_especialidade':'S'}
        tipo = 'html'
        metodo = 'get'
    
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
            tipos_prestador = bs.find('ul').find_all('a')
            for tp in tipos_prestador:
                cd_tipo_prestador = tp.get('data-id')
                if cd_tipo_prestador:
                    nm_tipo_prestador = tp.text
                else:
                    continue
                
                erro, msg_erro = grava_tipo_prestador(id_plano, cd_tipo_prestador, nm_tipo_prestador)              
                
        except Exception as e:
            msg_erro = gera_msg_erro(e, 'Falhou na busca montagem dos bairros')
            grava_msg_erro(msg_erro)
            return
        
        #erro, msg_erro = grava_plano(nome, ans, tipo, status)
        if erro:
            grava_msg_erro(msg_erro)
            return
        
    
