CREATE DATABASE IF NOT EXISTS db;
USE db;

CREATE TABLE IF NOT EXISTS Tari (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nume_tara VARCHAR(255) ,
    latitudine  DOUBLE(8, 3) NOT NULL,
    longitudine   DOUBLE(8, 3) NOT NULL,
    UNIQUE (nume_tara)
);

CREATE TABLE IF NOT EXISTS Orase (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    id_tara INT NOT NULL,
    nume_oras VARCHAR(255),
    latitudine  DOUBLE(8, 3) NOT NULL,
    longitudine  DOUBLE(8, 3) NOT NULL,
    CONSTRAINT UC_Orase UNIQUE (id_tara, nume_oras)
);

CREATE TABLE IF NOT EXISTS Temperaturi (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    valoare  DOUBLE(8, 3) NOT NULL,
    timestamp timestamp(3) NULL DEFAULT CURRENT_TIMESTAMP(3),
    id_oras INT NOT NULL,
    CONSTRAINT Temp UNIQUE (id_oras, timestamp)
);