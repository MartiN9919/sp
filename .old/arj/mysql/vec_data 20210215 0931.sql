--
-- Скрипт сгенерирован Devart dbForge Studio for MySQL, Версия 7.3.137.0
-- Домашняя страница продукта: http://www.devart.com/ru/dbforge/mysql/studio
-- Дата скрипта: 15.02.2021 9:31:08
-- Версия сервера: 5.7.28-log
-- Версия клиента: 4.1
--


-- 
-- Отключение внешних ключей
-- 
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;

-- 
-- Установить режим SQL (SQL mode)
-- 
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

-- 
-- Установка кодировки, с использованием которой клиент будет посылать запросы на сервер
--
SET NAMES 'utf8';

--
-- Установка базы данных по умолчанию
--
USE vec_data;

--
-- Удалить таблицу "sys_script"
--
DROP TABLE IF EXISTS sys_script;

--
-- Удалить таблицу "sys_obj"
--
DROP TABLE IF EXISTS sys_obj;

--
-- Удалить таблицу "sys_list_top"
--
DROP TABLE IF EXISTS sys_list_top;

--
-- Удалить таблицу "sys_list_dop"
--
DROP TABLE IF EXISTS sys_list_dop;

--
-- Удалить таблицу "sys_key"
--
DROP TABLE IF EXISTS sys_key;

--
-- Удалить таблицу "sys_id"
--
DROP TABLE IF EXISTS sys_id;

--
-- Удалить таблицу "rel"
--
DROP TABLE IF EXISTS rel;

--
-- Удалить таблицу "owner_users"
--
DROP TABLE IF EXISTS owner_users;

--
-- Удалить таблицу "owner_regions"
--
DROP TABLE IF EXISTS owner_regions;

--
-- Удалить таблицу "owner_lines"
--
DROP TABLE IF EXISTS owner_lines;

--
-- Удалить таблицу "owner_groups"
--
DROP TABLE IF EXISTS owner_groups;

--
-- Удалить таблицу "obj_transport_row"
--
DROP TABLE IF EXISTS obj_transport_row;

--
-- Удалить таблицу "obj_point_row"
--
DROP TABLE IF EXISTS obj_point_row;

--
-- Удалить таблицу "obj_point_col"
--
DROP TABLE IF EXISTS obj_point_col;

--
-- Удалить таблицу "obj_person_p_row"
--
DROP TABLE IF EXISTS obj_person_p_row;

--
-- Удалить таблицу "obj_geometry_row"
--
DROP TABLE IF EXISTS obj_geometry_row;

--
-- Удалить таблицу "obj_geometry_col"
--
DROP TABLE IF EXISTS obj_geometry_col;

--
-- Удалить таблицу "obj_free_row"
--
DROP TABLE IF EXISTS obj_free_row;

--
-- Удалить таблицу "obj_file_row"
--
DROP TABLE IF EXISTS obj_file_row;

--
-- Удалить таблицу "obj_file_col"
--
DROP TABLE IF EXISTS obj_file_col;

--
-- Удалить таблицу "obj_case_row"
--
DROP TABLE IF EXISTS obj_case_row;

--
-- Удалить таблицу "input_groups"
--
DROP TABLE IF EXISTS input_groups;

--
-- Удалить таблицу "input_forms"
--
DROP TABLE IF EXISTS input_forms;

--
-- Удалить таблицу "input_fields"
--
DROP TABLE IF EXISTS input_fields;

--
-- Установка базы данных по умолчанию
--
USE vec_data;

--
-- Создать таблицу "input_fields"
--
CREATE TABLE input_fields (
  id int(11) UNSIGNED NOT NULL AUTO_INCREMENT,
  input_forms_id smallint(6) UNSIGNED DEFAULT NULL,
  title varchar(255) DEFAULT NULL,
  need bit(1) DEFAULT b'0',
  enabled bit(1) DEFAULT b'1',
  descript varchar(255) DEFAULT NULL,
  PRIMARY KEY (id),
  CONSTRAINT ind_form FOREIGN KEY (input_forms_id)
  REFERENCES input_forms (id) ON DELETE CASCADE ON UPDATE CASCADE
)
ENGINE = INNODB
AUTO_INCREMENT = 6
AVG_ROW_LENGTH = 3276
CHARACTER SET utf8
COLLATE utf8_general_ci
ROW_FORMAT = DYNAMIC;

--
-- Создать таблицу "input_forms"
--
CREATE TABLE input_forms (
  id smallint(6) UNSIGNED NOT NULL,
  parent_id smallint(6) UNSIGNED NOT NULL,
  title varchar(50) NOT NULL,
  icon varchar(25) DEFAULT NULL,
  enabled bit(1) DEFAULT b'1',
  descript varchar(255) DEFAULT NULL,
  PRIMARY KEY (id)
)
ENGINE = INNODB
AVG_ROW_LENGTH = 862
CHARACTER SET utf8
COLLATE utf8_general_ci
ROW_FORMAT = DYNAMIC;

--
-- Создать таблицу "input_groups"
--
CREATE TABLE input_groups (
  input_forms_id smallint(6) UNSIGNED NOT NULL,
  owner_groups_id tinyint(4) UNSIGNED NOT NULL,
  PRIMARY KEY (input_forms_id, owner_groups_id),
  CONSTRAINT ind_input_forms FOREIGN KEY (input_forms_id)
  REFERENCES input_forms (id) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT ind_input_groups FOREIGN KEY (owner_groups_id)
  REFERENCES owner_groups (id) ON DELETE CASCADE ON UPDATE CASCADE
)
ENGINE = INNODB
AVG_ROW_LENGTH = 682
CHARACTER SET utf8
COLLATE utf8_general_ci
ROW_FORMAT = DYNAMIC;

--
-- Создать таблицу "obj_case_row"
--
CREATE TABLE obj_case_row (
  id int(11) UNSIGNED NOT NULL,
  key_id smallint(6) UNSIGNED NOT NULL,
  val varchar(255) NOT NULL,
  dat datetime DEFAULT NULL,
  INDEX ind_id (id),
  INDEX ind_id_key (id, key_id)
)
ENGINE = INNODB
AVG_ROW_LENGTH = 2048
CHARACTER SET utf8
COLLATE utf8_general_ci
ROW_FORMAT = DYNAMIC;

--
-- Создать таблицу "obj_file_col"
--
CREATE TABLE obj_file_col (
  id int(11) UNSIGNED NOT NULL,
  type tinyint(4) UNSIGNED DEFAULT NULL,
  path varchar(255) DEFAULT NULL,
  PRIMARY KEY (id)
)
ENGINE = INNODB
CHARACTER SET utf8
COLLATE utf8_general_ci
ROW_FORMAT = DYNAMIC;

--
-- Создать таблицу "obj_file_row"
--
CREATE TABLE obj_file_row (
  id int(11) UNSIGNED NOT NULL,
  key_id smallint(6) UNSIGNED NOT NULL,
  val varchar(255) NOT NULL,
  dat datetime DEFAULT NULL,
  INDEX ind_id (id),
  INDEX ind_id_key (id, key_id)
)
ENGINE = INNODB
CHARACTER SET utf8
COLLATE utf8_general_ci
ROW_FORMAT = DYNAMIC;

--
-- Создать таблицу "obj_free_row"
--
CREATE TABLE obj_free_row (
  id int(11) UNSIGNED NOT NULL,
  key_id smallint(6) UNSIGNED NOT NULL,
  val varchar(255) NOT NULL,
  dat datetime DEFAULT NULL,
  INDEX ind_id (id),
  INDEX ind_id_key (id, key_id)
)
ENGINE = INNODB
AVG_ROW_LENGTH = 5461
CHARACTER SET utf8
COLLATE utf8_general_ci
ROW_FORMAT = DYNAMIC;

--
-- Создать таблицу "obj_geometry_col"
--
CREATE TABLE obj_geometry_col (
  id int(11) UNSIGNED NOT NULL,
  parent_id int(11) UNSIGNED NOT NULL DEFAULT 0,
  name varchar(25) NOT NULL,
  icon varchar(25) NOT NULL,
  location geometrycollection DEFAULT NULL,
  PRIMARY KEY (id)
)
ENGINE = INNODB
AVG_ROW_LENGTH = 1260
CHARACTER SET utf8
COLLATE utf8_general_ci
ROW_FORMAT = DYNAMIC;

--
-- Создать таблицу "obj_geometry_row"
--
CREATE TABLE obj_geometry_row (
  id int(11) UNSIGNED NOT NULL,
  key_id smallint(6) UNSIGNED NOT NULL,
  val varchar(255) NOT NULL,
  dat datetime DEFAULT NULL,
  INDEX ind_id (id),
  INDEX ind_id_key (id, key_id)
)
ENGINE = INNODB
AVG_ROW_LENGTH = 1638
CHARACTER SET utf8
COLLATE utf8_general_ci
ROW_FORMAT = DYNAMIC;

--
-- Создать таблицу "obj_person_p_row"
--
CREATE TABLE obj_person_p_row (
  id int(11) UNSIGNED NOT NULL,
  key_id smallint(6) UNSIGNED NOT NULL,
  val varchar(255) NOT NULL,
  dat datetime DEFAULT NULL,
  INDEX ind_id (id),
  INDEX ind_id_key (id, key_id)
)
ENGINE = INNODB
CHARACTER SET utf8
COLLATE utf8_general_ci
ROW_FORMAT = DYNAMIC;

--
-- Создать таблицу "obj_point_col"
--
CREATE TABLE obj_point_col (
  id int(11) UNSIGNED NOT NULL,
  lat double DEFAULT NULL,
  lon double DEFAULT NULL,
  address tinytext DEFAULT NULL COMMENT 'адрес',
  PRIMARY KEY (id),
  INDEX IDX_id (id)
)
ENGINE = INNODB
AVG_ROW_LENGTH = 2520
CHARACTER SET utf8
COLLATE utf8_general_ci
ROW_FORMAT = DYNAMIC;

--
-- Создать таблицу "obj_point_row"
--
CREATE TABLE obj_point_row (
  id int(11) UNSIGNED NOT NULL,
  key_id smallint(6) UNSIGNED NOT NULL,
  val varchar(255) NOT NULL,
  dat datetime DEFAULT NULL,
  INDEX ind_id (id),
  INDEX ind_id_key (id, key_id)
)
ENGINE = INNODB
CHARACTER SET utf8
COLLATE utf8_general_ci
ROW_FORMAT = DYNAMIC;

