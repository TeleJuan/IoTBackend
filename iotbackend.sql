create database iotbackend;

use iotbackend;

create table tipos(
	Nombre varchar(120),
	UNIQUE(Nombre)
)ENGINE=InnoDB;
create table ubicacion(
	Nombre varchar(120) not null,
	UNIQUE(Nombre)
)ENGINE=InnoDB;
create table unidad(
	Nombre varchar(120) not null,
	UNIQUE(Nombre)
)ENGINE=InnoDB;
create table usuario(
	Nombre_completo varchar(255) not null,
	Nombre_cuenta varchar(20) not null,
	password varchar(255) not null,
	UNIQUE (Nombre_cuenta)
)ENGINE=InnoDB;
create table dispositivo(
	serie varchar(20) not null,
	horario varchar(100),
	ubicacion varchar(120) ,
	UNIQUE(serie)
)ENGINE=InnoDB;
create table registro(
	Valor varchar(20) not null,
	Fecha date not null,
	dispositivo varchar(20),
	unidad varchar(120)
)ENGINE=InnoDB;