-- MySQL dump 10.13  Distrib 8.0.27, for Linux (x86_64)
--
-- Host: localhost    Database: test
-- ------------------------------------------------------
-- Server version	8.0.27-0ubuntu0.20.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=97 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add content type',4,'add_contenttype'),(14,'Can change content type',4,'change_contenttype'),(15,'Can delete content type',4,'delete_contenttype'),(16,'Can view content type',4,'view_contenttype'),(17,'Can add session',5,'add_session'),(18,'Can change session',5,'change_session'),(19,'Can delete session',5,'delete_session'),(20,'Can view session',5,'view_session'),(21,'Can add Группа',6,'add_modelownergroups'),(22,'Can change Группа',6,'change_modelownergroups'),(23,'Can delete Группа',6,'delete_modelownergroups'),(24,'Can view Группа',6,'view_modelownergroups'),(25,'Can add Линия',7,'add_modelownerlines'),(26,'Can change Линия',7,'change_modelownerlines'),(27,'Can delete Линия',7,'delete_modelownerlines'),(28,'Can view Линия',7,'view_modelownerlines'),(29,'Can add Регион',8,'add_modelownerregions'),(30,'Can change Регион',8,'change_modelownerregions'),(31,'Can delete Регион',8,'delete_modelownerregions'),(32,'Can view Регион',8,'view_modelownerregions'),(33,'Can add user',9,'add_modelcustomuser'),(34,'Can change user',9,'change_modelcustomuser'),(35,'Can delete user',9,'delete_modelcustomuser'),(36,'Can view user',9,'view_modelcustomuser'),(37,'Can add model owner line',10,'add_modelownerline'),(38,'Can change model owner line',10,'change_modelownerline'),(39,'Can delete model owner line',10,'delete_modelownerline'),(40,'Can view model owner line',10,'view_modelownerline'),(41,'Can add Скрипт',11,'add_modelscript'),(42,'Can change Скрипт',11,'change_modelscript'),(43,'Can delete Скрипт',11,'delete_modelscript'),(44,'Can view Скрипт',11,'view_modelscript'),(45,'Can add Классификатор',12,'add_modelkey'),(46,'Can change Классификатор',12,'change_modelkey'),(47,'Can delete Классификатор',12,'delete_modelkey'),(48,'Can view Классификатор',12,'view_modelkey'),(49,'Can add Список',13,'add_modellist'),(50,'Can change Список',13,'change_modellist'),(51,'Can delete Список',13,'delete_modellist'),(52,'Can view Список',13,'view_modellist'),(53,'Can add Поле списка',14,'add_modellistdop'),(54,'Can change Поле списка',14,'change_modellistdop'),(55,'Can delete Поле списка',14,'delete_modellistdop'),(56,'Can view Поле списка',14,'view_modellistdop'),(57,'Can add Объект',15,'add_modelobject'),(58,'Can change Объект',15,'change_modelobject'),(59,'Can delete Объект',15,'delete_modelobject'),(60,'Can view Объект',15,'view_modelobject'),(61,'Can add group',16,'add_group'),(62,'Can change group',16,'change_group'),(63,'Can delete group',16,'delete_group'),(64,'Can view group',16,'view_group'),(65,'Can add push information',17,'add_pushinformation'),(66,'Can change push information',17,'change_pushinformation'),(67,'Can delete push information',17,'delete_pushinformation'),(68,'Can view push information',17,'view_pushinformation'),(69,'Can add subscription info',18,'add_subscriptioninfo'),(70,'Can change subscription info',18,'change_subscriptioninfo'),(71,'Can delete subscription info',18,'delete_subscriptioninfo'),(72,'Can view subscription info',18,'view_subscriptioninfo'),(73,'Can add Файл',20,'add_modelofficialdocument'),(74,'Can change Файл',20,'change_modelofficialdocument'),(75,'Can delete Файл',20,'delete_modelofficialdocument'),(76,'Can view Файл',20,'view_modelofficialdocument'),(77,'Can add Уведомление',19,'add_modelnotification'),(78,'Can change Уведомление',19,'change_modelnotification'),(79,'Can delete Уведомление',19,'delete_modelnotification'),(80,'Can view Уведомление',19,'view_modelnotification'),(81,'Can add Тригеры',24,'add_modeltrigger'),(82,'Can change Тригеры',24,'change_modeltrigger'),(83,'Can delete Тригеры',24,'delete_modeltrigger'),(84,'Can view Тригеры',24,'view_modeltrigger'),(85,'Can add Формат телефонный номеров',23,'add_modelphonenumberformat'),(86,'Can change Формат телефонный номеров',23,'change_modelphonenumberformat'),(87,'Can delete Формат телефонный номеров',23,'delete_modelphonenumberformat'),(88,'Can view Формат телефонный номеров',23,'view_modelphonenumberformat'),(89,'Can add Классификатор объекта',21,'add_objectkey'),(90,'Can change Классификатор объекта',21,'change_objectkey'),(91,'Can delete Классификатор объекта',21,'delete_objectkey'),(92,'Can view Классификатор объекта',21,'view_objectkey'),(93,'Can add Классификатор связь',22,'add_rel'),(94,'Can change Классификатор связь',22,'change_rel'),(95,'Can delete Классификатор связь',22,'delete_rel'),(96,'Can view Классификатор связь',22,'view_rel');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `authentication_modelcustomuser`
--

