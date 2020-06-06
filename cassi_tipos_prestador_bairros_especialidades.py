# -*- coding: utf-8 -*-
"""
Created on Wed May 27 13:37:45 2020

@author: asgia
"""

from utils import busca_pagina, gera_msg_erro, grava_msg_erro, conecta_banco, remover_acentos
from cassi_ufs import busca_uf
from cassi_municipios import busca_municipio
from cassi_bairros import busca_bairro
from cassi_tipos_prestador import busca_tipo_prestador
from cassi_tipos_prestador_bairros import busca_tipo_prestador_bairro
from cassi_especialidades import busca_especialidade

def grava_tipo_prestador_bairro_especialidade(id_tipo_prestador, id_bairro, id_especialidade):
    '''Grava um Tipo Prestador-Bairro-Especialidade no banco de dados
    
    Parameters
    ----------
    id_tipo_prestador : int
        Identificador do Tipo Prestador.
    id_bairro : int
        Identificador do Bairro.
    id_especialidade : int
        Identificador da Especialidade.

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
        sql = 'INSERT INTO tb_tipo_prestador_bairro_especialidade (id_tipo_prestador, id_bairro, id_especialidade) '
        sql += 'VALUES (%s, %s, %s)'
        cursor.execute(sql, (id_tipo_prestador, id_bairro, id_especialidade))
        con.commit()
        con.close()
    except Exception as e:
        erro = 1
        msg_erro = gera_msg_erro(e, 'Falhou na gravação do tipo prestador bairro especialidade: ' + str(id_tipo_prestador)+ ' (' + str(id_bairro) + ')')
        
    return erro, msg_erro


def carrega_tipo_prestador_bairro_especialidade():

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
                
                erro, msg_erro, tipos_prestador_bairros = busca_tipo_prestador_bairro(None, id_bairro)
                
                if erro:
                    grava_msg_erro(msg_erro)
                    return
                
                for tipo_prestador_bairro in tipos_prestador_bairros:
                    id_tipo_prestador = tipo_prestador_bairro[0]
                    
                    erro, msg_erro, tipo_prestador = busca_tipo_prestador(id_tipo_prestador, id_plano)
                    
                    if erro:
                        grava_msg_erro(msg_erro)
                        return
                    
                    cd_tipo_prestador = tipo_prestador[0][2]
        
                    URL = 'https://www.redecredenciada.mobi/mobile-guia/v2/ws-especialidade.php'
                    parametros = {'id_operadora':19, 'id_cidade': cd_municipio,  
                                  'id_plano': id_plano, 'id_estado': sg_uf, 'bairro': nm_bairro,
                                  'id_tipo_prestador': cd_tipo_prestador,
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
                        especialidades = bs.find('ul').find_all('a')
                        for especialidade in especialidades:
                            cd_especialidade = especialidade.get('data-id')
                            
                            erro, msg_erro, especialidade = busca_especialidade(None, id_plano, cd_especialidade, None)
                
                            if erro:
                                grava_msg_erro(msg_erro)
                                return
                            
                            id_especialidade = especialidade[0][0]
                            
                            
                            erro, msg_erro = grava_tipo_prestador_bairro_especialidade(id_tipo_prestador, id_bairro, id_especialidade)
                            
                    except Exception as e:
                        msg_erro = gera_msg_erro(e, 'Falhou na busca montagem dos bairros')
                        grava_msg_erro(msg_erro)
                        return
                    
                    if erro:
                        grava_msg_erro(msg_erro)
                        return
