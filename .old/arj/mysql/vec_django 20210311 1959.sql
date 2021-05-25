--
-- Скрипт сгенерирован Devart dbForge Studio for MySQL, Версия 7.3.137.0
-- Домашняя страница продукта: http://www.devart.com/ru/dbforge/mysql/studio
-- Дата скрипта: 11.03.2021 19:59:47
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
USE vec_django;

--
-- Удалить таблицу "django_session"
--
DROP TABLE IF EXISTS django_session;

--
-- Удалить таблицу "django_migrations"
--
DROP TABLE IF EXISTS django_migrations;

--
-- Удалить таблицу "django_content_type"
--
DROP TABLE IF EXISTS django_content_type;

--
-- Удалить таблицу "django_admin_log"
--
DROP TABLE IF EXISTS django_admin_log;

--
-- Удалить таблицу "auth_user_user_permissions"
--
DROP TABLE IF EXISTS auth_user_user_permissions;

--
-- Удалить таблицу "auth_user_groups"
--
DROP TABLE IF EXISTS auth_user_groups;

--
-- Удалить таблицу "auth_user"
--
DROP TABLE IF EXISTS auth_user;

--
-- Удалить таблицу "auth_permission"
--
DROP TABLE IF EXISTS auth_permission;

--
-- Удалить таблицу "auth_group_permissions"
--
DROP TABLE IF EXISTS auth_group_permissions;

--
-- Удалить таблицу "auth_group"
--
DROP TABLE IF EXISTS auth_group;

--
-- Установка базы данных по умолчанию
--
USE vec_django;

--
-- Создать таблицу "auth_group"
--
CREATE TABLE auth_group (
  id int(11) NOT NULL AUTO_INCREMENT,
  name varchar(150) NOT NULL,
  PRIMARY KEY (id),
  UNIQUE INDEX name (name)
)
ENGINE = INNODB
AUTO_INCREMENT = 9
AVG_ROW_LENGTH = 2048
CHARACTER SET utf8
COLLATE utf8_general_ci
ROW_FORMAT = DYNAMIC;

--
-- Создать таблицу "auth_group_permissions"
--
CREATE TABLE auth_group_permissions (
  id int(11) NOT NULL AUTO_INCREMENT,
  group_id int(11) NOT NULL,
  permission_id int(11) NOT NULL,
  PRIMARY KEY (id),
  UNIQUE INDEX auth_group_permissions_group_id_permission_id_0cd325b0_uniq (group_id, permission_id),
  CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm FOREIGN KEY (permission_id)
  REFERENCES auth_permission (id) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id)
  REFERENCES auth_group (id) ON DELETE RESTRICT ON UPDATE RESTRICT
)
ENGINE = INNODB
CHARACTER SET utf8
COLLATE utf8_general_ci
ROW_FORMAT = DYNAMIC;

--
-- Создать таблицу "auth_permission"
--
CREATE TABLE auth_permission (
  id int(11) NOT NULL AUTO_INCREMENT,
  name varchar(255) NOT NULL,
  content_type_id int(11) NOT NULL,
  codename varchar(100) NOT NULL,
  PRIMARY KEY (id),
  UNIQUE INDEX auth_permission_content_type_id_codename_01ab375a_uniq (content_type_id, codename),
  CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co FOREIGN KEY (content_type_id)
  REFERENCES django_content_type (id) ON DELETE RESTRICT ON UPDATE RESTRICT
)
ENGINE = INNODB
AUTO_INCREMENT = 33
AVG_ROW_LENGTH = 585
CHARACTER SET utf8
COLLATE utf8_general_ci
ROW_FORMAT = DYNAMIC;

--
-- Создать таблицу "auth_user"
--
CREATE TABLE auth_user (
  id int(11) NOT NULL AUTO_INCREMENT,
  password varchar(128) NOT NULL,
  last_login datetime(6) DEFAULT NULL,
  is_superuser tinyint(1) NOT NULL,
  username varchar(150) NOT NULL,
  first_name varchar(150) NOT NULL,
  last_name varchar(150) NOT NULL,
  email varchar(254) NOT NULL,
  is_staff tinyint(1) NOT NULL,
  is_active tinyint(1) NOT NULL,
  date_joined datetime(6) NOT NULL,
  PRIMARY KEY (id),
  UNIQUE INDEX username (username)
)
ENGINE = INNODB
AUTO_INCREMENT = 6
AVG_ROW_LENGTH = 3276
CHARACTER SET utf8
COLLATE utf8_general_ci
ROW_FORMAT = DYNAMIC;

--
-- Создать таблицу "auth_user_groups"
--
CREATE TABLE auth_user_groups (
  id int(11) NOT NULL AUTO_INCREMENT,
  user_id int(11) NOT NULL,
  group_id int(11) NOT NULL,
  PRIMARY KEY (id),
  UNIQUE INDEX auth_user_groups_user_id_group_id_94350c0c_uniq (user_id, group_id),
  CONSTRAINT auth_user_groups_group_id_97559544_fk_auth_group_id FOREIGN KEY (group_id)
  REFERENCES auth_group (id) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT auth_user_groups_user_id_6a12ed8b_fk_auth_user_id FOREIGN KEY (user_id)
  REFERENCES auth_user (id) ON DELETE RESTRICT ON UPDATE RESTRICT
)
ENGINE = INNODB
AUTO_INCREMENT = 21
AVG_ROW_LENGTH = 1638
CHARACTER SET utf8
COLLATE utf8_general_ci
ROW_FORMAT = DYNAMIC;