--
-- Создать таблицу "obj_transport_row"
--
CREATE TABLE obj_transport_row (
  id int(11) UNSIGNED NOT NULL,
  key_id smallint(6) UNSIGNED NOT NULL,
  val varchar(255) NOT NULL,
  dat datetime DEFAULT NULL,
  INDEX ind_id (id),
  INDEX ind_id_key (id, key_id)
)
ENGINE = INNODB
CHARACTER SET utf8
COLLATE utf8_general_ci
ROW_FORMAT = DYNAMIC;

--
-- Создать таблицу "owner_groups"
--
CREATE TABLE owner_groups (
  id tinyint(4) UNSIGNED NOT NULL,
  owner_regions_id tinyint(4) UNSIGNED NOT NULL,
  owner_lines_id tinyint(4) UNSIGNED NOT NULL,
  title varchar(255) NOT NULL,
  descript varchar(255) DEFAULT NULL,
  PRIMARY KEY (id),
  CONSTRAINT ind_owner_line_id FOREIGN KEY (owner_lines_id)
  REFERENCES owner_lines (id) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT ind_owner_region_id FOREIGN KEY (owner_regions_id)
  REFERENCES owner_regions (id) ON DELETE CASCADE ON UPDATE CASCADE
)
ENGINE = INNODB
AVG_ROW_LENGTH = 364
CHARACTER SET utf8
COLLATE utf8_general_ci
ROW_FORMAT = DYNAMIC;

--
-- Создать таблицу "owner_lines"
--
CREATE TABLE owner_lines (
  id tinyint(4) UNSIGNED NOT NULL,
  parent_id tinyint(4) UNSIGNED NOT NULL,
  title varchar(255) NOT NULL,
  UNIQUE INDEX ind_id (id)
)
ENGINE = INNODB
AVG_ROW_LENGTH = 4096
CHARACTER SET utf8
COLLATE utf8_general_ci
ROW_FORMAT = DYNAMIC;

--
-- Создать таблицу "owner_regions"
--
CREATE TABLE owner_regions (
  id tinyint(4) UNSIGNED NOT NULL,
  parent_id tinyint(4) UNSIGNED NOT NULL,
  title varchar(255) NOT NULL,
  UNIQUE INDEX ind_id (id)
)
ENGINE = INNODB
AVG_ROW_LENGTH = 1489
CHARACTER SET utf8
COLLATE utf8_general_ci
ROW_FORMAT = DYNAMIC;

--
-- Создать таблицу "owner_users"
--
CREATE TABLE owner_users (
  id int(11) NOT NULL,
  owner_groups_id tinyint(4) UNSIGNED DEFAULT NULL,
  enabled bit(1) DEFAULT b'1',
  descript varchar(255) DEFAULT NULL,
  PRIMARY KEY (id),
  CONSTRAINT ind_group FOREIGN KEY (owner_groups_id)
  REFERENCES owner_groups (id) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT ind_user FOREIGN KEY (id)
  REFERENCES vec_django.auth_user (id) ON DELETE CASCADE ON UPDATE CASCADE
)
ENGINE = INNODB
CHARACTER SET utf8
COLLATE utf8_general_ci
ROW_FORMAT = DYNAMIC;

--
-- Создать таблицу "rel"
--
CREATE TABLE rel (
  key_id smallint(6) UNSIGNED NOT NULL,
  dat datetime DEFAULT NULL,
  obj_id_1 tinyint(4) UNSIGNED NOT NULL,
  rec_id_1 int(11) UNSIGNED NOT NULL,
  obj_id_2 tinyint(4) UNSIGNED NOT NULL,
  rec_id_2 int(11) UNSIGNED NOT NULL,
  INDEX ind_key_id (key_id),
  INDEX ind_obj_1 (obj_id_1),
  INDEX ind_obj_2 (obj_id_2),
  INDEX ind_obj_rec_1 (obj_id_1, rec_id_1),
  INDEX ind_obj_rec_2 (obj_id_2, rec_id_2)
)
ENGINE = INNODB
AVG_ROW_LENGTH = 4096
CHARACTER SET utf8
COLLATE utf8_general_ci
ROW_FORMAT = DYNAMIC
PARTITION BY RANGE COLUMNS (`key_id`)
(
PARTITION p10000 VALUES LESS THAN (10000),
PARTITION p20000 VALUES LESS THAN (20000),
PARTITION p30000 VALUES LESS THAN (30000),
PARTITION p40000 VALUES LESS THAN (40000),
PARTITION p50000 VALUES LESS THAN (50000),
PARTITION p60000 VALUES LESS THAN (60000),
PARTITION pmax VALUES LESS THAN (MAXVALUE)
);

--
-- Создать таблицу "sys_id"
--
CREATE TABLE sys_id (
  obj_id tinyint(4) UNSIGNED NOT NULL,
  id int(11) UNSIGNED NOT NULL DEFAULT 0,
  PRIMARY KEY (obj_id),
  CONSTRAINT sys_id__sys_obj FOREIGN KEY (obj_id)
  REFERENCES sys_obj (id) ON DELETE CASCADE ON UPDATE CASCADE
)
ENGINE = INNODB
AVG_ROW_LENGTH = 1820
CHARACTER SET utf8
COLLATE utf8_general_ci
COMMENT = 'Счетчик id объектов'
ROW_FORMAT = DYNAMIC;

--
-- Создать таблицу "sys_key"
--
CREATE TABLE sys_key (
  id smallint(6) UNSIGNED NOT NULL,
  obj_id tinyint(4) UNSIGNED NOT NULL,
  col bit(1) NOT NULL DEFAULT b'0' COMMENT 'таблица COL, иначе таблица ROW',
  need bit(1) NOT NULL DEFAULT b'0' COMMENT 'обязательный ключ',
  type_val enum ('str', 'int', 'float', 'bit', 'data', 'datatime', 'geometry') NOT NULL COMMENT 'тип данных',
  list_id mediumint(9) UNSIGNED DEFAULT NULL,
  name varchar(25) DEFAULT NULL,
  title varchar(50) NOT NULL,
  hint varchar(255) DEFAULT NULL COMMENT 'отображаемая подсказка',
  descript varchar(255) DEFAULT NULL,
  rel_obj_id_1 tinyint(4) UNSIGNED DEFAULT NULL,
  rel_obj_id_2 tinyint(4) UNSIGNED DEFAULT NULL,
  PRIMARY KEY (id),
  UNIQUE INDEX ind_id (id),
  INDEX ind_id_name (obj_id, name),
  CONSTRAINT ind_list FOREIGN KEY (list_id)
  REFERENCES sys_list_top (id) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT ind_obj FOREIGN KEY (obj_id)
  REFERENCES sys_obj (id) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT ind_rel_obj_1 FOREIGN KEY (rel_obj_id_1)
  REFERENCES sys_obj (id) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT ind_rel_obj_2 FOREIGN KEY (rel_obj_id_2)
  REFERENCES sys_obj (id) ON DELETE CASCADE ON UPDATE CASCADE
)
ENGINE = INNODB
AVG_ROW_LENGTH = 2048
CHARACTER SET utf8
COLLATE utf8_general_ci
ROW_FORMAT = DYNAMIC;

--
-- Создать таблицу "sys_list_dop"
--
CREATE TABLE sys_list_dop (
  id mediumint(9) UNSIGNED NOT NULL,
  val varchar(255) NOT NULL,
  dat_from date DEFAULT NULL,
  dat_to date DEFAULT NULL,
  INDEX ind_id (id),
  UNIQUE INDEX ind_id_val (id, val),
  CONSTRAINT ind_id_id FOREIGN KEY (id)
  REFERENCES sys_list_top (id) ON DELETE CASCADE ON UPDATE CASCADE
)
ENGINE = INNODB
AVG_ROW_LENGTH = 117
CHARACTER SET utf8
COLLATE utf8_general_ci
ROW_FORMAT = DYNAMIC;

--
-- Создать таблицу "sys_list_top"
--
CREATE TABLE sys_list_top (
  id mediumint(9) UNSIGNED NOT NULL AUTO_INCREMENT,
  name varchar(25) DEFAULT NULL,
  title varchar(50) DEFAULT NULL,
  strong bit(1) DEFAULT b'0',
  PRIMARY KEY (id),
  UNIQUE INDEX ind_name (name)
)
ENGINE = INNODB
AUTO_INCREMENT = 20
AVG_ROW_LENGTH = 862
CHARACTER SET utf8
COLLATE utf8_general_ci
ROW_FORMAT = DYNAMIC;

--
-- Создать таблицу "sys_obj"
--
CREATE TABLE sys_obj (
  id tinyint(4) UNSIGNED NOT NULL,
  name varchar(15) NOT NULL,
  title varchar(25) NOT NULL,
  title_single varchar(25) NOT NULL,
  icon varchar(25) NOT NULL,
  descript varchar(255) DEFAULT NULL,
  PRIMARY KEY (id)
)
ENGINE = INNODB
AVG_ROW_LENGTH = 1638
CHARACTER SET utf8
COLLATE utf8_general_ci
ROW_FORMAT = DYNAMIC;

--
-- Создать таблицу "sys_script"
--
CREATE TABLE sys_script (
  id smallint(6) UNSIGNED NOT NULL,
  name varchar(50) DEFAULT NULL,
  title varchar(25) DEFAULT NULL,
  text text DEFAULT NULL,
  descript mediumtext DEFAULT NULL,
  enabled bit(1) DEFAULT b'1',
  owner tinyint(4) UNSIGNED DEFAULT NULL,
  PRIMARY KEY (id),
  UNIQUE INDEX ind_name (name)
)
ENGINE = INNODB
AVG_ROW_LENGTH = 2730
CHARACTER SET utf8
COLLATE utf8_general_ci
ROW_FORMAT = DYNAMIC;

-- 
-- Вывод данных для таблицы input_fields
--
INSERT INTO input_fields VALUES
(1, 101, 'Фамилия, имя, отчество', True, True, NULL),
(2, 102, 'Полное наименование', True, True, NULL),
(3, 101, 'Дата рождения', False, True, NULL),
(4, 101, 'Гражданство', False, True, NULL),
(5, 101, 'Пол', True, True, NULL);

