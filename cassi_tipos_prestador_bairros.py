# -*- coding: utf-8 -*-
"""
Created on Mon May 25 13:44:28 2020

@author: asgia
"""

from utils import busca_pagina, gera_msg_erro, grava_msg_erro, conecta_banco, remover_acentos
from cassi_ufs import busca_uf
from cassi_municipios import busca_municipio
from cassi_bairros import busca_bairro
from cassi_tipos_prestador import busca_tipo_prestador

def grava_tipo_prestador_bairro(id_tipo_prestador, id_bairro):
    '''Grava uma UF no banco de dados
    
    Parameters
    ----------
    id_bairro : int
        Identificador do Bairro.
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
        sql = 'INSERT INTO tb_tipo_prestador_bairro (id_tipo_prestador, id_bairro) '
        sql += 'VALUES (%s, %s)'
        cursor.execute(sql, (id_tipo_prestador, id_bairro))
        con.commit()
        con.close()
    except Exception as e:
        erro = 1
        msg_erro = gera_msg_erro(e, 'Falhou na gravação do tipo prestador bairro: ' + str(id_tipo_prestador)+ ' (' + str(id_bairro) + ')')
        
    return erro, msg_erro

def busca_tipo_prestador_bairro(id_tipo_prestador = None, id_bairro = None):
    '''Busca Tipos Prestador Bairro no banco de dados
    
    Parameters
    ----------
    id_tipo_prestador : int
        Identificador do Tipo Prestador (opcional).
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
    tipos_prestador = None
    try:
        con = conecta_banco()
        cursor = con.cursor()
        sql = 'SELECT id_tipo_prestador, id_bairro'
        sql += ' from tb_tipo_prestador_bairro where 1 = 1'
        if id_tipo_prestador is not None:
            sql += ' and id_tipo_prestador = ' + str(id_tipo_prestador)
        if id_bairro is not None:
            sql += ' and id_bairro = ' + str(id_bairro)
        cursor.execute(sql)
        tipos_prestador = cursor.fetchall()
        con.close()
    except Exception as e:
        erro = 1
        msg_erro = gera_msg_erro(e, 'Falhou na consulta do Tipo Prestador Bairro: ' + str(id_tipo_prestador))
        
    return erro, msg_erro, tipos_prestador



def carrega_tipo_prestador_bairro():

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
            
            erro, msg_erro, bairros = busca_bairro(id_municipio)
    
            if erro:
                # Salva log de erro
                grava_msg_erro(msg_erro)
                return
            
            for bairro in bairros:
                id_bairro = bairro[0]
                nm_bairro = remover_acentos(bairro[2].strip().upper())
        
                URL = 'https://www.redecredenciada.mobi/mobile-guia/v2/ws-tipo-prestador.php'
                parametros = {'id_operadora':19, 'id_cidade': cd_municipio,  
                              'id_plano': id_plano, 'id_estado': sg_uf, 'bairro': nm_bairro,
                              'formatacao_texto':'2', 'force_especialidade':'S'}
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
                            
                            erro, msg_erro, tipo_prestador = busca_tipo_prestador(None, id_plano, cd_tipo_prestador)
        
                            if erro:
                                # Salva log de erro
                                grava_msg_erro(msg_erro)
                                return
                            id_tipo_prestador = tipo_prestador[0][0]
                                     
                            erro, msg_erro = grava_tipo_prestador_bairro(id_tipo_prestador, id_bairro)              
                        
                except Exception as e:
                    msg_erro = gera_msg_erro(e, 'Falhou na busca montagem dos bairros')
                    grava_msg_erro(msg_erro)
                    return
                
                if erro:
                    grava_msg_erro(msg_erro)
                    return
    