DROP TABLE IF EXISTS `authentication_modelcustomuser`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `authentication_modelcustomuser` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `is_write` tinyint(1) DEFAULT NULL,
  `owner_groups_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `authentication_modelcustomuser`
--

LOCK TABLES `authentication_modelcustomuser` WRITE;
/*!40000 ALTER TABLE `authentication_modelcustomuser` DISABLE KEYS */;
INSERT INTO `authentication_modelcustomuser` VALUES (1,'pbkdf2_sha256$260000$EQNaGBrGbtglTYYTg47k4m$qDhQUTkRjsUCItZs38l/BmThfMx8WQdYnXN8h5u0xIQ=','2021-12-07 07:39:48.129057',1,'admin','Иван','Иванов',1,1,1,1);
/*!40000 ALTER TABLE `authentication_modelcustomuser` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `authentication_modelcustomuser_groups`
--

DROP TABLE IF EXISTS `authentication_modelcustomuser_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `authentication_modelcustomuser_groups` (
  `id` int NOT NULL AUTO_INCREMENT,
  `modelcustomuser_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `authentication_modelcustomuser_groups`
--

LOCK TABLES `authentication_modelcustomuser_groups` WRITE;
/*!40000 ALTER TABLE `authentication_modelcustomuser_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `authentication_modelcustomuser_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `authentication_modelcustomuser_user_permissions`
--

DROP TABLE IF EXISTS `authentication_modelcustomuser_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `authentication_modelcustomuser_user_permissions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `modelcustomuser_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `authentication_modelcustomuser_user_permissions`
--

LOCK TABLES `authentication_modelcustomuser_user_permissions` WRITE;
/*!40000 ALTER TABLE `authentication_modelcustomuser_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `authentication_modelcustomuser_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_authentic` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_authentic` FOREIGN KEY (`user_id`) REFERENCES `authentication_modelcustomuser` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=748 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(9,'authentication','modelcustomuser'),(6,'authentication','modelownergroups'),(7,'authentication','modelownerlines'),(8,'authentication','modelownerregions'),(12,'classifier','modelkey'),(13,'classifier','modellist'),(14,'classifier','modellistdop'),(15,'classifier','modelobject'),(23,'classifier','modelphonenumberformat'),(21,'classifier','objectkey'),(22,'classifier','rel'),(4,'contenttypes','contenttype'),(19,'notifications','modelnotification'),(20,'official_documents','modelofficialdocument'),(10,'script','modelownerline'),(11,'script','modelscript'),(25,'script','modelscriptvariable'),(24,'script','modeltrigger'),(5,'sessions','session'),(16,'webpush','group'),(17,'webpush','pushinformation'),(18,'webpush','subscriptioninfo');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2021-04-16 09:22:18.033414'),(2,'contenttypes','0002_remove_content_type_name','2021-04-16 09:22:18.471231'),(3,'auth','0001_initial','2021-04-16 09:22:18.514971'),(4,'auth','0002_alter_permission_name_max_length','2021-04-16 09:22:18.623022'),(5,'auth','0003_alter_user_email_max_length','2021-04-16 09:22:18.627916'),(6,'auth','0004_alter_user_username_opts','2021-04-16 09:22:18.632945'),(7,'auth','0005_alter_user_last_login_null','2021-04-16 09:22:18.638923'),(8,'auth','0006_require_contenttypes_0002','2021-04-16 09:22:18.642937'),(9,'auth','0007_alter_validators_add_error_messages','2021-04-16 09:22:18.648847'),(10,'auth','0008_alter_user_username_max_length','2021-04-16 09:22:18.655045'),(11,'auth','0009_alter_user_last_name_max_length','2021-04-16 09:22:18.661505'),(12,'auth','0010_alter_group_name_max_length','2021-04-16 09:22:18.692224'),(13,'auth','0011_update_proxy_permissions','2021-04-16 09:22:18.699659'),(14,'auth','0012_alter_user_first_name_max_length','2021-04-16 09:22:18.705987'),(15,'authentication','0001_initial','2021-04-16 09:22:18.755041'),(16,'admin','0001_initial','2021-04-16 09:27:33.084976'),(17,'admin','0002_logentry_remove_auto_add','2021-04-16 09:27:33.137154'),(18,'admin','0003_logentry_add_action_flag_choices','2021-04-16 09:27:33.144234'),(19,'classifier','0001_initial','2021-04-16 09:27:33.151526'),(20,'script','0001_initial','2021-04-16 09:27:33.156991'),(21,'sessions','0001_initial','2021-04-16 09:27:33.174605'),(22,'webpush','0001_initial','2021-04-19 06:00:47.489369'),(23,'webpush','0002_auto_20190603_0005','2021-04-19 06:00:47.525894'),(24,'notifications','0001_initial','2021-04-21 13:56:04.327465'),(25,'official_documents','0001_initial','2021-04-21 13:56:04.333510'),(26,'script','0002_delete_modelownerline','2021-04-21 13:56:04.336857'),(27,'classifier','0002_modelphonenumberformat_objectkey_rel','2021-08-31 06:55:33.773116'),(28,'script','0002_modeltrigger','2021-08-31 06:55:33.781830');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `obj_case_row`
--

DROP TABLE IF EXISTS `obj_case_row`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `obj_case_row` (
  `rec_id` int unsigned NOT NULL,
  `key_id` smallint unsigned NOT NULL,
  `val` varchar(255) NOT NULL,
  `dat` datetime DEFAULT CURRENT_TIMESTAMP,
  KEY `ind_id` (`rec_id`),
  KEY `ind_id_key` (`rec_id`,`key_id`),
  FULLTEXT KEY `obj_case_row_val_IDX` (`val`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 AVG_ROW_LENGTH=2048 ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `obj_case_row`
--

LOCK TABLES `obj_case_row` WRITE;
/*!40000 ALTER TABLE `obj_case_row` DISABLE KEYS */;
/*!40000 ALTER TABLE `obj_case_row` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `obj_doc_row`
--

DROP TABLE IF EXISTS `obj_doc_row`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `obj_doc_row` (
  `rec_id` int unsigned NOT NULL,
  `key_id` smallint unsigned NOT NULL,
  `val` varchar(255) NOT NULL,
  `dat` datetime DEFAULT NULL,
  KEY `ind_id` (`rec_id`),
  KEY `ind_id_key` (`rec_id`,`key_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `obj_doc_row`
--

LOCK TABLES `obj_doc_row` WRITE;
/*!40000 ALTER TABLE `obj_doc_row` DISABLE KEYS */;
/*!40000 ALTER TABLE `obj_doc_row` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `obj_file_col`
--

DROP TABLE IF EXISTS `obj_file_col`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `obj_file_col` (
  `rec_id` int unsigned NOT NULL,
  `type` tinyint unsigned DEFAULT NULL,
  `path` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`rec_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `obj_file_col`
--

LOCK TABLES `obj_file_col` WRITE;
/*!40000 ALTER TABLE `obj_file_col` DISABLE KEYS */;
/*!40000 ALTER TABLE `obj_file_col` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `obj_file_row`
--

DROP TABLE IF EXISTS `obj_file_row`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `obj_file_row` (
  `rec_id` int unsigned NOT NULL,
  `key_id` smallint unsigned NOT NULL,
  `val` varchar(255) NOT NULL,
  `dat` datetime DEFAULT NULL,
  KEY `ind_id` (`rec_id`),
  KEY `ind_id_key` (`rec_id`,`key_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `obj_file_row`
--

LOCK TABLES `obj_file_row` WRITE;
/*!40000 ALTER TABLE `obj_file_row` DISABLE KEYS */;
/*!40000 ALTER TABLE `obj_file_row` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `obj_free_row`
--

DROP TABLE IF EXISTS `obj_free_row`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `obj_free_row` (
  `rec_id` int unsigned NOT NULL,
  `key_id` smallint unsigned NOT NULL,
  `val` varchar(255) NOT NULL,
  `dat` datetime DEFAULT NULL,
  KEY `ind_id` (`rec_id`),
  KEY `ind_id_key` (`rec_id`,`key_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 AVG_ROW_LENGTH=5461 ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `obj_free_row`
--

LOCK TABLES `obj_free_row` WRITE;
/*!40000 ALTER TABLE `obj_free_row` DISABLE KEYS */;
/*!40000 ALTER TABLE `obj_free_row` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `obj_geometry_col`
--

DROP TABLE IF EXISTS `obj_geometry_col`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `obj_geometry_col` (
  `rec_id` int unsigned NOT NULL,
  `parent_id` int unsigned NOT NULL DEFAULT '0',
  `name` varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `icon` varchar(25) NOT NULL,
  `location` geomcollection DEFAULT NULL,
  `dat` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 AVG_ROW_LENGTH=1260 ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `obj_geometry_col`
--

LOCK TABLES `obj_geometry_col` WRITE;
/*!40000 ALTER TABLE `obj_geometry_col` DISABLE KEYS */;
/*!40000 ALTER TABLE `obj_geometry_col` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `obj_geometry_row`
--

DROP TABLE IF EXISTS `obj_geometry_row`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `obj_geometry_row` (
  `rec_id` int unsigned NOT NULL,
  `key_id` smallint unsigned NOT NULL,
  `val` varchar(255) NOT NULL,
  `dat` datetime DEFAULT NULL,
  KEY `ind_id` (`rec_id`),
  KEY `ind_id_key` (`rec_id`,`key_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 AVG_ROW_LENGTH=1638 ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `obj_geometry_row`
--

LOCK TABLES `obj_geometry_row` WRITE;
/*!40000 ALTER TABLE `obj_geometry_row` DISABLE KEYS */;
/*!40000 ALTER TABLE `obj_geometry_row` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `obj_person_l_row`
--

DROP TABLE IF EXISTS `obj_person_l_row`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `obj_person_l_row` (
  `rec_id` int unsigned NOT NULL,
  `key_id` smallint unsigned NOT NULL,
  `val` varchar(255) NOT NULL,
  `dat` datetime DEFAULT NULL,
  KEY `ind_id` (`rec_id`),
  KEY `ind_id_key` (`rec_id`,`key_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `obj_person_l_row`
--

LOCK TABLES `obj_person_l_row` WRITE;
/*!40000 ALTER TABLE `obj_person_l_row` DISABLE KEYS */;
/*!40000 ALTER TABLE `obj_person_l_row` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `obj_person_p_row`
--

DROP TABLE IF EXISTS `obj_person_p_row`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `obj_person_p_row` (
  `rec_id` int unsigned NOT NULL,
  `key_id` smallint unsigned NOT NULL,
  `val` varchar(255) NOT NULL,
  `dat` datetime DEFAULT CURRENT_TIMESTAMP,
  KEY `ind_id` (`rec_id`),
  KEY `ind_id_key` (`rec_id`,`key_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `obj_person_p_row`
--

LOCK TABLES `obj_person_p_row` WRITE;
/*!40000 ALTER TABLE `obj_person_p_row` DISABLE KEYS */;
/*!40000 ALTER TABLE `obj_person_p_row` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `obj_point_col`
--

DROP TABLE IF EXISTS `obj_point_col`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `obj_point_col` (
  `rec_id` int unsigned NOT NULL,
  `point` point DEFAULT NULL,
  `dat` datetime DEFAULT NULL,
  KEY `IDX_id` (`rec_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 AVG_ROW_LENGTH=2520 ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `obj_point_col`
--

LOCK TABLES `obj_point_col` WRITE;
/*!40000 ALTER TABLE `obj_point_col` DISABLE KEYS */;
/*!40000 ALTER TABLE `obj_point_col` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `obj_point_row`
--

DROP TABLE IF EXISTS `obj_point_row`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `obj_point_row` (
  `rec_id` int unsigned NOT NULL,
  `key_id` smallint unsigned NOT NULL,
  `val` varchar(255) NOT NULL,
  `dat` datetime DEFAULT NULL,
  KEY `ind_id` (`rec_id`),
  KEY `ind_id_key` (`rec_id`,`key_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `obj_point_row`
--

LOCK TABLES `obj_point_row` WRITE;
/*!40000 ALTER TABLE `obj_point_row` DISABLE KEYS */;
/*!40000 ALTER TABLE `obj_point_row` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `obj_telefon_row`
--

DROP TABLE IF EXISTS `obj_telefon_row`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `obj_telefon_row` (
  `rec_id` int unsigned NOT NULL,
  `key_id` smallint unsigned NOT NULL,
  `val` varchar(255) NOT NULL,
  `dat` datetime DEFAULT NULL,
  KEY `ind_id` (`rec_id`),
  KEY `ind_id_key` (`rec_id`,`key_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `obj_telefon_row`
--

LOCK TABLES `obj_telefon_row` WRITE;
/*!40000 ALTER TABLE `obj_telefon_row` DISABLE KEYS */;
/*!40000 ALTER TABLE `obj_telefon_row` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `obj_transport_row`
--

DROP TABLE IF EXISTS `obj_transport_row`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `obj_transport_row` (
  `rec_id` int unsigned NOT NULL,
  `key_id` smallint unsigned NOT NULL,
  `val` varchar(255) NOT NULL,
  `dat` datetime DEFAULT NULL,
  KEY `ind_id` (`rec_id`),
  KEY `ind_id_key` (`rec_id`,`key_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `obj_transport_row`
--

LOCK TABLES `obj_transport_row` WRITE;
/*!40000 ALTER TABLE `obj_transport_row` DISABLE KEYS */;
/*!40000 ALTER TABLE `obj_transport_row` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `owner_groups`
--

DROP TABLE IF EXISTS `owner_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `owner_groups` (
  `id` int NOT NULL,
  `owner_regions_id` tinyint unsigned NOT NULL,
  `owner_lines_id` tinyint unsigned NOT NULL,
  `title` varchar(255) NOT NULL,
  `descript` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ind_owner_line_id` (`owner_lines_id`),
  KEY `ind_owner_region_id` (`owner_regions_id`),
  CONSTRAINT `ind_owner_line_id` FOREIGN KEY (`owner_lines_id`) REFERENCES `owner_lines` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `ind_owner_region_id` FOREIGN KEY (`owner_regions_id`) REFERENCES `owner_regions` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 AVG_ROW_LENGTH=364 ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `owner_groups`
--

LOCK TABLES `owner_groups` WRITE;
/*!40000 ALTER TABLE `owner_groups` DISABLE KEYS */;
INSERT INTO `owner_groups` VALUES (1,1,1,'Администратор','!!!'),(22,2,2,'ГПК А',NULL),(23,2,3,'ГПК О',NULL),(24,2,4,'ГПК И',NULL),(25,2,5,'ГПКД',NULL),(32,3,2,'Полоцк А',NULL),(33,3,3,'Полоцк О',NULL),(34,3,4,'Полоцк И',NULL),(35,3,5,'Полоцк Д',NULL),(42,4,2,'Сморгонь А',NULL),(43,4,3,'Сморгонь О',NULL),(44,4,4,'Сморгонь И',NULL),(45,4,5,'Сморгонь Д',NULL),(52,5,2,'Лида А',NULL),(53,5,3,'Лида О',NULL),(54,5,4,'Лида И',NULL),(55,5,5,'Лида Д',NULL),(62,6,2,'Гродно А',NULL),(63,6,3,'Гродно О',NULL),(64,6,4,'Гродно И',NULL),(65,6,5,'Гродно Д',NULL),(72,7,2,'Брест А',NULL),(73,7,3,'Брест О',NULL),(74,7,4,'Брест И',NULL),(75,7,5,'Брест Д',NULL),(82,8,2,'Пинск А',NULL),(83,8,3,'Пинск О',NULL),(84,8,4,'Пинск И',NULL),(85,8,5,'Пинск Д',NULL),(92,9,2,'Мозырь А',NULL),(93,9,3,'Мозырь О',NULL),(94,9,4,'Мозырь И',NULL),(95,9,5,'Мозырь Д',NULL),(102,10,2,'Гомель А',NULL),(103,10,3,'Гомель О',NULL),(104,10,4,'Гомель И',NULL),(105,10,5,'Гомель Д',NULL),(112,11,2,'ОП А',NULL),(113,11,3,'ОП О',NULL),(114,11,4,'ОП И',NULL),(115,11,5,'ОП Д',NULL),(122,12,2,'ОС А',NULL),(123,12,3,'ОС О',NULL),(124,12,4,'ОС И',NULL),(125,12,5,'ОС Д',NULL);
/*!40000 ALTER TABLE `owner_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `owner_lines`
--

DROP TABLE IF EXISTS `owner_lines`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `owner_lines` (
  `id` tinyint unsigned NOT NULL,
  `parent_id` tinyint unsigned NOT NULL,
  `title` varchar(255) NOT NULL,
  UNIQUE KEY `ind_id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 AVG_ROW_LENGTH=4096 ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `owner_lines`
--

LOCK TABLES `owner_lines` WRITE;
/*!40000 ALTER TABLE `owner_lines` DISABLE KEYS */;
INSERT INTO `owner_lines` VALUES (1,0,'Администратор'),(2,1,'a'),(3,2,'o'),(4,2,'i'),(5,2,'d');
/*!40000 ALTER TABLE `owner_lines` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `owner_regions`
--

DROP TABLE IF EXISTS `owner_regions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `owner_regions` (
  `id` tinyint unsigned NOT NULL,
  `parent_id` tinyint unsigned NOT NULL,
  `title` varchar(255) NOT NULL,
  UNIQUE KEY `ind_id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 AVG_ROW_LENGTH=1489 ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `owner_regions`
--

LOCK TABLES `owner_regions` WRITE;
/*!40000 ALTER TABLE `owner_regions` DISABLE KEYS */;
INSERT INTO `owner_regions` VALUES (1,0,'Администратор'),(2,1,'ГПК'),(3,2,'Полоцк'),(4,2,'Сморгонь'),(5,2,'Лида'),(6,2,'Гродно'),(7,2,'Брест'),(8,2,'Пинск'),(9,2,'Мозырь'),(10,2,'Гомель'),(11,2,'ОП'),(12,2,'ОС');
/*!40000 ALTER TABLE `owner_regions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rel`
--

DROP TABLE IF EXISTS `rel`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rel` (
  `rec_id` int unsigned DEFAULT NULL,
  `key_id` smallint unsigned NOT NULL,
  `dat` datetime DEFAULT NULL,
  `obj_id_1` tinyint unsigned NOT NULL,
  `rec_id_1` int unsigned NOT NULL,
  `obj_id_2` tinyint unsigned NOT NULL,
  `rec_id_2` int unsigned NOT NULL,
  `val` varchar(100) DEFAULT NULL,
  KEY `ind_key_id` (`key_id`),
  KEY `ind_obj_1` (`obj_id_1`),
  KEY `ind_obj_2` (`obj_id_2`),
  KEY `ind_obj_rec_1` (`obj_id_1`,`rec_id_1`),
  KEY `ind_obj_rec_2` (`obj_id_2`,`rec_id_2`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 AVG_ROW_LENGTH=4096 ROW_FORMAT=DYNAMIC
/*!50500 PARTITION BY RANGE  COLUMNS(key_id)
(PARTITION p10000 VALUES LESS THAN (10000) ENGINE = InnoDB,
 PARTITION p20000 VALUES LESS THAN (20000) ENGINE = InnoDB,
 PARTITION p30000 VALUES LESS THAN (30000) ENGINE = InnoDB,
 PARTITION p40000 VALUES LESS THAN (40000) ENGINE = InnoDB,
 PARTITION p50000 VALUES LESS THAN (50000) ENGINE = InnoDB,
 PARTITION p60000 VALUES LESS THAN (60000) ENGINE = InnoDB,
 PARTITION pmax VALUES LESS THAN (MAXVALUE) ENGINE = InnoDB) */;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rel`
--

LOCK TABLES `rel` WRITE;
/*!40000 ALTER TABLE `rel` DISABLE KEYS */;
/*!40000 ALTER TABLE `rel` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sys_id`
--

DROP TABLE IF EXISTS `sys_id`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sys_id` (
  `obj_id` tinyint unsigned NOT NULL,
  `id` int unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`obj_id`),
  CONSTRAINT `sys_id_FK` FOREIGN KEY (`obj_id`) REFERENCES `sys_obj` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 AVG_ROW_LENGTH=1820 ROW_FORMAT=DYNAMIC COMMENT='Счетчик id объектов';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_id`
--

LOCK TABLES `sys_id` WRITE;
/*!40000 ALTER TABLE `sys_id` DISABLE KEYS */;
INSERT INTO `sys_id` VALUES (1,1),(10,1),(15,1),(20,1),(25,1),(30,1),(35,1),(40,1),(45,1),(50,1),(52,1);
/*!40000 ALTER TABLE `sys_id` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sys_key`
--

DROP TABLE IF EXISTS `sys_key`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sys_key` (
  `id` smallint unsigned NOT NULL AUTO_INCREMENT,
  `obj_id` tinyint unsigned NOT NULL,
  `col` tinyint(1) NOT NULL DEFAULT '0' COMMENT 'таблица COL, иначе таблица ROW',
  `need` tinyint(1) NOT NULL DEFAULT '0' COMMENT 'обязательный ключ',
  `type` enum('number','text','datetime','date','checkbox','geometry','phone_number','file_photo','file_any') CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT 'text' COMMENT 'тип данных',
  `list_id` mediumint unsigned DEFAULT NULL,
  `name` varchar(25) DEFAULT NULL,
  `title` varchar(50) NOT NULL,
  `hint` varchar(255) DEFAULT NULL COMMENT 'отображаемая подсказка',
  `descript` text CHARACTER SET utf8 COLLATE utf8_general_ci,
  `rel_obj_1_id` tinyint unsigned DEFAULT NULL,
  `rel_obj_2_id` tinyint unsigned DEFAULT NULL,
  `path` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `priority` smallint unsigned DEFAULT NULL,
  `visible` enum('none','only_value','all') CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ind_id` (`id`),
  KEY `ind_id_name` (`obj_id`,`name`),
  KEY `ind_list` (`list_id`),
  KEY `ind_rel_obj_1` (`rel_obj_1_id`),
  KEY `ind_rel_obj_2` (`rel_obj_2_id`),
  KEY `sys_key_FK` (`path`),
  CONSTRAINT `ind_list` FOREIGN KEY (`list_id`) REFERENCES `sys_list_top` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `sys_key_FK` FOREIGN KEY (`obj_id`) REFERENCES `sys_obj` (`id`),
  CONSTRAINT `sys_key_FK_1` FOREIGN KEY (`rel_obj_1_id`) REFERENCES `sys_obj` (`id`),
  CONSTRAINT `sys_key_FK_2` FOREIGN KEY (`rel_obj_2_id`) REFERENCES `sys_obj` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=50215 DEFAULT CHARSET=utf8mb3 AVG_ROW_LENGTH=2048 ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_key`
--

LOCK TABLES `sys_key` WRITE;
/*!40000 ALTER TABLE `sys_key` DISABLE KEYS */;
INSERT INTO `sys_key` VALUES (1,1,0,0,'text',NULL,'rel_doc','Основание связи',NULL,'Служебная связь для указания источника информации о связи',1,20,NULL,NULL,'all'),(1101,1,0,0,'text',NULL,NULL,'Задержание (КоАП)/начало',NULL,NULL,35,45,NULL,NULL,'all'),(1102,1,0,0,'text',NULL,NULL,'Задержание (УПК)/начало',NULL,NULL,35,45,NULL,NULL,'all'),(1201,1,0,0,'text',NULL,NULL,'Авто ФЛ/владение/начало',NULL,NULL,35,50,NULL,NULL,'all'),(1202,1,0,0,'text',NULL,NULL,'Авто ФЛ/владение/конец',NULL,NULL,35,50,NULL,NULL,'all'),(1301,1,0,0,'text',54,NULL,'Учеба','','',35,40,NULL,NULL,'all'),(1304,1,0,1,'text',NULL,NULL,'Работа/начало',NULL,NULL,35,40,NULL,NULL,'all'),(1305,1,0,0,'text',NULL,NULL,'Работа/конец',NULL,NULL,35,40,NULL,NULL,'all'),(1306,1,0,0,'text',NULL,NULL,'Отпуск/начало',NULL,NULL,35,40,NULL,NULL,'all'),(1307,1,0,0,'text',NULL,NULL,'Отпуск/конец',NULL,NULL,35,40,NULL,NULL,'all'),(15000,15,0,1,'text',53,'owner_add_rw','Владелец: добавить чтение/запись','','! СПЕЦИАЛЬНЫЙ КЛЮЧ !',NULL,NULL,NULL,2,'all'),(15001,15,0,0,'text',53,'owner_add_ro','Владелец: добавить только чтение','','! СПЕЦИАЛЬНЫЙ КЛЮЧ !',NULL,NULL,NULL,NULL,'all'),(15002,15,0,0,'text',53,'owner_add_ro_limit','Владелец: добавить только чтение на период','','! СПЕЦИАЛЬНЫЙ КЛЮЧ !',NULL,NULL,NULL,NULL,'all'),(15003,15,0,0,'text',53,'owner_del','Владелец: запретить доступ','','! СПЕЦИАЛЬНЫЙ КЛЮЧ !',NULL,NULL,NULL,NULL,'all'),(15004,15,0,0,'checkbox',NULL,'owner_visible','Владелец: Отображать при запрете','','',NULL,NULL,NULL,NULL,'all'),(15010,15,0,0,'text',NULL,'type','Тип файла',NULL,'не  видится данный классификатор как необходимый для описания объекта',NULL,NULL,'02',NULL,'all'),(15011,15,0,0,'text',NULL,'path','Путь',NULL,'',NULL,NULL,'03',NULL,'all'),(20001,20,0,0,'text',53,'owner_add_rw','Владелец: добавить чтение/запись','','! СПЕЦИАЛЬНЫЙ КЛЮЧ !',NULL,NULL,NULL,NULL,'all'),(20002,20,0,0,'text',53,'owner_add_ro','Владелец: добавить только чтение','','! СПЕЦИАЛЬНЫЙ КЛЮЧ !',NULL,NULL,NULL,NULL,'all'),(20003,20,0,0,'text',53,'owner_add_ro_limit','Владелец: добавить только чтение на период','','! СПЕЦИАЛЬНЫЙ КЛЮЧ !',NULL,NULL,NULL,NULL,'all'),(20004,20,0,0,'text',53,'owner_del','Владелец: запретить доступ','','! СПЕЦИАЛЬНЫЙ КЛЮЧ !',NULL,NULL,NULL,NULL,'all'),(20005,20,0,0,'checkbox',NULL,'owner_visible','Владелец: Отображать при запрете','','',NULL,NULL,NULL,NULL,'all'),(25204,25,1,0,'geometry',NULL,'point','Точка','','',NULL,NULL,NULL,NULL,'none'),(30301,30,1,0,'text',49,'icon','Иконка','','',NULL,NULL,NULL,NULL,'all'),(30302,30,1,0,'text',48,'parent_id','Группа','','',NULL,NULL,NULL,NULL,'all'),(30303,30,1,0,'text',NULL,'name','Название','','',NULL,NULL,NULL,1,'all'),(30304,30,1,0,'geometry',NULL,'location','Локация','','',NULL,NULL,NULL,NULL,'none'),(35001,35,0,1,'text',NULL,'fio','ФИО','Фамилия, имя, отчество','при изменении фам старую удаляем, а новую вписываем, но продумать чтоб поиск осуществлялся и по старой и по новой фамилии+сюдаже вносить фио на англ языке+продумать как вывести в результат уже имеющегося объекта но с измененной фамилией с сохр всех связей',NULL,NULL,'01',1,'only_value'),(35002,35,0,1,'date',NULL,'birth_day','Дата рождения','','',NULL,NULL,'04',2,'all'),(35004,35,0,0,'text',1,'citizenship','Гражданство/Подданство',NULL,'словарь гражданство',NULL,NULL,'05',NULL,'all'),(35005,35,0,0,'text',19,'nationality','Национальность',NULL,'словарь национальность',NULL,NULL,'05а',NULL,'all'),(35013,35,0,0,'text',4,'status_social','Социальное положение','','словарь соц полож',NULL,NULL,'13',NULL,'only_value'),(35014,35,0,0,'text',5,'status_marital','Семейное положение','','словарь семейн полож',NULL,NULL,'12',NULL,'only_value'),(35015,35,0,0,'text',3,'education','Образование',NULL,'словарь образование',NULL,NULL,'10',NULL,'all'),(35017,35,0,0,'text',1,'language_skills','Знание иностранных языков',NULL,'словарь гражданство',NULL,NULL,'11',NULL,'all'),(35020,35,0,0,'text',29,'conviction????','Судимость',NULL,'словарь статья УК (как связь е получится т.к. не по всем статьям есть дела у нас, но как связь с документом в котором указана статья можно продумать, чтоб сделать как связь)',NULL,NULL,'14',NULL,'all'),(35022,35,0,0,'text',NULL,'special_signs','Особые приметы',NULL,'не словарь',NULL,NULL,'15',NULL,'all'),(40104,40,0,0,'text',31,'type','Вид деятельности',NULL,'словарь Вид деятельности из мнс',NULL,NULL,'07',NULL,'all'),(40105,40,0,0,'text',6,'ownership','Форма собственности',NULL,'словарь Форма собственности (взять из мнс)',NULL,NULL,'05',NULL,'all'),(40106,40,0,0,'text',30,'activity','Род деятельности',NULL,'словарь Род деятельности из мнс',NULL,NULL,'06',NULL,'all'),(40107,40,0,0,'text',NULL,'descript','Оперативная характеристика организации',NULL,'скорее всего как связь либо какое-то описание, либо словарь относительно опг, либо в объект добавлять доп классификаторы для описания опг либо не нужный классификатор? надо разобраться в ходе теста!',NULL,NULL,'08',NULL,'all'),(45000,45,0,0,'text',53,'owner_add_rw','Владелец: добавить чтение/запись','','! СПЕЦИАЛЬНЫЙ КЛЮЧ !',NULL,NULL,NULL,NULL,'all'),(45001,45,0,0,'text',53,'owner_add_ro','Владелец: добавить только чтение','','! СПЕЦИАЛЬНЫЙ КЛЮЧ !',NULL,NULL,NULL,NULL,'all'),(45002,45,0,0,'text',53,'owner_add_ro_limit','Владелец: добавить только чтение на период','','! СПЕЦИАЛЬНЫЙ КЛЮЧ !',NULL,NULL,NULL,NULL,'all'),(45003,45,0,0,'text',53,'owner_del','Владелец: запретить доступ','','! СПЕЦИАЛЬНЫЙ КЛЮЧ !',NULL,NULL,NULL,NULL,'all'),(45004,45,0,0,'checkbox',NULL,'owner_visible','Владелец: Отображать при запрете','','',NULL,NULL,NULL,NULL,'all'),(45501,45,0,1,'text',27,'type','Вид дела','','Перечень всех видов СД(+УД+АД)+\r\nобязательное',NULL,NULL,'01',2,'only_value'),(45503,45,0,1,'text',29,NULL,'Статья УК/КоАП (окраска)','','наименование и номера (ч., прим.)статей УК+КоАП\r\nобязательное\r\nсвязь с документом будет по объекту связи линия+ППД; окраска в классификаторе документа не нужна, т.к. будет в деле (т.к. нет четкого НПА какие статьи входят в линию)',NULL,NULL,'03а',3,'all'),(45505,45,0,0,'text',NULL,NULL,'Описание (суть материалов)',NULL,'краткое описание описание или краткая суть материалов, о чем дело',NULL,NULL,'04а',NULL,'all'),(45520,45,0,0,'date',NULL,NULL,'Дата заведения (возбуждения)',NULL,NULL,45,NULL,'04',NULL,'all'),(45521,45,0,0,'date',NULL,NULL,'Дата продления',NULL,'применительно к СД',45,NULL,'07',NULL,'all'),(45522,45,0,0,'date',NULL,NULL,'Дата приостановления',NULL,'относительно УД, АД',45,NULL,'05',NULL,'all'),(45523,45,0,0,'date',NULL,NULL,'Дата возобновления',NULL,'относительно УД, АД',45,NULL,'06',NULL,'all'),(45524,45,0,0,'date',NULL,NULL,'Дата прекращения',NULL,'применительно ко всем делам',45,NULL,'08',NULL,'all'),(45525,45,0,0,'text',40,NULL,'Основание прекращения',NULL,'словарь Основание прекращения',45,NULL,'09',NULL,'all'),(50001,50,0,0,'text',35,'brand','Марка','','',NULL,NULL,'03',2,'only_value'),(50002,50,0,0,'text',36,'model','Модель','','',NULL,NULL,'04',2,'only_value'),(50004,50,0,0,'text',34,'type','Вид транспорта','','словарь Вид транспорта',NULL,NULL,'01',3,'only_value'),(50005,50,0,1,'text',NULL,'number','Рег.номер','','1.запретить внесение серии номера на русской раскладке\r\n2.продумать как делать автоматическую выгрузку из списочных данных в файле на латинской транскрипции\r\n3.продумать как сделать запрет на наличие пробелов (тире, иных знаков и т.) в госномере при вводе',NULL,NULL,'05',1,'all'),(50007,50,0,0,'number',NULL,'money','Сумма оценки',NULL,'либо как-то через связь решить? либо здесь, но с пометкой \"в бел.руб.\"',NULL,NULL,'14',NULL,'all'),(50008,50,0,0,'text',1,'country','Государство принадлежности','','',NULL,NULL,'06',NULL,'only_value'),(50010,50,0,0,'text',NULL,'vin','VIN',NULL,'',NULL,NULL,'07',NULL,'all'),(50011,50,0,0,'text',NULL,'manufacture','Год выпуска',NULL,'не словарь-проще вводить вручную',NULL,NULL,'08',NULL,'all'),(50012,50,0,0,'text',NULL,'route???','Номер поезда, рейса самолета, автобуса',NULL,'характерно для автобусов в авто ппр, а также из АСУ \"Экспресс\" (удаленный доступ, выгрузка, письменный ответ на запрос)',NULL,NULL,'11',NULL,'all'),(50013,50,0,0,'text',37,'route','Маршрут поезда, самолета, автобуса',NULL,'маршрут минск-киев означает из минска в киев и из киева в минск',NULL,NULL,'10',NULL,'all'),(50014,50,0,0,'text',NULL,'number_carriage','Номер вагона',NULL,'',NULL,NULL,'12',NULL,'all'),(50015,50,0,0,'text',38,'color','Цвет',NULL,'',NULL,NULL,'09',NULL,'all'),(50016,50,0,0,'text',NULL,'measures ????','Принятые меры',NULL,'словарь либо как-то через связь решить?',NULL,NULL,'13',NULL,'all'),(50018,1,1,0,'geometry',NULL,'border_guard_fail','незаконный переход границы','где нарушили границу','-',35,45,NULL,NULL,'all'),(50019,20,0,1,'text',22,NULL,'Вид документа','','обязательное для вывода и поиска\r\nпредусмотреть вид документа из имеющегося перечня тематических информаций',NULL,NULL,'01',2,'all'),(50020,20,0,0,'text',NULL,'name_doc','Название документа','Вноситься должны сведения в полном объеме как изложено в названии документа без повторного указания вида документа','не обязательное, т.к. название может быть внесено неправильно и поиск будет не точным',NULL,NULL,'02',NULL,'all'),(50021,20,0,1,'date',NULL,'registration_doc','Дата регистрации документа','','обязательное, т.к. каждый год нумерация начинается сначала',NULL,NULL,'03',2,'all'),(50022,20,0,1,'text',NULL,'number_doc','Номер документа','','обязательное, т.к. каждый год нумерация и дата регистрации начинаются сначала',NULL,NULL,'04',2,'all'),(50029,20,0,0,'text',NULL,NULL,'Линия (в т.ч. тематич. инф.)',NULL,'продумать возможно ли включить сюда перечень тематических информаций',NULL,NULL,'06',NULL,'all'),(50031,20,0,0,'text',NULL,NULL,'Оценка информации по методу 4х4',NULL,'для этого классификатора надо создать словарь (А1,А2...,В1,....)',NULL,NULL,'08',NULL,'all'),(50032,20,0,0,'text',NULL,NULL,'Доп. данные',NULL,'надобность этого классификатора крайне редкая-например когда стало известно, что документ уничтожен без приобщения в дело. может и не стоит вообще этот классификатор оставлять?',NULL,NULL,'07',NULL,'all'),(50049,35,0,0,'text',NULL,NULL,'Дополнительные данные',NULL,'возможна будет востребована к примеру сделать отметку о том что чел умер',NULL,NULL,'99',NULL,'all'),(50052,35,0,0,'text',NULL,NULL,'Личный номер',NULL,'может его в связь с ДУЛ?',NULL,NULL,'99',NULL,'all'),(50054,52,0,1,'phone_number',NULL,NULL,'Номер абонента','Указывается с международным кодом, префиксом, без знака \"+\"','поиск на предмет наличия такого объекта в банке должен осуществляться по последним 7-ми цифрам номера',NULL,NULL,'01',1,'all'),(50055,52,0,0,'text',1,NULL,'Государство принадлежности',NULL,'словарь Гражданство+продумать о создании нового объекта \"технические средства\" куда включить инженерку, бла, р/ст, переносные утройства, датчики и т.д.',NULL,NULL,'02',NULL,'all'),(50067,45,0,0,'text',NULL,NULL,'Наименование дела','','Условное наименование ДОУ и иных СД кроме УД и АД\r\nобязательно к заполнению только для СД',NULL,NULL,'02',NULL,'only_value'),(50068,45,0,1,'text',NULL,NULL,'Номер дела','','предусм механизм 1. выдачи всех связей независ от вр когда номер перешел от одного владельца к др 2. выдачи связей по позжей дате ее внесения',NULL,NULL,'03',1,'all'),(50072,45,0,0,'text',NULL,NULL,'Архивный номер',NULL,'архивный номер дела после его прекращения без указания его регистрационного номера',NULL,NULL,'10',NULL,'all'),(50073,40,0,1,'text',NULL,NULL,'Наименование организации полное','Указываются полное наименование без сокращений и условных наименований (опг, топс, подразделений гг в т.ч. сопредел, взаимодействующие организации и их структурные подразделения и т.д. и т.п.)','не словарь',NULL,NULL,'01',1,'only_value'),(50083,40,0,0,'text',NULL,NULL,'Наименование организации сокращенное','','Возможно нет необходимости в данном поле. сокращенные наименования можно указывать в наименовании полном, либо не указывать там, но обязать сокращенные наименования преобразовывать в полные',NULL,NULL,'02',2,'only_value'),(50084,40,0,0,'text',NULL,NULL,'Наименование организации на латинице','','',NULL,NULL,'03',NULL,'only_value'),(50085,40,0,0,'text',1,NULL,'Государство','Указывается государство на территории которого зарегистрировано (для иностранных ЮЛ)','словарь Гражданство',NULL,NULL,'04',NULL,'all'),(50087,35,0,0,'text',NULL,NULL,'Кличка/Прозвище',NULL,'не словарь',NULL,NULL,'09а',NULL,'all'),(50088,30,0,0,'text',1,NULL,'Государство','','предполагается по гос.+обл.+р-н+н.п. связь с точкой по этим же классификаторам.\r\nнадо подумать-????',NULL,NULL,'01',2,'all'),(50089,30,0,0,'text',NULL,NULL,'Область','','',NULL,NULL,'02',NULL,'all'),(50090,30,0,0,'text',NULL,NULL,'Район','','',NULL,NULL,'03',NULL,'all'),(50091,30,0,0,'text',NULL,NULL,'Населенный пункт','','предусмотреть визуализацию по полям н.п.+ул.+дом+кв.',NULL,NULL,'04',1,'all'),(50097,25,0,0,'text',1,NULL,'Государство','','категория адреса должна выступать связью м/у каким-либо другим объектом и геометрией+точкой= объект-связь \"категория адреса\"-точка-связь \"Геометрия/Точка\"+для обл и р-н городов тоже заполняется',NULL,NULL,'01',2,'all'),(50098,25,0,0,'text',NULL,NULL,'Область','','словарь Область+для обл и р-н городов тоже заполняется (предусмотреть автоматическое внесений обл и р-н городов в классификаторы обл и р-н)',NULL,NULL,'02',NULL,'all'),(50099,25,0,0,'text',NULL,NULL,'Район','','словарь Район+для обл и р-н городов тоже заполняется (предусмотреть автоматическое внесений обл и р-н городов в классификаторы обл и р-н)',NULL,NULL,'03',NULL,'all'),(50100,25,0,0,'text',NULL,NULL,'Населенный пункт','','словарь Населенный пункт+для обл и р-н городов тоже заполняется (предусмотреть автоматическое внесений обл и р-н городов в классификаторы обл и р-н)',NULL,NULL,'04',3,'all'),(50101,25,0,0,'text',NULL,NULL,'Улица',NULL,'',NULL,NULL,'05',NULL,'all'),(50102,25,0,0,'text',NULL,NULL,'Дом',NULL,'',NULL,NULL,'06',NULL,'all'),(50103,25,0,0,'text',NULL,NULL,'Корпус',NULL,'',NULL,NULL,'07',NULL,'all'),(50104,25,0,0,'text',NULL,NULL,'Квартира',NULL,'разобраться нужна ли отметка \"специфический параметр\"',NULL,NULL,'08',NULL,'all'),(50105,25,0,0,'text',NULL,NULL,'П/ЗН','','переводить в словарь может и нет смысла?',NULL,NULL,'09',2,'all'),(50106,25,0,0,'text',46,NULL,'Точка на карте',NULL,'словарь Точка события на карте для обозначения места происшествия, ППД, нарушения ГГ  на местности, схроны, места установки катапульт, обнаружения следов и т.д.',NULL,NULL,'10',NULL,'all'),(50107,20,0,0,'text',29,NULL,'Статья УК/КоАП (окраска)',NULL,'словарь Статья УК',NULL,NULL,'06а',NULL,'all'),(50109,50,0,0,'text',NULL,NULL,'Рег.номер РФ',NULL,'предусм механизм 1. выдачи всех связей независ от вр когда номер перешел от одного владельца к др 2. выдачи связей по позжей дате ее внесения',NULL,NULL,'05а',NULL,'all'),(50110,15,0,1,'text',NULL,NULL,'Наименование файла','','продумать при внесении файла чтоб его название автоматически вносилось в этот классификатор',NULL,NULL,'01',1,'all'),(50111,35,0,0,'text',2,NULL,'Пол','','словарь Пол',NULL,NULL,'05б',NULL,'only_value'),(50112,40,0,0,'text',7,NULL,'ТОПС (ПХО РБ и сопредела)',NULL,'словарь ТОПС',NULL,NULL,'09',NULL,'all'),(50113,40,0,0,'text',15,NULL,'погк (опс) (в т.ч. сопредел)',NULL,'словарь наименование погк',NULL,NULL,'10',NULL,'all'),(50114,40,0,0,'text',14,NULL,'погз (погп) (в т.ч. сопредел)',NULL,'словарь наименование погз',NULL,NULL,'11',NULL,'all'),(50115,40,0,0,'text',41,NULL,'опк (в т.ч. сопредел)',NULL,'словарь опк',NULL,NULL,'12',NULL,'all'),(50117,40,0,0,'text',42,NULL,'Вид пункта пропуска',NULL,'словарь Вид пункта пропуска',NULL,NULL,'13',NULL,'all'),(50118,40,0,0,'text',41,NULL,'Пункт пропуска',NULL,'словарь опк',NULL,NULL,'14',NULL,'all'),(50120,1,0,0,'text',29,NULL,'документ/Окраска/дело',NULL,'словарь Статья УК/КоАП+предусмотреть возможность вывода информации при изменении статьи УК',20,45,'02',NULL,'all'),(50121,1,0,0,'text',NULL,NULL,'документ/Файл/файл',NULL,'без словаря',15,20,'03',NULL,'all'),(50122,1,0,0,'text',43,NULL,'документ/Линия/дело',NULL,'словарь Линия ППД+предусмотреть возможность вывода информации при изменении линии',20,45,'01',NULL,'all'),(50124,1,0,0,'text',17,NULL,'документ/Сотрудник ОПС/физлицо',NULL,'словарь Воинское звание+связь сотрудника ОПС с документом который он разработал',20,35,'04',NULL,'all'),(50125,1,0,0,'text',45,NULL,'дело/Категория лица в Деле/физлицо',NULL,'словарь Категория лица в ППД',35,45,'03',NULL,'all'),(50126,1,0,0,'text',NULL,NULL,'Место рождения','','т.к. ниже н.п. место рождения не опускается',30,35,'05',NULL,'all'),(50127,1,0,0,'text',NULL,NULL,'Место жительства','','предусмотреть механизм выдачи всех сведений при изменении места жительства',25,35,'06',NULL,'all'),(50128,1,0,0,'text',NULL,NULL,'Владелец абонентского номера','','предусм механизм 1. выдачи всех связей независ от вр когда номер перешел от одного владельца к др 2. выдачи связей по позжей дате ее внесения',35,52,'07',NULL,'all'),(50129,1,0,0,'text',43,NULL,'Использует абонентский номер в ППД','','словарь Линия ППД',35,52,'08',NULL,'all'),(50130,1,0,0,'text',NULL,NULL,'физлицо/Владелец т/с/транспорт',NULL,'',35,50,'09',NULL,'all'),(50131,1,0,0,'text',43,NULL,'физлицо/Использует т/с в ППД/транспорт',NULL,'словарь Линия ППД',35,50,'10',NULL,'all'),(50132,1,0,0,'text',NULL,NULL,'Пользуется абонентским номером','','',35,52,'08а',NULL,'all'),(50133,1,0,0,'text',NULL,NULL,'физлицо/Пользуется т/с/транспорт',NULL,'',35,50,'11',NULL,'all'),(50134,1,0,0,'text',47,NULL,'физлицо/Место работы/организация',NULL,'словарь Должность',35,40,'12',NULL,'all'),(50135,1,0,0,'text',NULL,NULL,'организация/Участок ответственности/геометрия',NULL,'применяется для ПХО РБ и сопредела',30,40,'13',NULL,'all'),(50136,1,0,0,'text',NULL,'case_information','Электронная информация о деле','Электронная информация о деле','',15,45,NULL,NULL,'all'),(50137,1,0,0,'text',56,NULL,'физлицо/Родственная связь/физлицо','','словарь Родственная связь',35,35,NULL,NULL,'all'),(50141,1,0,0,'text',NULL,'border_guard_fail_point','нарушение государственной границы','','Тестовая связь',25,45,NULL,NULL,'all'),(50142,35,0,0,'file_photo',NULL,'photo_person_p','Фото','Фото физ лица','',NULL,NULL,NULL,NULL,'none'),(50143,35,0,0,'file_any',NULL,'files_person_p','Дополнительные файлы','Файлы характеризующие физ лицо','',NULL,NULL,NULL,NULL,'all'),(50144,1,0,0,'text',50,'role_in_unlegal_working','Причастен к незаконной деятельности','Данное физлицо причатсно к незаконной деятельности','Для Сморгони',20,35,NULL,NULL,'all'),(50145,1,0,0,'text',NULL,'temp_live_place','Место временного проживания','Место где данное физ лицо временно проживает','Для Сморгони',25,35,NULL,NULL,'all'),(50146,1,0,0,'text',NULL,'region_arest','Район задержания','Район задержания','для Сморгони',30,35,NULL,NULL,'all'),(50147,1,0,0,'text',NULL,'place_of_live','Место жительства','Место жительства','для Сморгони',30,35,NULL,NULL,'all'),(50148,1,0,0,'text',NULL,'place_of_temparaly_live','Место временного проживания','Место временного проживания','для Сморгони',30,35,NULL,NULL,'all'),(50149,1,0,0,'text',NULL,'link_to_p/z','Привязка к п/зн','Привязка к п/зн','для сморгони',25,30,NULL,NULL,'all'),(50150,1,0,0,'text',NULL,'place_of_arest','Место отбытия наказания','Место отбытия наказания','для Сморгони',30,35,NULL,NULL,'all'),(50151,1,0,0,'text',NULL,'place_holder','Место расположения','Место расположения','для Сморгони',30,40,NULL,NULL,'all'),(50152,1,0,0,'text',NULL,'arest_transport','Задержанный транспорт','Задержанный транспорт','для сморгони',20,50,NULL,NULL,'all'),(50153,1,0,0,'text',NULL,'leave_transport','скрывшийся транспорт','скрывшийся транспорт','для сморгони',20,50,NULL,NULL,'all'),(50154,1,0,0,'text',NULL,'car_route','Маршрут движения ТС','Маршрут движения ТС','для сморгони',30,50,NULL,NULL,'all'),(50155,1,0,0,'text',NULL,'route district','Район по маршруту движения ТС','Район по маршруту движения ТС','для сморгони',30,30,NULL,NULL,'all'),(50156,1,0,0,'text',NULL,'arest_car_place','Район задержания ТС','Район задержания ТС','для сморгони',30,50,NULL,NULL,'all'),(50157,1,0,0,'text',NULL,'link_to_point','Привязка к месту','Привязка к месту','для сморгони',25,30,NULL,NULL,'all'),(50158,1,0,0,'text',NULL,'passagire','Пассажир ТС','Пассажир ТС','для сморгони',35,50,NULL,NULL,'all'),(50159,1,0,0,'text',NULL,'friend','Дружеская связь','Дружеская связь','для сморгони',35,35,NULL,NULL,'all'),(50160,1,0,0,'text',NULL,'phone_link','Соединение ТЛФ','Соединение ТЛФ','для сморгони',52,52,NULL,NULL,'all'),(50161,1,0,0,'text',NULL,'share_home','Представившее жилье','Представившее жилье','для сморгони',25,35,NULL,NULL,'all'),(50162,1,0,0,'text',NULL,'place_of_registered','Место регистрации','Место регистрации','для сморгони',25,35,NULL,NULL,'all'),(50163,25,0,0,'text',NULL,'point_name','Название','Условное название точки','для сморгони',NULL,NULL,NULL,1,'all'),(50164,1,0,0,'text',NULL,'force_of_border_guard','П/Н ПОГЗ','наряд от заставы','для сморгони',40,40,NULL,NULL,'all'),(50165,1,0,0,'text',NULL,'place_of_work_border_guar','Место несения службы','Место несения службы','для сморгони',25,40,NULL,NULL,'all'),(50166,1,0,0,'text',NULL,'foreign_person','Сотрудник ПХО/сопредел','Сотрудник ПХО/сопредел','для сморгони',20,35,NULL,NULL,'all'),(50167,1,0,0,'text',NULL,'in_sostav','В составе','В составе','для сморгони',40,40,NULL,NULL,'all'),(50168,1,0,0,'text',NULL,'information_diller','Информатор','Лицо информирующее о незаконной деятеьности','для сморгони',35,40,NULL,NULL,'all'),(50169,1,0,0,'text',NULL,'point_holding','Место расположения','Место расположения организации','для сморгони',25,40,NULL,NULL,'all'),(50170,1,0,0,'text',54,'person_l_work_place','Место проведения работ','Место проведения работ организацией','для сморгони',30,40,NULL,NULL,'all'),(50171,1,0,0,'text',NULL,'zone_of_doing','Участок ответственности','Участок ответственности ПОГЗ','для презентации',25,40,NULL,NULL,'all'),(50172,1,0,0,'text',NULL,'usefull_transport','Штатное ТС','Штатное ТС организации','для презентации',40,50,NULL,NULL,'all'),(50173,1,0,0,'text',NULL,'place_of_looking','Место обнаружения','Место обнаружения ТС','для презентации',25,50,NULL,NULL,'all'),(50174,1,0,0,'text',NULL,'zone_of_looking','Место обнаружения','место обнаружения ТС','для презентации',30,50,NULL,NULL,'all'),(50175,1,0,0,'text',NULL,'group_route','Маршрут движения группы','Маршрут движения группы','для презентации',30,40,NULL,NULL,'all'),(50176,1,0,0,'text',NULL,'arest_person_p','Задержание нарушителя','Задержание нарушителя','для презентации',35,40,NULL,NULL,'all'),(50177,1,0,0,'text',NULL,'border_line_POGZ','Линия ГГ ПОГЗ','Участок Государственной Границы охраняемый заставой','для презентации',30,40,NULL,NULL,'all'),(50178,1,0,0,'text',NULL,'border_row_POGZ','Пограничная полоса ПОГЗ','Пограничная полоса на участке ПОГЗ','для презентации',30,40,NULL,NULL,'all'),(50179,1,0,0,'text',NULL,'border_zone_POGZ','Пограничная зона ПОГЗ','Граница пограничной зоны на участке данной заставы','для презентации',30,40,NULL,NULL,'all'),(50180,1,0,0,'text',54,'person_service','Служба','Состояние службы (начало, конец)','для презентации',35,40,NULL,NULL,'all'),(50181,1,0,0,'text',55,'POGZ_person_rank','Должность сотрудника ПОГЗ','Должность сотрудника ОПС на ПОГЗ','для презентации',35,40,NULL,NULL,'all'),(50182,1,0,0,'text',54,'marriage','Брак','Данные лица находятся в браке','для презентации',35,35,NULL,NULL,'all'),(50183,15,0,0,'file_any',NULL,'file_up\\download','Файл','файл для хранения на сервере','',NULL,NULL,NULL,NULL,'all'),(50184,1,0,0,'text',54,'serveice_sogg','Служба СОГГ','Служба СОГГ','для презентации',35,40,NULL,NULL,'all'),(50186,1,0,0,'text',NULL,'town_on_pogz_sector','НП в зоне ответственности ПОГЗ','НП в зоне ответственности ПОГЗ','для презентации',30,40,NULL,NULL,'all'),(50187,10,0,0,'text',57,'type_of_contraband','Тип контробанды','Тип контробанды','',NULL,NULL,NULL,NULL,'all'),(50188,10,0,0,'number',NULL,'numf_sigaret_blocks','Сигареты/Количество пачек','Количество пачек сигарет','',NULL,NULL,NULL,NULL,'all'),(50189,10,0,0,'number',NULL,'drags_mass','Наркотики/Масса в граммах','Масса наркотиков в граммах','',NULL,NULL,NULL,NULL,'all'),(50190,10,0,0,'number',NULL,'gun_caliber','Оружие/Калибр(мм)','Калибр оружия в миллимерах','',NULL,NULL,NULL,NULL,'all'),(50191,10,0,0,'text',NULL,'sigarets_type','Сигареты/Марка','Марка сигарет','',NULL,NULL,NULL,NULL,'all'),(50192,10,0,0,'text',NULL,'gun_model','Оружие/Модель','Модель оружия','',NULL,NULL,NULL,NULL,'all'),(50193,10,0,0,'text',NULL,'weapon_type','Оружие/Тип','Тип оружия','',NULL,NULL,NULL,NULL,'all'),(50195,10,0,0,'text',58,'drags_type','Наркотики/Тип','Тип наркотиков','',NULL,NULL,NULL,NULL,'all'),(50196,1,0,0,'text',NULL,'start_organization','Исходная организация','Организация разработавшая документ','',20,40,NULL,NULL,'all'),(50197,1,0,0,'text',NULL,'sector_of_cought','Район задержания МВД','Район задержания МВД','',30,35,NULL,NULL,'all'),(50198,1,0,0,'text',NULL,'person_owner','Имел при задержании','Имел при задержании','',10,35,NULL,NULL,'all'),(50199,30,0,0,'text',59,'list_of_types_geometry','Условное обозначение геометрии','','',NULL,NULL,NULL,NULL,'only_value'),(50200,25,0,0,'text',60,'list_of_types_point','Условное обозначение точки','','',NULL,NULL,NULL,NULL,'only_value'),(50204,30,0,0,'file_photo',NULL,'photo_geometry','Фото','Фото геометрии','',NULL,NULL,NULL,NULL,'none'),(50205,25,0,0,'file_photo',NULL,'point_photo','Фото','','',NULL,NULL,NULL,NULL,'none'),(50206,30,0,0,'file_photo',NULL,'photo_geometry_test','Фото тест','','',NULL,NULL,NULL,NULL,'none'),(50207,50,0,0,'file_photo',NULL,'transport_photo','Фото','Фотография транспорта','',NULL,NULL,NULL,NULL,'none'),(50208,1,0,0,'text',NULL,NULL,'Маршрут движения лица','Маршрут движения лица','',30,35,NULL,NULL,'all'),(50209,1,0,0,'text',NULL,NULL,'Место задержания ОПС','Место задержания ОПС','',25,35,NULL,NULL,'all'),(50210,1,0,0,'text',61,NULL,'Место совершения правонарушения МВД','Место совершения правонарушения','',25,35,NULL,NULL,'all'),(50211,1,0,0,'text',NULL,NULL,'Место задержания МВД','Место задержания','',25,35,NULL,NULL,'all'),(50212,30,0,0,'number',NULL,NULL,'Население','','',NULL,NULL,NULL,NULL,'all'),(50213,1,0,0,'text',61,NULL,'Место совершения правонарушения МВД Литва','Место совершения правонарушения МВД Латвии','',25,35,NULL,NULL,'all'),(50214,1,0,0,'text',NULL,NULL,'Место задержания МВД Литва','Место задержания МВД Латвии','',25,35,NULL,NULL,'all');
/*!40000 ALTER TABLE `sys_key` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sys_list_dop`
--

DROP TABLE IF EXISTS `sys_list_dop`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sys_list_dop` (
  `id` int NOT NULL AUTO_INCREMENT,
  `key_id` mediumint unsigned NOT NULL,
  `val` varchar(255) NOT NULL,
  `dat_from` date DEFAULT NULL,
  `dat_to` date DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ind_id` (`key_id`),
  CONSTRAINT `ind_id_id` FOREIGN KEY (`key_id`) REFERENCES `sys_list_top` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=625 DEFAULT CHARSET=utf8mb3 AVG_ROW_LENGTH=117 ROW_FORMAT=DYNAMIC COMMENT='содержание списков';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_list_dop`
--

LOCK TABLES `sys_list_dop` WRITE;
/*!40000 ALTER TABLE `sys_list_dop` DISABLE KEYS */;
INSERT INTO `sys_list_dop` VALUES (1,1,'Австралия',NULL,NULL),(2,1,'Австрия',NULL,NULL),(3,1,'Азербайджан',NULL,NULL),(4,1,'Аландские острова',NULL,NULL),(5,1,'Албания',NULL,NULL),(6,1,'Алжир',NULL,NULL),(7,1,'Американское Самоа',NULL,NULL),(8,1,'Ангилья',NULL,NULL),(9,1,'Ангола',NULL,NULL),(10,1,'Андорра',NULL,NULL),(11,1,'Антигуа и Барбуда',NULL,NULL),(12,1,'Аргентина',NULL,NULL),(13,1,'Армения',NULL,NULL),(14,1,'Аруба',NULL,NULL),(15,1,'Афганистан',NULL,NULL),(16,1,'Багамы',NULL,NULL),(17,1,'Бангладеш',NULL,NULL),(18,1,'Барбадос',NULL,NULL),(19,1,'Бахрейн',NULL,NULL),(20,1,'Беларусь',NULL,NULL),(21,1,'Белиз',NULL,NULL),(22,1,'Бельгия',NULL,NULL),(23,1,'Бенин',NULL,NULL),(24,1,'Бермуды',NULL,NULL),(25,1,'Болгария',NULL,NULL),(26,1,'Боливия, Многонациональное Государство ',NULL,NULL),(27,1,'Бонэйр, Синт-Эстатиус и Саба',NULL,NULL),(28,1,'Босния и Герцеговина',NULL,NULL),(29,1,'Ботсвана',NULL,NULL),(30,1,'Бразилия',NULL,NULL),(31,1,'Бруней-Даруссалам',NULL,NULL),(32,1,'Буркина-Фасо',NULL,NULL),(33,1,'Бурунди',NULL,NULL),(34,1,'Бутан',NULL,NULL),(35,1,'Вануату',NULL,NULL),(36,1,'Венгрия',NULL,NULL),(37,1,'Венесуэла, Боливарианская Республика ',NULL,NULL),(38,1,'Виргинские Острова, Британские',NULL,NULL),(39,1,'Виргинские Острова, США',NULL,NULL),(40,1,'Вьетнам',NULL,NULL),(41,1,'Габон',NULL,NULL),(42,1,'Гаити',NULL,NULL),(43,1,'Гайана',NULL,NULL),(44,1,'Гамбия',NULL,NULL),(45,1,'Гана',NULL,NULL),(46,1,'Гваделупа',NULL,NULL),(47,1,'Гватемала',NULL,NULL),(48,1,'Гвинея',NULL,NULL),(49,1,'Гвинея-Бисау',NULL,NULL),(50,1,'Германия',NULL,NULL),(51,1,'Гернси',NULL,NULL),(52,1,'Гибралтар',NULL,NULL),(53,1,'Гондурас',NULL,NULL),(54,1,'Гонконг',NULL,NULL),(55,1,'Гренада',NULL,NULL),(56,1,'Гренландия',NULL,NULL),(57,1,'Греция',NULL,NULL),(58,1,'Грузия',NULL,NULL),(59,1,'Гуам',NULL,NULL),(60,1,'Дания',NULL,NULL),(61,1,'Джерси',NULL,NULL),(62,1,'Джибути',NULL,NULL),(63,1,'Доминика',NULL,NULL),(64,1,'Доминиканская Республика',NULL,NULL),(65,1,'Египет',NULL,NULL),(66,1,'Замбия',NULL,NULL),(67,1,'Западная Сахара',NULL,NULL),(68,1,'Зимбабве',NULL,NULL),(69,1,'Израиль',NULL,NULL),(70,1,'Индия',NULL,NULL),(71,1,'Индонезия',NULL,NULL),(72,1,'Иордания',NULL,NULL),(73,1,'Ирак',NULL,NULL),(74,1,'Иран, Исламская Республика ',NULL,NULL),(75,1,'Ирландия',NULL,NULL),(76,1,'Исландия',NULL,NULL),(77,1,'Испания',NULL,NULL),(78,1,'Италия',NULL,NULL),(79,1,'Йемен',NULL,NULL),(80,1,'Кабо-Верде',NULL,NULL),(81,1,'Казахстан',NULL,NULL),(82,1,'Камбоджа',NULL,NULL),(83,1,'Камерун',NULL,NULL),(84,1,'Канада',NULL,NULL),(85,1,'Катар',NULL,NULL),(86,1,'Кения',NULL,NULL),(87,1,'Кипр',NULL,NULL),(88,1,'Кирибати',NULL,NULL),(89,1,'Китай',NULL,NULL),(90,1,'Кокосовые (Килинг) острова',NULL,NULL),(91,1,'Колумбия',NULL,NULL),(92,1,'Коморы',NULL,NULL),(93,1,'Конго',NULL,NULL),(94,1,'Конго, Демократическая Республика',NULL,NULL),(95,1,'Корея, Народно-Демократическая Республика',NULL,NULL),(96,1,'Корея, Республика',NULL,NULL),(97,1,'Коста-Рика',NULL,NULL),(98,1,'Кот-д’Ивуар',NULL,NULL),(99,1,'Куба',NULL,NULL),(100,1,'Кувейт',NULL,NULL),(101,1,'Кыргызстан',NULL,NULL),(102,1,'Кюрасао',NULL,NULL),(103,1,'Лаосская Народно-Демократическая Республика',NULL,NULL),(104,1,'Латвия',NULL,NULL),(105,1,'Лесото',NULL,NULL),(106,1,'Либерия',NULL,NULL),(107,1,'Ливан',NULL,NULL),(108,1,'Ливия',NULL,NULL),(109,1,'Литва',NULL,NULL),(110,1,'Лихтенштейн',NULL,NULL),(111,1,'Люксембург',NULL,NULL),(112,1,'Маврикий',NULL,NULL),(113,1,'Мавритания',NULL,NULL),(114,1,'Мадагаскар',NULL,NULL),(115,1,'Майотта',NULL,NULL),(116,1,'Макао',NULL,NULL),(117,1,'Малави',NULL,NULL),(118,1,'Малайзия',NULL,NULL),(119,1,'Мали',NULL,NULL),(120,1,'Мальдивы',NULL,NULL),(121,1,'Мальта',NULL,NULL),(122,1,'Марокко',NULL,NULL),(123,1,'Мартиника',NULL,NULL),(124,1,'Маршалловы Острова',NULL,NULL),(125,1,'Мексика',NULL,NULL),(126,1,'Микронезия, Федеративные Штаты',NULL,NULL),(127,1,'Мозамбик',NULL,NULL),(128,1,'Молдова',NULL,NULL),(129,1,'Монако',NULL,NULL),(130,1,'Монголия',NULL,NULL),(131,1,'Монтсеррат',NULL,NULL),(132,1,'Мьянма',NULL,NULL),(133,1,'Намибия',NULL,NULL),(134,1,'Науру',NULL,NULL),(135,1,'Непал',NULL,NULL),(136,1,'Нигер',NULL,NULL),(137,1,'Нигерия',NULL,NULL),(138,1,'Нидерланды',NULL,NULL),(139,1,'Никарагуа',NULL,NULL),(140,1,'Ниуэ',NULL,NULL),(141,1,'Новая Зеландия',NULL,NULL),(142,1,'Новая Каледония',NULL,NULL),(143,1,'Норвегия',NULL,NULL),(144,1,'Объединенные Арабские Эмираты',NULL,NULL),(145,1,'Оман',NULL,NULL),(146,1,'Остров Мэн',NULL,NULL),(147,1,'Остров Норфолк',NULL,NULL),(148,1,'Остров Рождества',NULL,NULL),(149,1,'Острова Кайман',NULL,NULL),(150,1,'Острова Кука',NULL,NULL),(151,1,'Острова Теркс И Кайкос',NULL,NULL),(152,1,'Пакистан',NULL,NULL),(153,1,'Палау',NULL,NULL),(154,1,'Палестина, государство',NULL,NULL),(155,1,'Панама',NULL,NULL),(156,1,'Папский престол',NULL,NULL),(157,1,'Папуа – Новая Гвинея',NULL,NULL),(158,1,'Парагвай',NULL,NULL),(159,1,'Перу',NULL,NULL),(160,1,'Питкэрн',NULL,NULL),(161,1,'Польша',NULL,NULL),(162,1,'Португалия',NULL,NULL),(163,1,'Пуэрто-Рико',NULL,NULL),(164,1,'Республика Беларусь',NULL,NULL),(165,1,'Реюньон',NULL,NULL),(166,1,'Российская Федерация',NULL,NULL),(167,1,'Руанда',NULL,NULL),(168,1,'Румыния',NULL,NULL),(169,1,'Самоа',NULL,NULL),(170,1,'Сан-Марино',NULL,NULL),(171,1,'Сан-Томе и Принсипи',NULL,NULL),(172,1,'Саудовская Аравия',NULL,NULL),(173,1,'Северная Македония',NULL,NULL),(174,1,'Северные Марианские Острова',NULL,NULL),(175,1,'Сейшелы',NULL,NULL),(176,1,'Сен Бартелеми',NULL,NULL),(177,1,'Сен Мартин (французская часть)',NULL,NULL),(178,1,'Сен-Мартен (Нидерландская часть)',NULL,NULL),(179,1,'Сен-Пьер и Микелон',NULL,NULL),(180,1,'Сенегал',NULL,NULL),(181,1,'Сент-Винсент и Гренадины',NULL,NULL),(182,1,'Сент-Китс и Невис',NULL,NULL),(183,1,'Сент-Люсия',NULL,NULL),(184,1,'Сербия',NULL,NULL),(185,1,'Сингапур',NULL,NULL),(186,1,'Сирийская Арабская Республика',NULL,NULL),(187,1,'Словакия',NULL,NULL),(188,1,'Словения',NULL,NULL),(189,1,'Соединенное Королевство Великобритании и Северной Ирландии',NULL,NULL),(190,1,'Соединенные Штаты Америки',NULL,NULL),(191,1,'Соломоновы острова',NULL,NULL),(192,1,'Сомали',NULL,NULL),(193,1,'Судан',NULL,NULL),(194,1,'Суринам',NULL,NULL),(195,1,'Сьерра-Леоне',NULL,NULL),(196,1,'Таджикистан',NULL,NULL),(197,1,'Таиланд',NULL,NULL),(198,1,'Тайвань (Китай)',NULL,NULL),(199,1,'Танзания, Объединенная Республика ',NULL,NULL),(200,1,'Тимор-Лесте',NULL,NULL),(201,1,'Того',NULL,NULL),(202,1,'Токелау',NULL,NULL),(203,1,'Тонга',NULL,NULL),(204,1,'Тринидад и Тобаго',NULL,NULL),(205,1,'Тувалу',NULL,NULL),(206,1,'Тунис',NULL,NULL),(207,1,'Туркменистан',NULL,NULL),(208,1,'Турция',NULL,NULL),(209,1,'Уганда',NULL,NULL),(210,1,'Узбекистан',NULL,NULL),(211,1,'Украина',NULL,NULL),(212,1,'Уоллис и Футуна',NULL,NULL),(213,1,'Уругвай',NULL,NULL),(214,1,'Фарерские острова',NULL,NULL),(215,1,'Фиджи',NULL,NULL),(216,1,'Филиппины',NULL,NULL),(217,1,'Финляндия',NULL,NULL),(218,1,'Фолклендские острова (Мальвинские)',NULL,NULL),(219,1,'Франция',NULL,NULL),(220,1,'Французская Гвиана',NULL,NULL),(221,1,'Французская Полинезия',NULL,NULL),(222,1,'Хорватия',NULL,NULL),(223,1,'Центрально-африканская Республика',NULL,NULL),(224,1,'Чад',NULL,NULL),(225,1,'Черногория',NULL,NULL),(226,1,'Чехия',NULL,NULL),(227,1,'Чили',NULL,NULL),(228,1,'Швейцария',NULL,NULL),(229,1,'Швеция',NULL,NULL),(230,1,'Шпицберген и Ян-Майен',NULL,NULL),(231,1,'Шри-Ланка',NULL,NULL),(232,1,'Эквадор',NULL,NULL),(233,1,'Экваториальная Гвинея',NULL,NULL),(234,1,'Эль-Сальвадор',NULL,NULL),(235,1,'Эритрея',NULL,NULL),(236,1,'Эсватини',NULL,NULL),(237,1,'Эстония',NULL,NULL),(238,1,'Эфиопия',NULL,NULL),(239,1,'Южно-Африканская Республика',NULL,NULL),(240,1,'Южный Судан',NULL,NULL),(241,1,'Ямайка',NULL,NULL),(242,1,'Япония',NULL,NULL),(243,2,'Женский',NULL,NULL),(244,2,'Мужской',NULL,NULL),(245,3,'Высшее',NULL,NULL),(246,3,'Высшее военное',NULL,NULL),(247,3,'Начальная школа',NULL,NULL),(248,3,'Незаконченное высшее',NULL,NULL),(249,3,'Профессионально-техническое',NULL,NULL),(250,3,'Среднее базовое',NULL,NULL),(251,3,'Среднее полное',NULL,NULL),(252,3,'Среднее специальное',NULL,NULL),(253,4,'Безработный',NULL,NULL),(254,4,'Военнослужащий',NULL,NULL),(255,4,'Домохозяйка',NULL,NULL),(256,4,'Колхозник',NULL,NULL),(257,4,'Несовершеннолетний',NULL,NULL),(258,4,'Отбывает наказание в МЛС(О)',NULL,NULL),(259,4,'Отпуск по уходу за ребенком',NULL,NULL),(260,4,'Пенсионер',NULL,NULL),(261,4,'Предприниматель',NULL,NULL),(262,4,'Работник по контракту',NULL,NULL),(263,4,'Работники культуры, науки, медицины, образования',NULL,NULL),(264,4,'Рабочий',NULL,NULL),(265,4,'Служащий',NULL,NULL),(266,4,'Состоит на учете в службе занятости, как безработный',NULL,NULL),(267,4,'Сотрудник Министерства по налогам и сборам',NULL,NULL),(268,4,'Сотрудник органов внутренних дел',NULL,NULL),(269,4,'Сотрудник органов пограничной службы',NULL,NULL),(270,4,'Сотрудник подразделений МЧС',NULL,NULL),(271,4,'Сотрудник таможенных органов',NULL,NULL),(272,4,'Студент высшего УО',NULL,NULL),(273,4,'Студент средне специального УО',NULL,NULL),(274,4,'Учащийся',NULL,NULL),(275,4,'Учащийся профессионально-технического УО',NULL,NULL),(276,4,'Учредитель (собственник) юридического лица',NULL,NULL),(277,5,'Вдовец (вдова)',NULL,NULL),(278,5,'Женат (замужем)',NULL,NULL),(279,5,'Разведен (разведена)',NULL,NULL),(280,5,'Холост (незамужем)',NULL,NULL),(281,6,'Государственная',NULL,NULL),(282,6,'Частная',NULL,NULL),(283,7,'Полоцкий пого',NULL,NULL),(284,7,'Сморгоньская погг',NULL,NULL),(285,7,'Гродненкая погг',NULL,NULL),(286,7,'Лидский пого',NULL,NULL),(287,7,'Гомельская погг',NULL,NULL),(288,7,'Пинский пого',NULL,NULL),(289,7,'Мозырьский пого',NULL,NULL),(290,7,'Брестская погг',NULL,NULL),(291,7,'опогк \"Минск\"',NULL,NULL),(292,8,'Да',NULL,NULL),(293,8,'Нет',NULL,NULL),(296,10,'Авиа',NULL,NULL),(297,10,'Белорусско-латвийский',NULL,NULL),(298,10,'Белорусско-литовский',NULL,NULL),(299,10,'Белорусско-польский',NULL,NULL),(300,10,'Белорусско-российский',NULL,NULL),(301,10,'Белорусско-украинский',NULL,NULL),(302,10,'Иное',NULL,NULL),(303,11,'Линия границы',NULL,NULL),(304,11,'Пограничная зона',NULL,NULL),(305,11,'Пограничная полоса',NULL,NULL),(306,11,'Пункт пропуска',NULL,NULL),(307,11,'Пункт пропуска сопредельного государства',NULL,NULL),(308,11,'Территория республики',NULL,NULL),(309,11,'Территория сопредельного государства',NULL,NULL),(310,12,'В Республику Беларусь',NULL,NULL),(311,12,'Из Республики Беларусь',NULL,NULL),(312,12,'Тыловой район',NULL,NULL),(313,13,'Погз № 1',NULL,NULL),(314,13,'Погз № 10',NULL,NULL),(315,13,'Погз № 11',NULL,NULL),(316,13,'Погз № 12',NULL,NULL),(317,13,'Погз № 13',NULL,NULL),(318,13,'Погз № 14',NULL,NULL),(319,13,'Погз № 15',NULL,NULL),(320,13,'Погз № 16',NULL,NULL),(321,13,'Погз № 17',NULL,NULL),(322,13,'Погз № 18',NULL,NULL),(323,13,'Погз № 19',NULL,NULL),(324,13,'Погз № 2',NULL,NULL),(325,13,'Погз № 3',NULL,NULL),(326,13,'Погз № 4',NULL,NULL),(327,13,'Погз № 5',NULL,NULL),(328,13,'Погз № 6',NULL,NULL),(329,13,'Погз № 7',NULL,NULL),(330,13,'Погз № 8',NULL,NULL),(331,13,'Погз № 9',NULL,NULL),(332,14,'Погп № 1',NULL,NULL),(333,14,'Погп № 2',NULL,NULL),(334,14,'Погп № 3',NULL,NULL),(335,14,'Погп № 4',NULL,NULL),(336,14,'Погп № 5',NULL,NULL),(337,14,'Погп № 6',NULL,NULL),(338,15,'Гудогай погк (опс)',NULL,NULL),(339,15,'Лоев погк (обо)',NULL,NULL),(340,15,'Малорита погк (опс)',NULL,NULL),(341,15,'Опса погк (опс)',NULL,NULL),(342,15,'Поречье погк (опс)',NULL,NULL),(343,15,'Поставы погк (опс)',NULL,NULL),(344,15,'Речица погк (опс)',NULL,NULL),(345,16,'Задержание по ОД',NULL,NULL),(346,16,'Задержание по результатам работы с местным населением',NULL,NULL),(347,17,'ефрейтор',NULL,NULL),(348,17,'капитан',NULL,NULL),(349,17,'лейтенант',NULL,NULL),(350,17,'майор',NULL,NULL),(351,17,'младший лейтенант',NULL,NULL),(352,17,'младший сержант',NULL,NULL),(353,17,'подполковник',NULL,NULL),(354,17,'полковник',NULL,NULL),(355,17,'прапорщик',NULL,NULL),(356,17,'рядовой',NULL,NULL),(357,17,'сержант',NULL,NULL),(358,17,'старший лейтенант',NULL,NULL),(359,17,'старший прапорщик',NULL,NULL),(360,17,'старший сержант',NULL,NULL),(361,17,'старшина',NULL,NULL),(362,18,'английский',NULL,NULL),(363,18,'грузинский',NULL,NULL),(364,18,'испанский',NULL,NULL),(365,18,'итальянский',NULL,NULL),(366,18,'китайский',NULL,NULL),(367,18,'латышский',NULL,NULL),(368,18,'литовский',NULL,NULL),(369,18,'немецкий',NULL,NULL),(370,18,'польский',NULL,NULL),(371,18,'русский',NULL,NULL),(372,18,'украинский',NULL,NULL),(373,18,'французский',NULL,NULL),(374,18,'японский',NULL,NULL),(375,19,'азербаджанец(ка)',NULL,NULL),(376,19,'алжирец(ка)',NULL,NULL),(377,19,'американец(ка)',NULL,NULL),(378,19,'англичанин(ка)',NULL,NULL),(379,19,'армянин(ка)',NULL,NULL),(380,19,'афганец(ка)',NULL,NULL),(381,19,'белорус(ка)',NULL,NULL),(382,19,'вьетнамец(ка)',NULL,NULL),(383,19,'грузин(ка)',NULL,NULL),(384,19,'дагестанец(ка)',NULL,NULL),(385,19,'еврей(ка)',NULL,NULL),(386,19,'египтянин(ка)',NULL,NULL),(387,19,'ингуш(ка)',NULL,NULL),(388,19,'индус(ка)',NULL,NULL),(389,19,'иранец(ка)',NULL,NULL),(390,19,'казах(шка)',NULL,NULL),(391,19,'камерунец(ка)',NULL,NULL),(392,19,'китаец(янка)',NULL,NULL),(393,19,'кубинец(ка)',NULL,NULL),(394,19,'кыргыз(ка)',NULL,NULL),(395,19,'латыш(ка)',NULL,NULL),(396,19,'ливанец(ка)',NULL,NULL),(397,19,'литовец(ка)',NULL,NULL),(398,19,'молдованин(ка)',NULL,NULL),(399,19,'немец(ка)',NULL,NULL),(400,19,'нигериец(йка)',NULL,NULL),(401,19,'пакистанец(ка)',NULL,NULL),(402,19,'поляк(ка)',NULL,NULL),(403,19,'пуштун(ка)',NULL,NULL),(404,19,'русский(ая)',NULL,NULL),(405,19,'сенигалец(ка)',NULL,NULL),(406,19,'серб(ка)',NULL,NULL),(407,19,'сириец(ка)',NULL,NULL),(408,19,'сомалиец(ка)',NULL,NULL),(409,19,'таджик(ка)',NULL,NULL),(410,19,'тамилец(ка)',NULL,NULL),(411,19,'туркмен(ка)',NULL,NULL),(412,19,'турок(ка)',NULL,NULL),(413,19,'узбек(ка)',NULL,NULL),(414,19,'украинец(ка)',NULL,NULL),(415,19,'цыган(ка)',NULL,NULL),(416,19,'чеченец(ка)',NULL,NULL),(417,19,'эфиоп(ка)',NULL,NULL),(456,19,'венгр(ка)',NULL,NULL),(458,22,'постановление',NULL,NULL),(459,22,'план',NULL,NULL),(460,22,'протокол',NULL,NULL),(461,22,'письмо',NULL,NULL),(462,22,'акт',NULL,NULL),(463,22,'справка',NULL,NULL),(464,22,'сопровдоительное',NULL,NULL),(465,22,'выписка',NULL,NULL),(466,7,'1250',NULL,NULL),(477,27,'УД',NULL,NULL),(478,27,'АД',NULL,NULL),(479,27,'НД',NULL,NULL),(480,22,'тематическое информирование',NULL,NULL),(484,29,'организация незаконной миграции - ст.371 УК РБ',NULL,NULL),(485,29,'незаконный оборот наркотических средств, психотропных веществ, их прекурсоров и аналогов - ст.328 УК РБ',NULL,NULL),(486,29,'незаконная предпринимательская деятельность - ст.233 УК РБ',NULL,NULL),(487,30,'частный извоз',NULL,NULL),(488,30,'розничная торговля',NULL,NULL),(489,30,'разведение крупнорогатого скота',NULL,NULL),(490,31,'фермерство',NULL,NULL),(491,31,'животноводство',NULL,NULL),(492,31,'торговля',NULL,NULL),(493,32,'Минская',NULL,NULL),(494,32,'Калининградская',NULL,NULL),(495,32,'Черниговская',NULL,NULL),(496,33,'Березовский',NULL,NULL),(497,33,'Ачхой-Мартановский',NULL,NULL),(498,33,'Столбцовский',NULL,NULL),(499,34,'грузовой повышенной проходимости с открытым кузовом',NULL,NULL),(500,34,'легковой',NULL,NULL),(501,34,'авиационный',NULL,NULL),(502,35,'ситроен',NULL,NULL),(503,35,'УАЗ',NULL,NULL),(504,35,'тойота',NULL,NULL),(505,36,'Ксантия',NULL,NULL),(506,36,'Ларгус',NULL,NULL),(507,36,'Цивик',NULL,NULL),(508,37,'Минск-Киев',NULL,NULL),(509,37,'Стамбул-Москва',NULL,NULL),(510,37,'Минск-Санкт-Петербург',NULL,NULL),(511,34,'грузовой тягач',NULL,NULL),(512,34,'грузовой повышенной проходимости',NULL,NULL),(513,34,'прицеп открытый',NULL,NULL),(514,34,'прицеп крытый',NULL,NULL),(515,34,'грузовой повышенной проходимости с закрытым кузовом',NULL,NULL),(516,34,'грузовой повышенной проходимости для перевозки людей',NULL,NULL),(517,34,'грузовой для перевозки людей',NULL,NULL),(518,34,'грузовой с открытым кузовом',NULL,NULL),(519,34,'грузовой с закрытым кузовом',NULL,NULL),(520,38,'красный',NULL,NULL),(521,38,'зеленый',NULL,NULL),(522,38,'синий',NULL,NULL),(523,39,'Минск',NULL,NULL),(524,39,'Лоев',NULL,NULL),(525,39,'Заболоть',NULL,NULL),(526,40,'передано в суд',NULL,NULL),(527,40,'объединено с УД',NULL,NULL),(528,40,'решение суда',NULL,NULL),(529,41,'Бенякони',NULL,NULL),(530,41,'Бенякони-1',NULL,NULL),(531,41,'Бенякони-2',NULL,NULL),(532,41,'Бобровники',NULL,NULL),(533,41,'Новая Гута',NULL,NULL),(534,42,'авто',NULL,NULL),(535,42,'авиа',NULL,NULL),(536,42,'ж/д',NULL,NULL),(537,42,'упрощенный (пуп)',NULL,NULL),(538,42,'пешеходный',NULL,NULL),(539,42,'временный ппр',NULL,NULL),(540,41,'Каменный Лог',NULL,NULL),(541,41,'Гудогай',NULL,NULL),(542,41,'Гудогай-1',NULL,NULL),(543,41,'Гудогай-2',NULL,NULL),(544,43,'противодействие незаконной миграции',NULL,NULL),(545,43,'противодействие НОН',NULL,NULL),(546,43,'противодействие ТМЦ',NULL,NULL),(547,29,'нарушение правил пребывания иностранного гражданина, лица без гражданства на территории Республики Беларусь - ст.23.55 КоАП',NULL,NULL),(548,29,'незаконное пересечение Государственной границы Республики Беларусь - 23.29 КоАП',NULL,NULL),(549,45,'дилер',NULL,NULL),(550,45,'организатор',NULL,NULL),(551,45,'соучастник',NULL,NULL),(552,45,'исполнитель',NULL,NULL),(553,45,'пособник',NULL,NULL),(555,45,'подозреваемый',NULL,NULL),(556,45,'потерпевший',NULL,NULL),(557,46,'место задержания',NULL,NULL),(558,46,'место совершения',NULL,NULL),(559,46,'место наблюдения',NULL,NULL),(560,46,'место происшествия',NULL,NULL),(561,47,'старший смены п/н',NULL,NULL),(562,47,'директор',NULL,NULL),(563,47,'заместитель начальника по ИР',NULL,NULL),(564,47,'начальник службы безопасности',NULL,NULL),(565,47,'начальник отдела кадров',NULL,NULL),(566,47,'начальник опк',NULL,NULL),(567,49,'стрелка влево (mdi-check)',NULL,NULL),(568,49,'человек (mdi-account)',NULL,NULL),(569,49,'предупреждение (mdi-alert)',NULL,NULL),(570,49,'(mdi-diamond)',NULL,NULL),(571,49,'(mdi-city)',NULL,NULL),(572,49,'(mdi-numeric)',NULL,NULL),(573,49,'(mdi-account-multiple)',NULL,NULL),(574,49,'(mdi-chevron-double-down)',NULL,NULL),(575,49,'(mdi-cloud-outline)',NULL,NULL),(576,49,'(mdi-play-pause)',NULL,NULL),(577,49,'(mdi-glass-tulip)',NULL,NULL),(578,22,'отчет',NULL,NULL),(579,22,'заявление',NULL,NULL),(580,22,'рапорт',NULL,NULL),(581,50,'организатор',NULL,NULL),(582,50,'сообщник',NULL,NULL),(583,31,'лагерь приема иностранцев',NULL,NULL),(584,31,'сдача транспорта в аренду',NULL,NULL),(585,50,'исполнитель',NULL,NULL),(590,54,'Начало',NULL,NULL),(591,54,'Конец',NULL,NULL),(592,55,'заместитеть начальника ПОГЗ',NULL,NULL),(593,55,'начальник ПОГЗ',NULL,NULL),(594,56,'Родитель/Ребенок',NULL,NULL),(595,56,'Брат/Сестра',NULL,NULL),(596,56,'Дядя(Тетя)/Племянник(Племянница)',NULL,NULL),(597,57,'Сигареты',NULL,NULL),(598,57,'Наркотики',NULL,NULL),(599,57,'Оружие',NULL,NULL),(600,58,'Героин',NULL,NULL),(601,58,'Марихуана',NULL,NULL),(602,58,'Гашиш',NULL,NULL),(603,59,'Забор оградительный (line-engeneer_zagr_invisible hidden)',NULL,NULL),(604,60,'Расположение заставы (icon-svg-force_frontier_inside)',NULL,NULL),(605,59,'Линия ГГ (line_layout_border hidden)',NULL,NULL),(606,59,'Пограничная полоса (line_border_path hidden)',NULL,NULL),(607,59,'Границы ПОГЗ(arc-layout-start arrow-layout-double-end)',NULL,NULL),(608,60,'Пограничный наряд (icon-file-border-guard-focres)',NULL,NULL),(609,60,'Пограничный знак (icon-svg-engineer_border_sign)',NULL,NULL),(610,60,'Наблюдательная вышка (icon-svg-engineer_tower_industrial)',NULL,NULL),(611,60,'Камера (icon-svg-engineer_video)',NULL,NULL),(612,59,'КСП (line-engeneer_ksp hidden)',NULL,NULL),(613,60,'Расположение заставы сопредел (icon-svg-force_frontier_outside)',NULL,NULL),(614,61,'Изнасилование',NULL,NULL),(615,61,'Кража',NULL,NULL),(616,61,'Злостное хулиганство',NULL,NULL),(617,59,'Штрих-пунктир (line_layout_1 hidden)',NULL,NULL),(618,59,'Маршрут вертолета (line-force_helicopter_route_inside hidden)',NULL,NULL),(619,59,'Маршрут вертолета сопредел (line-force_helicopter_route_outside hidden)',NULL,NULL),(620,60,'Пограничный наряд (icon-svg-force_patrol_inside)',NULL,NULL),(621,60,'Пограничный наряд сопредел (icon-svg-force_patrol_outside)',NULL,NULL),(622,59,'Маршрут БПЛА сопредел (line-force_quadcopter_route_outside hidden)',NULL,NULL),(623,59,'Границы ПОГЗ сопредел(arrow-layout-double-end)',NULL,NULL),(624,60,'Место задержания ОПС (icon-svg-point_detention_inside)',NULL,NULL);
/*!40000 ALTER TABLE `sys_list_dop` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sys_list_top`
--

DROP TABLE IF EXISTS `sys_list_top`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sys_list_top` (
  `id` mediumint unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(25) DEFAULT NULL,
  `title` varchar(50) DEFAULT NULL,
  `strong` bit(1) DEFAULT b'0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ind_name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=62 DEFAULT CHARSET=utf8mb3 AVG_ROW_LENGTH=862 ROW_FORMAT=DYNAMIC COMMENT='списки';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_list_top`
--

LOCK TABLES `sys_list_top` WRITE;
/*!40000 ALTER TABLE `sys_list_top` DISABLE KEYS */;
INSERT INTO `sys_list_top` VALUES (1,'citizenship','Гражданство',_binary '\0'),(2,'sex','Пол',_binary ''),(3,'education','Образование',_binary ''),(4,'social_status','Социальное положение',_binary '\0'),(5,'marital_status','Семейное положение',_binary '\0'),(6,'ownership','Форма собственности',_binary '\0'),(7,'tops','ТОПС',_binary '\0'),(8,'yes_no','Да/Нет',_binary '\0'),(10,'plot','Участок по направлению',_binary '\0'),(11,'category_location','Категория места',_binary '\0'),(12,'course','Направление',_binary '\0'),(13,'number_pogz','Номер погз',_binary '\0'),(14,'number_pogp','Наименование погз, погп',_binary '\0'),(15,'pogk','Наименование погк',_binary '\0'),(16,'od','Задержание ОД',_binary '\0'),(17,'rang','Воинское звание',_binary '\0'),(18,'language_skils','Знание языков',_binary '\0'),(19,'nationality','Национальность',_binary '\0'),(22,'type_doc','Вид документа',_binary '\0'),(27,'type_book','Вид дела',_binary '\0'),(29,'st','Статья УК/КоАП',_binary '\0'),(30,'activ_org','Род деятельности',_binary '\0'),(31,'vid_org','Вид деятельности',_binary '\0'),(32,'oblast','Область',_binary '\0'),(33,'raion','Район',_binary '\0'),(34,'vid_transporta','Вид транспорта',_binary '\0'),(35,'marka_transport','Марка транспорта',_binary '\0'),(36,'model_transport','Модель транспорта',_binary '\0'),(37,'marshrut_transport','Маршрут транспорта (сообщение)',_binary '\0'),(38,'color','Цвет',_binary '\0'),(39,'nasel_punkt','Населенный пункт',_binary '\0'),(40,'osnovanie_prekr','Основание прекращения',_binary '\0'),(41,'opk','Пункт пропуска',_binary '\0'),(42,'vid_ppr','Вид пункта пропуска',_binary '\0'),(43,'line_ppd','Линия ППД',_binary '\0'),(45,'category_men','Категория лица в деле',_binary '\0'),(46,'toch_sob','Точка события на карте',_binary '\0'),(47,'dolznost','Должность',_binary '\0'),(48,'geometry_folders','Папки геометрии',_binary '\0'),(49,'icons','Иконки',_binary '\0'),(50,'role_in_document','Роль в документе',_binary '\0'),(53,'user_groups','Группы пользователей',_binary '\0'),(54,'work_status','Статус работ',_binary '\0'),(55,'rank_POGZ','Должность ПОГЗ',_binary '\0'),(56,'kinship_status','Статус родства',_binary '\0'),(57,'type_contraban_list','Тип контробанды',_binary '\0'),(58,'drags_type','Тип наркотиков',_binary '\0'),(59,'type_of_geometry','Условное обозначение геометрии',_binary '\0'),(60,'type_of_point','Условное обозначение точки',_binary '\0'),(61,'Offense','Правонарушение',_binary '\0');
/*!40000 ALTER TABLE `sys_list_top` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sys_notify`
--

DROP TABLE IF EXISTS `sys_notify`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sys_notify` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `from_user_id` int DEFAULT NULL,
  `to_user_id` int DEFAULT NULL,
  `date_time` datetime DEFAULT NULL,
  `type` enum('information','error','warning') CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `content` text,
  `file_id` int DEFAULT NULL,
  `geometry` text CHARACTER SET utf8 COLLATE utf8_general_ci,
  `is_read` bit(1) DEFAULT b'0',
  PRIMARY KEY (`id`),
  KEY `sys_notify_FK_1` (`from_user_id`),
  KEY `sys_notify_FK` (`file_id`),
  KEY `sys_notify_FK_2` (`to_user_id`),
  CONSTRAINT `sys_notify_FK` FOREIGN KEY (`file_id`) REFERENCES `sys_reports` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `sys_notify_FK_1` FOREIGN KEY (`from_user_id`) REFERENCES `authentication_modelcustomuser` (`id`),
  CONSTRAINT `sys_notify_FK_2` FOREIGN KEY (`to_user_id`) REFERENCES `authentication_modelcustomuser` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=454 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_notify`
--

LOCK TABLES `sys_notify` WRITE;
/*!40000 ALTER TABLE `sys_notify` DISABLE KEYS */;
/*!40000 ALTER TABLE `sys_notify` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sys_obj`
--

DROP TABLE IF EXISTS `sys_obj`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sys_obj` (
  `id` tinyint unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(15) NOT NULL,
  `title` varchar(25) NOT NULL,
  `title_single` varchar(25) NOT NULL,
  `icon` varchar(25) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT 'fa_link',
  `descript` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=53 DEFAULT CHARSET=utf8mb3 AVG_ROW_LENGTH=1638 ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_obj`
--

LOCK TABLES `sys_obj` WRITE;
/*!40000 ALTER TABLE `sys_obj` DISABLE KEYS */;
INSERT INTO `sys_obj` VALUES (1,'rel','события/связи','событие/связь','mdi-link',NULL),(10,'free','значения','значение','mdi-star-outline',NULL),(15,'file','файлы','файл','mdi-file-outline',NULL),(20,'doc','документы','документ','mdi-format-align-left',NULL),(25,'point','точки','точка','mdi-map-marker-outline',NULL),(30,'geometry','геометрия','геометрия','mdi-vector-polygon',NULL),(35,'person_p','физлица','физлицо','mdi-account-outline',NULL),(40,'person_l','организации','организация','mdi-stamper',''),(45,'case','дела','дело','mdi-lock-outline',NULL),(50,'transport','транспорт','транспорт','mdi-car-outline',NULL),(52,'telefon','телефон','телефон','mdi-phone-classic',NULL);
/*!40000 ALTER TABLE `sys_obj` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sys_phone_number_format`
--

DROP TABLE IF EXISTS `sys_phone_number_format`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sys_phone_number_format` (
  `id` tinyint unsigned NOT NULL AUTO_INCREMENT,
  `country` varchar(29) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `country_code` int DEFAULT NULL,
  `length` int DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=204 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_phone_number_format`
--

LOCK TABLES `sys_phone_number_format` WRITE;
/*!40000 ALTER TABLE `sys_phone_number_format` DISABLE KEYS */;
INSERT INTO `sys_phone_number_format` VALUES (1,'Россия',7,11),(2,'Украина',380,12),(3,'Казахстан',77,11),(4,'Литва',370,11),(5,'Беларусь',375,12),(6,'США',1,11),(7,'Абхазия',7940,11),(8,'Австралия',61,11),(9,'Австрия',43,12),(10,'Азербайджан',994,12),(11,'Албания',355,12),(12,'Алжир',213,12),(13,'Ангола',244,12),(14,'Андорра',376,9),(15,'Антигуа и Барбуда',1268,11),(16,'Аргентина',54,13),(17,'Армения',374,11),(18,'Аруба',297,10),(19,'Афганистан',93,11),(20,'Багамские о-ва',1242,11),(21,'Бангладеш',880,13),(22,'Барбадос',1246,11),(23,'Бахрейн',973,11),(24,'Белиз',501,10),(25,'Бельгия',32,11),(26,'Бенин',229,11),(27,'Берег слоновой кости',225,11),(28,'Бермуды',1441,11),(29,'Болгария',359,12),(30,'Боливия',591,11),(31,'Босния',387,11),(32,'Ботсвана',267,11),(33,'Бразилия',55,12),(34,'Британские Вирджинские о-ва',1284,11),(35,'Бруней',673,10),(36,'Буркина Фасо',226,11),(37,'Бурунди',257,11),(38,'Бутан',975,11),(39,'Вануату',678,10),(40,'Великобритания',44,12),(41,'Венгрия',36,11),(42,'Венесуэла',58,12),(43,'Восточный Тимор',670,11),(44,'Вьетнам',84,11),(45,'Габон',241,11),(46,'Гаити',509,11),(47,'Гамбия',220,10),(48,'Гана',233,12),(49,'Гваделупа',590,12),(50,'Гватемала',502,11),(51,'Гвинея',224,11),(52,'Гвинея-Бисау',245,10),(53,'Германия',49,12),(54,'Гибралтар',350,11),(55,'Гонг Конг',852,11),(56,'Гондурас',504,11),(57,'Гренада',1473,11),(58,'Гренландия',299,9),(59,'Греция',30,12),(60,'Грузия',995,12),(61,'Гуам',671,11),(62,'Дания',45,10),(63,'Доминика',1767,11),(64,'Доминиканская республика',1809,11),(65,'Египет',20,12),(66,'Замбия',260,12),(67,'Зимбабве',263,12),(68,'Израиль',972,12),(69,'Индия',91,12),(70,'Индонезия',62,11),(71,'Иордания',962,12),(72,'Ирак',964,13),(73,'Иран',98,12),(74,'Ирландия',353,12),(75,'Исландия',354,10),(76,'Испания',34,11),(77,'Италия',39,12),(78,'Йемен',967,12),(79,'Каймановы о-ва',1345,11),(80,'Камбоджа',855,11),(81,'Камерун',237,11),(82,'Канада',1,11),(83,'Капе Верде',238,10),(84,'Катар',974,11),(85,'Кения',254,12),(86,'Кипр',357,11),(87,'Китай',86,13),(88,'Колумбия',57,12),(89,'Коморские о-ва',269,10),(90,'Конго',242,12),(91,'Конго',242,12),(92,'Косово',3478,0),(93,'Коста-Рика',506,11),(94,'Куба',53,10),(95,'Кыргызстан',996,12),(96,'Кювейт',965,11),(97,'Кюрасао',599,11),(98,'Латвия',371,11),(99,'Лесото',266,11),(100,'Либерия',231,10),(101,'Ливан',961,11),(102,'Ливия',21,12),(103,'Лихтенштейн',423,12),(104,'Люксенбург',352,12),(105,'Маврикий',230,10),(106,'Мавритания',222,11),(107,'Мадагаскар',261,12),(108,'Макао',853,11),(109,'Македония',389,11),(110,'Малави',265,12),(111,'Малайзия',60,11),(112,'Мали',223,11),(113,'Мальдивы',960,10),(114,'Мальта',356,11),(115,'Марокко',212,12),(116,'Мартиника',596,12),(117,'Мексика',52,13),(118,'Мозамбик',258,12),(119,'Молдова',373,11),(120,'Монако',377,12),(121,'Монголия',976,11),(122,'Монтенегро',381,11),(123,'Намибия',264,12),(124,'Науру',674,10),(125,'Непал',977,13),(126,'Нигер',227,11),(127,'Нигерия',234,13),(128,'Нидерланды',31,11),(129,'Никарагуа',505,11),(130,'Новая Зеландия',64,11),(131,'Новая Каледония',687,9),(132,'Норвегия',47,10),(133,'о-ва Кука',682,8),(134,'Объединенные Арабские эмираты',971,12),(135,'Оман',968,11),(136,'Пакистан',92,12),(137,'Палестина',970,12),(138,'Панама',507,11),(139,'Папуа-Новая Гвинея',675,10),(140,'Парагвай',595,12),(141,'Перу',51,11),(142,'Польша',48,11),(143,'Португалия',351,12),(144,'Пуэрто Рико',1787,11),(145,'Реюнион',262,12),(146,'Руанда',250,12),(147,'Румыния',40,11),(148,'Самоа',685,9),(149,'Сан-Марино',378,11),(150,'Санта Лючия',1758,11),(151,'Саудовская Аравия',966,12),(152,'Северная Корея',82,13),(153,'Северо-Марианские о-ва',670,11),(154,'Сейшельские острова',248,10),(155,'Сенегал',221,12),(156,'Сент Винцент и Гренадины',1784,11),(157,'Сент-Китс и Невис',1869,11),(158,'Сербия',381,11),(159,'Сингапур',65,10),(160,'Сирия',963,12),(161,'Словакия',421,12),(162,'Словения',386,11),(163,'Соломоновы острова',677,10),(164,'Судан',249,12),(165,'Суринам',597,10),(166,'Сьерра-Леоне',232,11),(167,'Таджикистан',992,12),(168,'Таиланд',66,11),(169,'Тайвань',886,12),(170,'Танзания',255,12),(171,'Того',228,11),(172,'Тонга',676,10),(173,'Тринидад и Тобаго',1868,11),(174,'Тунис',216,11),(175,'Туркменистан',993,11),(176,'Турция',90,12),(177,'Уганда',256,12),(178,'Узбекистан',998,12),(179,'Уругвай',598,11),(180,'Фарерские острова',298,9),(181,'Фиджи',679,10),(182,'Филиппины',63,12),(183,'Финляндия',358,12),(184,'Франция',33,11),(185,'Французская Гвиана',594,12),(186,'Французская Полинезия',689,9),(187,'Хорватия',385,11),(188,'ЦАР',236,11),(189,'Чад',235,11),(190,'Чешская республика',420,12),(191,'Чили',56,11),(192,'Швейцария',41,11),(193,'Швеция',46,11),(194,'Шри-Ланка',94,11),(195,'Эквадор',593,12),(196,'Экваториальная Гвинея',240,12),(197,'Эль Сальвадор',503,11),(198,'Эстония',372,11),(199,'Эфиопия',251,12),(200,'ЮАР',27,11),(201,'Южная Корея',82,12),(202,'Ямайка',1876,11),(203,'Япония',81,12);
/*!40000 ALTER TABLE `sys_phone_number_format` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sys_reports`
--

DROP TABLE IF EXISTS `sys_reports`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sys_reports` (
  `id` int NOT NULL AUTO_INCREMENT,
  `path` varchar(255) NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `date_auto_remove` datetime DEFAULT NULL,
  `params` text,
  `status` enum('in_progress','done','error') DEFAULT NULL,
  `user_id` int DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=232 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_reports`
--

LOCK TABLES `sys_reports` WRITE;
/*!40000 ALTER TABLE `sys_reports` DISABLE KEYS */;
/*!40000 ALTER TABLE `sys_reports` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sys_script`
--

DROP TABLE IF EXISTS `sys_script`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sys_script` (
  `id` smallint unsigned NOT NULL AUTO_INCREMENT,
  `parent_id` smallint unsigned DEFAULT NULL,
  `title` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `icon` varchar(25) DEFAULT NULL,
  `hint` varchar(255) DEFAULT NULL,
  `content` text,
  `descript` mediumtext,
  `variables` text CHARACTER SET utf8 COLLATE utf8_general_ci,
  `enabled` tinyint(1) NOT NULL DEFAULT '1',
  `owner_id` tinyint unsigned DEFAULT NULL,
  `type` enum('map','report') DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ind_name` (`title`),
  KEY `sys_script_owner_id_de248bfe_fk_owner_lines_id` (`owner_id`),
  KEY `sys_script_parent_id_de218bfe_fk_sys_script_id` (`parent_id`),
  CONSTRAINT `sys_script_owner_id_de248bfe_fk_owner_lines_id` FOREIGN KEY (`owner_id`) REFERENCES `owner_lines` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `sys_script_parent_id_de218bfe_fk_sys_script_id` FOREIGN KEY (`parent_id`) REFERENCES `sys_script` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=135 DEFAULT CHARSET=utf8mb3 AVG_ROW_LENGTH=2048 ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_script`
--

LOCK TABLES `sys_script` WRITE;
/*!40000 ALTER TABLE `sys_script` DISABLE KEYS */;
/*!40000 ALTER TABLE `sys_script` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sys_script_variable`
--

DROP TABLE IF EXISTS `sys_script_variable`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sys_script_variable` (
  `id` tinyint unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `title` varchar(255) DEFAULT NULL,
  `hint` varchar(255) DEFAULT NULL,
  `type` enum('number','text','datetime','date','checkbox','geometry','phone_number','list','search','file_any') CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `list_id` mediumint unsigned DEFAULT NULL,
  `obj_id` tinyint unsigned DEFAULT NULL,
  `script_id` smallint unsigned DEFAULT NULL,
  `necessary` tinyint(1) DEFAULT '1',
  PRIMARY KEY (`id`),
  KEY `sys_script_variables_FK` (`list_id`),
  KEY `sys_script_variables_FK_1` (`obj_id`),
  KEY `sys_script_variables_FK_2` (`script_id`),
  CONSTRAINT `sys_script_variables_FK` FOREIGN KEY (`list_id`) REFERENCES `sys_list_top` (`id`),
  CONSTRAINT `sys_script_variables_FK_1` FOREIGN KEY (`obj_id`) REFERENCES `sys_obj` (`id`),
  CONSTRAINT `sys_script_variables_FK_2` FOREIGN KEY (`script_id`) REFERENCES `sys_script` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=65 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_script_variable`
--

LOCK TABLES `sys_script_variable` WRITE;
/*!40000 ALTER TABLE `sys_script_variable` DISABLE KEYS */;
/*!40000 ALTER TABLE `sys_script_variable` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sys_sript_result`
--

DROP TABLE IF EXISTS `sys_sript_result`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sys_sript_result` (
  `id` tinyint unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(256) DEFAULT NULL,
  `user` int DEFAULT NULL,
  `params` text,
  `result` text,
  `date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `map_sript_result_FK` (`user`),
  CONSTRAINT `map_sript_result_FK` FOREIGN KEY (`user`) REFERENCES `authentication_modelcustomuser` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_sript_result`
--

LOCK TABLES `sys_sript_result` WRITE;
/*!40000 ALTER TABLE `sys_sript_result` DISABLE KEYS */;
/*!40000 ALTER TABLE `sys_sript_result` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sys_templates`
--

DROP TABLE IF EXISTS `sys_templates`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sys_templates` (
  `id` int NOT NULL AUTO_INCREMENT,
  `group_id` int DEFAULT NULL,
  `title` varchar(100) DEFAULT NULL,
  `active_scripts` text CHARACTER SET utf8 COLLATE utf8_general_ci,
  `passive_scripts` text,
  PRIMARY KEY (`id`),
  KEY `sys_templates_FK_1` (`group_id`),
  CONSTRAINT `sys_templates_FK` FOREIGN KEY (`group_id`) REFERENCES `owner_groups` (`id`),
  CONSTRAINT `sys_templates_FK_1` FOREIGN KEY (`group_id`) REFERENCES `owner_groups` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=47 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_templates`
--

LOCK TABLES `sys_templates` WRITE;
/*!40000 ALTER TABLE `sys_templates` DISABLE KEYS */;
/*!40000 ALTER TABLE `sys_templates` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sys_trigger`
--

DROP TABLE IF EXISTS `sys_trigger`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sys_trigger` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `object_id` tinyint unsigned DEFAULT NULL,
  `title` varchar(50) DEFAULT NULL,
  `hint` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `content` text,
  `variables` text,
  PRIMARY KEY (`id`),
  KEY `sys_triger_FK` (`object_id`),
  CONSTRAINT `sys_triger_FK` FOREIGN KEY (`object_id`) REFERENCES `sys_obj` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_trigger`
--

LOCK TABLES `sys_trigger` WRITE;
/*!40000 ALTER TABLE `sys_trigger` DISABLE KEYS */;
/*!40000 ALTER TABLE `sys_trigger` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sys_trigger_variable`
--

DROP TABLE IF EXISTS `sys_trigger_variable`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sys_trigger_variable` (
  `id` tinyint unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `title` varchar(255) DEFAULT NULL,
  `hint` varchar(255) DEFAULT NULL,
  `type` enum('number','text','datetime','date','checkbox','geometry','phone_number','list','search','file_any') CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `list_id` mediumint unsigned DEFAULT NULL,
  `obj_id` tinyint unsigned DEFAULT NULL,
  `trigger_id` int unsigned DEFAULT NULL,
  `necessary` tinyint(1) DEFAULT '1',
  PRIMARY KEY (`id`),
  KEY `sys_trigger_variables_FK` (`list_id`),
  KEY `sys_trigger_variables_FK_1` (`obj_id`),
  KEY `sys_trigger_variable_FK` (`trigger_id`),
  CONSTRAINT `sys_trigger_variable_FK` FOREIGN KEY (`trigger_id`) REFERENCES `sys_trigger` (`id`),
  CONSTRAINT `sys_trigger_variables_FK` FOREIGN KEY (`list_id`) REFERENCES `sys_list_top` (`id`),
  CONSTRAINT `sys_trigger_variables_FK_1` FOREIGN KEY (`obj_id`) REFERENCES `sys_obj` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_trigger_variable`
--

LOCK TABLES `sys_trigger_variable` WRITE;
/*!40000 ALTER TABLE `sys_trigger_variable` DISABLE KEYS */;
/*!40000 ALTER TABLE `sys_trigger_variable` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-12-07 11:58:42
