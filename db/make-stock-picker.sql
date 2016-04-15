/* Drop tables with foreign keys first to
   maintain referential integrity
*/

delete from stock_prices;
drop table stock_prices;

delete from stock_dividends;
drop table stock_dividends;

/*
delete from companies;
drop table companies;
*/


delete from stock_volumes;
drop table stock_volumes;

delete from stocks;
drop table stocks;

delete from text;
drop table text;

CREATE TABLE stocks(
  ticker         varchar(10) UNIQUE  NOT NULL,
  stock_index    varchar(20)  NOT NULL,
  company_name   varchar(100) NOT NULL,
  start_date     date,
  end_date       date, 
  PRIMARY KEY    (ticker, stock_index)
);

/*
CREATE TABLE companies(
  ticker         varchar(10) NOT NULL,
  name           varchar(200) NOT NULL,
  sector         varchar(100),
  industry       varchar(100),
  full_time_emps integer,
  PRIMARY KEY    (ticker, name),
  FOREIGN KEY (ticker) REFERENCES stocks(ticker) ON DELETE SET NULL ON UPDATE SET NULL
);   
*/


CREATE TABLE stock_prices(
  ticker         varchar(10) NOT NULL,
  pdate          date        NOT NULL,
  open_price     numeric(12,4),
  close_price    numeric(12,4),
  high           numeric(12,4),
  low            numeric(12,4),
  PRIMARY KEY    (ticker, pdate),
  FOREIGN KEY (ticker) REFERENCES stocks(ticker)  ON DELETE SET NULL ON UPDATE SET NULL
);

CREATE TABLE stock_dividends(
  ticker        varchar(10) NOT NULL,
  ddate         date        NOT NULL,
  price         numeric(14,6) NOT NULL,
  PRIMARY KEY   (ticker, ddate),
  FOREIGN KEY   (ticker) REFERENCES stocks(ticker) ON DELETE SET NULL ON UPDATE SET NULL
);

CREATE TABLE stock_volumes(
  ticker        varchar(10) NOT NULL,
  vdate         date        NOT NULL,
  volume        numeric(14,0) NOT NULL,
  PRIMARY KEY   (ticker, vdate),
  FOREIGN KEY   (ticker) REFERENCES stocks(ticker) ON DELETE SET NULL ON UPDATE SET NULL
);


CREATE TABLE text(
  author_name    varchar(100),
  file_location  varchar(100) NOT NULL PRIMARY KEY,
  description    text,
  title          varchar(100),
  text_type      varchar(100),
  pub_date       varchar(100), 
  von_value      numeric(3)
);
  
CREATE INDEX STOCK_TICKER
ON stocks(ticker);

CREATE INDEX TICKER_PDATE
ON stock_prices(ticker, pdate);  

CREATE INDEX TICKER_DDATE
ON stock_dividends(ticker, ddate);

CREATE INDEX TICKER_VOLUME
on stock_volumes(ticker, vdate);



