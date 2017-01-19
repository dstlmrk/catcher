SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

CREATE SCHEMA IF NOT EXISTS `catcher` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci ;
SHOW WARNINGS;
USE `catcher` ;

-- -----------------------------------------------------
-- Table `catcher`.`role`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `catcher`.`role` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `catcher`.`role` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `type` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `role_UNIQUE` (`type` ASC))
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `catcher`.`user`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `catcher`.`user` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `catcher`.`user` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `login` VARCHAR(255) NOT NULL,
  `email` VARCHAR(255) NOT NULL,
  `password` CHAR(64) NOT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `role_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `email_UNIQUE` (`email` ASC),
  INDEX `fk_user_role1_idx` (`role_id` ASC),
  UNIQUE INDEX `login_UNIQUE` (`login` ASC),
  CONSTRAINT `fk_user_role1`
    FOREIGN KEY (`role_id`)
    REFERENCES `catcher`.`role` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `catcher`.`division`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `catcher`.`division` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `catcher`.`division` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `type` VARCHAR(16) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `division_UNIQUE` (`type` ASC))
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `catcher`.`team`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `catcher`.`team` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `catcher`.`team` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `division_id` INT NOT NULL,
  `name` VARCHAR(45) NOT NULL,
  `shortcut` CHAR(3) NOT NULL,
  `deleted` TINYINT(1) NOT NULL DEFAULT 0,
  `city` VARCHAR(45) NULL,
  `country` CHAR(3) NULL,
  `cald_id` INT NULL DEFAULT NULL,
  `user_id` INT NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_team_category1_idx` (`division_id` ASC),
  UNIQUE INDEX `name_UNIQUE` (`name` ASC, `division_id` ASC),
  INDEX `fk_team_user1_idx` (`user_id` ASC),
  CONSTRAINT `fk_team_category1`
    FOREIGN KEY (`division_id`)
    REFERENCES `catcher`.`division` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_team_user1`
    FOREIGN KEY (`user_id`)
    REFERENCES `catcher`.`user` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `catcher`.`tournament`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `catcher`.`tournament` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `catcher`.`tournament` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `division_id` INT NOT NULL,
  `name` VARCHAR(45) NOT NULL,
  `teams_count` INT NOT NULL,
  `state` ENUM('created','prepared','in progress','terminated') NOT NULL DEFAULT 'created',
  `date_start` DATETIME NOT NULL,
  `date_stop` DATETIME NOT NULL,
  `city` VARCHAR(45) NULL,
  `country` VARCHAR(3) NULL,
  `cald` TINYINT(1) NOT NULL DEFAULT FALSE,
  `user_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_tournament_category1_idx` (`division_id` ASC),
  INDEX `fk_tournament_user1_idx` (`user_id` ASC),
  CONSTRAINT `fk_tournament_category1`
    FOREIGN KEY (`division_id`)
    REFERENCES `catcher`.`division` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_tournament_user1`
    FOREIGN KEY (`user_id`)
    REFERENCES `catcher`.`user` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `catcher`.`field`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `catcher`.`field` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `catcher`.`field` (
  `id` INT NOT NULL,
  `tournament_id` INT NOT NULL,
  `name` VARCHAR(45) NULL,
  PRIMARY KEY (`id`, `tournament_id`),
  INDEX `fk_field_tournament1_idx` (`tournament_id` ASC),
  CONSTRAINT `fk_field_tournament1`
    FOREIGN KEY (`tournament_id`)
    REFERENCES `catcher`.`tournament` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `catcher`.`identificator`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `catcher`.`identificator` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `catcher`.`identificator` (
  `tournament_id` INT NOT NULL,
  `ide` CHAR(3) NOT NULL,
  `is_match` TINYINT(1) NOT NULL,
  INDEX `fk_table1_tournament1_idx` (`tournament_id` ASC),
  PRIMARY KEY (`ide`, `tournament_id`),
  CONSTRAINT `fk_table1_tournament1`
    FOREIGN KEY (`tournament_id`)
    REFERENCES `catcher`.`tournament` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `catcher`.`match`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `catcher`.`match` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `catcher`.`match` (
  `home_team_id` INT NULL DEFAULT NULL,
  `away_team_id` INT NULL DEFAULT NULL,
  `time_start` TIMESTAMP NULL DEFAULT NULL,
  `time_stop` TIMESTAMP NULL DEFAULT NULL,
  `state` ENUM('prepared','in progress','terminated') NOT NULL DEFAULT 'prepared',
  `score_home` TINYINT NULL DEFAULT NULL,
  `score_away` TINYINT NULL DEFAULT NULL,
  `description` VARCHAR(45) NULL DEFAULT NULL,
  `looser_final_standing` SMALLINT NULL DEFAULT NULL,
  `winner_final_standing` SMALLINT NULL DEFAULT NULL,
  `winner_next_step_ide` CHAR(3) NULL DEFAULT NULL,
  `looser_next_step_ide` CHAR(3) NULL DEFAULT NULL,
  `group_ide` CHAR(3) NULL DEFAULT NULL,
  `ide` CHAR(3) NOT NULL,
  `tournament_id` INT NOT NULL,
  `field_id` INT NOT NULL,
  INDEX `fk_match_team1_idx` (`home_team_id` ASC),
  INDEX `fk_match_team2_idx` (`away_team_id` ASC),
  INDEX `fk_match_identificator1_idx` (`ide` ASC, `tournament_id` ASC),
  PRIMARY KEY (`ide`, `tournament_id`),
  INDEX `fk_match_field1_idx` (`field_id` ASC, `tournament_id` ASC),
  CONSTRAINT `fk_match_team1`
    FOREIGN KEY (`home_team_id`)
    REFERENCES `catcher`.`team` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_match_team2`
    FOREIGN KEY (`away_team_id`)
    REFERENCES `catcher`.`team` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_match_identificator1`
    FOREIGN KEY (`ide` , `tournament_id`)
    REFERENCES `catcher`.`identificator` (`ide` , `tournament_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_match_field1`
    FOREIGN KEY (`field_id` , `tournament_id`)
    REFERENCES `catcher`.`field` (`id` , `tournament_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `catcher`.`group`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `catcher`.`group` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `catcher`.`group` (
  `teams_count` INT NOT NULL,
  `description` VARCHAR(45) NULL COMMENT 'Nazev skupiny, napr. Skupina A',
  `ide` CHAR(3) NOT NULL,
  `tournament_id` INT NOT NULL,
  UNIQUE INDEX `description_UNIQUE` (`description` ASC)  COMMENT ' /* comment truncated */ /*Kazda skupina musi mit na turnaji jiny popisek.

*/',
  INDEX `fk_group_identificator1_idx` (`ide` ASC, `tournament_id` ASC),
  PRIMARY KEY (`ide`, `tournament_id`),
  CONSTRAINT `fk_group_identificator1`
    FOREIGN KEY (`ide` , `tournament_id`)
    REFERENCES `catcher`.`identificator` (`ide` , `tournament_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `catcher`.`group_has_team`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `catcher`.`group_has_team` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `catcher`.`group_has_team` (
  `matches_count` SMALLINT NOT NULL DEFAULT 0,
  `wins_count` SMALLINT NOT NULL DEFAULT 0,
  `losses_count` SMALLINT NOT NULL DEFAULT 0,
  `plus_count` SMALLINT NOT NULL DEFAULT 0,
  `minus_count` SMALLINT NOT NULL DEFAULT 0,
  `points_count` SMALLINT NOT NULL DEFAULT 0,
  `standing` SMALLINT NULL DEFAULT NULL,
  `team_id` INT NOT NULL,
  `group_ide` CHAR(3) NOT NULL,
  `tournament_id` INT NOT NULL,
  INDEX `fk_group_has_team_team1_idx` (`team_id` ASC),
  INDEX `fk_group_has_team_group1_idx` (`group_ide` ASC, `tournament_id` ASC),
  PRIMARY KEY (`group_ide`, `tournament_id`, `team_id`),
  CONSTRAINT `fk_group_has_team_team1`
    FOREIGN KEY (`team_id`)
    REFERENCES `catcher`.`team` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_group_has_team_group1`
    FOREIGN KEY (`group_ide` , `tournament_id`)
    REFERENCES `catcher`.`group` (`ide` , `tournament_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `catcher`.`advancement`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `catcher`.`advancement` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `catcher`.`advancement` (
  `standing` SMALLINT NOT NULL,
  `final_standing` SMALLINT NULL DEFAULT NULL,
  `next_step_ide` VARCHAR(3) NULL DEFAULT NULL,
  `group_ide` CHAR(3) NOT NULL,
  `tournament_id` INT NOT NULL,
  PRIMARY KEY (`standing`, `group_ide`, `tournament_id`),
  INDEX `fk_advancement_group1_idx` (`group_ide` ASC, `tournament_id` ASC),
  CONSTRAINT `fk_advancement_group1`
    FOREIGN KEY (`group_ide` , `tournament_id`)
    REFERENCES `catcher`.`group` (`ide` , `tournament_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `catcher`.`standing`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `catcher`.`standing` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `catcher`.`standing` (
  `tournament_id` INT NOT NULL,
  `standing` SMALLINT NOT NULL,
  `team_id` INT NULL,
  INDEX `fk_standings_tournament1_idx` (`tournament_id` ASC),
  INDEX `fk_standings_team1_idx` (`team_id` ASC),
  PRIMARY KEY (`tournament_id`, `standing`),
  CONSTRAINT `fk_standings_tournament1`
    FOREIGN KEY (`tournament_id`)
    REFERENCES `catcher`.`tournament` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_standings_team1`
    FOREIGN KEY (`team_id`)
    REFERENCES `catcher`.`team` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
COMMENT = 'Tabulka se vyplni na konci turnaje (nebo muze klidne i postu /* comment truncated */ /*pne).*/';

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `catcher`.`participation`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `catcher`.`participation` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `catcher`.`participation` (
  `tournament_id` INT NOT NULL,
  `team_id` INT NOT NULL,
  `seeding` INT NULL,
  `team_shortcut` VARCHAR(3) NOT NULL,
  PRIMARY KEY (`tournament_id`, `team_id`),
  INDEX `fk_participation_team1_idx` (`team_id` ASC),
  UNIQUE INDEX `tournament_team_shortcut_UNIQUE` (`team_shortcut` ASC, `tournament_id` ASC),
  CONSTRAINT `fk_participation_tournament1`
    FOREIGN KEY (`tournament_id`)
    REFERENCES `catcher`.`tournament` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_participation_team1`
    FOREIGN KEY (`team_id`)
    REFERENCES `catcher`.`team` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `catcher`.`api_key`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `catcher`.`api_key` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `catcher`.`api_key` (
  `key` VARCHAR(255) NOT NULL,
  `valid_to` DATETIME NOT NULL,
  `user_id` INT NOT NULL,
  PRIMARY KEY (`key`),
  INDEX `fk_api_key_user1_idx` (`user_id` ASC),
  CONSTRAINT `fk_api_key_user1`
    FOREIGN KEY (`user_id`)
    REFERENCES `catcher`.`user` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

SHOW WARNINGS;

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
