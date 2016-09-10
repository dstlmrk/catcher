-- -----------------------------------------------------
-- ignoruje cizi klice
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
-- -----------------------------------------------------
START TRANSACTION;
-- -----------------------------------------------------
INSERT INTO `test_catcher`.`division` 
(`id`, `division`) VALUES 
(1   , 'open'    ),
(2   , 'women'   ),
(3   , 'mixed'   ),
(4   , 'masters' ),
(5   , 'junior'  );
-- -----------------------------------------------------
INSERT INTO `test_catcher`.`role` 
(`id`, `role`     ) VALUES 
(1   , 'organizer'),
(2   , 'admin'    );


-- -----------------------------------------------------

-- INSERT INTO `catcher`.`user`
-- (`id`, `email`               , `password`, `api_key`                         , `role_id`) VALUES
-- (1   , 'veselj43@fit.cvut.cz', 'heslo'   , 'W1x8UmkV5RWCZOXuRmcqqnrt6qQNnjnr', 1        );
-- (2   , 'dstlmrk@gmail.com'   , 'heslo'   , 'nVFrrUXJSAXmTPp9lvZZLEyjiRVUydIg', '', NULL),
-- (3   , 'list@zlutazimnice.cz', 'heslo'   , 'M7mz4BwcdwR8QmfdKJw2w3PJj3j2YZlB', '', NULL);


-- INSERT INTO `test_catcher`.`team`
-- (`id`, `division_id`, `cald_id`, `name`             , `shortcut`, `city`          , `country`, `website`, `user_id`) VALUES
-- (1   , 1     ,      NULL, "FC Praha"         , "PRA"     , "Praha"         , "CZE" ,      NULL, NULL   ),
-- (2   , 1     ,      NULL, "FC Brno"          , "BRN"     , "Brno"          , "CZE" ,      NULL, NULL   ),
-- (3   , 1     ,      NULL, "FC Plzeň"         , "PLZ"     , "Plzeň"         , "CZE" ,      NULL, NULL   ),
-- (4   , 1     ,      NULL, "FC Ostrava"       , "OST"     , "Ostrava"       , "CZE" ,      NULL, NULL   ),
-- (5   , 1     ,      NULL, "FC Olomouc"       , "OLO"     , "Olomouc"       , "CZE" ,      NULL, NULL   ),
-- (6   , 1     ,      NULL, "FC Hradec Králové", "HKR"     , "Hradec Králové", "CZE" ,      NULL, NULL   ),
-- (7   , 1     ,      NULL, "FC Most"          , "MST"     , "Most"          , "CZE" ,      NULL, NULL   ),
-- (8   , 1     ,      NULL, "FC Cheb"          , "CHB"     , "Cheb"          , "CZE" ,      NULL, NULL   ),
-- (9   , 1     ,      NULL, "FC Jihlava"       , "JIH"     , "Jihlava"       , "CZE" ,      NULL, NULL   ),
-- (10  , 1     ,      NULL, "FC Zlín"          , "ZLI"     , "Zlín"          , "CZE" ,      NULL, NULL   ),
-- (11  , 1     ,      NULL, "FC Bratislava"    , "BRA"     , "Bratislava"    , "SVK" ,      NULL, NULL   ),
-- (12  , 1     ,      NULL, "For delete"      ,  "DEL"     , "Kralupy n.V."  , "CZE" ,      NULL, NULL   );
-- -----------------------------------------------------
-- INSERT INTO `test_catcher`.`team` 