-- 
-- Вывод данных для таблицы input_forms
--
INSERT INTO input_forms VALUES
(1, 0, 'Объект', 'fa-folder', True, NULL),
(2, 0, 'Событие / Связь', 'fa-link', True, NULL),
(101, 1, 'Физлицо', 'fa-user', True, NULL),
(102, 1, 'Юрлицо', 'fa-stamp', True, NULL),
(103, 1, 'Транспорт', 'fa-car', True, NULL),
(104, 1, 'Дело', 'fa-lock', True, NULL),
(105, 1, 'Точка', 'fa-map-marker-alt', True, NULL),
(106, 1, 'Геометрия', 'fa-draw-polygon', True, NULL),
(107, 1, 'Файл', 'fa-file', True, NULL),
(108, 1, 'Документ', 'fa-align-left', True, NULL),
(200, 2, 'ОРД', 'fa-folder', True, NULL),
(300, 2, 'Административка', 'fa-folder', True, NULL),
(400, 2, 'Погранконтроль', 'fa-folder', True, NULL),
(2001, 200, 'ДОУ', 'fa-bomb', True, NULL),
(2002, 200, 'Сигнальная подборка', 'fa-info', True, NULL),
(3001, 300, 'НГГ', 'fa-angry', True, NULL),
(3002, 300, 'ТМЦ', 'fa-dollar-sign', True, NULL),
(3003, 300, 'Мигранты', 'fa-running', True, NULL),
(3004, 300, 'Наркотики', 'fa-syringe', True, NULL),
(3005, 300, 'Оружие', 'fa-bomb', True, NULL),
(4001, 400, 'Пересечение границы', 'fa-grip-lines', True, NULL);

-- 
-- Вывод данных для таблицы input_groups
--
INSERT INTO input_groups VALUES
(1, 22),
(2, 22),
(101, 22),
(102, 22),
(103, 22),
(104, 22),
(105, 22),
(106, 22),
(107, 22),
(108, 22),
(101, 23),
(102, 23),
(101, 24),
(102, 24),
(101, 25),
(102, 25),
(101, 32),
(102, 32),
(101, 33),
(102, 33),
(101, 34),
(102, 34),
(101, 35),
(102, 35);

-- 
-- Вывод данных для таблицы obj_case_row
--
INSERT INTO obj_case_row VALUES
(30, 45502, 'ДОУ', NULL),
(30, 45505, 'Описание и только', NULL),
(31, 45502, 'УД', NULL),
(31, 45505, 'Описание 2', NULL),
(32, 45502, 'АД', NULL),
(32, 45505, 'Описание 3', NULL),
(33, 45502, 'АД', NULL),
(33, 45505, 'Описание 4', NULL);

-- 
-- Вывод данных для таблицы obj_file_col
--
-- Таблица vec_data.obj_file_col не содержит данных

-- 
-- Вывод данных для таблицы obj_file_row
--
-- Таблица vec_data.obj_file_row не содержит данных

-- 
-- Вывод данных для таблицы obj_free_row
--
INSERT INTO obj_free_row VALUES
(30, 80, 'val 1', '2020-01-01 00:00:00'),
(30, 80, 'val 2', '2020-01-02 00:00:00'),
(30, 80, 'val 3', '2020-02-02 00:00:00');

-- 
-- Вывод данных для таблицы obj_geometry_col
--
INSERT INTO obj_geometry_col VALUES
(30, 0, 'Группа 0', 'fa-folder', NULL),
(31, 0, 'Группа 1', 'fa-folder', NULL),
(32, 30, 'Группа 11', 'fa-folder', NULL),
(41, 32, 'Тест 41', 'fa-lock', GeomFromWKB(x'01070000000100000001030000000100000004000000CDCCCCCCCC3C42401D5A643BDFCF4D4014AE47E17A444540B29DEFA7C61B4D4066666666669646403D0AD7A370BD4E40CDCCCCCCCC3C42401D5A643BDFCF4D40')),
(42, 30, 'Тест 41', 'fa-lock', GeomFromWKB(x'010700000001000000010300000001000000040000009A99999999793A401D5A643BDFCF4D4014AE47E17A444040B29DEFA7C61B4D4066666666669641403D0AD7A370BD4E409A99999999793A401D5A643BDFCF4D40')),
(51, 0, 'Тест 51', 'fa-lock', GeomFromWKB(x'01070000000300000001010000007A6F0C01C0253A40986BD102B4114B400103000000010000000E00000043C879FF1FD73740CF31207BBD9D4A40572250FD83183840E59CD843FBAA4A40AE2EA704C4503840F52F49658ABB4A400551F701488138409085E81038DA4A408978EBFCDB6538401F80D4264EF24A40D4635B069C2D384061DF4E22C2F94A403D0E83F92BF83740C8EC2C7AA7F64A408527F4FA93CC37402E56D4601AF84A402F6EA301BC953740F419506F46F74A4072361D01DC843740D6A9F23D23F94A40D0285DFA978C3740F1F3DF83D7EA4A400F09DFFB1B90374029E9616875E04A400B0BEE073CAC374038F4160FEFBF4A4043C879FF1FD73740CF31207BBD9D4A4001010000001842CEFBFFC8384094347F4C6BDF4A40')),
(52, 0, 'Тест 52', 'fa-lock', GeomFromWKB(x'01070000000300000001030000000100000006000000F4DE180280DF3840A52C431CEB044B401842CEFBFFC8384053B131AF230C4B40E1ED4108C84B3940C347C494480A4B40381092054C7C39400229B16B7BF74A40E8BD310400233940E0F3C308E1EB4A40F4DE180280DF3840A52C431CEB044B40010300000001000000060000001842CEFBFF303A400ADAE4F049954B40454772F90F4D3B40EF552B137E214C40A5F5B704E06B3D409C8713984EB94B40D3FA5B02F06B3C404D9EB29AAE934B409032E202D0C83B408995D1C8E7794B401842CEFBFF303A400ADAE4F049954B40010200000009000000622D3E05C0F839408274B169A5FC4B40B39597FC4F4A3A40E69315C3D5234C40E19A3BFA5FB23A408849B89047104C40DF1B4300700C3A4022A81ABD1ABA4B409ED2C1FA3F0F3A404E0E9F74227D4B40C9586DFE5F393B4079E8BB5B59324B40622D3E05C0143C40ECDE8AC4041D4B4099D4D00660AF3D403C8386FE094A4B407CEE04FBAFB73F4078094E7D205B4B40')),
(53, 0, 'Тест 53', 'fa-lock', GeomFromWKB(x'010700000002000000010300000001000000050000009032E202D0F83840E44C13B69F544B40EDBB22F8DF063940F06C8FDE70734B400000000000043A40F9F5436CB0584B402463B5F97FED39405F7F129F3B254B409032E202D0F83840E44C13B69F544B40010300000001000000050000009032E202D0F83840EF552B137E214C40E19A3BFA5FFE39409EEDD11BEE1F4C40672B2FF99F903A4064EB19C231F34B4099D4D006602B3A406902452C62D04B409032E202D0F83840EF552B137E214C40')),
(54, 0, 'Тест 54', 'fa-lock', GeomFromWKB(x'0107000000030000000103000000010000000800000016C3D50110A73B4015E63DCE34FB4A406B662D05A4E53B40DB5207793DF64A404D6A6803B0D93B40FBE6FEEA71E54A40E1ED4108C8673B408C82E0F1EDD74A402F6EA301BC193B40709692E524E84A4052D158FB3B033B4064744012F6FF4A400BB8E7F9D32E3B4008AEF204C20C4B4016C3D50110A73B4015E63DCE34FB4A40010200000005000000C7D9740470933A40AF5C6F9BA91E4B407CEE04FBAF7F3B4052103CBEBD4F4B40880FECF82FF03B40200BD12170164B40DF1B430070DC3C40AF5C6F9BA91E4B407A6F0C01C0F53C408907944DB9F84A400101000000F25F200890553A40D28BDAFD2A004B40')),
(55, 0, 'Тест 55', 'fa-lock', GeomFromWKB(x'0107000000030000000101000000DC9C4A068066394031CD74AF93564A40010200000004000000F65D11FC6F393A40DF878384281D4A4078F01307D0333A40A27C410B09764A40BD378600E0303C4063096B63EC2A4A40D57954FCDFF53A40DF878384281D4A40010300000001000000040000009ED2C1FA3F5B3940CAFCA36FD2E44A404D6A6803B0253B405F7F129F3B254B40BFB67EFACFBA3A405D19541B9CB84A409ED2C1FA3F5B3940CAFCA36FD2E44A40')),
(56, 0, 'Тест 56', 'fa-lock', GeomFromWKB(x'010700000002000000010300000001000000060000001C7DCC0704B6384050AA7D3A1E354A405E6743FE9901394050AA7D3A1E354A405E6743FE990139405A2DB0C744444A40172CD505BCD038404E621058393E4A401C7DCC0704B638405A2DB0C744444A401C7DCC0704B6384050AA7D3A1E354A40010100000064AC36FFAF8238405E0EBBEF18704A40')),
(57, 0, 'Тест 57', 'fa-lock', GeomFromWKB(x'010700000002000000010100000043C879FF1F5B3B4043E6CAA0DA4A4B4001030000000100000004000000560C570740F03A40DCF0BBE996CF4B40F25F200890713C4041F0F8F6AEBF4B408411FB04500C3C40ADF9F19716314C40560C570740F03A40DCF0BBE996CF4B40')),
(58, 0, 'Тест 58', 'fa-lock', GeomFromWKB(x'0107000000030000000102000000050000009702D2FE07383A40267156444D304B40BA6587F887213A40E961687572FC4A40E19A3BFA5F9638401B2E724F57F34A40C9586DFE5F1D3940A2B77878CF534B407CEE04FBAF173A40E8DEC325C76D4B400103000000010000000400000070CD1DFD2FF338404487C09140094B40D07B630800AA3940742502D53F404B40469A780778E63940252026E142104B4070CD1DFD2FF338404487C09140094B400101000000672B2FF99F903A4089247A19C5224B40'));

-- 
-- Вывод данных для таблицы obj_geometry_row
--
INSERT INTO obj_geometry_row VALUES
(41, 81, '5', NULL),
(42, 81, '-1', NULL),
(51, 81, '0.05', NULL),
(52, 81, '50', NULL),
(53, 81, '-5', NULL),
(54, 81, '100', NULL),
(55, 81, '0', NULL),
(56, 81, '20', NULL),
(57, 81, '-3', NULL),
(58, 81, '4', NULL);

-- 
-- Вывод данных для таблицы obj_person_p_row
--
-- Таблица vec_data.obj_person_p_row не содержит данных

