-- MySQL dump 10.13  Distrib 8.0.44, for Linux (x86_64)
--
-- Host: localhost    Database: shop_database
-- ------------------------------------------------------
-- Server version	8.0.44-0ubuntu0.22.04.1

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
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add product',7,'add_product'),(26,'Can change product',7,'change_product'),(27,'Can delete product',7,'delete_product'),(28,'Can view product',7,'view_product'),(29,'Can add category',8,'add_category'),(30,'Can change category',8,'change_category'),(31,'Can delete category',8,'delete_category'),(32,'Can view category',8,'view_category'),(33,'Can add cart item',9,'add_cartitem'),(34,'Can change cart item',9,'change_cartitem'),(35,'Can delete cart item',9,'delete_cartitem'),(36,'Can view cart item',9,'view_cartitem'),(37,'Can add cart',10,'add_cart'),(38,'Can change cart',10,'change_cart'),(39,'Can delete cart',10,'delete_cart'),(40,'Can view cart',10,'view_cart'),(41,'Can add customer',11,'add_customer'),(42,'Can change customer',11,'change_customer'),(43,'Can delete customer',11,'delete_customer'),(44,'Can view customer',11,'view_customer');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$1000000$W6KjgpiU6fSRZ6r3A2rrTH$QbfKFwaqhNTWh6IkT2xhDXMSZEBCnODnm41RpZSBVDQ=','2026-01-05 17:16:16.282335',0,'zakjer','John','Doe','zakjer@wp.pl',0,1,'2025-11-02 20:19:27.209675'),(2,'pbkdf2_sha256$1000000$KYxzbDglfELvYJD4T57UCr$2LQDv499X4p1Vgze88TxWg/VxnnSZHLz/5+LsniYzdM=','2026-01-05 17:16:36.988508',1,'admin','','','admin@wp.pl',1,1,'2025-11-03 18:19:01.581305');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(5,'contenttypes','contenttype'),(6,'sessions','session'),(10,'shop','cart'),(9,'shop','cartitem'),(8,'shop','category'),(11,'shop','customer'),(7,'shop','product');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2025-10-27 19:17:08.770013'),(2,'auth','0001_initial','2025-10-27 19:17:09.403627'),(3,'admin','0001_initial','2025-10-27 19:17:09.551113'),(4,'admin','0002_logentry_remove_auto_add','2025-10-27 19:17:09.565387'),(5,'admin','0003_logentry_add_action_flag_choices','2025-10-27 19:17:09.583930'),(6,'contenttypes','0002_remove_content_type_name','2025-10-27 19:17:09.671935'),(7,'auth','0002_alter_permission_name_max_length','2025-10-27 19:17:09.739909'),(8,'auth','0003_alter_user_email_max_length','2025-10-27 19:17:09.764108'),(9,'auth','0004_alter_user_username_opts','2025-10-27 19:17:09.777952'),(10,'auth','0005_alter_user_last_login_null','2025-10-27 19:17:09.837282'),(11,'auth','0006_require_contenttypes_0002','2025-10-27 19:17:09.846162'),(12,'auth','0007_alter_validators_add_error_messages','2025-10-27 19:17:09.864309'),(13,'auth','0008_alter_user_username_max_length','2025-10-27 19:17:09.885116'),(14,'auth','0009_alter_user_last_name_max_length','2025-10-27 19:17:09.905018'),(15,'auth','0010_alter_group_name_max_length','2025-10-27 19:17:09.931802'),(16,'auth','0011_update_proxy_permissions','2025-10-27 19:17:09.947033'),(17,'auth','0012_alter_user_first_name_max_length','2025-10-27 19:17:09.969288'),(18,'sessions','0001_initial','2025-10-27 19:17:10.016742'),(19,'shop','0001_initial','2025-10-27 19:17:10.035520'),(20,'shop','0002_category_product_created_at_product_discount_price_and_more','2025-10-28 10:43:57.559445'),(21,'shop','0003_cart_customer_cartitem_cart_customer','2025-11-02 20:12:23.918324');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('0lbs5uuv55r7tug0ua8pu2fdd91ksl5g','e30:1vFebO:g4yUaknMmtG2QRZoRH-Szcf5XRnKrxjwfoZM8FFA8Ok','2025-11-16 20:23:02.968843'),('0mcd2hpbnyxwf8kugbjmbuulk6mtq6od','e30:1vFebH:My496w_FAQmDYYG7zH16difOYryHLt3bOOvVB1KUv0I','2025-11-16 20:22:55.157176'),('751ha9ss6umkm8zwit42aig2yr49txt6','eyJjYXJ0Ijp7IjUiOjIsIjYiOjF9fQ:1vFXQK:gBRRTIeXWzfryClAbRtlcSIF3AmqDJ7elLgL7UrZhAU','2025-11-16 12:43:08.330581'),('fkbwbegudfj9f0zi90rn7cgzplr9iq45','.eJxVjDsOwjAQRO_iGln-fyjpcwZrvd7gAHKkOKkQdyeRUoA01bw382YJtrWmrdOSpsKuTLHLb5cBn9QOUB7Q7jPHua3LlPmh8JN2PsyFXrfT_Tuo0Ou-zhogj0oUTRh9sNKCCsEoqagQKhejjATaZXTOZxR7hCZnvA1iNCGyzxfsKTek:1vcoC5:DOnBKSrjZUjUemw4sdLa0WrQdzdSN8xbgD52j_6W3u8','2026-01-19 17:16:37.011900'),('i4d591wowjr79dsgi7brs7iydzbxr1jz','.eJxVjM0OwiAQhN-FsyGwYqEevfcZyLK72KqBpD8n47tbkh50jvN9M28VcVvHuC0yx4nVVYE6_XYJ6SmlAX5guVdNtazzlHRT9EEXPVSW1-1w_w5GXMa2hpA9Ucc25R4ZKQfqjdsDBj13jOJAyFhvXU_GJIDdPneOg5MLiPp8AQgDOFM:1vFz9S:ndkhLNOo74pNHg_wRPrCVpDmHmAmFfrVVXw2aNo_spo','2025-11-17 18:19:34.313663'),('i6oh6humf65yvobmz6ix3cntjpwg0b9g','e30:1vFeYW:q16CfLxEBEF4bQOG0x5A5SEKfZnKZBNzMhk9YVRTk1Y','2025-11-16 20:20:04.331514'),('y5427a5q0dkn0sb2085yt8eajki4lhsx','.eJxVjDsOwjAQBe_iGlkbm_WHkj5nsHb9wQHkSHFSIe4OkVJA-2bmvUSgba1h63kJUxIXocTpd2OKj9x2kO7UbrOMc1uXieWuyIN2Oc4pP6-H-3dQqddvbQbMGU1UlAC0wqK1hRwVIoNnixZssufivLMMwN4UB6S1ToYHE9GL9wfC9Tbl:1vGDqL:R39AfBz0M5xl0NQqItiD-0kkSSvf2p37rOulXE3hfu8','2025-11-18 10:00:49.187298'),('zu4vy1uw4i6occt2m0xlojl38o0l5oh8','.eJxVjDsOwjAQRO_iGln-fyjpcwZrvd7gAHKkOKkQdyeRUoA01bw382YJtrWmrdOSpsKuTLHLb5cBn9QOUB7Q7jPHua3LlPmh8JN2PsyFXrfT_Tuo0Ou-zhogj0oUTRh9sNKCCsEoqagQKhejjATaZXTOZxR7hCZnvA1iNCGyzxfsKTek:1vNuP3:V4RJWK35BYdple3IJAqIIXJfDFluebyw7iqTOVH-vXo','2025-12-09 14:52:25.145836');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `shop_cart`
--

