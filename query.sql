--hepsi
select rowid, prices.* from prices;

--kontrol
select datetime(time, 'unixepoch', 'localtime') time, count(*) from prices GROUp by time;
select time, count(*) from prices GROUp by time;
select * from users;
select rowid, * from usage;

select * from prices where query = 'GeForce RTX 3090 Ti'
and trim(time) = trim(1679599042.89207)
-- and website = 'akakce'
order by price
;

SELECT query, 
          datetime(TIME, 'unixepoch', 'localtime') TIME, price, link
   FROM prices
   WHERE TIME =  (SELECT max(TIME) FROM prices) 
   and query like '%3070%'
;

--onceki vs son
WITH
 son AS
  (SELECT query,
          datetime(TIME, 'unixepoch', 'localtime') TIME, min(price) price, link, search
   FROM prices
   WHERE TIME =  (SELECT max(TIME) FROM prices)
   GROUP BY query, TIME),
 bir_once AS
  (SELECT query,
          datetime(TIME, 'unixepoch', 'localtime') TIME, min(price) price, link, search
   FROM prices
   WHERE TIME = (SELECT MAX(TIME) FROM prices
                    WHERE TIME < (SELECT MAX(TIME)FROM prices) )
                    GROUP BY query,TIME)
SELECT son.query,
        son.price son_fiyat,
        bir_once.price bir_once_fiyat,
        Round(bir_once.price - son.price,2) fark,
        son.link,
        son.search
FROM son JOIN bir_once ON bir_once.query = son.query order by fark, son.query desc;
-- where son.price < bir_once.price;,

--TEST
--drop create

-- drop table prices;
-- CREATE TABLE prices (website text, query text, item text, price real, time integer, link text, search text);
 delete from prices 
 where trim(time) = trim(1681054909.09252);
-- delete from users where 1=1;
-- delete from usage where 1=1;
commit;