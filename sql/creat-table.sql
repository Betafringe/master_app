DROP TABLE IF EXISTS `Comment`;
CREATE TABLE `Comment` (
  `comm_id` int(11) NOT NULL auto_increment,
  `content` varchar(512) CHARACTER SET utf8,
	`car_name` varchar(64) CHARACTER SET utf8,
  PRIMARY KEY (`comm_id`)
) ENGINE=InnoDB;

DROP TABLE IF EXISTS `Sentiment`;
CREATE TABLE `Sentiment` (
  `senti_id` int(11) NOT NULL auto_increment,
  `comm_id` int(11) NOT NULL,
	`cate_id` int(11) NOT NULL,
	`senti_value` int(11) NOT NULL,
  PRIMARY KEY (`senti_id`)
) ENGINE=InnoDB;

DROP TABLE IF EXISTS `Category`;
CREATE TABLE `Category` (
  `cate_id` int(11) NOT NULL,
	`cate_name` varchar(64) CHARACTER SET utf8,
  PRIMARY KEY (`cate_id`)
) ENGINE=InnoDB;

DROP TABLE IF EXISTS `Sentiment_Aspect_word`;
CREATE TABLE `Sentiment_Aspect_word` (
  `senti_id` int(11) NOT NULL,
  `aspect_word` varchar(64) NOT NULL,
  PRIMARY KEY (`senti_id`, `aspect_word`)
) ENGINE=InnoDB;