--
-- Создать таблицу "auth_user_user_permissions"
--
CREATE TABLE auth_user_user_permissions (
  id int(11) NOT NULL AUTO_INCREMENT,
  user_id int(11) NOT NULL,
  permission_id int(11) NOT NULL,
  PRIMARY KEY (id),
  UNIQUE INDEX auth_user_user_permissions_user_id_permission_id_14a6b632_uniq (user_id, permission_id),
  CONSTRAINT auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm FOREIGN KEY (permission_id)
  REFERENCES auth_permission (id) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id FOREIGN KEY (user_id)
  REFERENCES auth_user (id) ON DELETE RESTRICT ON UPDATE RESTRICT
)
ENGINE = INNODB
CHARACTER SET utf8
COLLATE utf8_general_ci
ROW_FORMAT = DYNAMIC;

--
-- Создать таблицу "django_admin_log"
--
CREATE TABLE django_admin_log (
  id int(11) NOT NULL AUTO_INCREMENT,
  action_time datetime(6) NOT NULL,
  object_id longtext DEFAULT NULL,
  object_repr varchar(200) NOT NULL,
  action_flag smallint(5) UNSIGNED NOT NULL,
  change_message longtext NOT NULL,
  content_type_id int(11) DEFAULT NULL,
  user_id int(11) NOT NULL,
  PRIMARY KEY (id),
  CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co FOREIGN KEY (content_type_id)
  REFERENCES django_content_type (id) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT django_admin_log_user_id_c564eba6_fk_auth_user_id FOREIGN KEY (user_id)
  REFERENCES auth_user (id) ON DELETE RESTRICT ON UPDATE RESTRICT
)
ENGINE = INNODB
AUTO_INCREMENT = 80
AVG_ROW_LENGTH = 237
CHARACTER SET utf8
COLLATE utf8_general_ci
ROW_FORMAT = DYNAMIC;

--
-- Создать таблицу "django_content_type"
--
CREATE TABLE django_content_type (
  id int(11) NOT NULL AUTO_INCREMENT,
  app_label varchar(100) NOT NULL,
  model varchar(100) NOT NULL,
  PRIMARY KEY (id),
  UNIQUE INDEX django_content_type_app_label_model_76bd3d3b_uniq (app_label, model)
)
ENGINE = INNODB
AUTO_INCREMENT = 11
AVG_ROW_LENGTH = 1638
CHARACTER SET utf8
COLLATE utf8_general_ci
ROW_FORMAT = DYNAMIC;

--
-- Создать таблицу "django_migrations"
--
CREATE TABLE django_migrations (
  id int(11) NOT NULL AUTO_INCREMENT,
  app varchar(255) NOT NULL,
  name varchar(255) NOT NULL,
  applied datetime(6) NOT NULL,
  PRIMARY KEY (id)
)
ENGINE = INNODB
AUTO_INCREMENT = 21
AVG_ROW_LENGTH = 910
CHARACTER SET utf8
COLLATE utf8_general_ci
ROW_FORMAT = DYNAMIC;

--
-- Создать таблицу "django_session"
--
CREATE TABLE django_session (
  session_key varchar(40) NOT NULL,
  session_data longtext NOT NULL,
  expire_date datetime(6) NOT NULL,
  PRIMARY KEY (session_key),
  INDEX django_session_expire_date_a5c62663 (expire_date)
)
ENGINE = INNODB
AVG_ROW_LENGTH = 496
CHARACTER SET utf8
COLLATE utf8_general_ci
ROW_FORMAT = DYNAMIC;

-- 
-- Вывод данных для таблицы auth_group
--
INSERT INTO auth_group VALUES
(7, 'level_brest'),
(6, 'level_gpk'),
(8, 'level_grodno'),
(1, 'type_analitic'),
(5, 'type_conf'),
(4, 'type_inquest'),
(2, 'type_ord'),
(3, 'type_scout');

-- 
-- Вывод данных для таблицы auth_group_permissions
--
-- Таблица vec_django.auth_group_permissions не содержит данных

-- 
-- Вывод данных для таблицы auth_permission
--
INSERT INTO auth_permission VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 2, 'add_permission'),
(6, 'Can change permission', 2, 'change_permission'),
(7, 'Can delete permission', 2, 'delete_permission'),
(8, 'Can view permission', 2, 'view_permission'),
(9, 'Can add group', 3, 'add_group'),
(10, 'Can change group', 3, 'change_group'),
(11, 'Can delete group', 3, 'delete_group'),
(12, 'Can view group', 3, 'view_group'),
(13, 'Can add user', 4, 'add_user'),
(14, 'Can change user', 4, 'change_user'),
(15, 'Can delete user', 4, 'delete_user'),
(16, 'Can view user', 4, 'view_user'),
(17, 'Can add content type', 5, 'add_contenttype'),
(18, 'Can change content type', 5, 'change_contenttype'),
(19, 'Can delete content type', 5, 'delete_contenttype'),
(20, 'Can view content type', 5, 'view_contenttype'),
(21, 'Can add session', 6, 'add_session'),
(22, 'Can change session', 6, 'change_session'),
(23, 'Can delete session', 6, 'delete_session'),
(24, 'Can view session', 6, 'view_session'),
(25, 'Can add уведомление', 7, 'add_model_alerts'),
(26, 'Can change уведомление', 7, 'change_model_alerts'),
(27, 'Can delete уведомление', 7, 'delete_model_alerts'),
(28, 'Can view уведомление', 7, 'view_model_alerts'),
(29, 'Can add группа', 9, 'add_model_auth_group'),
(30, 'Can change группа', 9, 'change_model_auth_group'),
(31, 'Can delete группа', 9, 'delete_model_auth_group'),
(32, 'Can view группа', 9, 'view_model_auth_group');

