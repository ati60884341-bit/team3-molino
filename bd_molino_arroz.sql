-- Base de datos del modulo Control de Humedad de Arroz (Team 3 - Molinos de Lambayeque)
-- Ejecutar completo en MySQL Workbench (rayo / Ctrl+Shift+Enter)

DROP DATABASE IF EXISTS bd_molino_arroz;
CREATE DATABASE bd_molino_arroz CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE bd_molino_arroz;

-- Tabla unica del escenario
CREATE TABLE muestras_arroz (
    id_muestra      INT            NOT NULL AUTO_INCREMENT,
    lote            VARCHAR(20)    NOT NULL,
    variedad        VARCHAR(60)    NOT NULL,
    humedad_grano   DECIMAL(5,2)   NOT NULL,
    registrado_en   TIMESTAMP      NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id_muestra)
) ENGINE=InnoDB;

-- Procedimientos almacenados: listar, buscar, registrar
DELIMITER $$

DROP PROCEDURE IF EXISTS sp_muestras_listar$$
CREATE PROCEDURE sp_muestras_listar()
BEGIN
    SELECT id_muestra, lote, variedad, humedad_grano, registrado_en
    FROM muestras_arroz
    ORDER BY id_muestra DESC;
END$$

DROP PROCEDURE IF EXISTS sp_muestras_buscar$$
CREATE PROCEDURE sp_muestras_buscar(
    IN p_criterio VARCHAR(100)
)
BEGIN
    DECLARE v_termino VARCHAR(102);
    SET v_termino = CONCAT('%', IFNULL(TRIM(p_criterio), ''), '%');

    SELECT id_muestra, lote, variedad, humedad_grano, registrado_en
    FROM muestras_arroz
    WHERE lote LIKE v_termino
       OR variedad LIKE v_termino
    ORDER BY id_muestra DESC;
END$$

DROP PROCEDURE IF EXISTS sp_muestra_registrar$$
CREATE PROCEDURE sp_muestra_registrar(
    IN  p_lote           VARCHAR(20),
    IN  p_variedad       VARCHAR(60),
    IN  p_humedad_grano  DECIMAL(5,2),
    OUT p_id_generado    INT
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;

    START TRANSACTION;

    IF p_lote IS NULL OR TRIM(p_lote) = '' THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'El lote es obligatorio.';
    END IF;

    IF p_variedad IS NULL OR TRIM(p_variedad) = '' THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'La variedad es obligatoria.';
    END IF;

    IF p_humedad_grano IS NULL OR p_humedad_grano < 0 OR p_humedad_grano > 100 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'La humedad del grano debe estar entre 0% y 100%.';
    END IF;

    INSERT INTO muestras_arroz (lote, variedad, humedad_grano)
    VALUES (TRIM(p_lote), TRIM(p_variedad), p_humedad_grano);

    SET p_id_generado = LAST_INSERT_ID();

    COMMIT;
END$$

DELIMITER ;

-- Datos de ejemplo (opcional, se puede borrar)
CALL sp_muestra_registrar('LOTE-2026-001', 'IR-43', 11.20, @id1);
CALL sp_muestra_registrar('LOTE-2026-002', 'Capirona', 13.10, @id2);
CALL sp_muestra_registrar('LOTE-2026-003', 'NIR-1', 15.80, @id3);
