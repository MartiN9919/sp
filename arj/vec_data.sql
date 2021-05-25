-- MySQL dump 10.13  Distrib 8.0.23, for Linux (x86_64)
--
-- Host: localhost    Database: vec_data
-- ------------------------------------------------------
-- Server version	8.0.23-0ubuntu0.20.04.1

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
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
) ENGINE=InnoDB AUTO_INCREMENT=81 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add content type',4,'add_contenttype'),(14,'Can change content type',4,'change_contenttype'),(15,'Can delete content type',4,'delete_contenttype'),(16,'Can view content type',4,'view_contenttype'),(17,'Can add session',5,'add_session'),(18,'Can change session',5,'change_session'),(19,'Can delete session',5,'delete_session'),(20,'Can view session',5,'view_session'),(21,'Can add Группа',6,'add_modelownergroups'),(22,'Can change Группа',6,'change_modelownergroups'),(23,'Can delete Группа',6,'delete_modelownergroups'),(24,'Can view Группа',6,'view_modelownergroups'),(25,'Can add Линия',7,'add_modelownerlines'),(26,'Can change Линия',7,'change_modelownerlines'),(27,'Can delete Линия',7,'delete_modelownerlines'),(28,'Can view Линия',7,'view_modelownerlines'),(29,'Can add Регион',8,'add_modelownerregions'),(30,'Can change Регион',8,'change_modelownerregions'),(31,'Can delete Регион',8,'delete_modelownerregions'),(32,'Can view Регион',8,'view_modelownerregions'),(33,'Can add user',9,'add_modelcustomuser'),(34,'Can change user',9,'change_modelcustomuser'),(35,'Can delete user',9,'delete_modelcustomuser'),(36,'Can view user',9,'view_modelcustomuser'),(37,'Can add model owner line',10,'add_modelownerline'),(38,'Can change model owner line',10,'change_modelownerline'),(39,'Can delete model owner line',10,'delete_modelownerline'),(40,'Can view model owner line',10,'view_modelownerline'),(41,'Can add Скрипт',11,'add_modelscript'),(42,'Can change Скрипт',11,'change_modelscript'),(43,'Can delete Скрипт',11,'delete_modelscript'),(44,'Can view Скрипт',11,'view_modelscript'),(45,'Can add Классификатор',12,'add_modelkey'),(46,'Can change Классификатор',12,'change_modelkey'),(47,'Can delete Классификатор',12,'delete_modelkey'),(48,'Can view Классификатор',12,'view_modelkey'),(49,'Can add Список',13,'add_modellist'),(50,'Can change Список',13,'change_modellist'),(51,'Can delete Список',13,'delete_modellist'),(52,'Can view Список',13,'view_modellist'),(53,'Can add Поле списка',14,'add_modellistdop'),(54,'Can change Поле списка',14,'change_modellistdop'),(55,'Can delete Поле списка',14,'delete_modellistdop'),(56,'Can view Поле списка',14,'view_modellistdop'),(57,'Can add Объект',15,'add_modelobject'),(58,'Can change Объект',15,'change_modelobject'),(59,'Can delete Объект',15,'delete_modelobject'),(60,'Can view Объект',15,'view_modelobject'),(61,'Can add group',16,'add_group'),(62,'Can change group',16,'change_group'),(63,'Can delete group',16,'delete_group'),(64,'Can view group',16,'view_group'),(65,'Can add push information',17,'add_pushinformation'),(66,'Can change push information',17,'change_pushinformation'),(67,'Can delete push information',17,'delete_pushinformation'),(68,'Can view push information',17,'view_pushinformation'),(69,'Can add subscription info',18,'add_subscriptioninfo'),(70,'Can change subscription info',18,'change_subscriptioninfo'),(71,'Can delete subscription info',18,'delete_subscriptioninfo'),(72,'Can view subscription info',18,'view_subscriptioninfo'),(73,'Can add Файл',20,'add_modelofficialdocument'),(74,'Can change Файл',20,'change_modelofficialdocument'),(75,'Can delete Файл',20,'delete_modelofficialdocument'),(76,'Can view Файл',20,'view_modelofficialdocument'),(77,'Can add Уведомление',19,'add_modelnotification'),(78,'Can change Уведомление',19,'change_modelnotification'),(79,'Can delete Уведомление',19,'delete_modelnotification'),(80,'Can view Уведомление',19,'view_modelnotification');
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
  `owner_groups_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `authentication_modelcustomuser`
--

LOCK TABLES `authentication_modelcustomuser` WRITE;
/*!40000 ALTER TABLE `authentication_modelcustomuser` DISABLE KEYS */;
INSERT INTO `authentication_modelcustomuser` VALUES (1,'pbkdf2_sha256$260000$sL7vWvWbW45Y2KbyGY8I05$Q4pi7xCNFuLbzCoXNn6D9LzPsiB+BqiQanNekE0GLIo=','2021-04-28 07:01:16.101359',1,'pushkin','Максим','Бурень',1,1,1),(2,'pbkdf2_sha256$216000$HsYAoFjAkup3$Wmcg7bEFWO1TkkRwXkg0F5KHLF/WFbS9/ZF3+ZHoIKc=','2021-04-16 09:45:48.465221',0,'evgestrogan','Кирилл','Стасюк',1,1,23);
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
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
) ENGINE=InnoDB AUTO_INCREMENT=75 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2021-04-16 09:31:57.341869','1','pushkin',2,'[{\"changed\": {\"fields\": [\"\\u0413\\u0440\\u0443\\u043f\\u043f\\u0430 \\u0434\\u043e\\u0441\\u0442\\u0443\\u043f\\u0430\"]}}]',9,1),(2,'2021-04-16 09:36:40.343980','2','evgestrogan',1,'[{\"added\": {}}]',9,1),(3,'2021-04-16 09:37:19.310153','2','evgestrogan',2,'[{\"changed\": {\"fields\": [\"First name\", \"Last name\", \"Staff status\", \"\\u0413\\u0440\\u0443\\u043f\\u043f\\u0430 \\u0434\\u043e\\u0441\\u0442\\u0443\\u043f\\u0430\"]}}]',9,1),(4,'2021-04-16 12:34:31.762091','2','evgestrogan',2,'[{\"changed\": {\"fields\": [\"\\u0413\\u0440\\u0443\\u043f\\u043f\\u0430 \\u0434\\u043e\\u0441\\u0442\\u0443\\u043f\\u0430\"]}}]',9,1),(5,'2021-04-21 08:53:09.040562','35','information',1,'[{\"added\": {}}]',19,1),(6,'2021-04-21 08:55:54.279974','35','information',2,'[]',19,1),(7,'2021-04-21 08:56:12.440275','35','information',2,'[]',19,1),(8,'2021-04-21 08:56:27.923759','36','information',1,'[{\"added\": {}}]',19,1),(9,'2021-04-21 08:56:56.010317','37','information',1,'[{\"added\": {}}]',19,1),(10,'2021-04-21 09:04:09.084482','37','information',2,'[]',19,1),(11,'2021-04-21 09:44:26.679384','37','information',2,'[]',19,1),(12,'2021-04-21 09:48:58.450274','40','warning',1,'[{\"added\": {}}]',19,1),(13,'2021-04-21 09:49:40.765615','42','information',1,'[{\"added\": {}}]',19,1),(14,'2021-04-21 10:38:59.886850','43','information',1,'[{\"added\": {}}]',19,1),(15,'2021-04-21 10:39:14.282192','43','information',3,'',19,1),(16,'2021-04-21 10:39:14.289657','42','information',3,'',19,1),(17,'2021-04-21 10:39:14.292264','40','warning',3,'',19,1),(18,'2021-04-21 10:39:14.293715','37','information',3,'',19,1),(19,'2021-04-21 10:39:14.295331','36','information',3,'',19,1),(20,'2021-04-21 10:39:14.296474','35','information',3,'',19,1),(21,'2021-04-21 11:12:17.104002','44','warning',1,'[{\"added\": {}}]',19,1),(22,'2021-04-21 11:12:40.240087','45','information',1,'[{\"added\": {}}]',19,1),(23,'2021-04-21 11:52:58.908589','46','information',1,'[{\"added\": {}}]',19,1),(24,'2021-04-21 12:24:25.970065','51','information',1,'[{\"added\": {}}]',19,1),(25,'2021-04-21 12:28:42.647062','52','information',1,'[{\"added\": {}}]',19,1),(26,'2021-04-21 12:29:17.069171','52','information',3,'',19,1),(27,'2021-04-21 12:29:17.077393','51','information',3,'',19,1),(28,'2021-04-21 12:29:17.080202','46','information',3,'',19,1),(29,'2021-04-21 12:29:17.082542','45','information',3,'',19,1),(30,'2021-04-21 12:29:17.085607','44','warning',3,'',19,1),(31,'2021-04-21 12:29:32.450828','53','information',1,'[{\"added\": {}}]',19,1),(32,'2021-04-21 12:29:45.229358','54','warning',1,'[{\"added\": {}}]',19,1),(33,'2021-04-21 14:19:27.779135','55','error',1,'[{\"added\": {}}]',19,1),(34,'2021-04-21 14:19:40.195072','56','information',1,'[{\"added\": {}}]',19,1),(35,'2021-04-21 14:21:58.342981','55','error',3,'',19,1),(36,'2021-04-21 14:24:08.886191','57','error',1,'[{\"added\": {}}]',19,1),(37,'2021-04-26 09:38:54.382977','None','папка отчетов',1,'[{\"added\": {}}]',11,1),(38,'2021-04-26 11:43:57.545410','None','тестовый отчет',1,'[{\"added\": {}}]',11,1),(39,'2021-04-26 11:46:26.504809','40','тестовый отчет',2,'[]',11,1),(40,'2021-04-26 11:47:17.927593','40','тестовый отчет',2,'[{\"changed\": {\"fields\": [\"\\u041f\\u0435\\u0440\\u0435\\u043c\\u0435\\u043d\\u043d\\u044b\\u0435\"]}}]',11,1),(41,'2021-04-26 12:27:49.913100','40','тестовый отчет',2,'[]',11,1),(42,'2021-04-26 12:28:58.822015','40','тестовый отчет',2,'[]',11,1),(43,'2021-04-26 12:29:30.526260','40','тестовый отчет',2,'[]',11,1),(44,'2021-04-26 12:29:51.006803','40','тестовый отчет',2,'[]',11,1),(45,'2021-04-26 12:31:02.438862','40','тестовый отчет',2,'[]',11,1),(46,'2021-04-26 12:31:23.185645','40','тестовый отчет',2,'[]',11,1),(47,'2021-04-26 12:32:42.931298','40','тестовый отчет',2,'[{\"changed\": {\"fields\": [\"\\u0422\\u0435\\u043a\\u0441\\u0442 \\u0441\\u043a\\u0440\\u0438\\u043f\\u0442\\u0430\"]}}]',11,1),(48,'2021-04-26 12:35:26.624998','40','тестовый отчет',2,'[]',11,1),(49,'2021-04-26 12:40:57.663386','40','тестовый отчет',2,'[{\"changed\": {\"fields\": [\"\\u0422\\u0435\\u043a\\u0441\\u0442 \\u0441\\u043a\\u0440\\u0438\\u043f\\u0442\\u0430\"]}}]',11,1),(50,'2021-04-26 12:42:38.327962','40','тестовый отчет',2,'[{\"changed\": {\"fields\": [\"\\u0422\\u0435\\u043a\\u0441\\u0442 \\u0441\\u043a\\u0440\\u0438\\u043f\\u0442\\u0430\"]}}]',11,1),(51,'2021-04-26 12:47:24.030604','40','тестовый отчет',2,'[]',11,1),(52,'2021-04-26 12:48:24.105497','40','тестовый отчет',2,'[]',11,1),(53,'2021-04-26 12:48:57.069178','40','тестовый отчет',2,'[]',11,1),(54,'2021-04-27 06:04:17.611353','40','тестовый отчет',2,'[]',11,1),(55,'2021-04-27 06:17:45.217357','40','тестовый отчет',2,'[]',11,1),(56,'2021-04-27 06:18:53.770875','40','тестовый отчет',2,'[]',11,1),(57,'2021-04-27 06:25:41.573152','40','тестовый отчет',2,'[{\"changed\": {\"fields\": [\"\\u0422\\u0435\\u043a\\u0441\\u0442 \\u0441\\u043a\\u0440\\u0438\\u043f\\u0442\\u0430\"]}}]',11,1),(58,'2021-04-27 06:27:00.790764','40','тестовый отчет',2,'[{\"changed\": {\"fields\": [\"\\u0422\\u0435\\u043a\\u0441\\u0442 \\u0441\\u043a\\u0440\\u0438\\u043f\\u0442\\u0430\"]}}]',11,1),(59,'2021-04-27 06:29:53.518909','40','тестовый отчет',2,'[{\"changed\": {\"fields\": [\"\\u0422\\u0435\\u043a\\u0441\\u0442 \\u0441\\u043a\\u0440\\u0438\\u043f\\u0442\\u0430\"]}}]',11,1),(60,'2021-04-27 06:30:16.112750','40','тестовый отчет',2,'[]',11,1),(61,'2021-04-27 06:33:59.505725','40','тестовый отчет',2,'[{\"changed\": {\"fields\": [\"\\u0422\\u0435\\u043a\\u0441\\u0442 \\u0441\\u043a\\u0440\\u0438\\u043f\\u0442\\u0430\"]}}]',11,1),(62,'2021-04-27 06:34:23.464583','40','тестовый отчет',2,'[]',11,1),(63,'2021-04-27 06:40:08.689110','None','получить geojson',1,'[{\"added\": {}}]',11,1),(64,'2021-04-27 09:23:22.627780','50012','Номер поезда, рейса самолета, автобуса',2,'[]',12,1),(65,'2021-04-28 07:19:48.523355','90','information',3,'',19,1),(66,'2021-04-28 07:19:48.527819','89','information',3,'',19,1),(67,'2021-04-28 07:19:48.529638','88','information',3,'',19,1),(68,'2021-04-28 07:19:48.530820','87','information',3,'',19,1),(69,'2021-04-28 07:19:48.532572','86','information',3,'',19,1),(70,'2021-04-28 07:19:48.533668','85','information',3,'',19,1),(71,'2021-04-28 07:19:48.535353','84','information',3,'',19,1),(72,'2021-04-28 07:19:48.536971','59','information',3,'',19,1),(73,'2021-04-28 08:11:20.152707','40','тестовый отчет',2,'[]',11,1),(74,'2021-04-28 08:11:49.436929','40','тестовый отчет',2,'[]',11,1);
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
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(9,'authentication','modelcustomuser'),(6,'authentication','modelownergroups'),(7,'authentication','modelownerlines'),(8,'authentication','modelownerregions'),(12,'classifier','modelkey'),(13,'classifier','modellist'),(14,'classifier','modellistdop'),(15,'classifier','modelobject'),(4,'contenttypes','contenttype'),(19,'notifications','modelnotification'),(20,'official_documents','modelofficialdocument'),(10,'script','modelownerline'),(11,'script','modelscript'),(5,'sessions','session'),(16,'webpush','group'),(17,'webpush','pushinformation'),(18,'webpush','subscriptioninfo');
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
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2021-04-16 09:22:18.033414'),(2,'contenttypes','0002_remove_content_type_name','2021-04-16 09:22:18.471231'),(3,'auth','0001_initial','2021-04-16 09:22:18.514971'),(4,'auth','0002_alter_permission_name_max_length','2021-04-16 09:22:18.623022'),(5,'auth','0003_alter_user_email_max_length','2021-04-16 09:22:18.627916'),(6,'auth','0004_alter_user_username_opts','2021-04-16 09:22:18.632945'),(7,'auth','0005_alter_user_last_login_null','2021-04-16 09:22:18.638923'),(8,'auth','0006_require_contenttypes_0002','2021-04-16 09:22:18.642937'),(9,'auth','0007_alter_validators_add_error_messages','2021-04-16 09:22:18.648847'),(10,'auth','0008_alter_user_username_max_length','2021-04-16 09:22:18.655045'),(11,'auth','0009_alter_user_last_name_max_length','2021-04-16 09:22:18.661505'),(12,'auth','0010_alter_group_name_max_length','2021-04-16 09:22:18.692224'),(13,'auth','0011_update_proxy_permissions','2021-04-16 09:22:18.699659'),(14,'auth','0012_alter_user_first_name_max_length','2021-04-16 09:22:18.705987'),(15,'authentication','0001_initial','2021-04-16 09:22:18.755041'),(16,'admin','0001_initial','2021-04-16 09:27:33.084976'),(17,'admin','0002_logentry_remove_auto_add','2021-04-16 09:27:33.137154'),(18,'admin','0003_logentry_add_action_flag_choices','2021-04-16 09:27:33.144234'),(19,'classifier','0001_initial','2021-04-16 09:27:33.151526'),(20,'script','0001_initial','2021-04-16 09:27:33.156991'),(21,'sessions','0001_initial','2021-04-16 09:27:33.174605'),(22,'webpush','0001_initial','2021-04-19 06:00:47.489369'),(23,'webpush','0002_auto_20190603_0005','2021-04-19 06:00:47.525894'),(24,'notifications','0001_initial','2021-04-21 13:56:04.327465'),(25,'official_documents','0001_initial','2021-04-21 13:56:04.333510'),(26,'script','0002_delete_modelownerline','2021-04-21 13:56:04.336857');
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('g094jzf4xldwl23853qdrio6cxli2bt5','.eJxVjMsOwiAUBf-FtSFCCty6dO83EO4DqRpISrtq_Hdt0oVuz8ycTcW0LiWuXeY4sbooo06_GyZ6St0BP1K9N02tLvOEelf0Qbu-NZbX9XD_Dkrq5VtbNtaMwGFAR5B48GwhoBfIbrAoYJzxRADikHPwTrJkGF0mFnsOXr0_5MQ4Wg:1lbeCC:nXNLZlHNEKg0CiJM1OFdzjL3si0N7ooWSJIHlj9g8YM','2021-05-12 07:01:16.105427');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `obj_case_row`
--

DROP TABLE IF EXISTS `obj_case_row`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `obj_case_row` (
  `id` int unsigned NOT NULL,
  `key_id` smallint unsigned NOT NULL,
  `val` varchar(255) NOT NULL,
  `dat` datetime DEFAULT NULL,
  KEY `ind_id` (`id`),
  KEY `ind_id_key` (`id`,`key_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=2048 ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `obj_case_row`
