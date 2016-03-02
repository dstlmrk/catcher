SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

CREATE SCHEMA IF NOT EXISTS `catcher` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci ;
SHOW WARNINGS;
USE `catcher` ;

-- -----------------------------------------------------
-- Table `catcher`.`user`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `catcher`.`user` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `catcher`.`user` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nickname` VARCHAR(45) NULL,
  `email` VARCHAR(90) NOT NULL,
  `password` VARCHAR(45) NOT NULL,
  `created_at` TIMESTAMP NULL,
  `last_login_at` TIMESTAMP NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `catcher`.`role`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `catcher`.`role` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `catcher`.`role` (
  `role` VARCHAR(45) NOT NULL,
  `user_id` INT NOT NULL,
  INDEX `fk_role_user1_idx` (`user_id` ASC),
  PRIMARY KEY (`role`),
  CONSTRAINT `fk_role_user1`
    FOREIGN KEY (`user_id`)
    REFERENCES `catcher`.`user` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `catcher`.`club`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `catcher`.`club` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `catcher`.`club` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `user_id` INT NULL COMMENT 'Do budoucna by asi melo byt not null.',
  `cald_id` VARCHAR(45) NULL,
  `name` VARCHAR(45) NOT NULL,
  `shortcut` VARCHAR(3) NOT NULL,
  `city` VARCHAR(45) NULL,
  `country` VARCHAR(3) NULL COMMENT 'ISO 3166-1 alpha-3\n',
  PRIMARY KEY (`id`),
  UNIQUE INDEX `shortcut_UNIQUE` (`shortcut` ASC),
  UNIQUE INDEX `name_UNIQUE` (`name` ASC),
  INDEX `fk_club_user1_idx` (`user_id` ASC),
  CONSTRAINT `fk_club_user1`
    FOREIGN KEY (`user_id`)
    REFERENCES `catcher`.`user` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `catcher`.`player`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `catcher`.`player` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `catcher`.`player` (
  `id` INT NOT NULL,
  `firstname` VARCHAR(45) NOT NULL,
  `lastname` VARCHAR(45) NOT NULL,
  `nickname` VARCHAR(45) NULL,
  `number` VARCHAR(45) NULL,
  `cald_id` INT NULL,
  `ranking` FLOAT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `cald_id_UNIQUE` (`cald_id` ASC))
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `catcher`.`division`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `catcher`.`division` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `catcher`.`division` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `division` VARCHAR(10) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `catcher`.`team`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `catcher`.`team` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `catcher`.`team` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `club_id` INT NOT NULL,
  `division_id` INT NOT NULL,
  `degree` VARCHAR(1) NOT NULL DEFAULT 'A',
  INDEX `fk_team_club1_idx` (`club_id` ASC),
  PRIMARY KEY (`id`),
  INDEX `fk_team_category1_idx` (`division_id` ASC),
  UNIQUE INDEX `unique_index` (`club_id` ASC, `division_id` ASC, `degree` ASC),
  CONSTRAINT `fk_team_club1`
    FOREIGN KEY (`club_id`)
    REFERENCES `catcher`.`club` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_team_category1`
    FOREIGN KEY (`division_id`)
    REFERENCES `catcher`.`division` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `catcher`.`club_has_player`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `catcher`.`club_has_player` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `catcher`.`club_has_player` (
  `club_id` INT NOT NULL,
  `player_id` INT NOT NULL,
  PRIMARY KEY (`club_id`, `player_id`),
  INDEX `fk_club_has_player_player1_idx` (`player_id` ASC),
  INDEX `fk_club_has_player_club1_idx` (`club_id` ASC),
  CONSTRAINT `fk_club_has_player_club1`
    FOREIGN KEY (`club_id`)
    REFERENCES `catcher`.`club` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_club_has_player_player1`
    FOREIGN KEY (`player_id`)
    REFERENCES `catcher`.`player` (`id`)
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
  `cald_tournament` TINYINT(1) NOT NULL,
  `teams` INT NOT NULL,
  `terminated` TINYINT(1) NOT NULL DEFAULT FALSE,
  `name` VARCHAR(45) NULL,
  `start_on` DATETIME NULL,
  `city` VARCHAR(45) NULL,
  `country` VARCHAR(3) NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_tournament_category1_idx` (`division_id` ASC),
  CONSTRAINT `fk_tournament_category1`
    FOREIGN KEY (`division_id`)
    REFERENCES `catcher`.`division` (`id`)
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
  `name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`, `tournament_id`),
  INDEX `fk_field_tournament1_idx` (`tournament_id` ASC),
  UNIQUE INDEX `name_UNIQUE` (`name` ASC, `tournament_id` ASC)  COMMENT ' /* comment truncated */ /*Na turnaji jsou ruzna hriste.*/',
  CONSTRAINT `fk_field_tournament1`
    FOREIGN KEY (`tournament_id`)
    REFERENCES `catcher`.`tournament` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `catcher`.`team_at_tournament`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `catcher`.`team_at_tournament` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `catcher`.`team_at_tournament` (
  `tournament_id` INT NOT NULL,
  `team_id` INT NOT NULL,
  `seeding` INT NULL,
  PRIMARY KEY (`tournament_id`, `team_id`),
  INDEX `fk_tournament_has_team_team1_idx` (`team_id` ASC),
  INDEX `fk_tournament_has_team_tournament1_idx` (`tournament_id` ASC),
  CONSTRAINT `fk_tournament_has_team_tournament1`
    FOREIGN KEY (`tournament_id`)
    REFERENCES `catcher`.`tournament` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_tournament_has_team_team1`
    FOREIGN KEY (`team_id`)
    REFERENCES `catcher`.`team` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `catcher`.`player_at_tournament`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `catcher`.`player_at_tournament` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `catcher`.`player_at_tournament` (
  `tournament_id` INT NOT NULL,
  `team_id` INT NOT NULL,
  `player_id` INT NOT NULL,
  `assists` VARCHAR(45) NOT NULL DEFAULT 0,
  `scores` VARCHAR(45) NOT NULL DEFAULT 0,
  `total` VARCHAR(45) NOT NULL DEFAULT 0,
  `matches` VARCHAR(45) NOT NULL DEFAULT 0,
  PRIMARY KEY (`tournament_id`, `team_id`, `player_id`),
  INDEX `fk_tournament_has_team_has_player_player1_idx` (`player_id` ASC),
  INDEX `fk_tournament_has_team_has_player_tournament_has_team1_idx` (`tournament_id` ASC, `team_id` ASC),
  CONSTRAINT `fk_tournament_has_team_has_player_tournament_has_team1`
    FOREIGN KEY (`tournament_id` , `team_id`)
    REFERENCES `catcher`.`team_at_tournament` (`tournament_id` , `team_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_tournament_has_team_has_player_player1`
    FOREIGN KEY (`player_id`)
    REFERENCES `catcher`.`player` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `catcher`.`tournament_has_identificator`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `catcher`.`tournament_has_identificator` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `catcher`.`tournament_has_identificator` (
  `identificator_id` INT NOT NULL,
  `tournament_id` INT NOT NULL,
  `identificator` VARCHAR(3) NOT NULL,
  INDEX `fk_table1_tournament1_idx` (`tournament_id` ASC),
  PRIMARY KEY (`identificator_id`),
  UNIQUE INDEX `identificator_UNIQUE` (`tournament_id` ASC, `identificator` ASC),
  CONSTRAINT `fk_table1_tournament1`
    FOREIGN KEY (`tournament_id`)
    REFERENCES `catcher`.`tournament` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
COMMENT = 'Tahle tabulka je tu proto, aby nevznikaly duplicitni identif /* comment truncated */ /*icatory napric group a match.

tournament_id a indentificator jsou unikatni dvojice*/';

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `catcher`.`match`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `catcher`.`match` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `catcher`.`match` (
  `id` INT NOT NULL,
  `tournament_id` INT NOT NULL,
  `identificator_id` INT NOT NULL,
  `team_id_home` INT NULL,
  `team_id_away` INT NULL,
  `field_id` INT NOT NULL,
  `start_time` DATETIME NOT NULL,
  `terminated` TINYINT(1) NOT NULL DEFAULT FALSE,
  `score_home` TINYINT NULL,
  `score_away` TINYINT NULL,
  `spirit_away` TINYINT NULL,
  `spirit_home` TINYINT NULL,
  `description` VARCHAR(45) NULL,
  `final_standing_winner` SMALLINT NULL,
  `final_standing_looser` SMALLINT NULL,
  `flip` TINYINT(1) NULL COMMENT '0 - home, 1 - away',
  `identificator_id_winner` INT NULL,
  `identificator_id_looser` INT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_game_tournament1_idx` (`tournament_id` ASC),
  INDEX `fk_match_team1_idx` (`team_id_home` ASC),
  INDEX `fk_match_team2_idx` (`team_id_away` ASC),
  INDEX `fk_match_field1_idx` (`field_id` ASC),
  INDEX `fk_match_tournament_has_identificator1_idx` (`identificator_id` ASC),
  INDEX `fk_match_tournament_has_identificator2_idx` (`identificator_id_winner` ASC),
  INDEX `fk_match_tournament_has_identificator3_idx` (`identificator_id_looser` ASC),
  CONSTRAINT `fk_game_tournament1`
    FOREIGN KEY (`tournament_id`)
    REFERENCES `catcher`.`tournament` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_match_team1`
    FOREIGN KEY (`team_id_home`)
    REFERENCES `catcher`.`team` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_match_team2`
    FOREIGN KEY (`team_id_away`)
    REFERENCES `catcher`.`team` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_match_field1`
    FOREIGN KEY (`field_id`)
    REFERENCES `catcher`.`field` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_match_tournament_has_identificator1`
    FOREIGN KEY (`identificator_id`)
    REFERENCES `catcher`.`tournament_has_identificator` (`identificator_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_match_tournament_has_identificator2`
    FOREIGN KEY (`identificator_id_winner`)
    REFERENCES `catcher`.`tournament_has_identificator` (`identificator_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_match_tournament_has_identificator3`
    FOREIGN KEY (`identificator_id_looser`)
    REFERENCES `catcher`.`tournament_has_identificator` (`identificator_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `catcher`.`player_at_match`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `catcher`.`player_at_match` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `catcher`.`player_at_match` (
  `match_id` INT NOT NULL,
  `tournament_id` INT NOT NULL,
  `team_id` INT NOT NULL,
  `player_id` INT NOT NULL,
  `asissts` INT NOT NULL,
  `scores` INT NOT NULL,
  `total` INT NOT NULL,
  PRIMARY KEY (`match_id`, `tournament_id`, `team_id`, `player_id`),
  INDEX `fk_match_has_tournament_has_player_tournament_has_player1_idx` (`tournament_id` ASC, `team_id` ASC, `player_id` ASC),
  INDEX `fk_match_has_tournament_has_player_match1_idx` (`match_id` ASC),
  CONSTRAINT `fk_match_has_tournament_has_player_match1`
    FOREIGN KEY (`match_id`)
    REFERENCES `catcher`.`match` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_match_has_tournament_has_player_tournament_has_player1`
    FOREIGN KEY (`tournament_id` , `team_id` , `player_id`)
    REFERENCES `catcher`.`player_at_tournament` (`tournament_id` , `team_id` , `player_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `catcher`.`point`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `catcher`.`point` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `catcher`.`point` (
  `match_id` INT NOT NULL,
  `order` INT NOT NULL,
  `player_id_assist` INT NULL,
  `player_id_score` INT NULL,
  `score_home` INT NOT NULL,
  `score_away` INT NOT NULL,
  `home_point` TINYINT(1) NOT NULL,
  PRIMARY KEY (`match_id`, `order`),
  INDEX `fk_point_player1_idx` (`player_id_assist` ASC),
  INDEX `fk_point_player2_idx` (`player_id_score` ASC),
  CONSTRAINT `fk_point_match1`
    FOREIGN KEY (`match_id`)
    REFERENCES `catcher`.`match` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_point_player1`
    FOREIGN KEY (`player_id_assist`)
    REFERENCES `catcher`.`player` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_point_player2`
    FOREIGN KEY (`player_id_score`)
    REFERENCES `catcher`.`player` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `catcher`.`team_spirit_at_match`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `catcher`.`team_spirit_at_match` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `catcher`.`team_spirit_at_match` (
  `match_id` INT NOT NULL,
  `team_id` INT NOT NULL COMMENT 'Getting team\n',
  `comment` VARCHAR(255) NULL,
  `rules` TINYINT NOT NULL,
  `fouls` TINYINT NOT NULL,
  `fair` TINYINT NOT NULL,
  `positive` TINYINT NOT NULL,
  `communication` TINYINT NOT NULL,
  `total` TINYINT NOT NULL,
  PRIMARY KEY (`match_id`, `team_id`),
  INDEX `fk_match_spirit_match1_idx` (`match_id` ASC),
  CONSTRAINT `fk_match_spirit_match1`
    FOREIGN KEY (`match_id`)
    REFERENCES `catcher`.`match` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `catcher`.`team_spirit_at_tournament`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `catcher`.`team_spirit_at_tournament` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `catcher`.`team_spirit_at_tournament` (
  `tournament_id` INT NOT NULL,
  `team_id` INT NOT NULL,
  `rules_avg` FLOAT NULL,
  `rules_avg_given` FLOAT NULL,
  `fouls_avg` FLOAT NULL,
  `fouls_avg_given` FLOAT NULL,
  `fair_avg` FLOAT NULL,
  `fair_avg_given` FLOAT NULL,
  `positive_avg` FLOAT NULL,
  `positive_avg_given` FLOAT NULL,
  `communition_avg` FLOAT NULL,
  `communition_avg_given` FLOAT NULL,
  `total_avg` FLOAT NULL,
  `total_avg_given` FLOAT NULL,
  `matches` SMALLINT NOT NULL DEFAULT 0,
  PRIMARY KEY (`tournament_id`, `team_id`),
  INDEX `fk_team_spirit_tournament_team1_idx` (`tournament_id` ASC, `team_id` ASC),
  CONSTRAINT `fk_team_spirit_tournament_team1`
    FOREIGN KEY (`tournament_id` , `team_id`)
    REFERENCES `catcher`.`team_at_tournament` (`tournament_id` , `team_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
COMMENT = 'TODO: Tahle tabulka se muze pouzit v budoucnu pro team_spiri /* comment truncated */ /*t_overall*/';

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `catcher`.`group`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `catcher`.`group` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `catcher`.`group` (
  `id` VARCHAR(45) NOT NULL,
  `identificator_id` INT NOT NULL,
  `tournament_id` INT NOT NULL,
  `teams` INT NOT NULL,
  `description` VARCHAR(45) NOT NULL COMMENT 'Nazev skupiny, napr. Skupina A',
  PRIMARY KEY (`id`),
  UNIQUE INDEX `description_UNIQUE` (`description` ASC, `tournament_id` ASC)  COMMENT ' /* comment truncated */ /*Kazda skupina musi mit na turnaji jiny popisek.

*/',
  INDEX `fk_group_tournament_has_identificator1_idx` (`identificator_id` ASC),
  INDEX `fk_group_tournament1_idx` (`tournament_id` ASC),
  CONSTRAINT `fk_group_tournament_has_identificator1`
    FOREIGN KEY (`identificator_id`)
    REFERENCES `catcher`.`tournament_has_identificator` (`identificator_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_group_tournament1`
    FOREIGN KEY (`tournament_id`)
    REFERENCES `catcher`.`tournament` (`id`)
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
  `group_id` VARCHAR(3) NOT NULL,
  `tournament_id` INT NOT NULL,
  `team_id` INT NOT NULL,
  `matches` SMALLINT NOT NULL DEFAULT 0,
  `wins` SMALLINT NOT NULL DEFAULT 0,
  `losses` SMALLINT NOT NULL DEFAULT 0,
  `plus` SMALLINT NOT NULL DEFAULT 0,
  `minus` SMALLINT NOT NULL DEFAULT 0,
  `points` SMALLINT NOT NULL DEFAULT 0,
  `standing` SMALLINT NULL,
  PRIMARY KEY (`group_id`, `tournament_id`, `team_id`),
  INDEX `fk_group_has_team_at_tournament_team_at_tournament1_idx` (`tournament_id` ASC, `team_id` ASC),
  CONSTRAINT `fk_group_has_team_at_tournament_team_at_tournament1`
    FOREIGN KEY (`tournament_id` , `team_id`)
    REFERENCES `catcher`.`team_at_tournament` (`tournament_id` , `team_id`)
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
  `group_id` VARCHAR(45) NOT NULL,
  `final_standing` SMALLINT NULL,
  `identificator_id` INT NOT NULL,
  PRIMARY KEY (`standing`, `group_id`),
  INDEX `fk_advancement_group1_idx` (`group_id` ASC),
  INDEX `fk_advancement_tournament_has_identificator1_idx` (`identificator_id` ASC),
  CONSTRAINT `fk_advancement_group1`
    FOREIGN KEY (`group_id`)
    REFERENCES `catcher`.`group` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_advancement_tournament_has_identificator1`
    FOREIGN KEY (`identificator_id`)
    REFERENCES `catcher`.`tournament_has_identificator` (`identificator_id`)
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
  `team_id` INT NOT NULL,
  `standing` SMALLINT NOT NULL,
  INDEX `fk_standings_tournament1_idx` (`tournament_id` ASC),
  INDEX `fk_standings_team1_idx` (`team_id` ASC),
  PRIMARY KEY (`tournament_id`, `team_id`, `standing`),
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
-- Table `catcher`.`user_has_tournament`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `catcher`.`user_has_tournament` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `catcher`.`user_has_tournament` (
  `user_id` INT NOT NULL,
  `tournament_id` INT NOT NULL,
  PRIMARY KEY (`user_id`, `tournament_id`),
  INDEX `fk_user_has_tournament_tournament1_idx` (`tournament_id` ASC),
  INDEX `fk_user_has_tournament_user1_idx` (`user_id` ASC),
  CONSTRAINT `fk_user_has_tournament_user1`
    FOREIGN KEY (`user_id`)
    REFERENCES `catcher`.`user` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_user_has_tournament_tournament1`
    FOREIGN KEY (`tournament_id`)
    REFERENCES `catcher`.`tournament` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

SHOW WARNINGS;

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;