CREATE SEQUENCE public.pois_id_seq
    INCREMENT 1
    START 13
    MINVALUE 1
    MAXVALUE 2147483647
    CACHE 1;

CREATE TABLE public.pois
(
    id integer NOT NULL DEFAULT nextval('pois_id_seq'::regclass),
    name text COLLATE pg_catalog."default" NOT NULL,
    type text COLLATE pg_catalog."default" NOT NULL,
    condition integer NOT NULL,
    active boolean NOT NULL,
    geom geometry(Point,23700) NOT NULL,
    CONSTRAINT pois_pkey PRIMARY KEY (id)
)