--

LOCK TABLES `obj_case_row` WRITE;
/*!40000 ALTER TABLE `obj_case_row` DISABLE KEYS */;
INSERT INTO `obj_case_row` VALUES (30,45502,'ДОУ',NULL),(30,45505,'Описание и только',NULL),(31,45502,'УД',NULL),(31,45505,'Описание 2',NULL),(32,45502,'АД',NULL),(32,45505,'Описание 3',NULL),(33,45502,'АД',NULL),(33,45505,'Описание 4',NULL);
/*!40000 ALTER TABLE `obj_case_row` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `obj_file_col`
--

DROP TABLE IF EXISTS `obj_file_col`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `obj_file_col` (
  `id` int unsigned NOT NULL,
  `type` tinyint unsigned DEFAULT NULL,
  `path` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;
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
  `id` int unsigned NOT NULL,
  `key_id` smallint unsigned NOT NULL,
  `val` varchar(255) NOT NULL,
  `dat` datetime DEFAULT NULL,
  KEY `ind_id` (`id`),
  KEY `ind_id_key` (`id`,`key_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;
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
  `id` int unsigned NOT NULL,
  `key_id` smallint unsigned NOT NULL,
  `val` varchar(255) NOT NULL,
  `dat` datetime DEFAULT NULL,
  KEY `ind_id` (`id`),
  KEY `ind_id_key` (`id`,`key_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=5461 ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `obj_free_row`
--

LOCK TABLES `obj_free_row` WRITE;
/*!40000 ALTER TABLE `obj_free_row` DISABLE KEYS */;
INSERT INTO `obj_free_row` VALUES (30,80,'val 1','2020-01-01 00:00:00'),(30,80,'val 2','2020-01-02 00:00:00'),(30,80,'val 3','2020-02-02 00:00:00');
/*!40000 ALTER TABLE `obj_free_row` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `obj_geometry_col`
--

DROP TABLE IF EXISTS `obj_geometry_col`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `obj_geometry_col` (
  `id` int unsigned NOT NULL,
  `parent_id` int unsigned NOT NULL DEFAULT '0',
  `name` varchar(25) NOT NULL,
  `icon` varchar(25) NOT NULL,
  `location` geomcollection DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=1260 ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `obj_geometry_col`
--

LOCK TABLES `obj_geometry_col` WRITE;
/*!40000 ALTER TABLE `obj_geometry_col` DISABLE KEYS */;
INSERT INTO `obj_geometry_col` VALUES (30,0,'Группа 0','fa-folder',NULL),(31,0,'Группа 1','fa-folder',NULL),(32,30,'Группа 11','fa-folder',NULL),(34,0,'','',_binary '\�\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\�\�\�\�\�<B@Zd;\�\�M@�G\�zDE@��\�\�M@fffff�F@=\nףp�N@\�\�\�\�\�<B@Zd;\�\�M@'),(36,0,'','',_binary '\�\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\�\�\�\�\�<B@Zd;\�\�M@�G\�zDE@��\�\�M@fffff�F@=\nףp�N@\�\�\�\�\�<B@Zd;\�\�M@'),(37,0,'','',_binary '\�\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\�\�\�\�\�<B@Zd;\�\�M@�G\�zDE@��\�\�M@fffff�F@=\nףp�N@\�\�\�\�\�<B@Zd;\�\�M@'),(38,0,'','',_binary '\�\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\�\�\�\�\�<B@Zd;\�\�M@�G\�zDE@��\�\�M@fffff�F@=\nףp�N@\�\�\�\�\�<B@Zd;\�\�M@'),(39,0,'','',_binary '\�\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\�\�\�\�\�<B@Zd;\�\�M@�G\�zDE@��\�\�M@fffff�F@=\nףp�N@\�\�\�\�\�<B@Zd;\�\�M@'),(40,0,'','',_binary '\�\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\�\�\�\�\�<B@Zd;\�\�M@�G\�zDE@��\�\�M@fffff�F@=\nףp�N@\�\�\�\�\�<B@Zd;\�\�M@'),(41,32,'Тест 41','fa-lock',_binary '\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\�\�\�\�\�<B@Zd;\�\�M@�G\�zDE@��\�\�M@fffff�F@=\nףp�N@\�\�\�\�\�<B@Zd;\�\�M@'),(42,30,'Тест 41','fa-lock',_binary '\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0�����y:@Zd;\�\�M@�G\�zD@@��\�\�M@fffff�A@=\nףp�N@�����y:@Zd;\�\�M@'),(46,0,'','',_binary '\�\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\�\�\�\�\�<B@Zd;\�\�M@�G\�zDE@��\�\�M@fffff�F@=\nףp�N@\�\�\�\�\�<B@Zd;\�\�M@'),(47,0,'','',_binary '\�\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\�\�\�\�\�<B@Zd;\�\�M@�G\�zDE@��\�\�M@fffff�F@=\nףp�N@\�\�\�\�\�<B@Zd;\�\�M@'),(48,0,'','',_binary '\�\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\�\�\�\�\�<B@Zd;\�\�M@�G\�zDE@��\�\�M@fffff�F@=\nףp�N@\�\�\�\�\�<B@Zd;\�\�M@'),(49,0,'','',_binary '\�\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\�\�\�\�\�<B@Zd;\�\�M@�G\�zDE@��\�\�M@fffff�F@=\nףp�N@\�\�\�\�\�<B@Zd;\�\�M@'),(50,0,'','',_binary '\�\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\�\�\�\�\�<B@Zd;\�\�M@�G\�zDE@��\�\�M@fffff�F@=\nףp�N@\�\�\�\�\�<B@Zd;\�\�M@'),(51,0,'Тест 51','fa-lock',_binary '\0\0\0\0\0\0\0\0\0\0\0\0\0zo�%:@�k\��K@\0\0\0\0\0\0\0\0\0C\�y�\�7@\�1 {��J@W\"P��8@\�\�C��J@�.�\�P8@\�/Ie��J@Q\�H�8@��\�8\�J@�x\��\�e8@�\�&N\�J@\�c[�-8@a\�N\"\��J@=��+�7@\�\�,z�\�J@�\'\���\�7@.V\�`\Z�J@/n���7@\�PoF\�J@r6܄7@֩\�=#�J@\�(]���7@\�\�߃\�\�J@	\���7@)\�ahu\�J@\�<�7@8\�\�J@C\�y�\�7@\�1 {��J@\0\0\0B\���\�8@�4Lk\�J@'),(52,0,'Тест 52','fa-lock',_binary '\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\�\��\�8@�,C\�K@B\���\�8@S�1�#K@\�\�A\�K9@\�GĔH\nK@8�L|9@)�k{\�J@\�1\0#9@\�\�\�\�\�J@\�\��\�8@�,C\�K@\0\0\0\0\0\0\0\0\0B\���0:@\n\�\�\�I�K@EGr�M;@\�U+~!L@�\��\�k=@���N�K@\��[\�k<@M�����K@�2\�\�\�;@��\�\�\�yK@B\���0:@\n\�\�\�I�K@\0\0\0	\0\0\0b->��9@�t�i��K@����OJ:@\�\�\�#L@\�;�_�:@�I��GL@\�C\0p:@\"�\Z�\Z�K@�\���?:@N�t\"}K@\�Xm�_9;@y\�[Y2K@b->�<@\�ފ\�K@�\�\�`�=@<���	JK@|\����?@x	N} [K@'),(53,0,'Тест 53','fa-lock',_binary '\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0�2\�\��8@\�L��TK@\��\"�\�9@\�l�\�psK@\0\0\0\0\0:@�\�Cl�XK@$c��\�9@_�;%K@�2\�\��8@\�L��TK@\0\0\0\0\0\0\0\0\0�2\�\��8@\�U+~!L@\�;�_�9@�\�\�\�L@g+/���:@d\�\�1\�K@�\�\�`+:@iE,b\�K@�2\�\��8@\�U+~!L@'),(54,0,'Тест 54','fa-lock',_binary '\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\�\��;@\�=\�4�J@kf-�\�;@\�Ry=\�J@Mjh�\�;@�\��\�q\�J@\�\�A\�g;@��\�\�\�\�J@/n��;@p��\�$\�J@R\�X�;;@dt@\��J@�\��\�.;@�\�\�K@\�\��;@\�=\�4�J@\0\0\0\0\0\0\�\�tp�:@�\\o��K@|\���;@R<��OK@�\��/\�;@ \�!pK@\�C\0p\�<@�\\o��K@zo�\�<@��M��J@\0\0\0\�_ �U:@ҋ\��*\0K@'),(55,0,'Тест 55','fa-lock',_binary '\0\0\0\0\0\0\0\0\0\0\0\0\0ܜJ�f9@1\�t��VJ@\0\0\0\0\0\0\�]�o9:@߇��(J@x\�\�3:@�|A	vJ@�7�\0\�0<@c	kc\�*J@\�yT�\�\�:@߇��(J@\0\0\0\0\0\0\0\0\0�\���?[9@\���o\�\�J@Mjh�%;@_�;%K@��~�Ϻ:@]T��J@�\���?[9@\���o\�\�J@'),(56,0,'Тест 56','fa-lock',_binary '\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0}\��8@P�}:5J@^gC��9@P�}:5J@^gC��9@Z-�\�DDJ@,\��\�8@NbX9>J@}\��8@Z-�\�DDJ@}\��8@P�}:5J@\0\0\0d�6���8@^�\�pJ@'),(57,0,'Тест 57','fa-lock',_binary '\0\0\0\0\0\0\0\0\0\0\0\0\0C\�y�[;@C\�ʠ\�JK@\0\0\0\0\0\0\0\0\0VW@\�:@\�\�\�\�K@\�_ �q<@A\��\���K@��P<@��\�1L@VW@\�:@\�\�\�\�K@'),(58,0,'Тест 58','fa-lock',_binary '\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0�\��8:@&qVDM0K@�e���!:@\�ahur�J@\�;�_�8@.rOW\�J@\�Xm�_9@��xx\�SK@|\���:@\�\�\�%\�mK@\0\0\0\0\0\0\0\0\0p\��/\�8@D���@	K@\�{c\0�9@t%\�?@K@F�xx\�9@% &\�BK@p\��/\�8@D���@	K@\0\0\0g+/���:@�$z\�\"K@');
/*!40000 ALTER TABLE `obj_geometry_col` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `obj_geometry_row`
--

DROP TABLE IF EXISTS `obj_geometry_row`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `obj_geometry_row` (
  `id` int unsigned NOT NULL,
  `key_id` smallint unsigned NOT NULL,
  `val` varchar(255) NOT NULL,
  `dat` datetime DEFAULT NULL,
  KEY `ind_id` (`id`),
  KEY `ind_id_key` (`id`,`key_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=1638 ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `obj_geometry_row`
--

LOCK TABLES `obj_geometry_row` WRITE;
/*!40000 ALTER TABLE `obj_geometry_row` DISABLE KEYS */;
INSERT INTO `obj_geometry_row` VALUES (41,81,'5',NULL),(42,81,'-1',NULL),(51,81,'0.05',NULL),(52,81,'50',NULL),(53,81,'-5',NULL),(54,81,'100',NULL),(55,81,'0',NULL),(56,81,'20',NULL),(57,81,'-3',NULL),(58,81,'4',NULL);
/*!40000 ALTER TABLE `obj_geometry_row` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `obj_person_p_row`
--

DROP TABLE IF EXISTS `obj_person_p_row`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `obj_person_p_row` (
  `id` int unsigned NOT NULL,
  `key_id` smallint unsigned NOT NULL,
  `val` varchar(255) NOT NULL,
  `dat` datetime DEFAULT NULL,
  KEY `ind_id` (`id`),
  KEY `ind_id_key` (`id`,`key_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;
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
  `id` int unsigned NOT NULL,
  `lat` double DEFAULT NULL,
  `lon` double DEFAULT NULL,
  `address` tinytext COMMENT 'адрес',
  PRIMARY KEY (`id`),
  KEY `IDX_id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=2520 ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `obj_point_col`
--

LOCK TABLES `obj_point_col` WRITE;
/*!40000 ALTER TABLE `obj_point_col` DISABLE KEYS */;
INSERT INTO `obj_point_col` VALUES (33,52.0839356,23.650415,'Брест, ул.Русакова,124'),(34,54.4773572,26.3932509,'Сморгонь, ул.Белинского,124'),(35,55.4798043,28.7796702,'Полоцк, ул.Софии Полоцкой, 3'),(36,53.8870722,27.962096,'Самолеты Минск'),(37,53.2628595,23.8672983,'Нижний Новгород, 40 лет Победы ул., 7'),(38,53.2255994,23.8739022,'Нижний Новгород, 60-летия Октября б-р, 2а, САЮС'),(39,53.2241874,23.8191839,'Нижний Новгород, Агрономов ул, 77'),(40,53.2490319,24.0470196,'Нижний Новгород, Адмирала Макарова ул., 16-40'),(41,52.8521343,23.9992328,'Нижний Новгород, Акимова ул., 50'),(42,52.8345252,23.9736483,'Нижний Новгород, Алексеевская ул., 1'),(43,52.8685392,24.1087106,'Нижний Новгород, Алексеевская ул., 6/16'),(44,53.9232459,24.466538,'Нижний Новгород, Алексеевская ул., 8а1'),(45,53.7653914,24.3036483,'Нижний Новгород, Анкудиновское ш, 184'),(46,53.3524766,24.7062152,'Нижний Новгород, Анкудиновское ш, 3а'),(47,54.8527277,27.0920334,'Нижний Новгород, Анкудиновское ш, 85'),(48,55.5022909,27.939888,'Нижний Новгород, Аральская ул., 23'),(49,54.7061863,30.5381097,'Нижний Новгород, Артельная ул., 3'),(50,53.7793249,30.3136429,'Нижний Новгород, Артемовская ул., 30'),(51,52.3222736,30.2990905,'Нижний Новгород, Аэропорт ул., 1'),(52,52.3162907,28.5324098,'Нижний Новгород, Б. Корнилова ул., 5/1'),(53,52.3969908,28.3072926,'Нижний Новгород, Б. Корнилова ул., 6/1'),(54,53.6174398,27.9788652,'<strong>НГГ</strong><br />ушел и не поймали'),(55,53.4621,26.9469,'Тест 1'),(56,53.4506,26.8133,'Тест 2'),(57,53.4718,26.6726,'Тест 3'),(58,53.5038,26.9488,'Тест 4');
/*!40000 ALTER TABLE `obj_point_col` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `obj_point_row`
--

DROP TABLE IF EXISTS `obj_point_row`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `obj_point_row` (
  `id` int unsigned NOT NULL,
  `key_id` smallint unsigned NOT NULL,
  `val` varchar(255) NOT NULL,
  `dat` datetime DEFAULT NULL,
  KEY `ind_id` (`id`),
  KEY `ind_id_key` (`id`,`key_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `obj_point_row`
--

LOCK TABLES `obj_point_row` WRITE;
/*!40000 ALTER TABLE `obj_point_row` DISABLE KEYS */;
/*!40000 ALTER TABLE `obj_point_row` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `obj_transport_row`
--

DROP TABLE IF EXISTS `obj_transport_row`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `obj_transport_row` (
  `id` int unsigned NOT NULL,
  `key_id` smallint unsigned NOT NULL,
  `val` varchar(255) NOT NULL,
  `dat` datetime DEFAULT NULL,
  KEY `ind_id` (`id`),
  KEY `ind_id_key` (`id`,`key_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=364 ROW_FORMAT=DYNAMIC;
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=4096 ROW_FORMAT=DYNAMIC;
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=1489 ROW_FORMAT=DYNAMIC;
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
  `key_id` smallint unsigned NOT NULL,
  `dat` datetime DEFAULT NULL,
  `obj_id_1` tinyint unsigned NOT NULL,
  `rec_id_1` int unsigned NOT NULL,
  `obj_id_2` tinyint unsigned NOT NULL,
  `rec_id_2` int unsigned NOT NULL,
  KEY `ind_key_id` (`key_id`),
  KEY `ind_obj_1` (`obj_id_1`),
  KEY `ind_obj_2` (`obj_id_2`),
  KEY `ind_obj_rec_1` (`obj_id_1`,`rec_id_1`),
  KEY `ind_obj_rec_2` (`obj_id_2`,`rec_id_2`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=4096 ROW_FORMAT=DYNAMIC
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
INSERT INTO `rel` VALUES (32,NULL,25,38,45,30),(32,NULL,25,39,45,33),(32,NULL,25,40,45,32),(32,NULL,25,41,45,32),(32,NULL,25,42,45,32),(33,'2020-04-15 00:00:00',25,33,45,33),(33,'2020-05-04 00:00:00',25,34,45,30),(33,'2020-01-23 00:00:00',25,35,45,31),(33,'2020-06-03 00:00:00',25,36,45,33),(33,'2020-07-03 00:00:00',25,37,45,31),(32,'2020-01-07 00:00:00',25,43,45,30),(34,'2020-01-08 00:00:00',25,44,45,31),(34,'2020-01-08 00:00:00',25,45,45,33),(34,'2020-04-10 00:00:00',25,46,45,31),(34,'2020-01-10 00:00:00',25,47,45,30),(34,'2020-01-10 00:00:00',25,48,45,31),(35,'2020-02-21 00:00:00',25,49,45,32),(35,'2020-05-12 00:00:00',25,50,45,33),(35,'2020-01-13 00:00:00',25,51,45,30),(35,'2020-01-23 00:00:00',25,52,45,33),(35,'2020-07-13 00:00:00',25,53,45,30),(36,'2020-02-14 00:00:00',25,54,45,31),(36,'2020-01-14 00:00:00',25,55,45,32),(36,'2020-03-14 00:00:00',25,56,45,33),(36,'0000-00-00 00:00:00',25,57,45,32),(36,'2020-01-14 00:00:00',25,58,45,31),(41,'2020-05-01 00:00:00',30,42,45,31),(41,'2020-05-05 00:00:00',30,52,45,31),(41,'2020-05-06 00:00:00',30,53,45,31),(41,'2020-05-07 00:00:00',30,54,45,33),(41,'2020-05-01 00:00:00',30,55,45,33),(42,'2020-05-02 00:00:00',30,55,45,31),(42,'2020-05-08 00:00:00',30,56,45,31),(42,'2020-05-09 00:00:00',30,57,45,32),(42,'2020-05-02 00:00:00',30,58,45,33),(43,'2020-05-03 00:00:00',30,52,45,31),(43,'2020-05-04 00:00:00',30,56,45,32),(31,NULL,15,200,30,100),(35,NULL,25,45,45,398),(506,NULL,30,74,50,12);
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
  CONSTRAINT `sys_id__sys_obj` FOREIGN KEY (`obj_id`) REFERENCES `sys_obj` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=1820 ROW_FORMAT=DYNAMIC COMMENT='Счетчик id объектов';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_id`
--

LOCK TABLES `sys_id` WRITE;
/*!40000 ALTER TABLE `sys_id` DISABLE KEYS */;
INSERT INTO `sys_id` VALUES (10,32),(15,6),(20,0),(25,1),(30,51),(35,0),(40,0),(45,1),(50,1);
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
  `type_val` enum('number','text','datetime','date','checkbox','geometry') CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT 'text' COMMENT 'тип данных',
  `list_id` mediumint unsigned DEFAULT NULL,
  `name` varchar(25) DEFAULT NULL,
  `title` varchar(50) NOT NULL,
  `hint` varchar(255) DEFAULT NULL COMMENT 'отображаемая подсказка',
  `descript` varchar(255) DEFAULT NULL,
  `rel_obj_1_id` tinyint unsigned DEFAULT NULL,
  `rel_obj_2_id` tinyint unsigned DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ind_id` (`id`),
  KEY `ind_id_name` (`obj_id`,`name`),
  KEY `ind_list` (`list_id`),
  KEY `ind_rel_obj_1` (`rel_obj_1_id`),
  KEY `ind_rel_obj_2` (`rel_obj_2_id`),
  CONSTRAINT `ind_list` FOREIGN KEY (`list_id`) REFERENCES `sys_list_top` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `ind_obj` FOREIGN KEY (`obj_id`) REFERENCES `sys_obj` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `ind_rel_obj_1` FOREIGN KEY (`rel_obj_1_id`) REFERENCES `sys_obj` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `ind_rel_obj_2` FOREIGN KEY (`rel_obj_2_id`) REFERENCES `sys_obj` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=50019 DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=2048 ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_key`
