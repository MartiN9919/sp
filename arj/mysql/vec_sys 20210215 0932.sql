--
-- Скрипт сгенерирован Devart dbForge Studio for MySQL, Версия 7.3.137.0
-- Домашняя страница продукта: http://www.devart.com/ru/dbforge/mysql/studio
-- Дата скрипта: 15.02.2021 9:32:59
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
USE vec_sys;

--
-- Удалить таблицу "alerts"
--
DROP TABLE IF EXISTS alerts;

--
-- Установка базы данных по умолчанию
--
USE vec_sys;

--
-- Создать таблицу "alerts"
--
CREATE TABLE alerts (
  id int(11) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'порядковый номер',
  content varchar(255) NOT NULL COMMENT 'Содержание сообщения',
  type varchar(8) NOT NULL DEFAULT 'info' COMMENT 'Тип сообщения [error], success, warn',
  wait tinyint(4) UNSIGNED NOT NULL DEFAULT 0 COMMENT 'Время показа сообщения, в сек. 0 - не скрывать',
  owner varchar(5) NOT NULL DEFAULT '' COMMENT 'id владельца сообщения',
  users varchar(255) NOT NULL DEFAULT '' COMMENT 'id пользователей-адресатов, через пробел. Если не указано - то всем',
  groups varchar(255) NOT NULL DEFAULT '' COMMENT 'Группы, которым адресовано сообщение, через пробел. Если не указано - то всем',
  enabled tinyint(1) NOT NULL DEFAULT 1 COMMENT 'доступность',
  descript varchar(255) NOT NULL DEFAULT '' COMMENT 'Описание',
  PRIMARY KEY (id)
)
ENGINE = INNODB
AUTO_INCREMENT = 12
AVG_ROW_LENGTH = 1489
CHARACTER SET utf8
COLLATE utf8_general_ci
COMMENT = 'Сообщения пользователям'
ROW_FORMAT = DYNAMIC;

-- 
-- Вывод данных для таблицы alerts
--
INSERT INTO alerts VALUES
(1, 'Храните пароль в тайне!', 'error', 10, '', '', '', 1, 'Дежурное сообщение'),
(2, 'Второй тип сообщения', 'info', 30, '', '', 'level_gpk type_ord', 1, ''),
(3, '', 'info', 0, '', '', '', 0, ''),
(4, '', 'warn', 0, '', '', '', 0, ''),
(5, '', 'warn', 0, '', '', '', 0, ''),
(6, '', 'error', 0, '', '', '', 0, ''),
(7, '', 'warn', 0, '', '', '', 0, ''),
(8, '', 'warn', 0, '', '', '', 0, ''),
(9, 'Проверка связи', 'info', 0, '1', '1', '', 1, 'от пользователя с сайта'),
(10, '55555', 'info', 0, '1', '1', '', 1, 'от пользователя с сайта'),
(11, 'Проверка связи 2', 'info', 0, '1', '1', '', 1, 'от пользователя с сайта');
-- 
-- Восстановить предыдущий режим SQL (SQL mode)
-- 
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;

-- 
-- Включение внешних ключей
-- 
/*!40014 SET FOREIGN_KEY_CHECKS = @OLD_FOREIGN_KEY_CHECKS */;
