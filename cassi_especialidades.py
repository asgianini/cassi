# -*- coding: utf-8 -*-
"""
Created on Mon May 25 17:12:37 2020

@author: asgia
"""

from utils import busca_pagina, gera_msg_erro, grava_msg_erro, conecta_banco
from cassi_planos import busca_plano

def grava_especialidade(id_plano, cd_especialidade, nm_especialidade):
    '''Grava uma UF no banco de dados
    
    Parameters
    ----------
    id_plano : int
        Identificador do Plano.
    cd_especialidade : string
        Código da especialidade.
    nm_especialidade : string
        Nome da especialidade.

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
        sql = 'INSERT INTO tb_especialidade (id_plano, cd_especialidade, nm_especialidade) '
        sql += 'VALUES (%s, %s, %s)'
        cursor.execute(sql, (id_plano, cd_especialidade, nm_especialidade))
        con.commit()
        con.close()
    except Exception as e:
        erro = 1
        msg_erro = gera_msg_erro(e, 'Falhou na gravação da especialidade: ' + nm_especialidade + ' (' + str(cd_especialidade) + ')')
        
    return erro, msg_erro

def busca_especialidade(id_especialidade = None, id_plano = None, cd_especialidade = None, nm_especialidade = None):
    '''Busca Especialidade no banco de dados
    
    Parameters
    ----------
    id_especialidade : int
        Identificador da Especialidade (opcional).
    id_plano : int
        Identificador do Plano (opcional)
    cd_especialidade : int
        Código da Especialidade no Plano (opcional).
    nm_especialidade : string
        Nome da especialidade (opcional)
    
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
        sql = 'SELECT id_especialidade, id_plano, cd_especialidade, nm_especialidade'
        sql += ' from tb_especialidade where 1 = 1'
        if id_especialidade is not None:
            sql += ' and id_especialidade = ' + str(id_especialidade)
        if id_plano is not None:
            sql += ' and id_plano = ' + str(id_plano)
        if cd_especialidade is not None:
            sql += ' and cd_especialidade = \'' + str(cd_especialidade) + '\''
        if nm_especialidade is not None:
            sql += ' and nm_especialidade = \'' + str(nm_especialidade) + '\''
        cursor.execute(sql)
        tipos_prestador = cursor.fetchall()
        con.close()
    except Exception as e:
        erro = 1
        msg_erro = gera_msg_erro(e, 'Falhou na consulta da Especialidade: ' + str(id_especialidade))
        
    return erro, msg_erro, tipos_prestador




def carrega_especialidade():
    erro, msg_erro, planos = busca_plano()
    
    if erro:
        # Salva log de erro
        grava_msg_erro(msg_erro)
        return
    
    for plano in planos:
        id_plano = plano[0]
        
        URL = 'https://www.redecredenciada.mobi/mobile-guia/v2/ws-especialidade.php'
        parametros = {'id_operadora':19, 'id_cidade': '',  
                      'id_plano': id_plano, 'id_estado': '', 'bairro': '',
                      'formatacao_texto':'2',
                      'force_especialidade':'S', 'id_tipo_prestador': ''}
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
            especialidades = bs.find('ul').find_all('a')
            for especialidade in especialidades:
                cd_especialidade = especialidade.get('data-id')
                nm_especialidade = especialidade.text
                
                erro, msg_erro = grava_especialidade(id_plano, cd_especialidade, nm_especialidade)              
                
        except Exception as e:
            msg_erro = gera_msg_erro(e, 'Falhou na busca montagem dos bairros')
            grava_msg_erro(msg_erro)
            return
    
        if erro:
            grava_msg_erro(msg_erro)
            return
    