--

LOCK TABLES `sys_key` WRITE;
/*!40000 ALTER TABLE `sys_key` DISABLE KEYS */;
INSERT INTO `sys_key` VALUES (31,1,0,0,'text',NULL,'photo_panorama','photo_panorama',NULL,NULL,NULL,NULL),(32,1,0,0,'text',NULL,'ngg_smoke','ngg_smoke',NULL,NULL,NULL,NULL),(33,1,0,0,'text',NULL,'ngg_migrate','ngg_migrate',NULL,NULL,NULL,NULL),(34,1,0,0,'text',NULL,'ngg_tmc','ngg_tmc',NULL,NULL,NULL,NULL),(35,1,0,0,'text',NULL,'ngg_opg','ngg_opg',NULL,NULL,NULL,NULL),(36,1,0,0,'text',NULL,'ngg_npr','ngg_npr',NULL,NULL,NULL,NULL),(41,1,0,0,'text',NULL,'arial_1','arial_1',NULL,NULL,NULL,NULL),(42,1,0,0,'text',NULL,'arial_2','arial_2',NULL,NULL,NULL,NULL),(43,1,0,0,'text',NULL,'arial_3','arial_3',NULL,NULL,NULL,NULL),(80,10,0,0,'text',NULL,'test_free_30','test_free_30',NULL,NULL,NULL,NULL),(81,30,0,0,'text',NULL,'test_geo_color','test_geo_color',NULL,NULL,NULL,NULL),(501,1,0,0,'text',NULL,NULL,'Дело/объединение',NULL,NULL,45,NULL),(502,1,0,0,'text',NULL,NULL,'Дело/выделение',NULL,NULL,45,NULL),(506,1,0,0,'text',NULL,NULL,'Дело/принятие к производству',NULL,NULL,45,35),(1001,1,0,0,'text',NULL,NULL,'ДОУ/оперативная категория лица/организатор',NULL,NULL,35,45),(1002,1,0,0,'text',NULL,NULL,'ДОУ/оперативная категория лица/исполнитель',NULL,NULL,35,45),(1003,1,0,0,'text',NULL,NULL,'ДОУ/оперативная категория лица/пособник',NULL,NULL,35,45),(1101,1,0,0,'text',NULL,NULL,'Задержание (КоАП)/начало',NULL,NULL,35,45),(1102,1,0,0,'text',NULL,NULL,'Задержание (УПК)/начало',NULL,NULL,35,45),(1201,1,0,0,'text',NULL,NULL,'Авто ФЛ/владение/начало',NULL,NULL,35,50),(1202,1,0,0,'text',NULL,NULL,'Авто ФЛ/владение/конец',NULL,NULL,35,50),(1301,1,0,0,'text',NULL,NULL,'Учеба/поступление',NULL,NULL,35,40),(1302,1,0,0,'text',NULL,NULL,'Учеба/отчисление',NULL,NULL,35,40),(1303,1,0,0,'text',NULL,NULL,'Учеба/завершение',NULL,NULL,35,40),(1304,1,0,1,'text',NULL,NULL,'Работа/начало',NULL,NULL,35,40),(1305,1,0,0,'text',NULL,NULL,'Работа/конец',NULL,NULL,35,40),(1306,1,0,0,'text',NULL,NULL,'Отпуск/начало',NULL,NULL,35,40),(1307,1,0,0,'text',NULL,NULL,'Отпуск/конец',NULL,NULL,35,40),(10000,10,0,0,'text',NULL,'owner_add_rw','Владелец: добавить чтение/запись',NULL,'! СПЕЦИАЛЬНЫЙ КЛЮЧ !',NULL,NULL),(10001,10,0,0,'text',NULL,'owner_add_ro','Владелец: добавить только чтение',NULL,'! СПЕЦИАЛЬНЫЙ КЛЮЧ !',NULL,NULL),(10002,10,0,0,'text',NULL,'owner_add_ro_limit','Владелец: добавить только чтение на период',NULL,'! СПЕЦИАЛЬНЫЙ КЛЮЧ !',NULL,NULL),(10003,10,0,0,'text',NULL,'owner_del','Владелец: запретить доступ',NULL,'! СПЕЦИАЛЬНЫЙ КЛЮЧ !',NULL,NULL),(10010,10,0,0,'text',NULL,'test_free_30','test_free_30',NULL,NULL,NULL,NULL),(15000,15,0,1,'text',NULL,'owner_add_rw','Владелец: добавить чтение/запись',NULL,'! СПЕЦИАЛЬНЫЙ КЛЮЧ !',NULL,NULL),(15001,15,0,0,'text',NULL,'owner_add_ro','Владелец: добавить только чтение',NULL,'! СПЕЦИАЛЬНЫЙ КЛЮЧ !',NULL,NULL),(15002,15,0,0,'text',NULL,'owner_add_ro_limit','Владелец: добавить только чтение на период',NULL,'! СПЕЦИАЛЬНЫЙ КЛЮЧ !',NULL,NULL),(15003,15,0,0,'text',NULL,'owner_del','Владелец: запретить доступ',NULL,'! СПЕЦИАЛЬНЫЙ КЛЮЧ !',NULL,NULL),(15010,15,1,1,'text',NULL,'type','Тип',NULL,NULL,NULL,NULL),(15011,15,1,1,'text',NULL,'path','Путь',NULL,NULL,NULL,NULL),(25202,25,1,0,'text',NULL,'lat','Широта',NULL,NULL,NULL,NULL),(25203,25,1,0,'text',NULL,'lon','Долгота',NULL,NULL,NULL,NULL),(25204,25,1,0,'text',NULL,'address','Адрес',NULL,NULL,NULL,NULL),(30301,30,1,0,'text',NULL,'icon','Иконка',NULL,NULL,NULL,NULL),(30302,30,1,0,'text',NULL,'parent_id','Группа',NULL,NULL,NULL,NULL),(30303,30,1,0,'text',NULL,'name','Название',NULL,NULL,NULL,NULL),(30304,30,1,0,'geometry',NULL,'location','Локация',NULL,NULL,NULL,NULL),(35001,35,1,1,'text',NULL,'fio','ФИО','Фамилия, имя, отчество',NULL,NULL,NULL),(35002,35,1,0,'text',NULL,'birth_day','Дата рождения',NULL,NULL,NULL,NULL),(35003,35,1,0,'text',2,'sex','Пол',NULL,NULL,NULL,NULL),(35004,35,1,1,'text',1,'citizenship','Гражданство',NULL,NULL,NULL,NULL),(35005,35,1,0,'text',19,'nationality','Национальность',NULL,NULL,NULL,NULL),(35006,35,0,0,'text',NULL,'photo ??????','Фото лица',NULL,'В свзяь',NULL,NULL),(35007,35,1,0,'text',NULL,'birth_place','Место рождения',NULL,NULL,NULL,NULL),(35008,35,0,0,'text',NULL,'residence','Место жительства',NULL,'В свзяь',NULL,NULL),(35009,35,0,0,'text',NULL,'work????','Место работы',NULL,'В свзяь',NULL,NULL),(35010,35,0,0,'text',NULL,'ident_doc','ID-документ',NULL,NULL,NULL,NULL),(35011,35,0,0,'text',NULL,'migrant','Незаконный мигрант',NULL,'В свзяь',NULL,NULL),(35012,35,0,0,'text',NULL,'fio_dop','ФИО доп',NULL,NULL,NULL,NULL),(35013,35,0,0,'text',NULL,'status_social','Социальное положение',NULL,NULL,NULL,NULL),(35014,35,0,0,'text',NULL,'status_marital','Семейное положение',NULL,'словарь',NULL,NULL),(35015,35,1,0,'text',3,'education','Образование',NULL,NULL,NULL,NULL),(35016,35,0,0,'text',NULL,'public_association','Принадлежность к партиям',NULL,NULL,NULL,NULL),(35017,35,0,0,'text',NULL,'language_skills','Знание иностранных языков',NULL,'словарь',NULL,NULL),(35020,35,0,0,'text',NULL,'conviction????','Судимость',NULL,'словарь',NULL,NULL),(35021,35,0,0,'text',NULL,'alias','Псевдоним (кличка)',NULL,NULL,NULL,NULL),(35022,35,0,0,'text',NULL,'special_signs','Особые приметы',NULL,NULL,NULL,NULL),(35023,35,0,0,'text',NULL,NULL,'ОПС: подразделение',NULL,NULL,NULL,NULL),(35997,35,0,0,'text',NULL,'position','ОПС/Должность','Только для сотрудников ОПС','словарь+ушел',NULL,NULL),(35998,35,0,0,'text',NULL,NULL,'ОПС/Структурное подразделение',NULL,'словарь+ушел',NULL,NULL),(35999,35,0,0,'text',NULL,'rank','ОПС/Воинское звание',NULL,'словарь',NULL,NULL),(40101,40,1,1,'text',NULL,'name','Название полное',NULL,NULL,NULL,NULL),(40102,40,0,0,'text',NULL,'address','Юридический адрес ',NULL,NULL,NULL,NULL),(40103,40,0,0,'text',NULL,'name_dop','Название доп',NULL,NULL,NULL,NULL),(40104,40,0,0,'text',NULL,'type','Вид',NULL,NULL,NULL,NULL),(40105,40,0,0,'text',NULL,'ownership','Форма собственности',NULL,'словарь',NULL,NULL),(40106,40,0,0,'text',NULL,'activity','Род деятельности',NULL,NULL,NULL,NULL),(40107,40,0,0,'text',NULL,'descript','Оперативная характеристика организации',NULL,NULL,NULL,NULL),(40108,40,0,0,'text',NULL,'representation','Представительство',NULL,NULL,NULL,NULL),(40109,40,0,0,'text',NULL,'representation????','Адрес представительства',NULL,'????',NULL,NULL),(40110,40,0,0,'text',NULL,'telephone ????','Телефон',NULL,'????? связь',NULL,NULL),(40111,40,0,0,'text',NULL,'transport','Транспорт',NULL,'???? связь',NULL,NULL),(40112,40,0,0,'text',NULL,'source_information','Источник сведений',NULL,'словарь ???? удалить',NULL,NULL),(40113,40,0,0,'text',NULL,NULL,'Учебное заведение гражданское',NULL,NULL,NULL,NULL),(40114,40,0,0,'text',NULL,NULL,'Учебное заведение военное',NULL,NULL,NULL,NULL),(45000,45,0,0,'text',NULL,'owner_add_rw','Владелец: добавить чтение/запись',NULL,'! СПЕЦИАЛЬНЫЙ КЛЮЧ !',NULL,NULL),(45001,45,0,0,'text',NULL,'owner_add_ro','Владелец: добавить только чтение',NULL,'! СПЕЦИАЛЬНЫЙ КЛЮЧ !',NULL,NULL),(45002,45,0,0,'text',NULL,'owner_add_ro_limit','Владелец: добавить только чтение на период',NULL,'! СПЕЦИАЛЬНЫЙ КЛЮЧ !',NULL,NULL),(45003,45,0,0,'text',NULL,'owner_del','Владелец: запретить доступ',NULL,'! СПЕЦИАЛЬНЫЙ КЛЮЧ !',NULL,NULL),(45501,45,0,1,'text',NULL,'type','Вид дела',NULL,'словарь ДОУ+УД+АД',NULL,NULL),(45502,45,0,0,'text',NULL,NULL,'Статья/начало',NULL,'словарь, сделать словарь окраски и линии',NULL,NULL),(45503,45,0,0,'text',NULL,NULL,'Статья/конец',NULL,'словарь',NULL,NULL),(45505,45,0,0,'text',NULL,NULL,'Описание',NULL,'Номер, архивный номер, описание, суть материалов, пометки',NULL,NULL),(45515,45,0,1,'text',NULL,NULL,'Уничтожено',NULL,'? в описание',NULL,NULL),(45520,45,0,0,'text',NULL,NULL,'Движение/заведение (возбуждение)',NULL,NULL,45,NULL),(45521,45,0,0,'text',NULL,NULL,'Движение/продление',NULL,NULL,45,NULL),(45522,45,0,0,'text',NULL,NULL,'Движение/приостановление',NULL,NULL,45,NULL),(45523,45,0,0,'text',NULL,NULL,'Движение/возобновление',NULL,NULL,45,NULL),(45524,45,0,0,'text',NULL,NULL,'Движение/прекращение',NULL,'???',45,NULL),(45525,45,0,0,'text',NULL,NULL,'Движение/прекращение основание',NULL,NULL,45,NULL),(50001,50,1,1,'text',NULL,'brand','Марка',NULL,NULL,NULL,NULL),(50002,50,1,0,'text',NULL,'model','Модель',NULL,NULL,NULL,NULL),(50004,50,1,0,'text',NULL,'type','Вид транспорта',NULL,'словарь',NULL,NULL),(50005,50,1,0,'text',NULL,'number','Рег.номер',NULL,NULL,NULL,NULL),(50006,50,1,0,'text',NULL,'category','Категория транспорта',NULL,'словарь',NULL,NULL),(50007,50,0,0,'text',NULL,'money','Сумма оценки',NULL,'?????',NULL,NULL),(50008,50,1,0,'text',NULL,'country','Страна',NULL,'словарь',NULL,NULL),(50009,50,0,0,'text',NULL,'photo????','Фото автомобиля',NULL,'В свзяь',NULL,NULL),(50010,50,1,0,'text',NULL,'vin','VIN',NULL,NULL,NULL,NULL),(50011,50,1,0,'text',NULL,'manufacture','Год выпуска',NULL,'словарь',NULL,NULL),(50012,50,0,0,'text',NULL,'route???','Номер поезда, рейса самолета, автобуса',NULL,'????',NULL,NULL),(50013,50,0,0,'text',NULL,'route','Маршрут поезда, самолета, автобуса',NULL,'словарь',NULL,NULL),(50014,50,0,0,'text',NULL,'number_carriage','Номер вагона',NULL,NULL,NULL,NULL),(50015,50,0,0,'text',NULL,'color','Цвет',NULL,NULL,NULL,NULL),(50016,50,0,0,'text',NULL,'measures ????','Принятые меры',NULL,'словарь, ???????',NULL,NULL),(50018,1,1,0,'geometry',NULL,'border_guard_fail','незаконный переход границы','где нарушили границу','-',45,35);
/*!40000 ALTER TABLE `sys_key` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sys_list_dop`
--

DROP TABLE IF EXISTS `sys_list_dop`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sys_list_dop` (
  `key_id` mediumint unsigned NOT NULL,
  `val` varchar(255) NOT NULL,
  `dat_from` date DEFAULT NULL,
  `dat_to` date DEFAULT NULL,
  `id` int NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`),
  KEY `ind_id` (`key_id`),
  CONSTRAINT `ind_id_id` FOREIGN KEY (`key_id`) REFERENCES `sys_list_top` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=456 DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=117 ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_list_dop`
--

LOCK TABLES `sys_list_dop` WRITE;
/*!40000 ALTER TABLE `sys_list_dop` DISABLE KEYS */;
INSERT INTO `sys_list_dop` VALUES (1,'Австралия',NULL,NULL,1),(1,'Австрия',NULL,NULL,2),(1,'Азербайджан',NULL,NULL,3),(1,'Аландские острова',NULL,NULL,4),(1,'Албания',NULL,NULL,5),(1,'Алжир',NULL,NULL,6),(1,'Американское Самоа',NULL,NULL,7),(1,'Ангилья',NULL,NULL,8),(1,'Ангола',NULL,NULL,9),(1,'Андорра',NULL,NULL,10),(1,'Антигуа и Барбуда',NULL,NULL,11),(1,'Аргентина',NULL,NULL,12),(1,'Армения',NULL,NULL,13),(1,'Аруба',NULL,NULL,14),(1,'Афганистан',NULL,NULL,15),(1,'Багамы',NULL,NULL,16),(1,'Бангладеш',NULL,NULL,17),(1,'Барбадос',NULL,NULL,18),(1,'Бахрейн',NULL,NULL,19),(1,'Беларусь',NULL,NULL,20),(1,'Белиз',NULL,NULL,21),(1,'Бельгия',NULL,NULL,22),(1,'Бенин',NULL,NULL,23),(1,'Бермуды',NULL,NULL,24),(1,'Болгария',NULL,NULL,25),(1,'Боливия, Многонациональное Государство ',NULL,NULL,26),(1,'Бонэйр, Синт-Эстатиус и Саба',NULL,NULL,27),(1,'Босния и Герцеговина',NULL,NULL,28),(1,'Ботсвана',NULL,NULL,29),(1,'Бразилия',NULL,NULL,30),(1,'Бруней-Даруссалам',NULL,NULL,31),(1,'Буркина-Фасо',NULL,NULL,32),(1,'Бурунди',NULL,NULL,33),(1,'Бутан',NULL,NULL,34),(1,'Вануату',NULL,NULL,35),(1,'Венгрия',NULL,NULL,36),(1,'Венесуэла, Боливарианская Республика ',NULL,NULL,37),(1,'Виргинские Острова, Британские',NULL,NULL,38),(1,'Виргинские Острова, США',NULL,NULL,39),(1,'Вьетнам',NULL,NULL,40),(1,'Габон',NULL,NULL,41),(1,'Гаити',NULL,NULL,42),(1,'Гайана',NULL,NULL,43),(1,'Гамбия',NULL,NULL,44),(1,'Гана',NULL,NULL,45),(1,'Гваделупа',NULL,NULL,46),(1,'Гватемала',NULL,NULL,47),(1,'Гвинея',NULL,NULL,48),(1,'Гвинея-Бисау',NULL,NULL,49),(1,'Германия',NULL,NULL,50),(1,'Гернси',NULL,NULL,51),(1,'Гибралтар',NULL,NULL,52),(1,'Гондурас',NULL,NULL,53),(1,'Гонконг',NULL,NULL,54),(1,'Гренада',NULL,NULL,55),(1,'Гренландия',NULL,NULL,56),(1,'Греция',NULL,NULL,57),(1,'Грузия',NULL,NULL,58),(1,'Гуам',NULL,NULL,59),(1,'Дания',NULL,NULL,60),(1,'Джерси',NULL,NULL,61),(1,'Джибути',NULL,NULL,62),(1,'Доминика',NULL,NULL,63),(1,'Доминиканская Республика',NULL,NULL,64),(1,'Египет',NULL,NULL,65),(1,'Замбия',NULL,NULL,66),(1,'Западная Сахара',NULL,NULL,67),(1,'Зимбабве',NULL,NULL,68),(1,'Израиль',NULL,NULL,69),(1,'Индия',NULL,NULL,70),(1,'Индонезия',NULL,NULL,71),(1,'Иордания',NULL,NULL,72),(1,'Ирак',NULL,NULL,73),(1,'Иран, Исламская Республика ',NULL,NULL,74),(1,'Ирландия',NULL,NULL,75),(1,'Исландия',NULL,NULL,76),(1,'Испания',NULL,NULL,77),(1,'Италия',NULL,NULL,78),(1,'Йемен',NULL,NULL,79),(1,'Кабо-Верде',NULL,NULL,80),(1,'Казахстан',NULL,NULL,81),(1,'Камбоджа',NULL,NULL,82),(1,'Камерун',NULL,NULL,83),(1,'Канада',NULL,NULL,84),(1,'Катар',NULL,NULL,85),(1,'Кения',NULL,NULL,86),(1,'Кипр',NULL,NULL,87),(1,'Кирибати',NULL,NULL,88),(1,'Китай',NULL,NULL,89),(1,'Кокосовые (Килинг) острова',NULL,NULL,90),(1,'Колумбия',NULL,NULL,91),(1,'Коморы',NULL,NULL,92),(1,'Конго',NULL,NULL,93),(1,'Конго, Демократическая Республика',NULL,NULL,94),(1,'Корея, Народно-Демократическая Республика',NULL,NULL,95),(1,'Корея, Республика',NULL,NULL,96),(1,'Коста-Рика',NULL,NULL,97),(1,'Кот-д’Ивуар',NULL,NULL,98),(1,'Куба',NULL,NULL,99),(1,'Кувейт',NULL,NULL,100),(1,'Кыргызстан',NULL,NULL,101),(1,'Кюрасао',NULL,NULL,102),(1,'Лаосская Народно-Демократическая Республика',NULL,NULL,103),(1,'Латвия',NULL,NULL,104),(1,'Лесото',NULL,NULL,105),(1,'Либерия',NULL,NULL,106),(1,'Ливан',NULL,NULL,107),(1,'Ливия',NULL,NULL,108),(1,'Литва',NULL,NULL,109),(1,'Лихтенштейн',NULL,NULL,110),(1,'Люксембург',NULL,NULL,111),(1,'Маврикий',NULL,NULL,112),(1,'Мавритания',NULL,NULL,113),(1,'Мадагаскар',NULL,NULL,114),(1,'Майотта',NULL,NULL,115),(1,'Макао',NULL,NULL,116),(1,'Малави',NULL,NULL,117),(1,'Малайзия',NULL,NULL,118),(1,'Мали',NULL,NULL,119),(1,'Мальдивы',NULL,NULL,120),(1,'Мальта',NULL,NULL,121),(1,'Марокко',NULL,NULL,122),(1,'Мартиника',NULL,NULL,123),(1,'Маршалловы Острова',NULL,NULL,124),(1,'Мексика',NULL,NULL,125),(1,'Микронезия, Федеративные Штаты',NULL,NULL,126),(1,'Мозамбик',NULL,NULL,127),(1,'Молдова',NULL,NULL,128),(1,'Монако',NULL,NULL,129),(1,'Монголия',NULL,NULL,130),(1,'Монтсеррат',NULL,NULL,131),(1,'Мьянма',NULL,NULL,132),(1,'Намибия',NULL,NULL,133),(1,'Науру',NULL,NULL,134),(1,'Непал',NULL,NULL,135),(1,'Нигер',NULL,NULL,136),(1,'Нигерия',NULL,NULL,137),(1,'Нидерланды',NULL,NULL,138),(1,'Никарагуа',NULL,NULL,139),(1,'Ниуэ',NULL,NULL,140),(1,'Новая Зеландия',NULL,NULL,141),(1,'Новая Каледония',NULL,NULL,142),(1,'Норвегия',NULL,NULL,143),(1,'Объединенные Арабские Эмираты',NULL,NULL,144),(1,'Оман',NULL,NULL,145),(1,'Остров Мэн',NULL,NULL,146),(1,'Остров Норфолк',NULL,NULL,147),(1,'Остров Рождества',NULL,NULL,148),(1,'Острова Кайман',NULL,NULL,149),(1,'Острова Кука',NULL,NULL,150),(1,'Острова Теркс И Кайкос',NULL,NULL,151),(1,'Пакистан',NULL,NULL,152),(1,'Палау',NULL,NULL,153),(1,'Палестина, государство',NULL,NULL,154),(1,'Панама',NULL,NULL,155),(1,'Папский престол',NULL,NULL,156),(1,'Папуа – Новая Гвинея',NULL,NULL,157),(1,'Парагвай',NULL,NULL,158),(1,'Перу',NULL,NULL,159),(1,'Питкэрн',NULL,NULL,160),(1,'Польша',NULL,NULL,161),(1,'Португалия',NULL,NULL,162),(1,'Пуэрто-Рико',NULL,NULL,163),(1,'Республика Беларусь',NULL,NULL,164),(1,'Реюньон',NULL,NULL,165),(1,'Российская Федерация',NULL,NULL,166),(1,'Руанда',NULL,NULL,167),(1,'Румыния',NULL,NULL,168),(1,'Самоа',NULL,NULL,169),(1,'Сан-Марино',NULL,NULL,170),(1,'Сан-Томе и Принсипи',NULL,NULL,171),(1,'Саудовская Аравия',NULL,NULL,172),(1,'Северная Македония',NULL,NULL,173),(1,'Северные Марианские Острова',NULL,NULL,174),(1,'Сейшелы',NULL,NULL,175),(1,'Сен Бартелеми',NULL,NULL,176),(1,'Сен Мартин (французская часть)',NULL,NULL,177),(1,'Сен-Мартен (Нидерландская часть)',NULL,NULL,178),(1,'Сен-Пьер и Микелон',NULL,NULL,179),(1,'Сенегал',NULL,NULL,180),(1,'Сент-Винсент и Гренадины',NULL,NULL,181),(1,'Сент-Китс и Невис',NULL,NULL,182),(1,'Сент-Люсия',NULL,NULL,183),(1,'Сербия',NULL,NULL,184),(1,'Сингапур',NULL,NULL,185),(1,'Сирийская Арабская Республика',NULL,NULL,186),(1,'Словакия',NULL,NULL,187),(1,'Словения',NULL,NULL,188),(1,'Соединенное Королевство Великобритании и Северной Ирландии',NULL,NULL,189),(1,'Соединенные Штаты Америки',NULL,NULL,190),(1,'Соломоновы острова',NULL,NULL,191),(1,'Сомали',NULL,NULL,192),(1,'Судан',NULL,NULL,193),(1,'Суринам',NULL,NULL,194),(1,'Сьерра-Леоне',NULL,NULL,195),(1,'Таджикистан',NULL,NULL,196),(1,'Таиланд',NULL,NULL,197),(1,'Тайвань (Китай)',NULL,NULL,198),(1,'Танзания, Объединенная Республика ',NULL,NULL,199),(1,'Тимор-Лесте',NULL,NULL,200),(1,'Того',NULL,NULL,201),(1,'Токелау',NULL,NULL,202),(1,'Тонга',NULL,NULL,203),(1,'Тринидад и Тобаго',NULL,NULL,204),(1,'Тувалу',NULL,NULL,205),(1,'Тунис',NULL,NULL,206),(1,'Туркменистан',NULL,NULL,207),(1,'Турция',NULL,NULL,208),(1,'Уганда',NULL,NULL,209),(1,'Узбекистан',NULL,NULL,210),(1,'Украина',NULL,NULL,211),(1,'Уоллис и Футуна',NULL,NULL,212),(1,'Уругвай',NULL,NULL,213),(1,'Фарерские острова',NULL,NULL,214),(1,'Фиджи',NULL,NULL,215),(1,'Филиппины',NULL,NULL,216),(1,'Финляндия',NULL,NULL,217),(1,'Фолклендские острова (Мальвинские)',NULL,NULL,218),(1,'Франция',NULL,NULL,219),(1,'Французская Гвиана',NULL,NULL,220),(1,'Французская Полинезия',NULL,NULL,221),(1,'Хорватия',NULL,NULL,222),(1,'Центрально-африканская Республика',NULL,NULL,223),(1,'Чад',NULL,NULL,224),(1,'Черногория',NULL,NULL,225),(1,'Чехия',NULL,NULL,226),(1,'Чили',NULL,NULL,227),(1,'Швейцария',NULL,NULL,228),(1,'Швеция',NULL,NULL,229),(1,'Шпицберген и Ян-Майен',NULL,NULL,230),(1,'Шри-Ланка',NULL,NULL,231),(1,'Эквадор',NULL,NULL,232),(1,'Экваториальная Гвинея',NULL,NULL,233),(1,'Эль-Сальвадор',NULL,NULL,234),(1,'Эритрея',NULL,NULL,235),(1,'Эсватини',NULL,NULL,236),(1,'Эстония',NULL,NULL,237),(1,'Эфиопия',NULL,NULL,238),(1,'Южно-Африканская Республика',NULL,NULL,239),(1,'Южный Судан',NULL,NULL,240),(1,'Ямайка',NULL,NULL,241),(1,'Япония',NULL,NULL,242),(2,'Женский',NULL,NULL,243),(2,'Мужской',NULL,NULL,244),(3,'Высшее',NULL,NULL,245),(3,'Высшее военное',NULL,NULL,246),(3,'Начальная школа',NULL,NULL,247),(3,'Незаконченное высшее',NULL,NULL,248),(3,'Профессионально-техническое',NULL,NULL,249),(3,'Среднее базовое',NULL,NULL,250),(3,'Среднее полное',NULL,NULL,251),(3,'Среднее специальное',NULL,NULL,252),(4,'Безработный',NULL,NULL,253),(4,'Военнослужащий',NULL,NULL,254),(4,'Домохозяйка',NULL,NULL,255),(4,'Колхозник',NULL,NULL,256),(4,'Несовершеннолетний',NULL,NULL,257),(4,'Отбывает наказание в МЛС(О)',NULL,NULL,258),(4,'Отпуск по уходу за ребенком',NULL,NULL,259),(4,'Пенсионер',NULL,NULL,260),(4,'Предприниматель',NULL,NULL,261),(4,'Работник по контракту',NULL,NULL,262),(4,'Работники культуры, науки, медицины, образования',NULL,NULL,263),(4,'Рабочий',NULL,NULL,264),(4,'Служащий',NULL,NULL,265),(4,'Состоит на учете в службе занятости, как безработный',NULL,NULL,266),(4,'Сотрудник Министерства по налогам и сборам',NULL,NULL,267),(4,'Сотрудник органов внутренних дел',NULL,NULL,268),(4,'Сотрудник органов пограничной службы',NULL,NULL,269),(4,'Сотрудник подразделений МЧС',NULL,NULL,270),(4,'Сотрудник таможенных органов',NULL,NULL,271),(4,'Студент высшего УО',NULL,NULL,272),(4,'Студент средне специального УО',NULL,NULL,273),(4,'Учащийся',NULL,NULL,274),(4,'Учащийся профессионально-технического УО',NULL,NULL,275),(4,'Учредитель (собственник) юридического лица',NULL,NULL,276),(5,'Вдовец (вдова)',NULL,NULL,277),(5,'Женат (замужем)',NULL,NULL,278),(5,'Разведен (разведена)',NULL,NULL,279),(5,'Холост (незамужем)',NULL,NULL,280),(6,'Государственная',NULL,NULL,281),(6,'Частная',NULL,NULL,282),(7,'14 пого',NULL,NULL,283),(7,'15 погг',NULL,NULL,284),(7,'16 погг',NULL,NULL,285),(7,'18 пого',NULL,NULL,286),(7,'19 погг',NULL,NULL,287),(7,'20 пого',NULL,NULL,288),(7,'21 пого',NULL,NULL,289),(7,'86 погг',NULL,NULL,290),(7,'опогк \"Минск\"',NULL,NULL,291),(8,'Да',NULL,NULL,292),(8,'Нет',NULL,NULL,293),(9,'Зеленый',NULL,NULL,294),(9,'Красный',NULL,NULL,295),(10,'Авиа',NULL,NULL,296),(10,'Белорусско-латвийский',NULL,NULL,297),(10,'Белорусско-литовский',NULL,NULL,298),(10,'Белорусско-польский',NULL,NULL,299),(10,'Белорусско-российский',NULL,NULL,300),(10,'Белорусско-украинский',NULL,NULL,301),(10,'Иное',NULL,NULL,302),(11,'Линия границы',NULL,NULL,303),(11,'Пограничная зона',NULL,NULL,304),(11,'Пограничная полоса',NULL,NULL,305),(11,'Пункт пропуска',NULL,NULL,306),(11,'Пункт пропуска сопредельного государства',NULL,NULL,307),(11,'Территория республики',NULL,NULL,308),(11,'Территория сопредельного государства',NULL,NULL,309),(12,'В Республику Беларусь',NULL,NULL,310),(12,'Из Республики Беларусь',NULL,NULL,311),(12,'Тыловой район',NULL,NULL,312),(13,'Погз № 1',NULL,NULL,313),(13,'Погз № 10',NULL,NULL,314),(13,'Погз № 11',NULL,NULL,315),(13,'Погз № 12',NULL,NULL,316),(13,'Погз № 13',NULL,NULL,317),(13,'Погз № 14',NULL,NULL,318),(13,'Погз № 15',NULL,NULL,319),(13,'Погз № 16',NULL,NULL,320),(13,'Погз № 17',NULL,NULL,321),(13,'Погз № 18',NULL,NULL,322),(13,'Погз № 19',NULL,NULL,323),(13,'Погз № 2',NULL,NULL,324),(13,'Погз № 3',NULL,NULL,325),(13,'Погз № 4',NULL,NULL,326),(13,'Погз № 5',NULL,NULL,327),(13,'Погз № 6',NULL,NULL,328),(13,'Погз № 7',NULL,NULL,329),(13,'Погз № 8',NULL,NULL,330),(13,'Погз № 9',NULL,NULL,331),(14,'Погп № 1',NULL,NULL,332),(14,'Погп № 2',NULL,NULL,333),(14,'Погп № 3',NULL,NULL,334),(14,'Погп № 4',NULL,NULL,335),(14,'Погп № 5',NULL,NULL,336),(14,'Погп № 6',NULL,NULL,337),(15,'Гудогай погк (опс)',NULL,NULL,338),(15,'Лоев погк (обо)',NULL,NULL,339),(15,'Малорита погк (опс)',NULL,NULL,340),(15,'Опса погк (опс)',NULL,NULL,341),(15,'Поречье погк (опс)',NULL,NULL,342),(15,'Поставы погк (опс)',NULL,NULL,343),(15,'Речица погк (опс)',NULL,NULL,344),(16,'Задержание по ОД',NULL,NULL,345),(16,'Задержание по результатам работы с местным населением',NULL,NULL,346),(17,'ефрейтор',NULL,NULL,347),(17,'капитан',NULL,NULL,348),(17,'лейтенант',NULL,NULL,349),(17,'майор',NULL,NULL,350),(17,'младший лейтенант',NULL,NULL,351),(17,'младший сержант',NULL,NULL,352),(17,'подполковник',NULL,NULL,353),(17,'полковник',NULL,NULL,354),(17,'прапорщик',NULL,NULL,355),(17,'рядовой',NULL,NULL,356),(17,'сержант',NULL,NULL,357),(17,'старший лейтенант',NULL,NULL,358),(17,'старший прапорщик',NULL,NULL,359),(17,'старший сержант',NULL,NULL,360),(17,'старшина',NULL,NULL,361),(18,'английский',NULL,NULL,362),(18,'грузинский',NULL,NULL,363),(18,'испанский',NULL,NULL,364),(18,'итальянский',NULL,NULL,365),(18,'китайский',NULL,NULL,366),(18,'латышский',NULL,NULL,367),(18,'литовский',NULL,NULL,368),(18,'немецкий',NULL,NULL,369),(18,'польский',NULL,NULL,370),(18,'русский',NULL,NULL,371),(18,'украинский',NULL,NULL,372),(18,'французский',NULL,NULL,373),(18,'японский',NULL,NULL,374),(19,'азербаджанец',NULL,NULL,375),(19,'алжирец',NULL,NULL,376),(19,'американец',NULL,NULL,377),(19,'англичанин',NULL,NULL,378),(19,'армянин',NULL,NULL,379),(19,'афганец',NULL,NULL,380),(19,'белорус',NULL,NULL,381),(19,'вьетнамец',NULL,NULL,382),(19,'грузин',NULL,NULL,383),(19,'дагестанец',NULL,NULL,384),(19,'еврей',NULL,NULL,385),(19,'египтянин',NULL,NULL,386),(19,'ингуш',NULL,NULL,387),(19,'индус',NULL,NULL,388),(19,'иранец',NULL,NULL,389),(19,'казах',NULL,NULL,390),(19,'камерунец',NULL,NULL,391),(19,'китаец',NULL,NULL,392),(19,'кубинец',NULL,NULL,393),(19,'кыргыз',NULL,NULL,394),(19,'латыш',NULL,NULL,395),(19,'ливанец',NULL,NULL,396),(19,'литовец',NULL,NULL,397),(19,'молдованин',NULL,NULL,398),(19,'немец',NULL,NULL,399),(19,'нигериец',NULL,NULL,400),(19,'пакистанец',NULL,NULL,401),(19,'поляк',NULL,NULL,402),(19,'пуштун',NULL,NULL,403),(19,'русский',NULL,NULL,404),(19,'сенигалец',NULL,NULL,405),(19,'серб',NULL,NULL,406),(19,'сириец',NULL,NULL,407),(19,'сомалиец',NULL,NULL,408),(19,'таджик',NULL,NULL,409),(19,'тамилец',NULL,NULL,410),(19,'туркмен',NULL,NULL,411),(19,'турок',NULL,NULL,412),(19,'узбек',NULL,NULL,413),(19,'украинец',NULL,NULL,414),(19,'цыган',NULL,NULL,415),(19,'чеченец',NULL,NULL,416),(19,'эфиоп',NULL,NULL,417);
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
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=862 ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_list_top`
--

LOCK TABLES `sys_list_top` WRITE;
/*!40000 ALTER TABLE `sys_list_top` DISABLE KEYS */;
INSERT INTO `sys_list_top` VALUES (1,'citizenship','Гражданство',_binary '\0'),(2,'sex','Пол',_binary ''),(3,'education','Образование',_binary ''),(4,'social_status','Социальное положение',_binary '\0'),(5,'marital_status','Семейное положение',_binary '\0'),(6,'ownership','Форма собственности',_binary '\0'),(7,'tops','ТОПС',_binary '\0'),(8,'yes_no','Да/Нет',_binary '\0'),(9,'channel','Цвет канала',_binary '\0'),(10,'plot','Участок по направлению',_binary '\0'),(11,'category_location','Категория места',_binary '\0'),(12,'course','Направление',_binary '\0'),(13,'number_pogz','Номер погз',_binary '\0'),(14,'number_pogp','Номер погп',_binary '\0'),(15,'pogk','Погк',_binary '\0'),(16,'od','Задержание ОД',_binary '\0'),(17,'rang','Воинское звание',_binary '\0'),(18,'language_skils','Знание языков',_binary '\0'),(19,'nationality','Национальность',_binary '\0');
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
  PRIMARY KEY (`id`),
  KEY `sys_notify_FK` (`file_id`),
  KEY `sys_notify_FK_1` (`from_user_id`),
  KEY `sys_notify_FK_2` (`to_user_id`),
  CONSTRAINT `sys_notify_FK` FOREIGN KEY (`file_id`) REFERENCES `sys_reports` (`id`) ON DELETE SET NULL ON UPDATE SET NULL,
  CONSTRAINT `sys_notify_FK_1` FOREIGN KEY (`from_user_id`) REFERENCES `authentication_modelcustomuser` (`id`),
  CONSTRAINT `sys_notify_FK_2` FOREIGN KEY (`to_user_id`) REFERENCES `authentication_modelcustomuser` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=95 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_notify`
