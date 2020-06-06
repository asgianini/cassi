# -*- coding: utf-8 -*-
"""
Created on Fri May 29 20:23:37 2020

@author: asgia
"""


# -*- coding: utf-8 -*-
"""
Created on Wed May 27 13:37:45 2020

@author: asgia
"""

from utils import busca_pagina, gera_msg_erro, grava_msg_erro, conecta_banco, remover_acentos
from cassi_tipos_prestador import busca_tipo_prestador
from cassi_tipos_prestador_bairros import busca_tipo_prestador_bairro
from cassi_especialidades import busca_especialidade

def busca_uf_temp(id_uf = None):
    erro = 0
    msg_erro = None
    ufs = None
    try:
        con = conecta_banco()
        cursor = con.cursor()
        sql = 'SELECT id_uf, id_plano, cd_uf, sg_uf, nm_uf, cd_ibge from tb_uf'
        sql += ' where id_uf >= 106'
        if id_uf is not None:
            sql += ' where id_uf = ' + str(id_uf)
        cursor.execute(sql)
        ufs = cursor.fetchall()
        con.close()
    except Exception as e:
        erro = 1
        msg_erro = gera_msg_erro(e, 'Falhou na consulta da UF')
        
    return erro, msg_erro, ufs

def busca_municipio_temp(id_uf, id_municipio = None):
    erro = 0
    msg_erro = None
    municipios = None
    try:
        con = conecta_banco()
        cursor = con.cursor()
        sql = 'SELECT id_municipio, id_uf, cd_municipio, nm_municipio'
        sql += ' from tb_municipio where id_uf = ' + str(id_uf)
        sql += ' and id_municipio >= 6455'
        if id_municipio is not None:
            sql += ' and id_municipio = ' + str(id_municipio)
        cursor.execute(sql)
        municipios = cursor.fetchall()
        con.close()
    except Exception as e:
        erro = 1
        msg_erro = gera_msg_erro(e, 'Falhou na consulta do Municipio: ' + id_municipio)
        
    return erro, msg_erro, municipios

def busca_bairro_temp(id_municipio, id_bairro = None):
    erro = 0
    msg_erro = None
    bairros = None
    try:
        con = conecta_banco()
        cursor = con.cursor()
        sql = 'SELECT id_bairro, id_municipio, nm_bairro'
        sql += ' from tb_bairro where id_municipio = ' + str(id_municipio)
        sql += ' and id_bairro >= 24393'
        if id_bairro is not None:
            sql += ' and id_municipio = ' + str(id_bairro)
        cursor.execute(sql)
        bairros = cursor.fetchall()
        con.close()
    except Exception as e:
        erro = 1
        msg_erro = gera_msg_erro(e, 'Falhou na consulta do Municipio: ' + id_municipio)
        
    return erro, msg_erro, bairros

def grava_tipo_prestador_bairro_especialidade(id_tipo_prestador, id_bairro, id_especialidade):
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


def carrega_tipo_prestador_bairro_especialidade_temp():

    erro, msg_erro, ufs = busca_uf_temp()
    
    if erro:
        # Salva log de erro
        grava_msg_erro(msg_erro)
        return
    
    for uf in ufs:
        id_uf = uf[0]
        id_plano = uf[1]
        sg_uf = uf[3]
        
        
        
        erro, msg_erro, municipios = busca_municipio_temp(id_uf)
    
        if erro:
            # Salva log de erro
            grava_msg_erro(msg_erro)
            return
        
        for municipio in municipios:
            id_municipio = municipio[0]
            cd_municipio = municipio[2]
            
            erro, msg_erro, bairros = busca_bairro_temp(id_municipio)
    
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
