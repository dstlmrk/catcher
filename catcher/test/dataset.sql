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
INSERT INTO `test_catcher`.`club`
(`id`, `user_id`, `cald_id`, `name`             , `shortcut`, `city`          , `country`) VALUES
(1   , NULL     ,      NULL, "FC Praha"         , "PRA"     , "Praha"         , "CZE"    ),
(2   , NULL     ,      NULL, "FC Brno"          , "BRN"     , "Brno"          , "CZE"    ),
(3   , NULL     ,      NULL, "FC Plzeň"         , "PLZ"     , "Plzeň"         , "CZE"    ),
(4   , NULL     ,      NULL, "FC Ostrava"       , "OST"     , "Ostrava"       , "CZE"    ),
(5   , NULL     ,      NULL, "FC Olomouc"       , "OLO"     , "Olomouc"       , "CZE"    ),
(6   , NULL     ,      NULL, "FC Hradec Králové", "HKR"     , "Hradec Králové", "CZE"    ),
(7   , NULL     ,      NULL, "FC Most"          , "MST"     , "Most"          , "CZE"    ),
(8   , NULL     ,      NULL, "FC Cheb"          , "CHB"     , "Cheb"          , "CZE"    ),
(9   , NULL     ,      NULL, "FC Jihlava"       , "JIH"     , "Jihlava"       , "CZE"    ),
(10  , NULL     ,      NULL, "FC Zlín"          , "ZLI"     , "Zlín"          , "CZE"    ),
(11  , NULL     ,      NULL, "FC Bratislava"    , "BRA"     , "Bratislava"    , "SVK"    ),
(12  , NULL     ,      NULL, "For delete"      ,  "DEL"     , "Kralupy n.V."  , "CZE"    );
-- -----------------------------------------------------
INSERT INTO `test_catcher`.`team` 
(`id`, `club_id`, `division_id`, `degree`) VALUES 
(1   ,1        , 1            , 'A'     ),
(2   ,2        , 1            , 'A'     ),
(3   ,3        , 1            , 'A'     ),
(4   ,4        , 1            , 'A'     ),
(5   ,5        , 1            , 'A'     ),
(6   ,6        , 1            , 'A'     ),
(7   ,7        , 1            , 'A'     ),
(8   ,8        , 1            , 'A'     ),
(9   ,9        , 1            , 'A'     ),
(10  ,10       , 1            , 'A'     ),
(11  ,11       , 1            , 'A'     ),
(12  ,1        , 1            , 'B'     ),
(13  ,1        , 1            , 'C'     ),
(14  ,1        , 2            , 'A'     ),
(15  ,2        , 1            , 'B'     ),
(16  ,2        , 1            , 'D'     );
-- -----------------------------------------------------
INSERT INTO `test_catcher`.`player` 
(`id`, `firstname`, `lastname`, `nickname`, `number`, `ranking`, `cald_id`, `club_id`) VALUES 
(1   , "Matěj"    , "Novák"   , "Maty"    , 32      , NULL     , NULL     , 1        ),
(2   , "Martin"   , "Janda"   , "Marťas"  , 1       , NULL     , NULL     , 1        ),
(3   , "Pavel"    , "Kozlík"  , "Pavlík"  , NULL    , NULL     , NULL     , 1        ),
(4   , "Rudolf"   , "Kocur"   , "Ruda"    , 45      , NULL     , NULL     , 1        ),
(5   , "Jan"      , "Fridrich", "Honza"   , 73      , NULL     , NULL     , 1        ),
(6   , "Zdeněk"   , "Novák"   , "Zdenda"  , 24      , NULL     , NULL     , 1        ),
(7   , "Karel"    , "Vynnyk"  , NULL      , 37      , NULL     , NULL     , 1        ),
(8   , "Josef"    , "Hón"     , NULL      , 90      , NULL     , NULL     , 1        ),
(9   , "Bohumil"  , "Novák"   , NULL      , 10      , NULL     , NULL     , 1        ),
(10  , "Václav"   , "Vencl"   , NULL      , 13      , NULL     , NULL     , 1        ),
(12  , "Petr"     , "Šmejkal" , NULL      , 25      , NULL     , NULL     , 2        ),
(13  , "Miroslav" , "Egg"     , NULL      , 36      , NULL     , NULL     , 2        ),
(14  , "Vladimír" , "Šimovec" , NULL      , NULL    , NULL     , NULL     , 2        ),
(15  , "Tomáš"    , "Kracík"  , NULL      , 32      , NULL     , NULL     , 2        ),
(16  , "Ladislav" , "Stezka"  , NULL      , 11      , NULL     , NULL     , 2        ),
(17  , "Jiří"     , "Dytrt"   , NULL      , 8       , NULL     , NULL     , 2        ),
(18  , "Jaroslav" , "Stupecký", "Jarda"   , NULL    , NULL     , NULL     , 2        ),
(19  , "Antonín"  , "Kunc"    , "Andy"    , NULL    , NULL     , NULL     , 2        ),
(20  , "Jaromír"  , "Folta"   , "Jarda"   , 2       , NULL     , NULL     , 2        ),
(21  , "Milan"    , "Bajgar"  , "Míla"    , 27      , NULL     , NULL     , 2        ),
(22  , "Roman"    , "Frýdek"  , NULL      , NULL    , NULL     , NULL     , 2        ),
(23  , "Marek"    , "Kodera"  , NULL      , 23      , NULL     , NULL     , 2        ),
(24  , "Michal"   , "Charvát" , NULL      , NULL    , NULL     , NULL     , 3        ),
(25  , "Karel"    , "Krejčí"  , NULL      , NULL    , NULL     , NULL     , 3        ),
(26  , "Otto"     , "Krejčík" , NULL      , 4       , NULL     , NULL     , 3        ),
(27  , "František", "Bujko"   , NULL      , NULL    , NULL     , NULL     , 3        ),
(28  , "Lukáš"    , "Ambros"  , NULL      , 15      , NULL     , NULL     , 3        ),
(29  , "Ján"      , "Kočí"    , NULL      , NULL    , NULL     , NULL     , 3        ),
(30  , "Valerian" , "Štrobl"  , NULL      , 3       , NULL     , NULL     , 3        ),
(31  , "Jozef"    , "Vajrauch", NULL      , NULL    , NULL     , NULL     , 3        ),
(32  , "Adam"     , "Nevole"  , NULL      , NULL    , NULL     , NULL     , 3        ),
(33  , "Stanislav", "Sivák"   , NULL      , NULL    , NULL     , NULL     , 3        ),
(34  , "Zdeněk"   , "Borýsek" , NULL      , 5       , NULL     , NULL     , NULL     ),
(35  , "Jindřich" , "Vavřich" , NULL      , NULL    , NULL     , NULL     , NULL     ),
(36  , "Jan"      , "Čejka"   , NULL      , 9       , NULL     , NULL     , NULL     ),
(37  , "Jiří"     , "Šindelář", NULL      , 17      , NULL     , NULL     , NULL     ),
(38  , "Petr"     , "Říha"    , NULL      , NULL    , NULL     , NULL     , NULL     ),
(39  , "Milan"    , "Havelka" , NULL      , 6       , NULL     , NULL     , NULL     ),
(40  , "Miloš"    , "Švehla"  , NULL      , NULL    , NULL     , NULL     , NULL     ),
(41  , "Tomáš"    , "Dvořák"  , NULL      , 12      , NULL     , NULL     , NULL     ),
(42  , "Jaroslav" , "Pernica" , NULL      , 15      , NULL     , NULL     , NULL     );
-- -----------------------------------------------------
COMMIT;