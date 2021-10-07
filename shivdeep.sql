-- MySQL dump 10.13  Distrib 8.0.15, for Win64 (x86_64)
--
-- Host: localhost    Database: shivdeep
-- ------------------------------------------------------
-- Server version	8.0.15

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
 SET NAMES utf8mb4 ;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `location_pattern`
--

DROP TABLE IF EXISTS `location_pattern`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `location_pattern` (
  `LOCATION` varchar(300) DEFAULT NULL,
  `COUNT` int(3) DEFAULT NULL,
  `USER_ID` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `location_pattern`
--

LOCK TABLES `location_pattern` WRITE;
/*!40000 ALTER TABLE `location_pattern` DISABLE KEYS */;
/*!40000 ALTER TABLE `location_pattern` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `login_credenitals`
--

DROP TABLE IF EXISTS `login_credenitals`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `login_credenitals` (
  `MAIL_ID` varchar(200) DEFAULT NULL,
  `PASSWORD` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `login_credenitals`
--

LOCK TABLES `login_credenitals` WRITE;
/*!40000 ALTER TABLE `login_credenitals` DISABLE KEYS */;
/*!40000 ALTER TABLE `login_credenitals` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tweets_track`
--

DROP TABLE IF EXISTS `tweets_track`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `tweets_track` (
  `USER_ID` varchar(50) DEFAULT NULL,
  `TWEET_ID` varchar(50) DEFAULT NULL,
  `TWEET_TEXT` varchar(300) DEFAULT NULL,
  `DATE_OF_POST` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tweets_track`
--

LOCK TABLES `tweets_track` WRITE;
/*!40000 ALTER TABLE `tweets_track` DISABLE KEYS */;
INSERT INTO `tweets_track` VALUES ('1171000571119185921','1245573660636639233','#FEMA #PENTAGON #Trump this is a nightmare... Join us #LIVE #COVID19 \nPENTAGON To Get 100,000 BAGS For FEMA... (nig… https://t.co/ctiwubYuT8','2020-04-02'),('1245230935039045632','1245573718354493445','#trump may you rott in hell','2020-04-02'),('1245230935039045632','1245575862423961600','This system is nothing but piece of shit','2020-04-02'),('782663183223836673','1245576170281656326','So pathetic he cheats at golf little man playing with his little whit balls can’t handle the truth he makes up ever… https://t.co/WALHhnceeZ','2020-04-02'),('41221409','1245578197585899538','RT @FuckThe_NRA: Fuck Donald #Trump and anyone who supports him.','2020-04-02'),('2567755940','1245578433251299343','RT @AndyOstroy: What we’re seeing now is classic #Trump: claims something is a hoax, gets bitch-slapped for it, wastes months, finally gets…','2020-04-02'),('13482252','1245578606442467328','fucking A','2020-04-02'),('2336393412','1245579395114225666','@itsJeffTiedrich @realDonaldTrump What the fuck are you even talking about? You backwoods, hillbillie nobody. I kno… https://t.co/8hoyut2OL9','2020-04-02'),('3991108098','1245579555848380425','#Trump told reporters on Wednesday at a White House #Coronavirus Task Force news briefing that he does not intend t… https://t.co/IVALWQb2P8','2020-04-02'),('2749742877','1245579794709770240','RT @AndyOstroy: What we’re seeing now is classic #Trump: claims something is a hoax, gets bitch-slapped for it, wastes months, finally gets…','2020-04-02');
/*!40000 ALTER TABLE `tweets_track` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_track`
--

DROP TABLE IF EXISTS `user_track`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `user_track` (
  `USER_ID` varchar(50) NOT NULL,
  `USER_NAME` varchar(200) DEFAULT NULL,
  `SCREEN_NAME` varchar(200) DEFAULT NULL,
  `COUNT` int(3) DEFAULT NULL,
  `LATEST_TWEET_DATE` date DEFAULT NULL,
  PRIMARY KEY (`USER_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_track`
--

LOCK TABLES `user_track` WRITE;
/*!40000 ALTER TABLE `user_track` DISABLE KEYS */;
INSERT INTO `user_track` VALUES ('1245230935039045632','Shivdeep Chaudhari','ShivdeepChaudh1',2,'2020-04-02'),('13482252','Adam Welch','leemellow',1,'2020-04-02'),('2336393412','Raymond Woods','Raydemption44',1,'2020-04-02'),('2567755940','JoniResists ✍️ 🌊🇺🇸 🇬🇧 VoteBlueNoMatterWho2020','JoniResists',1,'2020-04-02'),('2749742877','Cindy Hambro','CindyHambro',1,'2020-04-02'),('3991108098','DT Next','dt_next',1,'2020-04-02'),('41221409','AD','Major_Wookie',1,'2020-04-02'),('782663183223836673','melina I stand with Greta','melina_mangiola',1,'2020-04-02');
/*!40000 ALTER TABLE `user_track` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `users` (
  `username` varchar(30) DEFAULT NULL,
  `password` varchar(30) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES ('shivdeepchaudhari23','iamshivdeep'),('onkar01','iamonkar');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-04-02 14:32:53
