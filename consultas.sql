--SELECT count(*) from tb_tipo_prestador_bairro
/*
select tu.id_plano, count(*)
from tb_tipo_prestador_bairro_especialidade ttpbe join
	 tb_tipo_prestador_bairro ttpb on (ttpbe.id_tipo_prestador = ttpb.id_tipo_prestador and ttpbe.id_bairro = ttpb.id_bairro) join
	 tb_especialidade te on (te.id_especialidade = ttpbe.id_especialidade) join
	 tb_tipo_prestador ttp on (ttpb.id_tipo_prestador = ttp.id_tipo_prestador) join 
	 tb_bairro tb on (ttpb.id_bairro = tb.id_bairro) join 
	 tb_municipio tm on (tb.id_municipio = tm.id_municipio) join 
	 tb_uf tu on (tm.id_uf = tu.id_uf)
group by tu.id_plano
*/
--select id_plano, count(*) from tb_tipo_prestador_especialidade group by 1
--delete from tb_tipo_prestador_bairro_especialidade;
--commit;
--select * from tb_bairro tb join tb_municipio tm on (tb.id_municipio = tm.id_municipio) where tm.cd_municipio = '1200401'
--select tu.id_plano, count(*)

SELECT te.nm_especialidade,  ttp.nm_tipo_prestador, tb.nm_bairro, tm.nm_municipio, tu.sg_uf,
tu.id_uf, tm.id_municipio, tb.id_bairro, ttp.id_tipo_prestador, te.id_especialidade
from tb_tipo_prestador_bairro_especialidade ttpbe join
	 tb_tipo_prestador_bairro ttpb on (ttpbe.id_tipo_prestador = ttpb.id_tipo_prestador and ttpbe.id_bairro = ttpb.id_bairro) join
	 tb_especialidade te on (te.id_especialidade = ttpbe.id_especialidade) join
	 tb_tipo_prestador ttp on (ttpb.id_tipo_prestador = ttp.id_tipo_prestador) join 
	 tb_bairro tb on (ttpb.id_bairro = tb.id_bairro) join 
	 tb_municipio tm on (tb.id_municipio = tm.id_municipio) join 
	 tb_uf tu on (tm.id_uf = tu.id_uf)
order by tu.id_uf desc, tm.id_municipio desc, tb.id_bairro desc, ttp.id_tipo_prestador desc, te.id_especialidade desc 
--where 1 = 1 and ttpb.id_bairro = 5

--select * from tb_tipo_prestador_bairro_especialidade order by id_bairro desc
--delete from tb_tipo_prestador_bairro_especialidade
--where id_bairro = 24393; --218
--commit;
--select * from tb_uf