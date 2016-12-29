# TODO: zustanou tady imputy, ktere nebudu provadet pres API
-- -----------------------------------------------------
-- Data for table `catcher`.`role`
-- -----------------------------------------------------
START TRANSACTION;
USE `catcher`;
INSERT INTO `catcher`.`role` (`id`, `type`) VALUES (1, 'club');
INSERT INTO `catcher`.`role` (`id`, `type`) VALUES (2, 'organizer');
INSERT INTO `catcher`.`role` (`id`, `type`) VALUES (3, 'admin');
COMMIT;

-- -----------------------------------------------------
-- Data for table `catcher`.`user`
-- -----------------------------------------------------
# START TRANSACTION;
# USE `catcher`;
# INSERT INTO `catcher`.`user` (`id`, `email`, `password`, `created_at`, `role_id`) VALUES
# (1, 'veselj43@fit.cvut.cz', 'catcher_heslo', '2016-12-15 05:31:21', 2),
# (2, 'dstlmrk@gmail.com'   , 'catcher_heslo', '2016-12-15 05:31:21', 2),
# (3, 'list@zlutazimnice.cz', 'catcher_heslo', '2016-12-15 05:31:21', 0);
# COMMIT;


-- -----------------------------------------------------
-- Data for table `catcher`.`api_key`
-- -----------------------------------------------------
# START TRANSACTION;
# USE `catcher`;
# INSERT INTO `catcher`.`api_key` (`key`, `valid_to`,  `user_id`) VALUES ('W1x8UmkV5RWCZOXuRmcqqnrt6qQNnjnQ', '2017-01-31 23:59:59', 1);
# INSERT INTO `catcher`.`api_key` (`key`, `valid_to`,  `user_id`) VALUES ('nVFrrUXJSAXmTPp9lvZZLEyjiRVUydIQ', '2017-01-31 23:59:59', 2);
# # INSERT INTO `catcher`.`api_key` (`key`, `valid_to`,  `user_id`) VALUES ('M7mz4BwcdwR8QmfdKJw2w3PJj3j2YZlQ', '2017-01-31 23:59:59', 3);
# COMMIT;

-- -----------------------------------------------------
-- Data for table `catcher`.`division`
-- -----------------------------------------------------
# START TRANSACTION;
# USE `catcher`;
# INSERT INTO `catcher`.`division` (`id`, `division`) VALUES (1, 'open');
# INSERT INTO `catcher`.`division` (`id`, `division`) VALUES (2, 'women');
# INSERT INTO `catcher`.`division` (`id`, `division`) VALUES (3, 'mixed');
# INSERT INTO `catcher`.`division` (`id`, `division`) VALUES (4, 'masters');
# INSERT INTO `catcher`.`division` (`id`, `division`) VALUES (5, 'junior');
#
# COMMIT;