-- 
-- Вывод данных для таблицы obj_point_col
--
INSERT INTO obj_point_col VALUES
(33, 52.0839356, 23.650415, 'Брест, ул.Русакова,124'),
(34, 54.4773572, 26.3932509, 'Сморгонь, ул.Белинского,124'),
(35, 55.4798043, 28.7796702, 'Полоцк, ул.Софии Полоцкой, 3'),
(36, 53.8870722, 27.962096, 'Самолеты Минск'),
(37, 53.2628595, 23.8672983, 'Нижний Новгород, 40 лет Победы ул., 7'),
(38, 53.2255994, 23.8739022, 'Нижний Новгород, 60-летия Октября б-р, 2а, САЮС'),
(39, 53.2241874, 23.8191839, 'Нижний Новгород, Агрономов ул, 77'),
(40, 53.2490319, 24.0470196, 'Нижний Новгород, Адмирала Макарова ул., 16-40'),
(41, 52.8521343, 23.9992328, 'Нижний Новгород, Акимова ул., 50'),
(42, 52.8345252, 23.9736483, 'Нижний Новгород, Алексеевская ул., 1'),
(43, 52.8685392, 24.1087106, 'Нижний Новгород, Алексеевская ул., 6/16'),
(44, 53.9232459, 24.466538, 'Нижний Новгород, Алексеевская ул., 8а1'),
(45, 53.7653914, 24.3036483, 'Нижний Новгород, Анкудиновское ш, 184'),
(46, 53.3524766, 24.7062152, 'Нижний Новгород, Анкудиновское ш, 3а'),
(47, 54.8527277, 27.0920334, 'Нижний Новгород, Анкудиновское ш, 85'),
(48, 55.5022909, 27.939888, 'Нижний Новгород, Аральская ул., 23'),
(49, 54.7061863, 30.5381097, 'Нижний Новгород, Артельная ул., 3'),
(50, 53.7793249, 30.3136429, 'Нижний Новгород, Артемовская ул., 30'),
(51, 52.3222736, 30.2990905, 'Нижний Новгород, Аэропорт ул., 1'),
(52, 52.3162907, 28.5324098, 'Нижний Новгород, Б. Корнилова ул., 5/1'),
(53, 52.3969908, 28.3072926, 'Нижний Новгород, Б. Корнилова ул., 6/1'),
(54, 53.6174398, 27.9788652, '<strong>НГГ</strong><br />ушел и не поймали'),
(55, 53.4621, 26.9469, 'Тест 1'),
(56, 53.4506, 26.8133, 'Тест 2'),
(57, 53.4718, 26.6726, 'Тест 3'),
(58, 53.5038, 26.9488, 'Тест 4');

-- 
-- Вывод данных для таблицы obj_point_row
--
-- Таблица vec_data.obj_point_row не содержит данных

-- 
-- Вывод данных для таблицы obj_transport_row
--
-- Таблица vec_data.obj_transport_row не содержит данных

-- 
-- Вывод данных для таблицы owner_groups
--
INSERT INTO owner_groups VALUES
(1, 1, 1, 'Администратор', '!!!'),
(22, 2, 2, 'ГПК А', NULL),
(23, 2, 3, 'ГПК О', NULL),
(24, 2, 4, 'ГПК И', NULL),
(25, 2, 5, 'ГПКД', NULL),
(32, 3, 2, 'Полоцк А', NULL),
(33, 3, 3, 'Полоцк О', NULL),
(34, 3, 4, 'Полоцк И', NULL),
(35, 3, 5, 'Полоцк Д', NULL),
(42, 4, 2, 'Сморгонь А', NULL),
(43, 4, 3, 'Сморгонь О', NULL),
(44, 4, 4, 'Сморгонь И', NULL),
(45, 4, 5, 'Сморгонь Д', NULL),
(52, 5, 2, 'Лида А', NULL),
(53, 5, 3, 'Лида О', NULL),
(54, 5, 4, 'Лида И', NULL),
(55, 5, 5, 'Лида Д', NULL),
(62, 6, 2, 'Гродно А', NULL),
(63, 6, 3, 'Гродно О', NULL),
(64, 6, 4, 'Гродно И', NULL),
(65, 6, 5, 'Гродно Д', NULL),
(72, 7, 2, 'Брест А', NULL),
(73, 7, 3, 'Брест О', NULL),
(74, 7, 4, 'Брест И', NULL),
(75, 7, 5, 'Брест Д', NULL),
(82, 8, 2, 'Пинск А', NULL),
(83, 8, 3, 'Пинск О', NULL),
(84, 8, 4, 'Пинск И', NULL),
(85, 8, 5, 'Пинск Д', NULL),
(92, 9, 2, 'Мозырь А', NULL),
(93, 9, 3, 'Мозырь О', NULL),
(94, 9, 4, 'Мозырь И', NULL),
(95, 9, 5, 'Мозырь Д', NULL),
(102, 10, 2, 'Гомель А', NULL),
(103, 10, 3, 'Гомель О', NULL),
(104, 10, 4, 'Гомель И', NULL),
(105, 10, 5, 'Гомель Д', NULL),
(112, 11, 2, 'ОП А', NULL),
(113, 11, 3, 'ОП О', NULL),
(114, 11, 4, 'ОП И', NULL),
(115, 11, 5, 'ОП Д', NULL),
(122, 12, 2, 'ОС А', NULL),
(123, 12, 3, 'ОС О', NULL),
(124, 12, 4, 'ОС И', NULL),
(125, 12, 5, 'ОС Д', NULL);

-- 
-- Вывод данных для таблицы owner_lines
--
INSERT INTO owner_lines VALUES
(1, 0, 'Администратор'),
(2, 1, 'a'),
(3, 2, 'o'),
(4, 2, 'i'),
(5, 2, 'd');

-- 
-- Вывод данных для таблицы owner_regions
--
INSERT INTO owner_regions VALUES
(1, 0, 'Администратор'),
(2, 1, 'ГПК'),
(3, 2, 'Полоцк'),
(4, 2, 'Сморгонь'),
(5, 2, 'Лида'),
(6, 2, 'Гродно'),
(7, 2, 'Брест'),
(8, 2, 'Пинск'),
(9, 2, 'Мозырь'),
(10, 2, 'Гомель'),
(11, 2, 'ОП'),
(12, 2, 'ОС');

-- 
-- Вывод данных для таблицы owner_users
--
INSERT INTO owner_users VALUES
(1, 1, True, NULL);

-- 
-- Вывод данных для таблицы rel
--
INSERT INTO rel VALUES
(32, NULL, 25, 38, 45, 30),
(32, NULL, 25, 39, 45, 33),
(32, NULL, 25, 40, 45, 32),
(32, NULL, 25, 41, 45, 32),
(32, NULL, 25, 42, 45, 32),
(33, '2020-04-15 00:00:00', 25, 33, 45, 33),
(33, '2020-05-04 00:00:00', 25, 34, 45, 30),
(33, '2020-01-23 00:00:00', 25, 35, 45, 31),
(33, '2020-06-03 00:00:00', 25, 36, 45, 33),
(33, '2020-07-03 00:00:00', 25, 37, 45, 31),
(32, '2020-01-07 00:00:00', 25, 43, 45, 30),
(34, '2020-01-08 00:00:00', 25, 44, 45, 31),
(34, '2020-01-08 00:00:00', 25, 45, 45, 33),
(34, '2020-04-10 00:00:00', 25, 46, 45, 31),
(34, '2020-01-10 00:00:00', 25, 47, 45, 30),
(34, '2020-01-10 00:00:00', 25, 48, 45, 31),
(35, '2020-02-21 00:00:00', 25, 49, 45, 32),
(35, '2020-05-12 00:00:00', 25, 50, 45, 33),
(35, '2020-01-13 00:00:00', 25, 51, 45, 30),
(35, '2020-01-23 00:00:00', 25, 52, 45, 33),
(35, '2020-07-13 00:00:00', 25, 53, 45, 30),
(36, '2020-02-14 00:00:00', 25, 54, 45, 31),
(36, '2020-01-14 00:00:00', 25, 55, 45, 32),
(36, '2020-03-14 00:00:00', 25, 56, 45, 33),
(36, '0000-00-00 00:00:00', 25, 57, 45, 32),
(36, '2020-01-14 00:00:00', 25, 58, 45, 31),
(41, '2020-05-01 00:00:00', 30, 42, 45, 31),
(41, '2020-05-05 00:00:00', 30, 52, 45, 31),
(41, '2020-05-06 00:00:00', 30, 53, 45, 31),
(41, '2020-05-07 00:00:00', 30, 54, 45, 33),
(41, '2020-05-01 00:00:00', 30, 55, 45, 33),
(42, '2020-05-02 00:00:00', 30, 55, 45, 31),
(42, '2020-05-08 00:00:00', 30, 56, 45, 31),
(42, '2020-05-09 00:00:00', 30, 57, 45, 32),
(42, '2020-05-02 00:00:00', 30, 58, 45, 33),
(43, '2020-05-03 00:00:00', 30, 52, 45, 31),
(43, '2020-05-04 00:00:00', 30, 56, 45, 32);

-- 
-- Вывод данных для таблицы sys_id
--
INSERT INTO sys_id VALUES
(10, 32),
(15, 130),
(20, 0),
(25, 0),
(30, 26),
(35, 0),
(40, 0),
(45, 0),
(50, 0);

