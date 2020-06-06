# -*- coding: utf-8 -*-
"""
Created on Sun May 24 23:01:43 2020

@author: asgia
"""


from utils import busca_pagina, gera_msg_erro, grava_msg_erro, conecta_banco
from cassi_ufs import busca_uf
from cassi_municipios import busca_municipio

def grava_bairro(id_municipio, nm_bairro):
    '''Grava uma UF no banco de dados
    
    Parameters
    ----------
    id_municipio : int
        Identificador do Municipio.
    nm_bairro : string
        Nome do bairro.

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
        sql = 'INSERT INTO tb_bairro (id_municipio, nm_bairro) '
        sql += 'VALUES (%s, %s)'
        cursor.execute(sql, (id_municipio, nm_bairro))
        con.commit()
        con.close()
    except Exception as e:
        erro = 1
        msg_erro = gera_msg_erro(e, 'Falhou na gravação do bairro: ' + nm_bairro + ' (' + str(id_municipio) + ')')
        
    return erro, msg_erro

def busca_bairro(id_municipio, id_bairro = None):
    '''Busca UFs no banco de dados
    
    Parameters
    ----------
    id_municipio : int
        Identificador do Município.
    id_bairro : int
        Identificador do Bairro (opcional).
    
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
    bairros = None
    try:
        con = conecta_banco()
        cursor = con.cursor()
        sql = 'SELECT id_bairro, id_municipio, nm_bairro'
        sql += ' from tb_bairro where id_municipio = ' + str(id_municipio)
        if id_bairro is not None:
            sql += ' and id_municipio = ' + str(id_bairro)
        cursor.execute(sql)
        bairros = cursor.fetchall()
        con.close()
    except Exception as e:
        erro = 1
        msg_erro = gera_msg_erro(e, 'Falhou na consulta do Municipio: ' + id_municipio)
        
    return erro, msg_erro, bairros


def carrega_bairro():

    erro, msg_erro, ufs = busca_uf()
    
    if erro:
        # Salva log de erro
        grava_msg_erro(msg_erro)
        return
    
    for uf in ufs:
        id_uf = uf[0]
        id_plano = uf[1]
        sg_uf = uf[3]
        
        
        
        erro, msg_erro, municipios = busca_municipio(id_uf)
    
        if erro:
            # Salva log de erro
            grava_msg_erro(msg_erro)
            return
        
        for municipio in municipios:
            id_municipio = municipio[0]
            cd_municipio = municipio[2]
        
            URL = 'https://www.redecredenciada.mobi/mobile-guia/v2/ws-bairro.php'
            parametros = {'id_operadora':19, 'id_cidade': cd_municipio,  
                          'id_plano': id_plano, 'id_estado': sg_uf,
                          'formatacao_texto':'1590372005692'}
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
                bairros = bs.find('ul').find_all('a')
                for bairro in bairros:
                    nm_bairro = bairro.text
                    if nm_bairro != 'TODOS': 
                        erro, msg_erro = grava_bairro(id_municipio, nm_bairro)              
                    
            except Exception as e:
                msg_erro = gera_msg_erro(e, 'Falhou na busca montagem dos bairros')
                grava_msg_erro(msg_erro)
                return
            
            #erro, msg_erro = grava_plano(nome, ans, tipo, status)
            if erro:
                grava_msg_erro(msg_erro)
                return
    
    
    