/* Drop tables with foreign keys first to
   maintain referential integrity
*/

delete from stock_price;
drop table stock_price;

delete from stock_dividend;
drop table stock_dividend;

delete from stock;
drop table stock;

delete from book;
drop table book;

delete from poem;
drop table poem;

delete from lyric;
drop table lyric;

delete from custom;
drop table custom;

delete from text;
drop table text;

CREATE TABLE stock(
  ticker         varchar(10) UNIQUE  NOT NULL,
  stock_index    varchar(20)  NOT NULL,
  company_name   varchar(100) NOT NULL,
  PRIMARY KEY    (ticker, stock_index)
);

CREATE TABLE stock_price(
  ticker         varchar(10) NOT NULL,
  pdate          date        NOT NULL,
  open_price     numeric(12,4),
  close_price    numeric(12,4),
  PRIMARY KEY    (ticker, pdate),
  FOREIGN KEY (ticker) REFERENCES stock(ticker)
);

CREATE TABLE stock_dividend(
  ticker        varchar(10) NOT NULL,
  ddate         date        NOT NULL,
  ex_date       date        NOT NULL,
  price         numeric(12,4) NOT NULL,
  PRIMARY KEY   (ticker, ddate),
  FOREIGN KEY   (ticker) REFERENCES stock(ticker)
);

CREATE TABLE text(
  author_name    varchar(100),
  file_location  varchar(100) NOT NULL PRIMARY KEY,
  description    text,
  title          varchar(100),
  word_count     int
);
   

CREATE TABLE book(
  pub_date       date,
  ISBN           numeric(13)
)INHERITS(text);

CREATE TABLE poem(
  pub_date       date
)INHERITS(text);

CREATE TABLE lyric(
  song           varchar(50),
  album          varchar(50)
 )INHERITS(text);

CREATE TABLE custom(
 )INHERITS(text);

  
  


