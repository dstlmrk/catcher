-- MySQL dump 10.13  Distrib 5.6.32-78.1, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: catcher
-- ------------------------------------------------------
-- Server version	5.6.32-78.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `advancement`
--

DROP TABLE IF EXISTS `advancement`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `advancement` (
  `standing` smallint(6) NOT NULL,
  `final_standing` smallint(6) DEFAULT NULL,
  `next_step_ide` varchar(3) DEFAULT NULL,
  `group_ide` char(3) NOT NULL,
  `tournament_id` int(11) NOT NULL,
  PRIMARY KEY (`standing`,`group_ide`,`tournament_id`),
  KEY `fk_advancement_group1_idx` (`group_ide`,`tournament_id`),
  CONSTRAINT `fk_advancement_group1` FOREIGN KEY (`group_ide`, `tournament_id`) REFERENCES `group` (`ide`, `tournament_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `api_key`
--

DROP TABLE IF EXISTS `api_key`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `api_key` (
  `key` varchar(255) NOT NULL,
  `valid_to` datetime NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`key`),
  KEY `fk_api_key_user1_idx` (`user_id`),
  CONSTRAINT `fk_api_key_user1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `division`
--

DROP TABLE IF EXISTS `division`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `division` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type` varchar(16) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `division_UNIQUE` (`type`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `field`
--

DROP TABLE IF EXISTS `field`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `field` (
  `id` int(11) NOT NULL,
  `tournament_id` int(11) NOT NULL,
  `name` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`,`tournament_id`),
  KEY `fk_field_tournament1_idx` (`tournament_id`),
  CONSTRAINT `fk_field_tournament1` FOREIGN KEY (`tournament_id`) REFERENCES `tournament` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `group`
--

DROP TABLE IF EXISTS `group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `group` (
  `teams_count` int(11) NOT NULL,
  `description` varchar(45) DEFAULT NULL COMMENT 'Nazev skupiny, napr. Skupina A',
  `ide` char(3) NOT NULL,
  `tournament_id` int(11) NOT NULL,
  PRIMARY KEY (`ide`,`tournament_id`),
  UNIQUE KEY `description_UNIQUE` (`description`) COMMENT ' /* comment truncated */ /*Kazda skupina musi mit na turnaji jiny popisek.\n\n*/',
  KEY `fk_group_identificator1_idx` (`ide`,`tournament_id`),
  CONSTRAINT `fk_group_identificator1` FOREIGN KEY (`ide`, `tournament_id`) REFERENCES `identificator` (`ide`, `tournament_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `group_has_team`
--

DROP TABLE IF EXISTS `group_has_team`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `group_has_team` (
  `matches_count` smallint(6) NOT NULL DEFAULT '0',
  `wins_count` smallint(6) NOT NULL DEFAULT '0',
  `losses_count` smallint(6) NOT NULL DEFAULT '0',
  `plus_count` smallint(6) NOT NULL DEFAULT '0',
  `minus_count` smallint(6) NOT NULL DEFAULT '0',
  `points_count` smallint(6) NOT NULL DEFAULT '0',
  `standing` smallint(6) DEFAULT NULL,
  `team_id` int(11) NOT NULL,
  `group_ide` char(3) NOT NULL,
  `tournament_id` int(11) NOT NULL,
  PRIMARY KEY (`group_ide`,`tournament_id`,`team_id`),
  KEY `fk_group_has_team_team1_idx` (`team_id`),
  KEY `fk_group_has_team_group1_idx` (`group_ide`,`tournament_id`),
  CONSTRAINT `fk_group_has_team_group1` FOREIGN KEY (`group_ide`, `tournament_id`) REFERENCES `group` (`ide`, `tournament_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_group_has_team_team1` FOREIGN KEY (`team_id`) REFERENCES `team` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `identificator`
--

DROP TABLE IF EXISTS `identificator`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `identificator` (
  `tournament_id` int(11) NOT NULL,
  `ide` char(3) NOT NULL,
  `is_match` tinyint(1) NOT NULL,
  PRIMARY KEY (`ide`,`tournament_id`),
  KEY `fk_table1_tournament1_idx` (`tournament_id`),
  CONSTRAINT `fk_table1_tournament1` FOREIGN KEY (`tournament_id`) REFERENCES `tournament` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `match`
--

DROP TABLE IF EXISTS `match`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `match` (
  `home_team_id` int(11) DEFAULT NULL,
  `away_team_id` int(11) DEFAULT NULL,
  `time_start` timestamp NULL DEFAULT NULL,
  `time_stop` timestamp NULL DEFAULT NULL,
  `state` enum('prepared','in progress','terminated') NOT NULL DEFAULT 'prepared',
  `score_home` tinyint(4) DEFAULT NULL,
  `score_away` tinyint(4) DEFAULT NULL,
  `description` varchar(45) DEFAULT NULL,
  `looser_final_standing` smallint(6) DEFAULT NULL,
  `winner_final_standing` smallint(6) DEFAULT NULL,
  `winner_next_step_ide` char(3) DEFAULT NULL,
  `looser_next_step_ide` char(3) DEFAULT NULL,
  `group_ide` char(3) DEFAULT NULL,
  `ide` char(3) NOT NULL,
  `tournament_id` int(11) NOT NULL,
  `field_id` int(11) NOT NULL,
  PRIMARY KEY (`ide`,`tournament_id`),
  KEY `fk_match_team1_idx` (`home_team_id`),
  KEY `fk_match_team2_idx` (`away_team_id`),
  KEY `fk_match_identificator1_idx` (`ide`,`tournament_id`),
  KEY `fk_match_field1_idx` (`field_id`,`tournament_id`),
  CONSTRAINT `fk_match_field1` FOREIGN KEY (`field_id`, `tournament_id`) REFERENCES `field` (`id`, `tournament_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_match_identificator1` FOREIGN KEY (`ide`, `tournament_id`) REFERENCES `identificator` (`ide`, `tournament_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_match_team1` FOREIGN KEY (`home_team_id`) REFERENCES `team` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_match_team2` FOREIGN KEY (`away_team_id`) REFERENCES `team` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `participation`
--

DROP TABLE IF EXISTS `participation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `participation` (
  `tournament_id` int(11) NOT NULL,
  `team_id` int(11) NOT NULL,
  `seeding` int(11) DEFAULT NULL,
  PRIMARY KEY (`tournament_id`,`team_id`),
  KEY `fk_participation_team1_idx` (`team_id`),
  CONSTRAINT `fk_participation_team1` FOREIGN KEY (`team_id`) REFERENCES `team` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_participation_tournament1` FOREIGN KEY (`tournament_id`) REFERENCES `tournament` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `role`
--

DROP TABLE IF EXISTS `role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `role` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type` varchar(45) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `role_UNIQUE` (`type`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `standing`
--

DROP TABLE IF EXISTS `standing`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `standing` (
  `tournament_id` int(11) NOT NULL,
  `standing` smallint(6) NOT NULL,
  `team_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`tournament_id`,`standing`),
  KEY `fk_standings_tournament1_idx` (`tournament_id`),
  KEY `fk_standings_team1_idx` (`team_id`),
  CONSTRAINT `fk_standings_team1` FOREIGN KEY (`team_id`) REFERENCES `team` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_standings_tournament1` FOREIGN KEY (`tournament_id`) REFERENCES `tournament` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Tabulka se vyplni na konci turnaje (nebo muze klidne i postu /* comment truncated */ /*pne).*/';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `team`
--

DROP TABLE IF EXISTS `team`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `team` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `division_id` int(11) NOT NULL,
  `name` varchar(45) NOT NULL,
  `shortcut` char(3) NOT NULL,
  `city` varchar(45) DEFAULT NULL,
  `country` char(3) DEFAULT NULL,
  `cald_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name_UNIQUE` (`name`,`division_id`),
  KEY `fk_team_category1_idx` (`division_id`),
  KEY `fk_team_user1_idx` (`user_id`),
  CONSTRAINT `fk_team_category1` FOREIGN KEY (`division_id`) REFERENCES `division` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_team_user1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tournament`
--

DROP TABLE IF EXISTS `tournament`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tournament` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `division_id` int(11) NOT NULL,
  `name` varchar(45) NOT NULL,
  `teams_count` int(11) NOT NULL,
  `state` enum('created','prepared','in progress','terminated') NOT NULL DEFAULT 'created',
  `date_start` datetime NOT NULL,
  `date_stop` datetime NOT NULL,
  `city` varchar(45) DEFAULT NULL,
  `country` varchar(3) DEFAULT NULL,
  `cald` tinyint(1) NOT NULL DEFAULT '0',
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_tournament_category1_idx` (`division_id`),
  KEY `fk_tournament_user1_idx` (`user_id`),
  CONSTRAINT `fk_tournament_category1` FOREIGN KEY (`division_id`) REFERENCES `division` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_tournament_user1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `login` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` char(64) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `role_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email_UNIQUE` (`email`),
  UNIQUE KEY `login_UNIQUE` (`login`),
  KEY `fk_user_role1_idx` (`role_id`),
  CONSTRAINT `fk_user_role1` FOREIGN KEY (`role_id`) REFERENCES `role` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-12-30 23:59:49
