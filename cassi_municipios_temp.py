# -*- coding: utf-8 -*-
"""
Created on Sun May 24 20:26:52 2020

@author: asgia
"""

from utils import busca_pagina, gera_msg_erro, grava_msg_erro, conecta_banco
from cassi_ufs import busca_uf

def grava_municipio_temp(id_uf, cd_municipio, nm_municipio):
    '''Grava uma UF no banco de dados
    
    Parameters
    ----------
    id_uf : int
        Identificador da UF.
    cd_municipio : string
        Código de identificação do município.
    nm_municipio : string
        Nome do municpio.

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
        sql = 'INSERT INTO tb_municipio_temp (id_uf, cd_municipio, nm_municipio) '
        sql += 'VALUES (%s, %s, %s)'
        cursor.execute(sql, (id_uf, cd_municipio, nm_municipio))
        con.commit()
        con.close()
    except Exception as e:
        erro = 1
        msg_erro = gera_msg_erro(e, 'Falhou na gravação do municipio: ' + nm_municipio)
        
    return erro, msg_erro

def busca_municipio_temp(id_uf, id_municipio = None):
    '''Busca UFs no banco de dados
    
    Parameters
    ----------
    id_uf : int
        Identificador da UF.
    id_municipio : int
        Identificador do Município (opcional).
    
    Returns
    -------
    erro : string
        Indicador de erro.
    msg_erro : string
        Mensagem de erro formatada.
    municipios : list
        Lista de Municípios.
    '''
    erro = 0
    msg_erro = None
    ufs = None
    try:
        con = conecta_banco()
        cursor = con.cursor()
        sql = 'SELECT id_municipio, id_uf, cd_municipio, nm_municipio'
        sql += ' from tb_municipio_temp where id_uf = ' + str(id_uf)
        if id_municipio is not None:
            sql += ' and id_municipio = ' + str(id_municipio)
        cursor.execute(sql)
        ufs = cursor.fetchall()
        con.close()
    except Exception as e:
        erro = 1
        msg_erro = gera_msg_erro(e, 'Falhou na consulta do Municipio: ' + id_municipio)
        
    return erro, msg_erro, ufs


def carrega_municipio_temp():
    #Carrega UFs
    #Conectar ao banco
    erro, msg_erro, ufs = busca_uf()
    
    if erro:
        # Salva log de erro
        grava_msg_erro(msg_erro)
        return
    
    for uf in ufs:
        sg_uf = uf[1]
        id_uf = uf[0]
        URL = 'https://www.redecredenciada.mobi/mobile-guia/v2/ws-cidade.php'
        parametros = {'id_operadora':19, 'id_estado': sg_uf, 'id_plano':9,
                  'formatacao_texto':'1590362791956'}
        tipo = 'html'
        metodo = 'get'

        erro, msg_erro, bs = busca_pagina(URL, tipo, parametros, metodo)
    
        if erro:
            # Salva log de erro
            grava_msg_erro(msg_erro)
            return
    
        try:
            municipios = bs.find('ul').find_all('a')
            for municipio in municipios:
                cd_municipio = municipio.get('data-id')
                nm_municipio = municipio.text
                
                erro, msg_erro = grava_municipio_temp(id_uf, cd_municipio, nm_municipio)              
                
        except Exception as e:
            msg_erro = gera_msg_erro(e, 'Falhou na busca montagem dos municipios')
            grava_msg_erro(msg_erro)
            return
        
        #erro, msg_erro = grava_plano(nome, ans, tipo, status)
        if erro:
            grava_msg_erro(msg_erro)
            return
    
    
    



