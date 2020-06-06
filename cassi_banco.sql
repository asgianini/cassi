------------------------------------------------------------------------------
---------------- SEQUENCES ---------------------------------------------------
------------------------------------------------------------------------------

-- SEQUENCE: public.tb_uf_id_uf_seq

DROP SEQUENCE IF EXISTS public.tb_uf_id_uf_seq;

CREATE SEQUENCE public.tb_uf_id_uf_seq
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 2147483647
    CACHE 1;

ALTER SEQUENCE public.tb_uf_id_uf_seq
    OWNER TO postgres;

-- SEQUENCE: public.tb_municipio_id_municipio_seq

DROP SEQUENCE IF EXISTS public.tb_municipio_id_municipio_seq;

CREATE SEQUENCE public.tb_municipio_id_municipio_seq
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 2147483647
    CACHE 1;

ALTER SEQUENCE public.tb_municipio_id_municipio_seq
    OWNER TO postgres;


-- SEQUENCE: public.tb_bairro_id_bairro_seq

DROP SEQUENCE IF EXISTS public.tb_bairro_id_bairro_seq;

CREATE SEQUENCE public.tb_bairro_id_bairro_seq
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 2147483647
    CACHE 1;

ALTER SEQUENCE public.tb_bairro_id_bairro_seq
    OWNER TO postgres;


-- SEQUENCE: public.tb_especialidade_id_especialidade_seq

DROP IF EXISTS SEQUENCE public.tb_especialidade_id_especialidade_seq;

CREATE SEQUENCE public.tb_especialidade_id_especialidade_seq
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 2147483647
    CACHE 1;

ALTER SEQUENCE public.tb_especialidade_id_especialidade_seq
    OWNER TO postgres;


-- SEQUENCE: public.tb_tipo_prestador_id_tipo_prestador_seq

DROP SEQUENCE public.tb_tipo_prestador_id_tipo_prestador_seq;

CREATE SEQUENCE public.tb_tipo_prestador_id_tipo_prestador_seq
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 2147483647
    CACHE 1;

ALTER SEQUENCE public.tb_tipo_prestador_id_tipo_prestador_seq
    OWNER TO postgres;


------------------------------------------------------------------------------
-------------------TABELAS ---------------------------------------------------
------------------------------------------------------------------------------

-- Table: public.tb_plano

DROP TABLE IF EXISTS public.tb_plano CASCADE;

CREATE TABLE public.tb_plano
(
    id_plano integer NOT NULL,
    nm_plano character varying(100) COLLATE pg_catalog."default" NOT NULL,
    cd_ans character varying(30) COLLATE pg_catalog."default",
    tp_plano character varying(50) COLLATE pg_catalog."default",
    st_plano character varying(100) COLLATE pg_catalog."default",
    CONSTRAINT tb_plano_pkey PRIMARY KEY (id_plano)
)

TABLESPACE pg_default;

ALTER TABLE public.tb_plano
    OWNER to postgres;


-- Table: public.tb_uf

DROP TABLE IF EXISTS public.tb_uf CASCADE;

CREATE TABLE public.tb_uf
(
    id_uf integer NOT NULL DEFAULT nextval('tb_uf_id_uf_seq'::regclass),
    id_plano integer NOT NULL,
    cd_uf integer NOT NULL,
    sg_uf character varying(2) COLLATE pg_catalog."default" NOT NULL,
    nm_uf character varying(50) COLLATE pg_catalog."default" NOT NULL,
    cd_ibge character varying(15) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT pk_uf PRIMARY KEY (id_uf),
    CONSTRAINT fk_uf_plano FOREIGN KEY (id_plano)
        REFERENCES public.tb_plano (id_plano) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE public.tb_uf
    OWNER to postgres;



-- Table: public.tb_municipio

DROP TABLE IF EXISTS public.tb_municipio CASCADE;

CREATE TABLE public.tb_municipio
(
    id_municipio integer NOT NULL DEFAULT nextval('tb_municipio_id_municipio_seq'::regclass),
    id_uf integer NOT NULL,
    cd_municipio character varying(20) COLLATE pg_catalog."default",
    nm_municipio character varying(100) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT pk_municipio PRIMARY KEY (id_municipio),
    CONSTRAINT fk_municipio_uf FOREIGN KEY (id_uf)
        REFERENCES public.tb_uf (id_uf) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
)

TABLESPACE pg_default;

ALTER TABLE public.tb_municipio
    OWNER to postgres;


-- Table: public.tb_bairro

DROP TABLE IF EXISTS public.tb_bairro CASCADE;

CREATE TABLE public.tb_bairro
(
    id_bairro integer NOT NULL DEFAULT nextval('tb_bairro_id_bairro_seq'::regclass),
    id_municipio integer NOT NULL,
    nm_bairro character varying(150) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT pk_bairro PRIMARY KEY (id_bairro),
    CONSTRAINT fk_bairro_municipio FOREIGN KEY (id_municipio)
        REFERENCES public.tb_municipio (id_municipio) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
)

TABLESPACE pg_default;

ALTER TABLE public.tb_bairro
    OWNER to postgres;



-- Table: public.tb_tipo_prestador

DROP TABLE public.tb_tipo_prestador CASCADE;

CREATE TABLE public.tb_tipo_prestador
(
    id_tipo_prestador integer NOT NULL DEFAULT nextval('tb_tipo_prestador_id_tipo_prestador_seq'::regclass),
    id_plano integer NOT NULL,
    cd_tipo_prestador integer NOT NULL,
    nm_tipo_prestador character varying(150) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT pk_tipo_prestador PRIMARY KEY (id_tipo_prestador),
    CONSTRAINT fk_tipo_prestador_plano FOREIGN KEY (id_plano)
        REFERENCES public.tb_plano (id_plano) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE public.tb_tipo_prestador
    OWNER to postgres;



-- Table: public.tb_tipo_prestador_bairro

DROP TABLE IF EXISTS public.tb_tipo_prestador_bairro CASCADE;

CREATE TABLE public.tb_tipo_prestador_bairro
(
    id_tipo_prestador integer NOT NULL,
    id_bairro integer NOT NULL,
    CONSTRAINT pk_tipo_prestador_bairro PRIMARY KEY (id_tipo_prestador, id_bairro),
    CONSTRAINT fk_tipo_prestador_bairro_bairro FOREIGN KEY (id_bairro)
        REFERENCES public.tb_bairro (id_bairro) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT fk_tipo_prestador_bairro_tipo_prestador FOREIGN KEY (id_tipo_prestador)
        REFERENCES public.tb_tipo_prestador (id_tipo_prestador) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE public.tb_tipo_prestador_bairro
    OWNER to postgres;


-- Table: public.tb_especialidade

DROP TABLE IF EXISTS public.tb_especialidade CASCADE;

CREATE TABLE public.tb_especialidade
(
    id_especialidade integer NOT NULL DEFAULT nextval('tb_especialidade_id_especialidade_seq'::regclass),
    cd_especialidade character varying(15) COLLATE pg_catalog."default" NOT NULL,
    nm_especialidade character varying(150) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT pk_especialidade PRIMARY KEY (id_especialidade)
)

TABLESPACE pg_default;

ALTER TABLE public.tb_especialidade
    OWNER to postgres;