-- 
-- Вывод данных для таблицы sys_key
--
INSERT INTO sys_key VALUES
(31, 1, False, False, 'int', NULL, 'photo_panorama', 'photo_panorama', NULL, NULL, NULL, NULL),
(32, 1, False, False, 'int', NULL, 'ngg_smoke', 'ngg_smoke', NULL, NULL, NULL, NULL),
(33, 1, False, False, 'int', NULL, 'ngg_migrate', 'ngg_migrate', NULL, NULL, NULL, NULL),
(34, 1, False, False, 'int', NULL, 'ngg_tmc', 'ngg_tmc', NULL, NULL, NULL, NULL),
(35, 1, False, False, 'int', NULL, 'ngg_opg', 'ngg_opg', NULL, NULL, NULL, NULL),
(36, 1, False, False, 'int', NULL, 'ngg_npr', 'ngg_npr', NULL, NULL, NULL, NULL),
(41, 1, False, False, 'int', NULL, 'arial_1', 'arial_1', NULL, NULL, NULL, NULL),
(42, 1, False, False, 'int', NULL, 'arial_2', 'arial_2', NULL, NULL, NULL, NULL),
(43, 1, False, False, 'int', NULL, 'arial_3', 'arial_3', NULL, NULL, NULL, NULL),
(80, 10, False, False, 'str', NULL, 'test_free_30', 'test_free_30', NULL, NULL, NULL, NULL),
(81, 30, False, False, 'int', NULL, 'test_geo_color', 'test_geo_color', NULL, NULL, NULL, NULL),
(501, 1, False, False, 'str', NULL, NULL, 'Дело/объединение', NULL, NULL, 45, NULL),
(502, 1, False, False, 'str', NULL, NULL, 'Дело/выделение', NULL, NULL, 45, NULL),
(506, 1, False, False, 'str', NULL, NULL, 'Дело/принятие к производству', NULL, NULL, 45, 35),
(1001, 1, False, False, 'int', NULL, NULL, 'ДОУ/оперативная категория лица/организатор', NULL, NULL, 35, 45),
(1002, 1, False, False, 'int', NULL, NULL, 'ДОУ/оперативная категория лица/исполнитель', NULL, NULL, 35, 45),
(1003, 1, False, False, 'int', NULL, NULL, 'ДОУ/оперативная категория лица/пособник', NULL, NULL, 35, 45),
(1101, 1, False, False, 'int', NULL, NULL, 'Задержание (КоАП)/начало', NULL, NULL, 35, 45),
(1102, 1, False, False, 'int', NULL, NULL, 'Задержание (УПК)/начало', NULL, NULL, 35, 45),
(1201, 1, False, False, 'int', NULL, NULL, 'Авто ФЛ/владение/начало', NULL, NULL, 35, 50),
(1202, 1, False, False, 'int', NULL, NULL, 'Авто ФЛ/владение/конец', NULL, NULL, 35, 50),
(1301, 1, False, False, 'int', NULL, NULL, 'Учеба/поступление', NULL, NULL, 35, 40),
(1302, 1, False, False, 'int', NULL, NULL, 'Учеба/отчисление', NULL, NULL, 35, 40),
(1303, 1, False, False, 'int', NULL, NULL, 'Учеба/завершение', NULL, NULL, 35, 40),
(1304, 1, False, True, 'int', NULL, NULL, 'Работа/начало', NULL, NULL, 35, 40),
(1305, 1, False, False, 'int', NULL, NULL, 'Работа/конец', NULL, NULL, 35, 40),
(1306, 1, False, False, 'str', NULL, NULL, 'Отпуск/начало', NULL, NULL, 35, 40),
(1307, 1, False, False, 'str', NULL, NULL, 'Отпуск/конец', NULL, NULL, 35, 40),
(10000, 10, False, False, 'int', NULL, 'owner_add_rw', 'Владелец: добавить чтение/запись', NULL, '! СПЕЦИАЛЬНЫЙ КЛЮЧ !', NULL, NULL),
(10001, 10, False, False, 'int', NULL, 'owner_add_ro', 'Владелец: добавить только чтение', NULL, '! СПЕЦИАЛЬНЫЙ КЛЮЧ !', NULL, NULL),
(10002, 10, False, False, 'int', NULL, 'owner_add_ro_limit', 'Владелец: добавить только чтение на период', NULL, '! СПЕЦИАЛЬНЫЙ КЛЮЧ !', NULL, NULL),
(10003, 10, False, False, 'int', NULL, 'owner_del', 'Владелец: запретить доступ', NULL, '! СПЕЦИАЛЬНЫЙ КЛЮЧ !', NULL, NULL),
(10010, 10, False, False, 'str', NULL, 'test_free_30', 'test_free_30', NULL, NULL, NULL, NULL),
(15000, 15, False, True, 'int', NULL, 'owner_add_rw', 'Владелец: добавить чтение/запись', NULL, '! СПЕЦИАЛЬНЫЙ КЛЮЧ !', NULL, NULL),
(15001, 15, False, False, 'int', NULL, 'owner_add_ro', 'Владелец: добавить только чтение', NULL, '! СПЕЦИАЛЬНЫЙ КЛЮЧ !', NULL, NULL),
(15002, 15, False, False, 'int', NULL, 'owner_add_ro_limit', 'Владелец: добавить только чтение на период', NULL, '! СПЕЦИАЛЬНЫЙ КЛЮЧ !', NULL, NULL),
(15003, 15, False, False, 'int', NULL, 'owner_del', 'Владелец: запретить доступ', NULL, '! СПЕЦИАЛЬНЫЙ КЛЮЧ !', NULL, NULL),
(15010, 15, True, True, 'int', NULL, 'type', 'Тип', NULL, NULL, NULL, NULL),
(15011, 15, True, True, 'str', NULL, 'path', 'Путь', NULL, NULL, NULL, NULL),
(25202, 25, True, False, 'float', NULL, 'lat', 'Широта', NULL, NULL, NULL, NULL),
(25203, 25, True, False, 'float', NULL, 'lon', 'Долгота', NULL, NULL, NULL, NULL),
(25204, 25, True, False, 'str', NULL, 'address', 'Адрес', NULL, NULL, NULL, NULL),
(30301, 30, True, False, 'str', NULL, 'icon', 'Иконка', NULL, NULL, NULL, NULL),
(30302, 30, True, False, 'int', NULL, 'parent_id', 'Группа', NULL, NULL, NULL, NULL),
(30303, 30, True, False, 'str', NULL, 'name', 'Название', NULL, NULL, NULL, NULL),
(30304, 30, True, False, 'geometry', NULL, 'location', 'Локация', NULL, NULL, NULL, NULL),
(35001, 35, True, True, 'str', NULL, 'fio', 'ФИО', 'Фамилия, имя, отчество', NULL, NULL, NULL),
(35002, 35, True, False, 'data', NULL, 'birth_day', 'Дата рождения', NULL, NULL, NULL, NULL),
(35003, 35, True, False, 'bit', 2, 'sex', 'Пол', NULL, NULL, NULL, NULL),
(35004, 35, True, True, 'str', 1, 'citizenship', 'Гражданство', NULL, NULL, NULL, NULL),
(35005, 35, True, False, 'str', 19, 'nationality', 'Национальность', NULL, NULL, NULL, NULL),
(35006, 35, False, False, 'bit', NULL, 'photo ??????', 'Фото лица', NULL, 'В свзяь', NULL, NULL),
(35007, 35, True, False, 'str', NULL, 'birth_place', 'Место рождения', NULL, NULL, NULL, NULL),
(35008, 35, False, False, 'str', NULL, 'residence', 'Место жительства', NULL, 'В свзяь', NULL, NULL),
(35009, 35, False, False, 'str', NULL, 'work????', 'Место работы', NULL, 'В свзяь', NULL, NULL),
(35010, 35, False, False, 'str', NULL, 'ident_doc', 'ID-документ', NULL, NULL, NULL, NULL),
(35011, 35, False, False, 'bit', NULL, 'migrant', 'Незаконный мигрант', NULL, 'В свзяь', NULL, NULL),
(35012, 35, False, False, 'str', NULL, 'fio_dop', 'ФИО доп', NULL, NULL, NULL, NULL),
(35013, 35, False, False, 'str', NULL, 'status_social', 'Социальное положение', NULL, NULL, NULL, NULL),
(35014, 35, False, False, 'str', NULL, 'status_marital', 'Семейное положение', NULL, 'словарь', NULL, NULL),
(35015, 35, True, False, 'str', 3, 'education', 'Образование', NULL, NULL, NULL, NULL),
(35016, 35, False, False, 'str', NULL, 'public_association', 'Принадлежность к партиям', NULL, NULL, NULL, NULL),
(35017, 35, False, False, 'str', NULL, 'language_skills', 'Знание иностранных языков', NULL, 'словарь', NULL, NULL),
(35020, 35, False, False, 'str', NULL, 'conviction????', 'Судимость', NULL, 'словарь', NULL, NULL),
(35021, 35, False, False, 'str', NULL, 'alias', 'Псевдоним (кличка)', NULL, NULL, NULL, NULL),
(35022, 35, False, False, 'str', NULL, 'special_signs', 'Особые приметы', NULL, NULL, NULL, NULL),
(35023, 35, False, False, 'str', NULL, NULL, 'ОПС: подразделение', NULL, NULL, NULL, NULL),
(35997, 35, False, False, 'str', NULL, 'position', 'ОПС/Должность', 'Только для сотрудников ОПС', 'словарь+ушел', NULL, NULL),
(35998, 35, False, False, 'str', NULL, NULL, 'ОПС/Структурное подразделение', NULL, 'словарь+ушел', NULL, NULL),
(35999, 35, False, False, 'str', NULL, 'rank', 'ОПС/Воинское звание', NULL, 'словарь', NULL, NULL),
(40101, 40, True, True, 'str', NULL, 'name', 'Название полное', NULL, NULL, NULL, NULL),
(40102, 40, False, False, 'str', NULL, 'address', 'Юридический адрес ', NULL, NULL, NULL, NULL),
(40103, 40, False, False, 'str', NULL, 'name_dop', 'Название доп', NULL, NULL, NULL, NULL),
(40104, 40, False, False, 'str', NULL, 'type', 'Вид', NULL, NULL, NULL, NULL),
(40105, 40, False, False, 'str', NULL, 'ownership', 'Форма собственности', NULL, 'словарь', NULL, NULL),
(40106, 40, False, False, 'str', NULL, 'activity', 'Род деятельности', NULL, NULL, NULL, NULL),
(40107, 40, False, False, 'str', NULL, 'descript', 'Оперативная характеристика организации', NULL, NULL, NULL, NULL),
(40108, 40, False, False, 'str', NULL, 'representation', 'Представительство', NULL, NULL, NULL, NULL),
(40109, 40, False, False, 'str', NULL, 'representation????', 'Адрес представительства', NULL, '????', NULL, NULL),
(40110, 40, False, False, 'str', NULL, 'telephone ????', 'Телефон', NULL, '????? связь', NULL, NULL),
(40111, 40, False, False, 'str', NULL, 'transport', 'Транспорт', NULL, '???? связь', NULL, NULL),
(40112, 40, False, False, 'str', NULL, 'source_information', 'Источник сведений', NULL, 'словарь ???? удалить', NULL, NULL),
(40113, 40, False, False, 'bit', NULL, NULL, 'Учебное заведение гражданское', NULL, NULL, NULL, NULL),
(40114, 40, False, False, 'bit', NULL, NULL, 'Учебное заведение военное', NULL, NULL, NULL, NULL),
(45000, 45, False, False, 'int', NULL, 'owner_add_rw', 'Владелец: добавить чтение/запись', NULL, '! СПЕЦИАЛЬНЫЙ КЛЮЧ !', NULL, NULL),
(45001, 45, False, False, 'int', NULL, 'owner_add_ro', 'Владелец: добавить только чтение', NULL, '! СПЕЦИАЛЬНЫЙ КЛЮЧ !', NULL, NULL),
(45002, 45, False, False, 'int', NULL, 'owner_add_ro_limit', 'Владелец: добавить только чтение на период', NULL, '! СПЕЦИАЛЬНЫЙ КЛЮЧ !', NULL, NULL),
(45003, 45, False, False, 'int', NULL, 'owner_del', 'Владелец: запретить доступ', NULL, '! СПЕЦИАЛЬНЫЙ КЛЮЧ !', NULL, NULL),
(45501, 45, False, True, 'str', NULL, 'type', 'Вид дела', NULL, 'словарь ДОУ+УД+АД', NULL, NULL),
(45502, 45, False, False, 'str', NULL, NULL, 'Статья/начало', NULL, 'словарь, сделать словарь окраски и линии', NULL, NULL),
(45503, 45, False, False, 'str', NULL, NULL, 'Статья/конец', NULL, 'словарь', NULL, NULL),
(45505, 45, False, False, 'str', NULL, NULL, 'Описание', NULL, 'Номер, архивный номер, описание, суть материалов, пометки', NULL, NULL),
(45515, 45, False, True, 'str', NULL, NULL, 'Уничтожено', NULL, '? в описание', NULL, NULL),
(45520, 45, False, False, 'str', NULL, NULL, 'Движение/заведение (возбуждение)', NULL, NULL, 45, NULL),
(45521, 45, False, False, 'str', NULL, NULL, 'Движение/продление', NULL, NULL, 45, NULL),
(45522, 45, False, False, 'str', NULL, NULL, 'Движение/приостановление', NULL, NULL, 45, NULL),
(45523, 45, False, False, 'str', NULL, NULL, 'Движение/возобновление', NULL, NULL, 45, NULL),
(45524, 45, False, False, 'str', NULL, NULL, 'Движение/прекращение', NULL, '???', 45, NULL),
(45525, 45, False, False, 'str', NULL, NULL, 'Движение/прекращение основание', NULL, NULL, 45, NULL),
(50001, 50, True, True, 'str', NULL, 'brand', 'Марка', NULL, NULL, NULL, NULL),
(50002, 50, True, False, 'str', NULL, 'model', 'Модель', NULL, NULL, NULL, NULL),
(50004, 50, True, False, 'str', NULL, 'type', 'Вид транспорта', NULL, 'словарь', NULL, NULL),
(50005, 50, True, False, 'str', NULL, 'number', 'Рег.номер', NULL, NULL, NULL, NULL),
(50006, 50, True, False, 'str', NULL, 'category', 'Категория транспорта', NULL, 'словарь', NULL, NULL),
(50007, 50, False, False, 'int', NULL, 'money', 'Сумма оценки', NULL, '?????', NULL, NULL),
(50008, 50, True, False, 'str', NULL, 'country', 'Страна', NULL, 'словарь', NULL, NULL),
(50009, 50, False, False, 'str', NULL, 'photo????', 'Фото автомобиля', NULL, 'В свзяь', NULL, NULL),
(50010, 50, True, False, 'str', NULL, 'vin', 'VIN', NULL, NULL, NULL, NULL),
(50011, 50, True, False, 'int', NULL, 'manufacture', 'Год выпуска', NULL, 'словарь', NULL, NULL),
(50012, 50, False, False, 'int', NULL, 'route???', 'Номер поезда, рейса самолета, автобуса', NULL, '????', NULL, NULL),
(50013, 50, False, False, 'str', NULL, 'route', 'Маршрут поезда, самолета, автобуса', NULL, 'словарь', NULL, NULL),
(50014, 50, False, False, 'int', NULL, 'number_carriage', 'Номер вагона', NULL, NULL, NULL, NULL),
(50015, 50, False, False, 'str', NULL, 'color', 'Цвет', NULL, NULL, NULL, NULL),
(50016, 50, False, False, 'str', NULL, 'measures ????', 'Принятые меры', NULL, 'словарь, ???????', NULL, NULL);

