create database iotbackend;

use iotbackend;

create table tipos(
	nombre varchar(120),
	UNIQUE(nombre)
)ENGINE=InnoDB;

create table ubicacion(
	nombre varchar(120) not null,
	UNIQUE(nombre)
)ENGINE=InnoDB;

create table unidad(
	nombre varchar(120) not null,
	UNIQUE(nombre)
)ENGINE=InnoDB;

create table usuario(
	nombre_completo varchar(255) not null,
	nombre_cuenta varchar(20) not null,
	pass varchar(255) not null,
	UNIQUE (Nombre_cuenta)
)ENGINE=InnoDB;

create table dispositivo(
	serie varchar(20) not null,
	ubicacion varchar(120) ,
	prioridad integer,
	UNIQUE(serie)
)ENGINE=InnoDB;

create table registro(
	valor varchar(20) not null,
	fecha date not null,
	serie varchar(20),
	unidad varchar(120)
)ENGINE=InnoDB;

create table horario(
	id VARCHAR(5),
	inicio VARCHAR(5),
	termino VARCHAR(5),
	limite INTEGER,

)ENGINE=InnoDB; 

create table timer(
	id VARCHAR(5),
	dias VARCHAR(13),
	serie VARCHAR(20) NOT NULL,
	duracion INTEGER,
	repeticion integer
)ENGINE=InnoDB; 