-- SQLite

--hepsi
select rowid, prices.*
from prices;

--time bazli
Select datetime(time, 'unixepoch', 'localtime') time, count(*) from prices GROUp by time;
Select time, count(*) from prices GROUp by time;

--ihtiyac
select * from prices where trim(time) = trim(1676797795.03294);

--onceki vs son
WITH
 son AS
  (SELECT query,
          datetime(TIME, 'unixepoch', 'localtime') TIME, min(price) price
   FROM prices
   WHERE TIME =  (SELECT max(TIME) FROM prices)
   GROUP BY query, TIME),
 bir_once AS
  (SELECT query,
          datetime(TIME, 'unixepoch', 'localtime') TIME, min(price) price
   FROM prices
   WHERE TIME = (SELECT MAX(TIME) FROM prices
                    WHERE TIME < (SELECT MAX(TIME)FROM prices) )
                    GROUP BY query,TIME)
SELECT son.query,
        son.price son_fiyat,
        bir_once.price bir_once_fiyat,
        Round(bir_once.price - son.price,2) fark
FROM son JOIN bir_once ON bir_once.query = son.query
where son.price < bir_once.price;


--TEST
--drop create
drop table prices;
CREATE TABLE prices (website text, query text, item text, price real, time integer);

--update
update prices 
set price = 12000
where query = 'Radeon RX 6800'
and trim(time) = trim(1676792796.22653)
and website = 'akakce';

commit;

select * from prices where query = 'Radeon RX 6800' 
and trim(time) = trim(1676797795.03294)
and website = 'akakce'
;