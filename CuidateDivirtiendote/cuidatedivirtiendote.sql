CREATE DATABASE IF NOT EXISTS cuidatedivirtiendote;
USE cuidatedivirtiendote;

-- Tabla usuarios
CREATE TABLE IF NOT EXISTS usuarios (
    ID_usuario INT AUTO_INCREMENT PRIMARY KEY,
    Nombre VARCHAR(100) NOT NULL,
    Apellido_paterno VARCHAR(100) NOT NULL,
    Apellido_materno VARCHAR(100) NOT NULL,
    Numero_Telefono VARCHAR(15) NOT NULL,
    Email VARCHAR(100) NOT NULL UNIQUE,
    Contraseña VARCHAR(255) NOT NULL,
    Rol VARCHAR(50) NOT NULL
);

-- Tabla dieta
CREATE TABLE IF NOT EXISTS dieta (
    ID_dieta INT AUTO_INCREMENT PRIMARY KEY,
    Nombre VARCHAR(255) NOT NULL,
    Descripcion TEXT NOT NULL
);

-- Tabla ejercicios
CREATE TABLE IF NOT EXISTS ejercicios (
    ID_ejercicio INT AUTO_INCREMENT PRIMARY KEY,
    Nombre VARCHAR(255) NOT NULL,
    Grupo_muscular VARCHAR(255) NOT NULL,
    Tipo_ejercicio VARCHAR(255) NOT NULL
);