-- 
-- Вывод данных для таблицы sys_list_dop
--
INSERT INTO sys_list_dop VALUES
(1, 'Австралия', NULL, NULL),
(1, 'Австрия', NULL, NULL),
(1, 'Азербайджан', NULL, NULL),
(1, 'Аландские острова', NULL, NULL),
(1, 'Албания', NULL, NULL),
(1, 'Алжир', NULL, NULL),
(1, 'Американское Самоа', NULL, NULL),
(1, 'Ангилья', NULL, NULL),
(1, 'Ангола', NULL, NULL),
(1, 'Андорра', NULL, NULL),
(1, 'Антигуа и Барбуда', NULL, NULL),
(1, 'Аргентина', NULL, NULL),
(1, 'Армения', NULL, NULL),
(1, 'Аруба', NULL, NULL),
(1, 'Афганистан', NULL, NULL),
(1, 'Багамы', NULL, NULL),
(1, 'Бангладеш', NULL, NULL),
(1, 'Барбадос', NULL, NULL),
(1, 'Бахрейн', NULL, NULL),
(1, 'Беларусь', NULL, NULL),
(1, 'Белиз', NULL, NULL),
(1, 'Бельгия', NULL, NULL),
(1, 'Бенин', NULL, NULL),
(1, 'Бермуды', NULL, NULL),
(1, 'Болгария', NULL, NULL),
(1, 'Боливия, Многонациональное Государство ', NULL, NULL),
(1, 'Бонэйр, Синт-Эстатиус и Саба', NULL, NULL),
(1, 'Босния и Герцеговина', NULL, NULL),
(1, 'Ботсвана', NULL, NULL),
(1, 'Бразилия', NULL, NULL),
(1, 'Бруней-Даруссалам', NULL, NULL),
(1, 'Буркина-Фасо', NULL, NULL),
(1, 'Бурунди', NULL, NULL),
(1, 'Бутан', NULL, NULL),
(1, 'Вануату', NULL, NULL),
(1, 'Венгрия', NULL, NULL),
(1, 'Венесуэла, Боливарианская Республика ', NULL, NULL),
(1, 'Виргинские Острова, Британские', NULL, NULL),
(1, 'Виргинские Острова, США', NULL, NULL),
(1, 'Вьетнам', NULL, NULL),
(1, 'Габон', NULL, NULL),
(1, 'Гаити', NULL, NULL),
(1, 'Гайана', NULL, NULL),
(1, 'Гамбия', NULL, NULL),
(1, 'Гана', NULL, NULL),
(1, 'Гваделупа', NULL, NULL),
(1, 'Гватемала', NULL, NULL),
(1, 'Гвинея', NULL, NULL),
(1, 'Гвинея-Бисау', NULL, NULL),
(1, 'Германия', NULL, NULL),
(1, 'Гернси', NULL, NULL),
(1, 'Гибралтар', NULL, NULL),
(1, 'Гондурас', NULL, NULL),
(1, 'Гонконг', NULL, NULL),
(1, 'Гренада', NULL, NULL),
(1, 'Гренландия', NULL, NULL),
(1, 'Греция', NULL, NULL),
(1, 'Грузия', NULL, NULL),
(1, 'Гуам', NULL, NULL),
(1, 'Дания', NULL, NULL),
(1, 'Джерси', NULL, NULL),
(1, 'Джибути', NULL, NULL),
(1, 'Доминика', NULL, NULL),
(1, 'Доминиканская Республика', NULL, NULL),
(1, 'Египет', NULL, NULL),
(1, 'Замбия', NULL, NULL),
(1, 'Западная Сахара', NULL, NULL),
(1, 'Зимбабве', NULL, NULL),
(1, 'Израиль', NULL, NULL),
(1, 'Индия', NULL, NULL),
(1, 'Индонезия', NULL, NULL),
(1, 'Иордания', NULL, NULL),
(1, 'Ирак', NULL, NULL),
(1, 'Иран, Исламская Республика ', NULL, NULL),
(1, 'Ирландия', NULL, NULL),
(1, 'Исландия', NULL, NULL),
(1, 'Испания', NULL, NULL),
(1, 'Италия', NULL, NULL),
(1, 'Йемен', NULL, NULL),
(1, 'Кабо-Верде', NULL, NULL),
(1, 'Казахстан', NULL, NULL),
(1, 'Камбоджа', NULL, NULL),
(1, 'Камерун', NULL, NULL),
(1, 'Канада', NULL, NULL),
(1, 'Катар', NULL, NULL),
(1, 'Кения', NULL, NULL),
(1, 'Кипр', NULL, NULL),
(1, 'Кирибати', NULL, NULL),
(1, 'Китай', NULL, NULL),
(1, 'Кокосовые (Килинг) острова', NULL, NULL),
(1, 'Колумбия', NULL, NULL),
(1, 'Коморы', NULL, NULL),
(1, 'Конго', NULL, NULL),
(1, 'Конго, Демократическая Республика', NULL, NULL),
(1, 'Корея, Народно-Демократическая Республика', NULL, NULL),
(1, 'Корея, Республика', NULL, NULL),
(1, 'Коста-Рика', NULL, NULL),
(1, 'Кот-д’Ивуар', NULL, NULL),
(1, 'Куба', NULL, NULL),
(1, 'Кувейт', NULL, NULL),
(1, 'Кыргызстан', NULL, NULL),
(1, 'Кюрасао', NULL, NULL),
(1, 'Лаосская Народно-Демократическая Республика', NULL, NULL),
(1, 'Латвия', NULL, NULL),
(1, 'Лесото', NULL, NULL),
(1, 'Либерия', NULL, NULL),
(1, 'Ливан', NULL, NULL),
(1, 'Ливия', NULL, NULL),
(1, 'Литва', NULL, NULL),
(1, 'Лихтенштейн', NULL, NULL),
(1, 'Люксембург', NULL, NULL),
(1, 'Маврикий', NULL, NULL),
(1, 'Мавритания', NULL, NULL),
(1, 'Мадагаскар', NULL, NULL),
(1, 'Майотта', NULL, NULL),
(1, 'Макао', NULL, NULL),
(1, 'Малави', NULL, NULL),
(1, 'Малайзия', NULL, NULL),
(1, 'Мали', NULL, NULL),
(1, 'Мальдивы', NULL, NULL),
(1, 'Мальта', NULL, NULL),
(1, 'Марокко', NULL, NULL),
(1, 'Мартиника', NULL, NULL),
(1, 'Маршалловы Острова', NULL, NULL),
(1, 'Мексика', NULL, NULL),
(1, 'Микронезия, Федеративные Штаты', NULL, NULL),
(1, 'Мозамбик', NULL, NULL),
(1, 'Молдова', NULL, NULL),
(1, 'Монако', NULL, NULL),
(1, 'Монголия', NULL, NULL),
(1, 'Монтсеррат', NULL, NULL),
(1, 'Мьянма', NULL, NULL),
(1, 'Намибия', NULL, NULL),
(1, 'Науру', NULL, NULL),
(1, 'Непал', NULL, NULL),
(1, 'Нигер', NULL, NULL),
(1, 'Нигерия', NULL, NULL),
(1, 'Нидерланды', NULL, NULL),
(1, 'Никарагуа', NULL, NULL),
(1, 'Ниуэ', NULL, NULL),
(1, 'Новая Зеландия', NULL, NULL),
(1, 'Новая Каледония', NULL, NULL),
(1, 'Норвегия', NULL, NULL),
(1, 'Объединенные Арабские Эмираты', NULL, NULL),
(1, 'Оман', NULL, NULL),
(1, 'Остров Мэн', NULL, NULL),
(1, 'Остров Норфолк', NULL, NULL),
(1, 'Остров Рождества', NULL, NULL),
(1, 'Острова Кайман', NULL, NULL),
(1, 'Острова Кука', NULL, NULL),
(1, 'Острова Теркс И Кайкос', NULL, NULL),
(1, 'Пакистан', NULL, NULL),
(1, 'Палау', NULL, NULL),
(1, 'Палестина, государство', NULL, NULL),
(1, 'Панама', NULL, NULL),
(1, 'Папский престол', NULL, NULL),
(1, 'Папуа – Новая Гвинея', NULL, NULL),
(1, 'Парагвай', NULL, NULL),
(1, 'Перу', NULL, NULL),
(1, 'Питкэрн', NULL, NULL),
(1, 'Польша', NULL, NULL),
(1, 'Португалия', NULL, NULL),
(1, 'Пуэрто-Рико', NULL, NULL),
(1, 'Республика Беларусь', NULL, NULL),
(1, 'Реюньон', NULL, NULL),
(1, 'Российская Федерация', NULL, NULL),
(1, 'Руанда', NULL, NULL),
(1, 'Румыния', NULL, NULL),
(1, 'Самоа', NULL, NULL),
(1, 'Сан-Марино', NULL, NULL),
(1, 'Сан-Томе и Принсипи', NULL, NULL),
(1, 'Саудовская Аравия', NULL, NULL),
(1, 'Северная Македония', NULL, NULL),
(1, 'Северные Марианские Острова', NULL, NULL),
(1, 'Сейшелы', NULL, NULL),
(1, 'Сен Бартелеми', NULL, NULL),
(1, 'Сен Мартин (французская часть)', NULL, NULL),
(1, 'Сен-Мартен (Нидерландская часть)', NULL, NULL),
(1, 'Сен-Пьер и Микелон', NULL, NULL),
(1, 'Сенегал', NULL, NULL),
(1, 'Сент-Винсент и Гренадины', NULL, NULL),
(1, 'Сент-Китс и Невис', NULL, NULL),
(1, 'Сент-Люсия', NULL, NULL),
(1, 'Сербия', NULL, NULL),
(1, 'Сингапур', NULL, NULL),
(1, 'Сирийская Арабская Республика', NULL, NULL),
(1, 'Словакия', NULL, NULL),
(1, 'Словения', NULL, NULL),
(1, 'Соединенное Королевство Великобритании и Северной Ирландии', NULL, NULL),
(1, 'Соединенные Штаты Америки', NULL, NULL),
(1, 'Соломоновы острова', NULL, NULL),
(1, 'Сомали', NULL, NULL),
(1, 'Судан', NULL, NULL),
(1, 'Суринам', NULL, NULL),
(1, 'Сьерра-Леоне', NULL, NULL),
(1, 'Таджикистан', NULL, NULL),
(1, 'Таиланд', NULL, NULL),
(1, 'Тайвань (Китай)', NULL, NULL),
(1, 'Танзания, Объединенная Республика ', NULL, NULL),
(1, 'Тимор-Лесте', NULL, NULL),
(1, 'Того', NULL, NULL),
(1, 'Токелау', NULL, NULL),
(1, 'Тонга', NULL, NULL),
(1, 'Тринидад и Тобаго', NULL, NULL),
(1, 'Тувалу', NULL, NULL),
(1, 'Тунис', NULL, NULL),
(1, 'Туркменистан', NULL, NULL),
(1, 'Турция', NULL, NULL),
(1, 'Уганда', NULL, NULL),
(1, 'Узбекистан', NULL, NULL),
(1, 'Украина', NULL, NULL),
(1, 'Уоллис и Футуна', NULL, NULL),
(1, 'Уругвай', NULL, NULL),
(1, 'Фарерские острова', NULL, NULL),
(1, 'Фиджи', NULL, NULL),
(1, 'Филиппины', NULL, NULL),
(1, 'Финляндия', NULL, NULL),
(1, 'Фолклендские острова (Мальвинские)', NULL, NULL),
(1, 'Франция', NULL, NULL),
(1, 'Французская Гвиана', NULL, NULL),
(1, 'Французская Полинезия', NULL, NULL),
(1, 'Хорватия', NULL, NULL),
(1, 'Центрально-африканская Республика', NULL, NULL),
(1, 'Чад', NULL, NULL),
(1, 'Черногория', NULL, NULL),
(1, 'Чехия', NULL, NULL),
(1, 'Чили', NULL, NULL),
(1, 'Швейцария', NULL, NULL),
(1, 'Швеция', NULL, NULL),
(1, 'Шпицберген и Ян-Майен', NULL, NULL),
(1, 'Шри-Ланка', NULL, NULL),
(1, 'Эквадор', NULL, NULL),
(1, 'Экваториальная Гвинея', NULL, NULL),
(1, 'Эль-Сальвадор', NULL, NULL),
(1, 'Эритрея', NULL, NULL),
(1, 'Эсватини', NULL, NULL),
(1, 'Эстония', NULL, NULL),
(1, 'Эфиопия', NULL, NULL),
(1, 'Южно-Африканская Республика', NULL, NULL),
(1, 'Южный Судан', NULL, NULL),
(1, 'Ямайка', NULL, NULL),
(1, 'Япония', NULL, NULL),
(2, 'Женский', NULL, NULL),
(2, 'Мужской', NULL, NULL),
(3, 'Высшее', NULL, NULL),
(3, 'Высшее военное', NULL, NULL),
(3, 'Начальная школа', NULL, NULL),
(3, 'Незаконченное высшее', NULL, NULL),
(3, 'Профессионально-техническое', NULL, NULL),
(3, 'Среднее базовое', NULL, NULL),
(3, 'Среднее полное', NULL, NULL),
(3, 'Среднее специальное', NULL, NULL),
(4, 'Безработный', NULL, NULL),
(4, 'Военнослужащий', NULL, NULL),
(4, 'Домохозяйка', NULL, NULL),
(4, 'Колхозник', NULL, NULL),
(4, 'Несовершеннолетний', NULL, NULL),
(4, 'Отбывает наказание в МЛС(О)', NULL, NULL),
(4, 'Отпуск по уходу за ребенком', NULL, NULL),
(4, 'Пенсионер', NULL, NULL),
(4, 'Предприниматель', NULL, NULL),
(4, 'Работник по контракту', NULL, NULL),
(4, 'Работники культуры, науки, медицины, образования', NULL, NULL),
(4, 'Рабочий', NULL, NULL),
(4, 'Служащий', NULL, NULL),
(4, 'Состоит на учете в службе занятости, как безработный', NULL, NULL),
(4, 'Сотрудник Министерства по налогам и сборам', NULL, NULL),
(4, 'Сотрудник органов внутренних дел', NULL, NULL),
(4, 'Сотрудник органов пограничной службы', NULL, NULL),
(4, 'Сотрудник подразделений МЧС', NULL, NULL),
(4, 'Сотрудник таможенных органов', NULL, NULL),
(4, 'Студент высшего УО', NULL, NULL),
(4, 'Студент средне специального УО', NULL, NULL),
(4, 'Учащийся', NULL, NULL),
(4, 'Учащийся профессионально-технического УО', NULL, NULL),
(4, 'Учредитель (собственник) юридического лица', NULL, NULL),
(5, 'Вдовец (вдова)', NULL, NULL),
(5, 'Женат (замужем)', NULL, NULL),
(5, 'Разведен (разведена)', NULL, NULL),
(5, 'Холост (незамужем)', NULL, NULL),
(6, 'Государственная', NULL, NULL),
(6, 'Частная', NULL, NULL),
(7, '14 пого', NULL, NULL),
(7, '15 погг', NULL, NULL),
(7, '16 погг', NULL, NULL),
(7, '18 пого', NULL, NULL),
(7, '19 погг', NULL, NULL),
(7, '20 пого', NULL, NULL),
(7, '21 пого', NULL, NULL),
(7, '86 погг', NULL, NULL),
(7, 'опогк "Минск"', NULL, NULL),
(8, 'Да', NULL, NULL),
(8, 'Нет', NULL, NULL),
(9, 'Зеленый', NULL, NULL),
(9, 'Красный', NULL, NULL),
(10, 'Авиа', NULL, NULL),
(10, 'Белорусско-латвийский', NULL, NULL),
(10, 'Белорусско-литовский', NULL, NULL),
(10, 'Белорусско-польский', NULL, NULL),
(10, 'Белорусско-российский', NULL, NULL),
(10, 'Белорусско-украинский', NULL, NULL),
(10, 'Иное', NULL, NULL),
(11, 'Линия границы', NULL, NULL),
(11, 'Пограничная зона', NULL, NULL),
(11, 'Пограничная полоса', NULL, NULL),
(11, 'Пункт пропуска', NULL, NULL),
(11, 'Пункт пропуска сопредельного государства', NULL, NULL),
(11, 'Территория республики', NULL, NULL),
(11, 'Территория сопредельного государства', NULL, NULL),
(12, 'В Республику Беларусь', NULL, NULL),
(12, 'Из Республики Беларусь', NULL, NULL),
(12, 'Тыловой район', NULL, NULL),
(13, 'Погз № 1', NULL, NULL),
(13, 'Погз № 10', NULL, NULL),
(13, 'Погз № 11', NULL, NULL),
(13, 'Погз № 12', NULL, NULL),
(13, 'Погз № 13', NULL, NULL),
(13, 'Погз № 14', NULL, NULL),
(13, 'Погз № 15', NULL, NULL),
(13, 'Погз № 16', NULL, NULL),
(13, 'Погз № 17', NULL, NULL),
(13, 'Погз № 18', NULL, NULL),
(13, 'Погз № 19', NULL, NULL),
(13, 'Погз № 2', NULL, NULL),
(13, 'Погз № 3', NULL, NULL),
(13, 'Погз № 4', NULL, NULL),
(13, 'Погз № 5', NULL, NULL),
(13, 'Погз № 6', NULL, NULL),
(13, 'Погз № 7', NULL, NULL),
(13, 'Погз № 8', NULL, NULL),
(13, 'Погз № 9', NULL, NULL),
(14, 'Погп № 1', NULL, NULL),
(14, 'Погп № 2', NULL, NULL),
(14, 'Погп № 3', NULL, NULL),
(14, 'Погп № 4', NULL, NULL),
(14, 'Погп № 5', NULL, NULL),
(14, 'Погп № 6', NULL, NULL),
(15, 'Гудогай погк (опс)', NULL, NULL),
(15, 'Лоев погк (обо)', NULL, NULL),
(15, 'Малорита погк (опс)', NULL, NULL),
(15, 'Опса погк (опс)', NULL, NULL),
(15, 'Поречье погк (опс)', NULL, NULL),
(15, 'Поставы погк (опс)', NULL, NULL),
(15, 'Речица погк (опс)', NULL, NULL),
(16, 'Задержание по ОД', NULL, NULL),
(16, 'Задержание по результатам работы с местным населением', NULL, NULL),
(17, 'ефрейтор', NULL, NULL),
(17, 'капитан', NULL, NULL),
(17, 'лейтенант', NULL, NULL),
(17, 'майор', NULL, NULL),
(17, 'младший лейтенант', NULL, NULL),
(17, 'младший сержант', NULL, NULL),
(17, 'подполковник', NULL, NULL),
(17, 'полковник', NULL, NULL),
(17, 'прапорщик', NULL, NULL),
(17, 'рядовой', NULL, NULL),
(17, 'сержант', NULL, NULL),
(17, 'старший лейтенант', NULL, NULL),
(17, 'старший прапорщик', NULL, NULL),
(17, 'старший сержант', NULL, NULL),
(17, 'старшина', NULL, NULL),
(18, 'английский', NULL, NULL),
(18, 'грузинский', NULL, NULL),
(18, 'испанский', NULL, NULL),
(18, 'итальянский', NULL, NULL),
(18, 'китайский', NULL, NULL),
(18, 'латышский', NULL, NULL),
(18, 'литовский', NULL, NULL),
(18, 'немецкий', NULL, NULL),
(18, 'польский', NULL, NULL),
(18, 'русский', NULL, NULL),
(18, 'украинский', NULL, NULL),
(18, 'французский', NULL, NULL),
(18, 'японский', NULL, NULL),
(19, 'азербаджанец', NULL, NULL),
(19, 'алжирец', NULL, NULL),
(19, 'американец', NULL, NULL),
(19, 'англичанин', NULL, NULL),
(19, 'армянин', NULL, NULL),
(19, 'афганец', NULL, NULL),
(19, 'белорус', NULL, NULL),
(19, 'вьетнамец', NULL, NULL),
(19, 'грузин', NULL, NULL),
(19, 'дагестанец', NULL, NULL),
(19, 'еврей', NULL, NULL),
(19, 'египтянин', NULL, NULL),
(19, 'ингуш', NULL, NULL),
(19, 'индус', NULL, NULL),
(19, 'иранец', NULL, NULL),
(19, 'казах', NULL, NULL),
(19, 'камерунец', NULL, NULL),
(19, 'китаец', NULL, NULL),
(19, 'кубинец', NULL, NULL),
(19, 'кыргыз', NULL, NULL),
(19, 'латыш', NULL, NULL),
(19, 'ливанец', NULL, NULL),
(19, 'литовец', NULL, NULL),
(19, 'молдованин', NULL, NULL),
(19, 'немец', NULL, NULL),
(19, 'нигериец', NULL, NULL),
(19, 'пакистанец', NULL, NULL),
(19, 'поляк', NULL, NULL),
(19, 'пуштун', NULL, NULL),
(19, 'русский', NULL, NULL),
(19, 'сенигалец', NULL, NULL),
(19, 'серб', NULL, NULL),
(19, 'сириец', NULL, NULL),
(19, 'сомалиец', NULL, NULL),
(19, 'таджик', NULL, NULL),
(19, 'тамилец', NULL, NULL),
(19, 'туркмен', NULL, NULL),
(19, 'турок', NULL, NULL),
(19, 'узбек', NULL, NULL),
(19, 'украинец', NULL, NULL),
(19, 'цыган', NULL, NULL),
(19, 'чеченец', NULL, NULL),
(19, 'эфиоп', NULL, NULL);