--

LOCK TABLES `sys_notify` WRITE;
/*!40000 ALTER TABLE `sys_notify` DISABLE KEYS */;
INSERT INTO `sys_notify` VALUES (53,2,1,'2021-04-21 12:29:32','information','ujnyhgtf',NULL,NULL),(54,2,1,'2021-04-21 12:29:45','warning','547n63by53r4 bwe',NULL,NULL),(56,2,1,'2021-04-21 14:19:40','information','rfewad',NULL,NULL),(57,2,1,'2021-04-21 14:24:09','error','jkmhgf',NULL,NULL);
/*!40000 ALTER TABLE `sys_notify` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sys_obj`
--

DROP TABLE IF EXISTS `sys_obj`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sys_obj` (
  `id` tinyint unsigned NOT NULL,
  `name` varchar(15) NOT NULL,
  `title` varchar(25) NOT NULL,
  `title_single` varchar(25) NOT NULL,
  `icon` varchar(25) NOT NULL,
  `descript` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=1638 ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_obj`
--

LOCK TABLES `sys_obj` WRITE;
/*!40000 ALTER TABLE `sys_obj` DISABLE KEYS */;
INSERT INTO `sys_obj` VALUES (1,'rel','события/связи','событие/связь','fa-link',NULL),(10,'free','значения','значение','fa-star',NULL),(15,'file','файлы','файл','fa-file',NULL),(20,'doc','документы','документ','fa-align-left',NULL),(25,'point','точки','точка','fa-map-marker-alt',NULL),(30,'geometry','геометрия','геометрия','fa-draw-polygon',NULL),(35,'person_p','физлица','физлицо','fa-user',NULL),(40,'person_l','юрлица','юрлицо','fa-stamp',NULL),(45,'case','дела','дело','fa-lock',NULL),(50,'transport','транспорт','транспорт','fa-car',NULL);
/*!40000 ALTER TABLE `sys_obj` ENABLE KEYS */;
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
  `owner_line_id` tinyint unsigned DEFAULT NULL,
  `owner_region_id` tinyint unsigned DEFAULT NULL,
  `date_auto_remove` datetime DEFAULT NULL,
  `params` text,
  `status` enum('in_progress','done','error') DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `sys_files_FK` (`owner_line_id`),
  KEY `sys_files_FK_1` (`owner_region_id`)
) ENGINE=InnoDB AUTO_INCREMENT=51 DEFAULT CHARSET=utf8;
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
  `variables` varchar(255) DEFAULT NULL,
  `enabled` tinyint(1) NOT NULL DEFAULT '1',
  `owner_id` tinyint unsigned DEFAULT NULL,
  `type` enum('map','report') DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ind_name` (`title`),
  KEY `sys_script_owner_id_de248bfe_fk_owner_lines_id` (`owner_id`),
  KEY `sys_script_parent_id_de218bfe_fk_sys_script_id` (`parent_id`),
  CONSTRAINT `sys_script_owner_id_de248bfe_fk_owner_lines_id` FOREIGN KEY (`owner_id`) REFERENCES `owner_lines` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `sys_script_parent_id_de218bfe_fk_sys_script_id` FOREIGN KEY (`parent_id`) REFERENCES `sys_script` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=42 DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=2048 ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_script`
