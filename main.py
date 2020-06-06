# -*- coding: utf-8 -*-
"""
Created on Sun May 24 23:23:35 2020

@author: asgia
"""

#from cassi_planos import carrega_plano
from cassi_ufs import carrega_uf
from cassi_municipios import carrega_municipio
from cassi_bairros import carrega_bairro
from cassi_tipos_prestador import carrega_tipo_prestador
from cassi_especialidades import carrega_especialidade
from cassi_tipos_prestador_bairros import carrega_tipo_prestador_bairro
from cassi_tipos_prestador_bairros_especialidades_temp import carrega_tipo_prestador_bairro_especialidade_temp

from cassi_municipios_temp import carrega_municipio_temp

import timeit


## Iniciar log


inicio = timeit.default_timer()


#carrega_plano()
#carrega_uf() # 9.37 segundos
#carrega_municipio() # 628.27 segundos
#carrega_bairro() # 2997 segundos

#carrega_tipo_prestador() # 11 segundos
#carrega_tipo_prestador_bairro() # 15558 segundos - 28685 segundos

#carrega_especialidade() # 40 segundos
carrega_tipo_prestador_bairro_especialidade_temp() # 197901 segundos - 7296 s
# Depois de 74430 segundos deu o seguinte erro
####################################################################
#Falhou no requests.get
#Função: busca_pagina
#HTTPSConnectionPool(host='www.redecredenciada.mobi', port=443): Max retries exceeded with url: /mobile-guia/v2/ws-especialidade.php?id_operadora=19&id_cidade=3549805&id_plano=8&id_estado=SP&bairro=VILA+AURORA&id_tipo_prestador=47&formatacao_texto=2&_=1590376516866&force_especialidade=S (Caused by NewConnectionError('<urllib3.connection.VerifiedHTTPSConnection object at 0x00000201B813E108>: Failed to establish a new connection: [Errno 11001] getaddrinfo failed'))

# O último registro:
# ESPECIALIDADE         TIPO PRESTADOR                          BAIRRO          MUNICIPIO               UF
#"OTORRINOLARINGOLOGIA"	"HOSPITAL ESPECIALIZADO / CARDIOLOGIA"	"Vila Aurora"	"São Jose do Rio Preto"	"SP"
# 43                     1	                                      5648	
fim = timeit.default_timer()
print ('duracao: %f' % (fim - inicio))