-- 
-- Вывод данных для таблицы auth_user
--
INSERT INTO auth_user VALUES
(1, 'pbkdf2_sha256$216000$us4rxLBIPHkx$O+JzBRHALETIP7cXqCPmeGmlvirfxM+kb79KeZoSoCk=', '2021-03-10 14:30:06.869479', 1, 'sysadmin', 'Геннадий', 'Вертинский', '', 1, 1, '2020-01-13 11:30:47'),
(2, 'pbkdf2_sha256$150000$lsjF9Fa42sbR$1bj1p0KfbP7kHma5LVhGEDsbBFo3r4dZ8We58FHQfHU=', '2020-03-11 08:42:54.844157', 0, 'test1', 'Тест 1', '1', '', 0, 1, '2020-02-20 10:55:23'),
(3, 'pbkdf2_sha256$150000$2eNbcr9r65GH$YEVdHcZDCAGEza9cYJMpZEMwWYWNYRA/4ZH90FtiTQQ=', '2020-03-10 11:20:09.410395', 0, 'test2', 'Тест 2', '2', '', 0, 1, '2020-02-20 10:55:49'),
(4, 'pbkdf2_sha256$150000$Hm5e9l94xrMJ$rLdSbXZdUQvJGDqgcT12EK/5wCCpQzDG8l9DvNc5s30=', '2020-03-10 13:38:08.13394', 0, 'test3', 'Тест 3', '3', '', 0, 1, '2020-02-20 14:18:15'),
(5, 'pbkdf2_sha256$216000$j1rndanawuz5$akIC0dtw88XsxRCv7H4cCTcHvGUwdGtiu6lPXuXC64A=', '2021-03-09 09:59:18', 1, 'dev', '1', 'developer', '', 1, 1, '2021-03-09 09:58:17');

-- 
-- Вывод данных для таблицы auth_user_groups
--
INSERT INTO auth_user_groups VALUES
(18, 1, 1),
(16, 1, 2),
(17, 1, 7),
(11, 2, 2),
(5, 2, 5),
(6, 3, 3),
(7, 3, 6),
(8, 4, 3),
(10, 4, 7),
(19, 5, 1),
(20, 5, 6);

-- 
-- Вывод данных для таблицы auth_user_user_permissions
--
-- Таблица vec_django.auth_user_user_permissions не содержит данных

