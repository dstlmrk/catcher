-- ignores foreign keys
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
-- --------------------------------------------------------------------
START TRANSACTION;
-- --------------------------------------------------------------------
INSERT INTO `test_catcher`.`division`
(`id`, `type`) VALUES
(1   , 'open'    ),
(2   , 'women'   ),
(3   , 'mixed'   ),
(4   , 'masters' ),
(5   , 'junior'  );
-- --------------------------------------------------------------------
INSERT INTO `test_catcher`.`role`
(`id`, `type`     ) VALUES
(1   , 'organizer'),
(2   , 'admin'    );
-- --------------------------------------------------------------------
COMMIT;