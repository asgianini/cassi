# -*- coding: utf-8 -*-
"""
Created on Sun May 24 23:23:35 2020

@author: asgia
"""

#from cassi_planos import carrega_plano
from datetime import datetime

from cassi_ufs import carrega_uf
from cassi_municipios import carrega_municipio
from cassi_bairros import carrega_bairro
from cassi_tipos_prestador import carrega_tipo_prestador
from cassi_especialidades import carrega_especialidade
from cassi_tipos_prestador_bairros import carrega_tipo_prestador_bairro
from cassi_tipos_prestador_bairros_especialidades_temp import carrega_tipo_prestador_bairro_especialidade_temp

from cassi_municipios_temp import carrega_municipio_temp
from cassi_lista_prestadores import carrega_lista_prestador
import timeit


## Iniciar log

print(datetime.now())
inicio = timeit.default_timer()



#carrega_plano()
#carrega_uf() # 9.37 segundos
#carrega_municipio() # 628.27 segundos
#carrega_bairro() # 2997 segundos

#carrega_tipo_prestador() # 11 segundos
#carrega_tipo_prestador_bairro() # 15558 segundos - 28685 segundos

#carrega_especialidade() # 40 segundos
#carrega_tipo_prestador_bairro_especialidade_temp() # 197901 segundos - 7296 s
# Depois de 74430 segundos deu o seguinte erro
carrega_lista_prestador()
# 10796 segundos - 10.811 tpbe (não valeu)


fim = timeit.default_timer()
print ('duracao: %f' % (fim - inicio))