-- 
-- Вывод данных для таблицы django_admin_log
--
INSERT INTO django_admin_log VALUES
(1, '2020-03-06 10:57:43.639696', '1', 'sysadmin', 2, '[{"changed": {"fields": ["first_name", "last_name", "last_login"]}}]', 4, 1),
(2, '2020-03-06 12:22:06.9388', '2', 'test1', 2, '[{"changed": {"fields": ["first_name"]}}]', 4, 1),
(3, '2020-03-06 12:22:18.409091', '3', 'test2', 2, '[{"changed": {"fields": ["first_name"]}}]', 4, 1),
(4, '2020-03-06 12:22:33.604346', '4', 'test3', 2, '[{"changed": {"fields": ["first_name"]}}]', 4, 1),
(5, '2020-03-09 13:34:25.139225', '3', 'Всем привет !!!! 555 [warn]; ОТКЛЮЧЕНО', 2, '[{"changed": {"fields": ["enabled"]}}]', 7, 1),
(6, '2020-03-09 14:58:45.898096', '3', 'Model_Alerts object (3)', 2, '[]', 7, 1),
(7, '2020-03-09 15:32:31.622083', '3', 'Model_Alerts object (3)', 2, '[{"changed": {"fields": ["enabled"]}}]', 7, 1),
(8, '2020-03-09 15:32:36.915821', '3', 'Model_Alerts object (3)', 2, '[{"changed": {"fields": ["enabled"]}}]', 7, 1),
(9, '2020-03-09 15:36:15.054274', '3', 'Model_Alerts object (3)', 2, '[{"changed": {"fields": ["type"]}}]', 7, 1),
(10, '2020-03-09 16:27:08.301619', '1', 'Model_Alerts object (1)', 2, '[{"changed": {"fields": ["wait"]}}]', 7, 1),
(11, '2020-03-09 16:27:08.333857', '2', 'Model_Alerts object (2)', 2, '[{"changed": {"fields": ["wait"]}}]', 7, 1),
(12, '2020-03-09 16:28:34.499647', '1', 'Model_Alerts object (1)', 2, '[{"changed": {"fields": ["descript"]}}]', 7, 1),
(13, '2020-03-09 16:29:12.401789', '4', 'Model_Alerts object (4)', 1, '[{"added": {}}]', 7, 1),
(14, '2020-03-09 16:29:44.956324', '4', 'Model_Alerts object (4)', 2, '[{"changed": {"fields": ["type"]}}]', 7, 1),
(15, '2020-03-10 07:02:15.146228', '1', 'Model_Alerts object (1)', 2, '[{"changed": {"fields": ["wait"]}}]', 7, 1),
(16, '2020-03-10 07:02:28.218611', '3', 'Model_Alerts object (3)', 2, '[{"changed": {"fields": ["enabled"]}}]', 7, 1),
(17, '2020-03-10 08:45:21.428725', '6', 'Model_Alerts object (6)', 2, '[{"changed": {"fields": ["type"]}}]', 7, 1),
(18, '2020-03-10 08:45:32.55846', '3', 'Model_Alerts object (3)', 2, '[{"changed": {"fields": ["enabled"]}}]', 7, 1),
(19, '2020-03-10 08:45:32.594047', '4', 'Model_Alerts object (4)', 2, '[{"changed": {"fields": ["enabled"]}}]', 7, 1),
(20, '2020-03-10 08:45:32.627508', '5', 'Model_Alerts object (5)', 2, '[{"changed": {"fields": ["enabled"]}}]', 7, 1),
(21, '2020-03-10 08:45:32.660605', '6', 'Model_Alerts object (6)', 2, '[{"changed": {"fields": ["enabled"]}}]', 7, 1),
(22, '2020-03-10 08:45:51.818595', '1', 'Model_Alerts object (1)', 2, '[{"changed": {"fields": ["wait"]}}]', 7, 1),
(23, '2020-03-30 16:22:24.47338', '11', 'Model_Alerts object (11)', 3, '', 7, 1),
(24, '2020-03-30 16:22:31.212977', '10', 'Model_Alerts object (10)', 3, '', 7, 1),
(25, '2020-03-30 16:22:37.747053', '9', 'Model_Alerts object (9)', 3, '', 7, 1),
(26, '2020-03-30 16:23:13.391181', '12', 'Model_Alerts object (12)', 3, '', 7, 1),
(27, '2020-05-06 13:54:05.536234', '1', 'type_scout', 2, '[{"changed": {"fields": ["name"]}}]', 3, 1),
(28, '2020-05-06 13:56:39.153652', '4', 'type_inquest', 2, '[{"changed": {"fields": ["name"]}}]', 3, 1),
(29, '2020-05-06 14:59:03.042854', '1', 'sysadmin', 2, '[{"changed": {"fields": ["groups"]}}]', 4, 1),
(30, '2020-05-06 15:08:55.004397', '1', 'sysadmin', 2, '[]', 4, 1),
(31, '2020-05-06 15:28:20.997505', '1', 'sysadmin', 2, '[{"changed": {"fields": ["groups"]}}]', 4, 1),
(32, '2020-05-06 15:32:52.390027', '1', 'sysadmin', 2, '[{"changed": {"fields": ["groups"]}}]', 4, 1),
(33, '2020-05-06 15:49:03.136763', '3', 'type2_analitic', 2, '[{"changed": {"fields": ["name"]}}]', 3, 1),
(34, '2020-05-06 15:49:34.563523', '3', 'type_analitic', 2, '[{"changed": {"fields": ["name"]}}]', 3, 1),
(35, '2020-05-06 15:49:46.916232', '7', 'level2_grodno', 2, '[{"changed": {"fields": ["name"]}}]', 3, 1),
(36, '2020-05-06 15:50:12.647784', '7', 'level_grodno', 2, '[{"changed": {"fields": ["name"]}}]', 3, 1),
(37, '2020-05-06 16:03:40.008005', '7', 'level2_grodno', 2, '[{"changed": {"fields": ["name"]}}]', 3, 1),
(38, '2020-05-06 16:04:02.141328', '7', 'level_grodno', 2, '[{"changed": {"fields": ["name"]}}]', 3, 1),
(39, '2020-05-06 16:05:05.577358', '3', 'type2_analitic', 2, '[{"changed": {"fields": ["name"]}}]', 3, 1),
(40, '2020-05-06 16:05:23.960788', '3', 'type_analitic', 2, '[{"changed": {"fields": ["name"]}}]', 3, 1),
(41, '2020-05-07 09:47:17.161259', '1', 'sysadmin', 2, '[{"changed": {"fields": ["groups"]}}]', 4, 1),
(42, '2020-05-07 09:48:02.734711', '1', 'sysadmin', 2, '[{"changed": {"fields": ["groups"]}}]', 4, 1),
(43, '2020-05-07 11:16:35.174797', '1', 'sysadmin', 2, '[{"changed": {"fields": ["groups"]}}]', 4, 1),
(44, '2020-05-07 11:54:12.044236', '8', 'level_conf', 1, '[{"added": {}}]', 3, 1),
(45, '2020-05-08 12:56:38.782531', '1', 'sysadmin', 2, '[{"changed": {"fields": ["groups"]}}]', 4, 1),
(46, '2020-05-08 15:54:57.206655', '10', 'Model_Geo_Geometry object (10)', 2, '[{"changed": {"fields": ["name"]}}]', 8, 1),
(47, '2020-05-12 09:41:12.708822', '8', 'Model_Geo_Geometry object (8)', 2, '[{"changed": {"fields": ["enabled"]}}]', 8, 1),
(48, '2020-05-12 14:31:44.863011', '7', 'Model_Geo_Geometry object (7)', 2, '[{"added": {"name": "\\u0433\\u0440\\u0443\\u043f\\u043f\\u0430-\\u0433\\u0435\\u043e\\u043c\\u0435\\u0442\\u0440\\u0438\\u044f", "object": "Model_Geo_Geometry_Auth_Group object (5)"}}]', 8, 1),
(49, '2020-05-12 14:32:18.311468', '7', 'Model_Geo_Geometry object (7)', 2, '[{"deleted": {"name": "\\u0433\\u0440\\u0443\\u043f\\u043f\\u0430-\\u0433\\u0435\\u043e\\u043c\\u0435\\u0442\\u0440\\u0438\\u044f", "object": "Model_Geo_Geometry_Auth_Group object (None)"}}]', 8, 1),
(50, '2020-05-12 14:32:34.100014', '7', 'Model_Geo_Geometry object (7)', 2, '[{"added": {"name": "\\u0433\\u0440\\u0443\\u043f\\u043f\\u0430-\\u0433\\u0435\\u043e\\u043c\\u0435\\u0442\\u0440\\u0438\\u044f", "object": "Model_Geo_Geometry_Auth_Group object (6)"}}, {"added": {"name": "\\u0433\\u0440\\u0443\\u043f\\u043f\\u0430-\\u0433\\u0435\\u043e\\u043c\\u0435\\u0442\\u0440\\u0438\\u044f", "object": "Model_Geo_Geometry_Auth_Group object (7)"}}]', 8, 1),
(51, '2020-05-12 14:38:46.099633', '2', '2222', 2, '[{"changed": {"fields": ["name"]}}]', 8, 1),
(52, '2020-05-12 14:41:21.418204', '12', '5657756 (12)', 1, '[{"added": {}}]', 8, 1),
(53, '2020-05-12 14:44:08.1376', '4', '333 (4)', 2, '[{"added": {"name": "\\u0433\\u0440\\u0443\\u043f\\u043f\\u0430-\\u0433\\u0435\\u043e\\u043c\\u0435\\u0442\\u0440\\u0438\\u044f", "object": "Model_Geo_Geometry_Auth_Group object (8)"}}]', 8, 1),
(54, '2020-05-12 14:49:11.961688', '4', '333 (4)', 2, '[{"deleted": {"name": "\\u0433\\u0440\\u0443\\u043f\\u043f\\u0430-\\u0433\\u0435\\u043e\\u043c\\u0435\\u0442\\u0440\\u0438\\u044f", "object": " "}}]', 8, 1),
(55, '2020-05-12 14:54:11.783812', '11', 'Пограничные столбы (11)', 2, '[{"added": {"name": "\\u0433\\u0440\\u0443\\u043f\\u043f\\u0430-\\u0433\\u0435\\u043e\\u043c\\u0435\\u0442\\u0440\\u0438\\u044f", "object": ""}}]', 8, 1),
(56, '2020-05-12 16:01:51.037504', '6', 'level_gpk', 2, '[{"added": {"name": "\\u0433\\u0440\\u0443\\u043f\\u043f\\u0430-\\u0433\\u0435\\u043e", "object": ""}}]', 9, 1),
(57, '2020-05-12 16:05:38.593091', '6', 'level_gpk', 2, '[{"added": {"name": "\\u0433\\u0440\\u0443\\u043f\\u043f\\u0430-\\u0433\\u0435\\u043e", "object": ""}}, {"added": {"name": "\\u0433\\u0440\\u0443\\u043f\\u043f\\u0430-\\u0433\\u0435\\u043e", "object": ""}}, {"added": {"name": "\\u0433\\u0440\\u0443\\u043f\\u043f\\u0430-\\u0433\\u0435\\u043e", "object": ""}}]', 9, 1),
(58, '2020-05-12 16:06:07.237268', '6', 'level_gpk', 2, '[{"added": {"name": "\\u0433\\u0440\\u0443\\u043f\\u043f\\u0430-\\u0433\\u0435\\u043e", "object": ""}}, {"added": {"name": "\\u0433\\u0440\\u0443\\u043f\\u043f\\u0430-\\u0433\\u0435\\u043e", "object": ""}}, {"added": {"name": "\\u0433\\u0440\\u0443\\u043f\\u043f\\u0430-\\u0433\\u0435\\u043e", "object": ""}}, {"added": {"name": "\\u0433\\u0440\\u0443\\u043f\\u043f\\u0430-\\u0433\\u0435\\u043e", "object": ""}}]', 9, 1),
(59, '2020-05-12 16:06:59.13626', '12', 'Тест 1', 2, '[{"changed": {"fields": ["name"]}}]', 8, 1),
(60, '2020-05-12 16:06:59.169622', '10', 'Тест 2', 2, '[{"changed": {"fields": ["name"]}}]', 8, 1),
(61, '2020-05-13 14:48:17.238346', '7', 'level_brest', 2, '[{"added": {"name": "\\u0433\\u0440\\u0443\\u043f\\u043f\\u0430-\\u0433\\u0435\\u043e", "object": ""}}]', 9, 1),
(62, '2020-05-13 15:50:37.533608', '12', 'Тест 1', 2, '[{"changed": {"fields": ["geo_geometry_auth_group"]}}]', 8, 1),
(63, '2020-05-13 15:50:54.00369', '12', 'Тест 1', 2, '[{"changed": {"fields": ["geo_geometry_auth_group"]}}]', 8, 1),
(64, '2020-05-13 15:51:51.916058', '9', '77777', 1, '[{"added": {}}, {"added": {"name": "\\u0433\\u0440\\u0443\\u043f\\u043f\\u0430-\\u0433\\u0435\\u043e", "object": ""}}]', 9, 1),
(65, '2020-05-13 15:52:34.613032', '9', 'level_lida', 2, '[{"changed": {"fields": ["name"]}}]', 9, 1),
(66, '2020-05-13 15:53:10.882945', '12', 'Тест 1', 2, '[{"changed": {"fields": ["geo_geometry_auth_group"]}}]', 8, 1),
(67, '2020-05-14 10:45:08.104891', '10', 'Тест 2', 2, '[{"changed": {"fields": ["id_parent"]}}]', 8, 1),
(68, '2020-05-14 10:54:32.863672', '11', 'Пограничные столбы2', 2, '[{"changed": {"fields": ["name"]}}]', 8, 1),
(69, '2020-05-14 10:54:42.619021', '11', 'Пограничные столбы', 2, '[{"changed": {"fields": ["name"]}}]', 8, 1),
(70, '2020-05-14 15:07:02.630135', '10', 'Тест 2', 2, '[{"changed": {"fields": ["id_parent"]}}]', 8, 1),
(71, '2020-05-18 11:28:25.097729', '1', 'Витебская', 2, '[{"changed": {"fields": ["name"]}}]', 8, 1),
(72, '2020-05-18 12:18:24.913985', '6', '556 Брест', 2, '[{"changed": {"fields": ["name"]}}]', 8, 1),
(73, '2020-07-13 11:46:18.384257', '7', '557', 2, '[{"changed": {"fields": ["geo_gc_auth_group"]}}]', 10, 1),
(74, '2021-03-09 09:58:17.971885', '5', 'test', 1, '[{"added": {}}]', 4, 1),
(75, '2021-03-09 09:59:03.985738', '5', 'dev', 2, '[{"changed": {"fields": ["Username", "Staff status", "Superuser status", "Groups"]}}]', 4, 1),
(76, '2021-03-09 10:00:00.298619', '5', 'dev', 2, '[{"changed": {"fields": ["First name", "Last name"]}}]', 4, 5),
(77, '2021-03-11 16:57:04.119797', '9', 'Model_Alerts object (9)', 2, '[{"changed": {"fields": ["\\u0421\\u043e\\u0434\\u0435\\u0440\\u0436\\u0430\\u043d\\u0438\\u0435"]}}]', 7, 1),
(78, '2021-03-11 16:57:04.158578', '11', 'Model_Alerts object (11)', 2, '[{"changed": {"fields": ["\\u0421\\u043e\\u0434\\u0435\\u0440\\u0436\\u0430\\u043d\\u0438\\u0435"]}}]', 7, 1),
(79, '2021-03-11 16:57:28.399261', '9', 'Model_Alerts object (9)', 2, '[{"changed": {"fields": ["\\u0422\\u0438\\u043f"]}}]', 7, 1);