LOCK TABLES `shop_cart` WRITE;
/*!40000 ALTER TABLE `shop_cart` DISABLE KEYS */;
INSERT INTO `shop_cart` VALUES (1,'2025-11-03 17:56:17.086800',1),(2,'2025-11-04 10:00:58.674532',2);
/*!40000 ALTER TABLE `shop_cart` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `shop_cartitem`
--

LOCK TABLES `shop_cartitem` WRITE;
/*!40000 ALTER TABLE `shop_cartitem` DISABLE KEYS */;
INSERT INTO `shop_cartitem` VALUES (1,2,1,11),(2,3,1,21),(3,3,2,11);
/*!40000 ALTER TABLE `shop_cartitem` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `shop_category`
--

LOCK TABLES `shop_category` WRITE;
/*!40000 ALTER TABLE `shop_category` DISABLE KEYS */;
INSERT INTO `shop_category` VALUES (1,'Books','books'),(2,'Video Games','video-games'),(3,'Movies','movies');
/*!40000 ALTER TABLE `shop_category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `shop_customer`
--

LOCK TABLES `shop_customer` WRITE;
/*!40000 ALTER TABLE `shop_customer` DISABLE KEYS */;
INSERT INTO `shop_customer` VALUES (1,NULL,NULL,1),(2,NULL,NULL,2);
/*!40000 ALTER TABLE `shop_customer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `shop_product`
--

LOCK TABLES `shop_product` WRITE;
/*!40000 ALTER TABLE `shop_product` DISABLE KEYS */;
INSERT INTO `shop_product` VALUES (9,'The Lord of the Rings','An epic high-fantasy novel by J.R.R. Tolkien, following the journey to destroy the One Ring.',29.99,'shop/images/lotr.png','2025-11-03 16:20:12.000000',24.99,'Classic fantasy adventure by Tolkien.',15,1),(10,'Harry Potter and the Philosopher\'s Stone','The first book in J.K. Rowling’s magical Harry Potter series.',19.99,'shop/images/harry_potter.png','2025-11-03 16:20:12.000000',NULL,'Start of the legendary Harry Potter saga.',20,1),(11,'1984','A dystopian social science fiction novel by George Orwell.',14.99,'shop/images/1984.png','2025-11-03 16:20:12.000000',NULL,'Classic dystopian novel.',25,1),(12,'The Hobbit','Prequel to The Lord of the Rings, following Bilbo Baggins on his unexpected adventure.',22.50,'shop/images/hobbit.png','2025-11-03 16:20:12.000000',18.50,'The adventure that started it all.',30,1),(13,'Dune','A science fiction masterpiece by Frank Herbert, exploring politics, religion, and ecology.',27.99,'shop/images/dune.png','2025-11-03 16:20:12.000000',23.99,'Sci-fi epic on the desert planet Arrakis.',18,1),(14,'The Legend of Zelda: Breath of the Wild','An open-world adventure game from Nintendo, featuring exploration and discovery.',59.99,'shop/images/zelda.png','2025-11-03 16:20:12.000000',49.99,'Explore the vast world of Hyrule.',10,2),(15,'Elden Ring','A dark fantasy action RPG developed by FromSoftware and published by Bandai Namco.',69.99,'shop/images/elden_ring.png','2025-11-03 16:20:12.000000',59.99,'Open-world soulslike adventure.',12,2),(16,'Minecraft','The popular sandbox game where players build and explore infinite worlds.',26.99,'shop/images/minecraft.png','2025-11-03 16:20:12.000000',NULL,'Creative and survival sandbox experience.',40,2),(17,'The Witcher 3: Wild Hunt','An action RPG based on Andrzej Sapkowski’s novels, following Geralt of Rivia.',39.99,'shop/images/witcher3.png','2025-11-03 16:20:12.000000',29.99,'Critically acclaimed fantasy RPG.',22,2),(18,'Grand Theft Auto V','An open-world crime and adventure game from Rockstar Games.',29.99,'shop/images/gta5.png','2025-11-03 16:20:12.000000',19.99,'Classic open-world crime game.',25,2),(19,'Inception','A mind-bending sci-fi thriller directed by Christopher Nolan.',17.99,'shop/images/inception.png','2025-11-03 16:20:12.000000',NULL,'Dream within a dream.',20,3),(20,'The Dark Knight','The second installment in Nolan’s Batman trilogy starring Christian Bale and Heath Ledger.',19.99,'shop/images/dark_knight.png','2025-11-03 16:20:12.000000',14.99,'Critically acclaimed Batman film.',25,3),(21,'Interstellar','A sci-fi epic about space exploration and the endurance of human spirit.',21.99,'shop/images/interstellar.png','2025-11-03 16:20:12.000000',17.99,'Visually stunning journey through space and time.',18,3),(22,'The Matrix','A sci-fi action classic where reality is not what it seems.',16.99,'shop/images/matrix.png','2025-11-03 16:20:12.000000',NULL,'Neo discovers the truth about reality.',30,3),(23,'Avengers: Endgame','The grand finale of Marvel’s Infinity Saga.',24.99,'shop/images/endgame.png','2025-11-03 16:20:12.000000',19.99,'Epic superhero conclusion.',22,3);
/*!40000 ALTER TABLE `shop_product` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-01-11 17:00:03