-- 
-- Вывод данных для таблицы sys_list_top
--
INSERT INTO sys_list_top VALUES
(1, 'citizenship', 'Гражданство', False),
(2, 'sex', 'Пол', True),
(3, 'education', 'Образование', True),
(4, 'social_status', 'Социальное положение', False),
(5, 'marital_status', 'Семейное положение', False),
(6, 'ownership', 'Форма собственности', False),
(7, 'tops', 'ТОПС', False),
(8, 'yes_no', 'Да/Нет', False),
(9, 'channel', 'Цвет канала', False),
(10, 'plot', 'Участок по направлению', False),
(11, 'category_location', 'Категория места', False),
(12, 'course', 'Направление', False),
(13, 'number_pogz', 'Номер погз', False),
(14, 'number_pogp', 'Номер погп', False),
(15, 'pogk', 'Погк', False),
(16, 'od', 'Задержание ОД', False),
(17, 'rang', 'Воинское звание', False),
(18, 'language_skils', 'Знание языков', False),
(19, 'nationality', 'Национальность', False);

-- 
-- Вывод данных для таблицы sys_obj
--
INSERT INTO sys_obj VALUES
(1, 'rel', 'события/связи', 'событие/связь', 'fa-link', NULL),
(10, 'free', 'значения', 'значение', 'fa-star', NULL),
(15, 'file', 'файлы', 'файл', 'fa-file', NULL),
(20, 'doc', 'документы', 'документ', 'fa-align-left', NULL),
(25, 'point', 'точки', 'точка', 'fa-map-marker-alt', NULL),
(30, 'geometry', 'геометрия', 'геометрия', 'fa-draw-polygon', NULL),
(35, 'person_p', 'физлица', 'физлицо', 'fa-user', NULL),
(40, 'person_l', 'юрлица', 'юрлицо', 'fa-stamp', NULL),
(45, 'case', 'дела', 'дело', 'fa-lock', NULL),
(50, 'transport', 'транспорт', 'транспорт', 'fa-car', NULL);