--

LOCK TABLES `sys_script` WRITE;
/*!40000 ALTER TABLE `sys_script` DISABLE KEYS */;
INSERT INTO `sys_script` VALUES (1,NULL,'Главная папка','home_icon','','','Корневая папка скриптов','',1,3,'map'),(2,1,'Контрабанда сигарет',NULL,'Контрабанда сигарет','group_id = 1\nrel_recs = io_get_rel(group_id,keys_rel,[object_name],None,where_dop)\nels = rel_rec_to_el(rel_recs)\ngeo_ids = el_to_rec_id(object_name,els)\nret = geo_id_to_fc(object_name,group_id,geo_ids,keys_obj)\nreturn ret','уксац','sigarets;сигареты;колличество сигарет;int\nweapons;оружие;колличество оружия;str',1,3,'map'),(4,NULL,'Вторая главная папка','home_icon',NULL,NULL,'2 корневая папка',NULL,1,3,'map'),(5,1,'вложенная папка','home_icon',NULL,NULL,'вложенная папка',NULL,1,3,'map'),(6,1,'2 вложенная папка','home_icon','','','2 вложенная папка','',1,3,'map'),(7,5,'скрипт 1 и еще больше текста что бы проверить',NULL,'скрипт 1 в вложенной папке','group_id = 1\nrel_recs = io_get_rel(group_id,keys_rel,[object_name],None,where_dop)\nels = rel_rec_to_el(rel_recs)\ngeo_ids = el_to_rec_id(object_name,els)\nret = geo_id_to_fc(object_name,group_id,geo_ids,keys_obj)\nreturn ret','уксацц','sigarets;сигареты;колличество сигарет;int\nweapons;оружие;колличество оружия;str',1,3,'map'),(8,NULL,'главный скрипт',NULL,'главный скрипт','group_id = 1\nrel_recs = io_get_rel(group_id,keys_rel,[object_name],None,where_dop)\nels = rel_rec_to_el(rel_recs)\ngeo_ids = el_to_rec_id(object_name,els)\nret = geo_id_to_fc(object_name,group_id,geo_ids,keys_obj)\nreturn ret','уксац','sigarets;сигареты;колличество сигарет;int\nweapons;оружие;колличество оружия;str',1,3,'map'),(9,NULL,'адреса',NULL,'получение адресов','group_id = 1\nrel_recs = io_get_rel(group_id,keys_rel,[object_name],None,where_dop)\nels = rel_rec_to_el(rel_recs)\ngeo_ids = el_to_rec_id(object_name,els)\nret = geo_id_to_fc(object_name,group_id,geo_ids,keys_obj)\nreturn ret','ак3','sigarets;сигареты;колличество сигарет;int\nweapons;оружие;колличество оружия;str',1,3,'map'),(10,NULL,'fghjkjhgfdhjbk',NULL,'получение адресов','group_id = 1\nrel_recs = io_get_rel(group_id,keys_rel,[object_name],None,where_dop)\nels = rel_rec_to_el(rel_recs)\ngeo_ids = el_to_rec_id(object_name,els)\nret = geo_id_to_fc(object_name,group_id,geo_ids,keys_obj)\nreturn ret','ак3','sigarets;сигареты;колличество сигарет;int\nweapons;оружие;колличество оружия;str',1,3,'map'),(11,1,'Главная папка 2','home_icon','','','Корневая папка скриптов','',1,3,'map'),(15,4,'SCRIIIIPT',NULL,'','keys_rel = [int(keys_rel)]\r\n\r\n\r\nreturn rel_to_geo_fc(obj,0,keys_rel=keys_rel,keys_obj=[\'parent_id\'])','Тестовое создание скрипта','obj;Тип объекта;Тип объекта;text\r\nkeys_rel;Ключ классификатора;Ключ классификатора;number',1,3,'map'),(33,NULL,'контробанда сигарет',NULL,'где сигареты проносят','if keys_rel.find(\',\') != -1:\r\n    keys_rel = [int(item) for item in keys_rel.split(\',\')]\r\nelse:\r\n    keys_rel = [int(keys_rel)]\r\n		\r\nres = rel_to_geo_fc(obj, 0, keys_rel=keys_rel, keys_obj=[\'parent_id\'],where_dop=[])\r\nreturn res','нткреиу','obj;Тип объекта;Тип объекта;text\r\nkeys_rel;Ключ классификатора;Ключ классификатора;number',1,3,'map'),(36,NULL,'папка отчетов','home_icon','отчеты','','онр','',1,3,'report'),(40,36,'тестовый отчет',NULL,'где сигареты проносят','path = title + \'.txt\'\r\nfile = open(path, \'w\')\r\nfile.write(weapons)\r\nfile.close()','асв','weapons;оружие;колличество оружия;str',1,3,'report'),(41,NULL,'получить geojson',NULL,'тестовый скрипт для получения геометрии','if keys_rel.find(\',\') != -1:\r\n    keys_rel = [int(item) for item in keys_rel.split(\',\')]\r\nelse:\r\n    keys_rel = [int(keys_rel)]\r\nres = rel_to_geo_fc(obj, 0, keys_rel=keys_rel, keys_obj=[\'parent_id\'],where_dop=[])\r\nreturn res','ксуем4к','obj;Тип объекта;Тип объекта;text\r\nkeys_rel;Ключ классификатора;Ключ классификатора;number',1,3,'map');
/*!40000 ALTER TABLE `sys_script` ENABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_templates`
--

LOCK TABLES `sys_templates` WRITE;
/*!40000 ALTER TABLE `sys_templates` DISABLE KEYS */;
INSERT INTO `sys_templates` VALUES (27,1,'новый шаблон 1','[{\"id\": 41, \"name\": \"получить geojson\", \"variables\": {\"obj\": {\"value\": \"geometry\", \"title\": \"Тип объекта\"}, \"keys_rel\": {\"value\": \"43\", \"title\": \"Ключ классификатора\"}}, \"color\": \"#FFA500FF\"}, {\"id\": 15, \"name\": \"SCRIIIIPT\", \"variables\": {\"obj\": {\"title\": \"Тип объекта\", \"value\": \"geometry\"}, \"keys_rel\": {\"title\": \"Ключ классификатора\", \"value\": \"41\"}}, \"color\": \"#CE0A0AFF\"}]','[{\"id\": 7, \"name\": \"скрипт 1 и еще больше текста что бы проверить\", \"variables\": {\"sigarets\": {\"title\": \"сигареты\", \"value\": \"trgfe\"}, \"weapons\": {\"title\": \"оружие\", \"value\": \"43\"}}, \"color\": \"#696969FF\"}]');
/*!40000 ALTER TABLE `sys_templates` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-04-29 10:19:17
