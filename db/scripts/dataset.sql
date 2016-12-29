-- -----------------------------------------------------
-- Data for table `catcher`.`role`
-- -----------------------------------------------------

-- TODO: PRESUNOUT POD init_data.py
START TRANSACTION;
USE `catcher`;
INSERT INTO `catcher`.`role` (`id`, `role`) VALUES (0, 'club');
INSERT INTO `catcher`.`role` (`id`, `role`) VALUES (1, 'organizer');
INSERT INTO `catcher`.`role` (`id`, `role`) VALUES (2, 'admin');

COMMIT;

-- -----------------------------------------------------
-- Data for table `catcher`.`user`
-- -----------------------------------------------------
# START TRANSACTION;
# USE `catcher`;
# INSERT INTO `catcher`.`user` (`id`, `email`, `password`, `api_key`, `created_at`, `role_id`) VALUES
# (1, 'veselj43@fit.cvut.cz', 'catcher_heslo', 'W1x8UmkV5RWCZOXuRmcqqnrt6qQNnjnQ', '', 2),
# (2, 'dstlmrk@gmail.com'   , 'catcher_heslo', 'nVFrrUXJSAXmTPp9lvZZLEyjiRVUydIQ', '', 2),
# (3, 'list@zlutazimnice.cz', 'catcher_heslo', 'M7mz4BwcdwR8QmfdKJw2w3PJj3j2YZlQ', '', 0);
#
# COMMIT;

-- -----------------------------------------------------
-- Data for table `catcher`.`division`
-- -----------------------------------------------------
START TRANSACTION;
USE `catcher`;
INSERT INTO `catcher`.`division` (`id`, `division`) VALUES (1, 'open');
INSERT INTO `catcher`.`division` (`id`, `division`) VALUES (2, 'women');
INSERT INTO `catcher`.`division` (`id`, `division`) VALUES (3, 'mixed');
INSERT INTO `catcher`.`division` (`id`, `division`) VALUES (4, 'masters');
INSERT INTO `catcher`.`division` (`id`, `division`) VALUES (5, 'junior');

COMMIT;