-- id, division_id, name, shortcut, city, country, website, cald_id, user_id
-- (`id`, `name`, `division_id`, `degree`) VALUES 
-- (1   ,"FC Praha"        , 1            , 'A'     ),
-- (2   ,"FC Brno"        , 1            , 'A'     ),
-- (3   ,"FC Plzeň"        , 1            , 'A'     ),
-- (4   ,"FC Ostrava"       , 1            , 'A'     ),
-- (5   ,"FC Olomouc"        , 1            , 'A'     ),
-- (6   ,6        , 1            , 'A'     ),
-- (7   ,7        , 1            , 'A'     ),
-- (8   ,8        , 1            , 'A'     ),
-- (9   ,9        , 1            , 'A'     ),
-- (10  ,10       , 1            , 'A'     ),
-- (11  ,11       , 1            , 'A'     ),
-- (12  ,1        , 1            , 'B'     ),
-- (13  ,1        , 1            , 'C'     ),
-- (14  ,1        , 2            , 'A'     ),
-- (15  ,2        , 1            , 'B'     ),
-- (16  ,2        , 1            , 'D'     );
-- -----------------------------------------------------
-- INSERT INTO `test_catcher`.`player` 
-- (`id`, `firstname`, `lastname`, `nickname`, `number`, `ranking`, `cald_id`, `club_id`) VALUES 
-- (1   , "Matěj"    , "Novák"   , "Maty"    , 32      , NULL     , NULL     , 1        ),
-- (2   , "Martin"   , "Janda"   , "Marťas"  , 1       , NULL     , NULL     , 1        ),
-- (3   , "Pavel"    , "Kozlík"  , "Pavlík"  , NULL    , NULL     , NULL     , 1        ),
-- (4   , "Rudolf"   , "Kocur"   , "Ruda"    , 45      , NULL     , NULL     , 1        ),
-- (5   , "Jan"      , "Fridrich", "Honza"   , 73      , NULL     , NULL     , 1        ),
-- (6   , "Zdeněk"   , "Novák"   , "Zdenda"  , 24      , NULL     , NULL     , 1        ),
-- (7   , "Karel"    , "Vynnyk"  , NULL      , 37      , NULL     , NULL     , 1        ),
-- (8   , "Josef"    , "Hón"     , NULL      , 90      , NULL     , NULL     , 1        ),
-- (9   , "Bohumil"  , "Novák"   , NULL      , 10      , NULL     , NULL     , 1        ),
-- (10  , "Václav"   , "Vencl"   , NULL      , 13      , NULL     , NULL     , 1        ),
-- (11  , "Jan"      , "Krátký"  , NULL      , 11      , NULL     , NULL     , 2        ),
-- (12  , "Petr"     , "Šmejkal" , NULL      , 25      , NULL     , NULL     , 2        ),
-- (13  , "Miroslav" , "Egg"     , NULL      , 36      , NULL     , NULL     , 2        ),
-- (14  , "Vladimír" , "Šimovec" , NULL      , NULL    , NULL     , NULL     , 2        ),
-- (15  , "Tomáš"    , "Kracík"  , NULL      , 32      , NULL     , NULL     , 2        ),
-- (16  , "Ladislav" , "Stezka"  , NULL      , 11      , NULL     , NULL     , 2        ),
-- (17  , "Jiří"     , "Dytrt"   , NULL      , 8       , NULL     , NULL     , 2        ),
-- (18  , "Jaroslav" , "Stupecký", "Jarda"   , NULL    , NULL     , NULL     , 2        ),
-- (19  , "Antonín"  , "Kunc"    , "Andy"    , NULL    , NULL     , NULL     , 2        ),
-- (20  , "Jaromír"  , "Folta"   , "Jarda"   , 2       , NULL     , NULL     , 2        ),
-- (21  , "Milan"    , "Bajgar"  , "Míla"    , 27      , NULL     , NULL     , 2        ),
-- (22  , "Roman"    , "Frýdek"  , NULL      , NULL    , NULL     , NULL     , 2        ),
-- (23  , "Marek"    , "Kodera"  , NULL      , 23      , NULL     , NULL     , 2        ),
-- (24  , "Michal"   , "Charvát" , NULL      , NULL    , NULL     , NULL     , 3        ),
-- (25  , "Karel"    , "Krejčí"  , NULL      , NULL    , NULL     , NULL     , 3        ),
-- (26  , "Otto"     , "Krejčík" , NULL      , 4       , NULL     , NULL     , 3        ),
-- (27  , "František", "Bujko"   , NULL      , NULL    , NULL     , NULL     , 3        ),
-- (28  , "Lukáš"    , "Ambros"  , NULL      , 15      , NULL     , NULL     , 3        ),
-- (29  , "Ján"      , "Kočí"    , NULL      , NULL    , NULL     , NULL     , 3        ),
-- (30  , "Valerian" , "Štrobl"  , NULL      , 3       , NULL     , NULL     , 3        ),
-- (31  , "Jozef"    , "Vajrauch", NULL      , NULL    , NULL     , NULL     , 3        ),
-- (32  , "Adam"     , "Nevole"  , NULL      , NULL    , NULL     , NULL     , 3        ),
-- (33  , "Stanislav", "Sivák"   , NULL      , NULL    , NULL     , NULL     , 3        ),
-- (34  , "Zdeněk"   , "Borýsek" , NULL      , 5       , NULL     , NULL     , NULL     ),
-- (35  , "Jindřich" , "Vavřich" , NULL      , NULL    , NULL     , NULL     , NULL     ),
-- (36  , "Jan"      , "Čejka"   , NULL      , 9       , NULL     , NULL     , NULL     ),
-- (37  , "Jiří"     , "Šindelář", NULL      , 17      , NULL     , NULL     , NULL     ),
-- (38  , "Petr"     , "Říha"    , NULL      , NULL    , NULL     , NULL     , NULL     ),
-- (39  , "Milan"    , "Havelka" , NULL      , 6       , NULL     , NULL     , NULL     ),
-- (40  , "Miloš"    , "Švehla"  , NULL      , NULL    , NULL     , NULL     , NULL     ),
-- (41  , "Tomáš"    , "Dvořák"  , NULL      , 12      , NULL     , NULL     , NULL     ),
-- (42  , "Jaroslav" , "Pernica" , NULL      , 15      , NULL     , NULL     , NULL     );
-- -----------------------------------------------------
COMMIT;