from utils import busca_pagina, gera_msg_erro, grava_msg_erro, conecta_banco
from cassi_tipos_prestador_bairros_especialidades import busca_tipo_prestador_bairro_especialidade


def grava_lista_prestador(id_tipo_prestador, id_bairro,
                                        id_especialidade, cd_prestador, nm_prestador,
                                        nm_especialidade, nm_logradouro_ampliado,
                                        nm_bairro, nm_municipio, sg_uf, tel_todos):
    '''Grava um registro de prestador no tipo lista no banco de dados

    Parameters
    ----------
    id_tipo_prestador : int
        Identificador do Tipo Prestador.
    id_bairro: int
        Identificador do bairro.
    id_especialidade : int
        Identificador da especialidade.
    cd_prestador : int
        Código do prestador no sistema de origem
    nm_prestador : string
        Nome do prestador
    nm_especialidade : string
        Nome da especialidade
    nm_logradouro_ampliado : string
        Nome do logradouro, número e complemento
    nm_bairro : string
        Nome do bairro
    nm_municipio : string
        Nome do município
    sg_uf : string
        Sigla da UF
    tel_todos : string
        Lista de telefones do prestador separado por |

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
        sql = 'INSERT INTO tb_lista_prestador(id_tipo_prestador, id_bairro, ' \
              'id_especialidade, cd_prestador, nm_prestador, ' \
              'nm_especialidade, nm_logradouro_ampliado, ' \
              'nm_bairro, nm_municipio, sg_uf, nr_telefones) '
        sql += 'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        cursor.execute(sql, (id_tipo_prestador, id_bairro,
                                        id_especialidade, cd_prestador, nm_prestador,
                                        nm_especialidade, nm_logradouro_ampliado,
                                        nm_bairro, nm_municipio, sg_uf, tel_todos))
        con.commit()
        con.close()
    except Exception as e:
        erro = 1
        msg_erro = gera_msg_erro(e, f'Falhou na gravação de lista prestador: '
                                    f'id_tipo_prestador: {id_tipo_prestador}, id_bairro: {id_bairro}, '
                                    f'id_especialidade: {id_especialidade}, '
                                    f'cd_prestador: {cd_prestador}')

    return erro, msg_erro


def carrega_lista_prestador():
    erro, msg_erro, prestador_bairro_especialidade = busca_tipo_prestador_bairro_especialidade()

    if erro:
        # Salva log de erro
        grava_msg_erro(msg_erro)
        return

    for pbe in prestador_bairro_especialidade:
        id_plano = pbe[0]
        id_uf = pbe[2]
        id_cidade = pbe[3]
        id_bairro = pbe[5]
        bairro = pbe[6]
        id_tipo_prestador = pbe[7]
        cd_tipo_prestador = pbe[8]
        id_especialidade = pbe[10]
        cd_especialidade = pbe[11]


        URL = 'https://www.redecredenciada.mobi/mobile-guia/v2/ws-busca.php'
        parametros = {'id_operadora': 19, 'id_plano': id_plano,
                      'id_estado': id_uf, 'id_cidade': id_cidade,
                      'bairro': bairro, 'id_tipo_prestador': cd_tipo_prestador,
                      'id_especialidade': cd_especialidade, 'regiao_tipo': 'endereco',
                      'utiliza_secoes': 'N', 'agrupa_espec': 'N',
                      'formatacao_texto': '2', 'paged': '0'}
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
            prestadores = bs.find_all('table', {'class': 'resultados-lista'})
            if prestadores is None:
                prestadores = bs.find_all('table', {'class': 'resultados-lista '})

            for prestador in prestadores:
                cd_prestador = prestador.get('data-id')

                nome = prestador.find('h5')
                if nome is not None:
                    nm_prestador = nome.text.strip()
                else:
                    nm_prestador = ''

                especialidade = prestador.find("span", {"class": "color-2"})
                if especialidade is not None:
                    nm_especialidade = especialidade.text.strip()
                else:
                    nm_especialidade = ''
                tel_todos = ''
                telefones = prestador.find('div', {'class': 'telefones'}).find_all('p')
                if telefones is not None:
                    for telefone in telefones:
                        if tel_todos == '':
                            tel_todos += f'{telefone.span.text}'
                        else:
                            tel_todos += f'|{telefone.span.text}'

                endereco = prestador.find('h6')
                if endereco is not None:
                    nm_logradouro_ampliado = endereco.text.strip()
                else:
                    nm_logradouro_ampliado = ''

                bairro = endereco.next_sibling.next_sibling
                nm_bairro = bairro.span.text

                mun_uf = bairro.next_sibling.next_sibling.span.text
                nm_municipio = mun_uf.split('/')[0]
                sg_uf = mun_uf.split('/')[1]

                # print(cd_prestador)
                # print(nome)
                # print(especialidade)
                # print(f'Nome: {nm_prestador}, especialidade: {nm_especialidade}')
                # print(tel_todos)
                # print(nm_logradouro_ampliado)
                # print(nm_bairro)
                # print(f'{nm_municipio}/{sg_uf}')

                erro, msg_erro = grava_lista_prestador(id_tipo_prestador, id_bairro,
                                        id_especialidade, cd_prestador, nm_prestador,
                                        nm_especialidade, nm_logradouro_ampliado,
                                        nm_bairro, nm_municipio, sg_uf, tel_todos)

        except Exception as e:
            msg_erro = gera_msg_erro(e, 'Falhou na busca montagem dos bairros')
            grava_msg_erro(msg_erro)
            return

        # erro, msg_erro = grava_plano(nome, ans, tipo, status)
        if erro:
            grava_msg_erro(msg_erro)
            return