-- 
-- Вывод данных для таблицы django_content_type
--
INSERT INTO django_content_type VALUES
(1, 'admin', 'logentry'),
(3, 'auth', 'group'),
(2, 'auth', 'permission'),
(4, 'auth', 'user'),
(5, 'contenttypes', 'contenttype'),
(7, 'map', 'model_alerts'),
(9, 'map', 'model_auth_group'),
(10, 'map', 'model_geo_gc'),
(8, 'map', 'model_geo_geometry'),
(6, 'sessions', 'session');

-- 
-- Вывод данных для таблицы django_migrations
--
INSERT INTO django_migrations VALUES
(1, 'contenttypes', '0001_initial', '2020-03-06 10:55:08.430518'),
(2, 'auth', '0001_initial', '2020-03-06 10:55:09.864453'),
(3, 'admin', '0001_initial', '2020-03-06 10:55:14.565831'),
(4, 'admin', '0002_logentry_remove_auto_add', '2020-03-06 10:55:15.558801'),
(5, 'admin', '0003_logentry_add_action_flag_choices', '2020-03-06 10:55:15.590977'),
(6, 'contenttypes', '0002_remove_content_type_name', '2020-03-06 10:55:16.280783'),
(7, 'auth', '0002_alter_permission_name_max_length', '2020-03-06 10:55:16.828777'),
(8, 'auth', '0003_alter_user_email_max_length', '2020-03-06 10:55:17.312244'),
(9, 'auth', '0004_alter_user_username_opts', '2020-03-06 10:55:17.332909'),
(10, 'auth', '0005_alter_user_last_login_null', '2020-03-06 10:55:17.689167'),
(11, 'auth', '0006_require_contenttypes_0002', '2020-03-06 10:55:17.705291'),
(12, 'auth', '0007_alter_validators_add_error_messages', '2020-03-06 10:55:17.770415'),
(13, 'auth', '0008_alter_user_username_max_length', '2020-03-06 10:55:18.195841'),
(14, 'auth', '0009_alter_user_last_name_max_length', '2020-03-06 10:55:18.620879'),
(15, 'auth', '0010_alter_group_name_max_length', '2020-03-06 10:55:19.096219'),
(16, 'auth', '0011_update_proxy_permissions', '2020-03-06 10:55:19.115951'),
(17, 'sessions', '0001_initial', '2020-03-06 10:55:19.278226'),
(18, 'map', '0001_initial', '2020-03-11 08:54:43.636471'),
(19, 'map', '0002_auto_20201015_1442', '2020-10-15 11:42:19.14115'),
(20, 'auth', '0012_alter_user_first_name_max_length', '2021-03-09 12:17:31.679685');