-- 
-- Вывод данных для таблицы sys_script
--
INSERT INTO sys_script VALUES
(1, 'rel_to_geo', NULL, '# ВХОД\r\n# obj_name  - объект = ''point'' или ''geometry''\r\n# keys_rel  - список rel-ключей по классификатору (наименования или индексы)\r\n# where_dop - дополнительные условия отбора в rel (список): [''dat is null''] \r\n# keys_obj  - возвращаемые в properties значения ключей, например, для geometry - [''name''], для point - [''address'']\r\n#\r\n# ВЫХОД\r\n# FC отобранных gео\r\n\r\n# значения по умолчанию\r\nif not var_exist(''keys_obj'' ): keys_obj  = []\r\nif not var_exist(''where_dop''): where_dop = []\r\n\r\n# записи rel\r\nrel_recs = io_get_rel(group_id, keys_rel, [obj_name], None, where_dop)\r\n\r\n# уникальные связанные объекты (obj_id, rec_id)\r\n# els = {(25, 34), (20, 1), (25, 33)}\r\nels = rel_rec_to_el(rel_recs)\r\n\r\n# geo_ids = [33, 34]\r\ngeo_ids = el_to_rec_id(obj_name, els)\r\n\r\n# результат в FC\r\nret = geo_id_to_fc(obj_name, group_id, geo_ids, keys_obj)\r\n\r\n# АЛЬТЕРНАТИВНЫЙ СКРИПТ\r\n#ret = rel_to_geo_fc(obj_name, group_id, keys_rel, keys_obj, where_dop)\r\n', NULL, True, NULL),
(10, 'geometry_tree', NULL, '# ВЫХОД [ {id: , name: , icon: }, ... ]\r\nret = io_get_geometry_tree(group_id, parent_id)\r\n', 'читать geometry с заданным parent_id', True, NULL),
(11, 'geometry_get', NULL, 'ret = io_get_obj(group_id, ''geometry'', [''ST_AsGeoJSON(location) AS location''], [id])\r\n', 'читать geometry', True, NULL),
(12, 'geometry_set', NULL, 'ret = io_set(group_id, ''geometry'', data)\r\n#ret = geometry_update_block(id, location)', 'обновить geometry в БД', True, NULL),
(20, 'obj_list', NULL, 'ret = obj_list()', '###########################################\r\n# СПИСОК ОБЪЕКТОВ\r\n###########################################', True, NULL),
(21, 'key_list', NULL, 'ret = key_list(obj)', '###########################################\r\n# ИНФОРМАЦИЯ ОБ ОБЪЕКТЕ OBJ И ЕГО КЛЮЧАХ\r\n###########################################\r\n# IN\r\n#     obj  объект (int или str)\r\n# OUT\r\n#     obj  {}    инфо об объекте SYS_OBJ\r\n#     keys []    инфо о  ключах  SYS_KEY', True, NULL);
-- 
-- Восстановить предыдущий режим SQL (SQL mode)
-- 
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;

-- 
-- Включение внешних ключей
-- 
/*!40014 SET FOREIGN_KEY_CHECKS = @OLD_FOREIGN_KEY_CHECKS */;
