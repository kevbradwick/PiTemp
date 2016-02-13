CREATE TABLE `readings` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `location` varchar(30) NOT NULL DEFAULT 'UNKNOWN',
  `reading_time` datetime NOT NULL,
  `celcius` float(5,2) NOT NULL,
  `farenheit` float(5,2) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