-- 
-- Вывод данных для таблицы django_session
--
INSERT INTO django_session VALUES
('2i1wk00q2entgzmq8zztmloqucafb9w0', 'ZjU0MzM1NjYxMDIwYTEzMTA4MWFkNmE0OTcyNDI2N2YwMzBkYzMwMjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJlNzg2MTFhNWY5OGFlMDZkYTJiYmZhNTgwMmQwNDFjMDAxMThkMjNiIn0=', '2020-05-20 15:00:50.136385'),
('35yqiuwu638mh6qqab12k1fuenybwf85', 'ZjU0MzM1NjYxMDIwYTEzMTA4MWFkNmE0OTcyNDI2N2YwMzBkYzMwMjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJlNzg2MTFhNWY5OGFlMDZkYTJiYmZhNTgwMmQwNDFjMDAxMThkMjNiIn0=', '2020-10-01 07:41:58.997526'),
('4ydyybsi94yjnpjdl0q4payvz9c78v4m', 'ZjU0MzM1NjYxMDIwYTEzMTA4MWFkNmE0OTcyNDI2N2YwMzBkYzMwMjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJlNzg2MTFhNWY5OGFlMDZkYTJiYmZhNTgwMmQwNDFjMDAxMThkMjNiIn0=', '2020-08-25 11:43:51.294492'),
('7qz16g8m96rselet4vhrg0qr3olrpb2r', 'ZjU0MzM1NjYxMDIwYTEzMTA4MWFkNmE0OTcyNDI2N2YwMzBkYzMwMjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJlNzg2MTFhNWY5OGFlMDZkYTJiYmZhNTgwMmQwNDFjMDAxMThkMjNiIn0=', '2020-08-06 07:28:25.69888'),
('8izkxi540drtsb3f3wmm7r4taqhftu16', 'ZjU0MzM1NjYxMDIwYTEzMTA4MWFkNmE0OTcyNDI2N2YwMzBkYzMwMjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJlNzg2MTFhNWY5OGFlMDZkYTJiYmZhNTgwMmQwNDFjMDAxMThkMjNiIn0=', '2020-03-27 10:12:27.143688'),
('8kueyqmt5en1u5cpl3jr9ydy9zpuhj18', 'ZjU0MzM1NjYxMDIwYTEzMTA4MWFkNmE0OTcyNDI2N2YwMzBkYzMwMjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJlNzg2MTFhNWY5OGFlMDZkYTJiYmZhNTgwMmQwNDFjMDAxMThkMjNiIn0=', '2020-10-29 11:04:33.457276'),
('an30hwcky3l0zh9hcfq0d9hwhwdyme1h', 'ZjU0MzM1NjYxMDIwYTEzMTA4MWFkNmE0OTcyNDI2N2YwMzBkYzMwMjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJlNzg2MTFhNWY5OGFlMDZkYTJiYmZhNTgwMmQwNDFjMDAxMThkMjNiIn0=', '2020-03-24 13:40:10.593746'),
('au2za56vjko0yo3mcri5ofg5n7cfge8d', 'ZjU0MzM1NjYxMDIwYTEzMTA4MWFkNmE0OTcyNDI2N2YwMzBkYzMwMjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJlNzg2MTFhNWY5OGFlMDZkYTJiYmZhNTgwMmQwNDFjMDAxMThkMjNiIn0=', '2020-06-01 07:41:53.376759'),
('cibw3c8uzmofrjb1mvxrp84o56n5a3yd', '.eJxVjDsOwjAQBe_iGln-xNGakp4zWOv1Lg4gR4qTCnF3iJQC2jcz76USbmtNW-clTUWdlVWn3y0jPbjtoNyx3WZNc1uXKetd0Qft-joXfl4O9--gYq_fWnL01pvoxQgLFQ-Bs4OIYMSP0QLxYDKiixxELAmNMAQbGZwPDEa9P_NUOBY:1lJWnJ:6-6qkxaaUCQSp9NP1fgfmvg5FqRRMKeYz2OcUo6bUeU', '2021-03-23 07:28:41.037637'),
('ctj8b08fgnyxaok9d1gujtqs2wmbusdr', 'ZjU0MzM1NjYxMDIwYTEzMTA4MWFkNmE0OTcyNDI2N2YwMzBkYzMwMjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJlNzg2MTFhNWY5OGFlMDZkYTJiYmZhNTgwMmQwNDFjMDAxMThkMjNiIn0=', '2020-10-15 09:11:14.819455'),
('ekyu8c2l58yoekwyxseryqyzv3rmr76l', 'ZjU0MzM1NjYxMDIwYTEzMTA4MWFkNmE0OTcyNDI2N2YwMzBkYzMwMjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJlNzg2MTFhNWY5OGFlMDZkYTJiYmZhNTgwMmQwNDFjMDAxMThkMjNiIn0=', '2020-11-12 14:04:09.700121'),
('elzolnxhqfvqf2wg1xfsgosm5ks037yc', 'ZjU0MzM1NjYxMDIwYTEzMTA4MWFkNmE0OTcyNDI2N2YwMzBkYzMwMjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJlNzg2MTFhNWY5OGFlMDZkYTJiYmZhNTgwMmQwNDFjMDAxMThkMjNiIn0=', '2020-06-29 06:51:46.705641'),
('hb8aldn2vzw9f93eeb63ixzp0bm2ibgs', 'ZjU0MzM1NjYxMDIwYTEzMTA4MWFkNmE0OTcyNDI2N2YwMzBkYzMwMjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJlNzg2MTFhNWY5OGFlMDZkYTJiYmZhNTgwMmQwNDFjMDAxMThkMjNiIn0=', '2020-05-14 06:02:54.353631'),
('jfljdv4dccasdr0zduy8hl5obgd8t9q9', '.eJxVjDsOwjAQBe_iGln-xNGakp4zWOv1Lg4gR4qTCnF3iJQC2jcz76USbmtNW-clTUWdlVWn3y0jPbjtoNyx3WZNc1uXKetd0Qft-joXfl4O9--gYq_fWnL01pvoxQgLFQ-Bs4OIYMSP0QLxYDKiixxELAmNMAQbGZwPDEa9P_NUOBY:1lJzqg:dUfSnFzgD7W-74SYpKwJ2r-IB0Lx3Sj6M_c5OI_g1fI', '2021-03-24 14:30:06.887862'),
('muns9n5lj1cu0gubcgibqpdo23jmvfsj', 'ZjU0MzM1NjYxMDIwYTEzMTA4MWFkNmE0OTcyNDI2N2YwMzBkYzMwMjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJlNzg2MTFhNWY5OGFlMDZkYTJiYmZhNTgwMmQwNDFjMDAxMThkMjNiIn0=', '2020-03-26 08:42:41.151112'),
('mxa397tdw0f13k9jfiqd048n13zw0sgr', 'ZjU0MzM1NjYxMDIwYTEzMTA4MWFkNmE0OTcyNDI2N2YwMzBkYzMwMjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJlNzg2MTFhNWY5OGFlMDZkYTJiYmZhNTgwMmQwNDFjMDAxMThkMjNiIn0=', '2020-12-01 12:46:35.087964'),
('o1lidfigunjgjqema8rr576f346nq574', 'ZjU0MzM1NjYxMDIwYTEzMTA4MWFkNmE0OTcyNDI2N2YwMzBkYzMwMjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJlNzg2MTFhNWY5OGFlMDZkYTJiYmZhNTgwMmQwNDFjMDAxMThkMjNiIn0=', '2020-04-14 06:39:11.230353'),
('ot3fk6b4f8pkma3ly827un7g5q5g8fwd', 'ZjU0MzM1NjYxMDIwYTEzMTA4MWFkNmE0OTcyNDI2N2YwMzBkYzMwMjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJlNzg2MTFhNWY5OGFlMDZkYTJiYmZhNTgwMmQwNDFjMDAxMThkMjNiIn0=', '2020-08-25 11:44:51.547995'),
('piccxo3kv3xqm7lafznhk3a8koplk9ea', 'ZjU0MzM1NjYxMDIwYTEzMTA4MWFkNmE0OTcyNDI2N2YwMzBkYzMwMjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJlNzg2MTFhNWY5OGFlMDZkYTJiYmZhNTgwMmQwNDFjMDAxMThkMjNiIn0=', '2021-02-19 08:59:56.895455'),
('pxrhws5xquex1guupix4c9sna495kijt', 'ZjU0MzM1NjYxMDIwYTEzMTA4MWFkNmE0OTcyNDI2N2YwMzBkYzMwMjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJlNzg2MTFhNWY5OGFlMDZkYTJiYmZhNTgwMmQwNDFjMDAxMThkMjNiIn0=', '2020-08-06 07:31:58.81195'),
('rbpq29at24ix1adq9bdy5lpz3oy3n0ke', 'ZjU0MzM1NjYxMDIwYTEzMTA4MWFkNmE0OTcyNDI2N2YwMzBkYzMwMjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJlNzg2MTFhNWY5OGFlMDZkYTJiYmZhNTgwMmQwNDFjMDAxMThkMjNiIn0=', '2020-07-20 14:39:01.215976'),
('s5qak6v28nkc421m9s347vly3flma57p', 'ZjU0MzM1NjYxMDIwYTEzMTA4MWFkNmE0OTcyNDI2N2YwMzBkYzMwMjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJlNzg2MTFhNWY5OGFlMDZkYTJiYmZhNTgwMmQwNDFjMDAxMThkMjNiIn0=', '2020-07-02 16:51:02.875763'),
('sx8sno56f0c7auy6u7mc5ouosurmw7qn', 'ZjU0MzM1NjYxMDIwYTEzMTA4MWFkNmE0OTcyNDI2N2YwMzBkYzMwMjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJlNzg2MTFhNWY5OGFlMDZkYTJiYmZhNTgwMmQwNDFjMDAxMThkMjNiIn0=', '2020-05-05 14:21:02.994279'),
('t4928p6hs7yp6bv3fbj4w4kwd8krc3es', 'ZjU0MzM1NjYxMDIwYTEzMTA4MWFkNmE0OTcyNDI2N2YwMzBkYzMwMjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJlNzg2MTFhNWY5OGFlMDZkYTJiYmZhNTgwMmQwNDFjMDAxMThkMjNiIn0=', '2020-04-08 14:14:43.278438'),
('t8xa4me36npa42828vdrjje5pbekmzcf', 'ZjU0MzM1NjYxMDIwYTEzMTA4MWFkNmE0OTcyNDI2N2YwMzBkYzMwMjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJlNzg2MTFhNWY5OGFlMDZkYTJiYmZhNTgwMmQwNDFjMDAxMThkMjNiIn0=', '2020-04-29 06:26:20.987217'),
('uz3eixnw0djtxo4yyzv55c9yvd1xo4ss', 'ZjU0MzM1NjYxMDIwYTEzMTA4MWFkNmE0OTcyNDI2N2YwMzBkYzMwMjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJlNzg2MTFhNWY5OGFlMDZkYTJiYmZhNTgwMmQwNDFjMDAxMThkMjNiIn0=', '2020-09-10 12:54:44.174321'),
('vknx9lz9lb185a3v6qqtf34c777za3n3', 'ZjU0MzM1NjYxMDIwYTEzMTA4MWFkNmE0OTcyNDI2N2YwMzBkYzMwMjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJlNzg2MTFhNWY5OGFlMDZkYTJiYmZhNTgwMmQwNDFjMDAxMThkMjNiIn0=', '2020-07-20 14:38:49.399159'),
('wcfgxkno9qzbkj3iktr91qthbgzf324t', '.eJxVjDsOwjAQBe_iGln-xNGakp4zWOv1Lg4gR4qTCnF3iJQC2jcz76USbmtNW-clTUWdlVWn3y0jPbjtoNyx3WZNc1uXKetd0Qft-joXfl4O9--gYq_fWnL01pvoxQgLFQ-Bs4OIYMSP0QLxYDKiixxELAmNMAQbGZwPDEa9P_NUOBY:1lJY8R:KmF14gLQrT_1aloEgj5BHhPJvRmpu8hDPsqja9RUFcA', '2021-03-23 08:54:35.339087'),
('xrefrv4cuyu1o94tj31m1nbu9nh2ttdz', 'ZjU0MzM1NjYxMDIwYTEzMTA4MWFkNmE0OTcyNDI2N2YwMzBkYzMwMjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJlNzg2MTFhNWY5OGFlMDZkYTJiYmZhNTgwMmQwNDFjMDAxMThkMjNiIn0=', '2021-03-16 07:26:18.439871'),
('yhlr16q167xl2ffdtvu0ccospd5fg2an', 'ZjU0MzM1NjYxMDIwYTEzMTA4MWFkNmE0OTcyNDI2N2YwMzBkYzMwMjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJlNzg2MTFhNWY5OGFlMDZkYTJiYmZhNTgwMmQwNDFjMDAxMThkMjNiIn0=', '2020-09-10 06:21:28.489559'),
('ymrke1gbvxvgpjpze2quncayywq4q0tp', 'ZjU0MzM1NjYxMDIwYTEzMTA4MWFkNmE0OTcyNDI2N2YwMzBkYzMwMjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJlNzg2MTFhNWY5OGFlMDZkYTJiYmZhNTgwMmQwNDFjMDAxMThkMjNiIn0=', '2020-07-14 11:41:40.553727'),
('yzcf3xwql6gvviyfe3asy9iulykhd8vc', 'ZjU0MzM1NjYxMDIwYTEzMTA4MWFkNmE0OTcyNDI2N2YwMzBkYzMwMjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJlNzg2MTFhNWY5OGFlMDZkYTJiYmZhNTgwMmQwNDFjMDAxMThkMjNiIn0=', '2020-04-17 15:59:36.48865'),
('yzdfv5sththkpp9x7o8ptp3gyjudqq7w', '.eJxVjDsOwjAQBe_iGln-xNGakp4zWOv1Lg4gR4qTCnF3iJQC2jcz76USbmtNW-clTUWdlVWn3y0jPbjtoNyx3WZNc1uXKetd0Qft-joXfl4O9--gYq_fWnL01pvoxQgLFQ-Bs4OIYMSP0QLxYDKiixxELAmNMAQbGZwPDEa9P_NUOBY:1lJbMZ:epdmNbkMhsmmKTARXUfiOTcLIWqMQcBKb-PI_dqBf_4', '2021-03-23 12:21:23.81391');
-- 
-- Восстановить предыдущий режим SQL (SQL mode)
-- 
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;

-- 
-- Включение внешних ключей
-- 
/*!40014 SET FOREIGN_KEY_CHECKS = @OLD_FOREIGN_KEY_CHECKS */;
