CREATE DATABASE article_spride;


CREATE TABLE IF NOT EXISTS article(
  title VARCHAR(200) NOT NULL ,
  create_date DATE,
  url VARCHAR(300) NOT NULL ,
  url_object_id VARCHAR(50) NOT NULL PRIMARY KEY,
  front_image_url VARCHAR(300),
  front_image_path VARCHAR(200),
  commont_nums INT(11) NOT NULL DEFAULT 0,
  fav_nums INT(11) NOT NULL DEFAULT 0,
  praise_nums INT(11) NOT NULL DEFAULT 0,
  tags VARCHAR(200),
  content LONGTEXT NOT NULL
);