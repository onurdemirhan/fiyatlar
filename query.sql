-- SQLite

--hepsi
select rowid, prices.* from prices;

--kontrol
Select datetime(time, 'unixepoch', 'localtime') time, count(*) from prices GROUp by time;
Select time, count(*) from prices GROUp by time;
select website, query, count(*) from prices group by website, query;

select * from prices where query = 'Radeon RX 7900 XT'
--and trim(time) = trim(1677333591.23728)
-- and website = 'akakce'
order by price
;

SELECT query,
          datetime(TIME, 'unixepoch', 'localtime') TIME, price, link
   FROM prices
   WHERE TIME =  (SELECT max(TIME) FROM prices) 
   and query = 'Radeon RX 7900 XT'
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
FROM son JOIN bir_once ON bir_once.query = son.query
where son.price < bir_once.price;


--TEST
--drop create
drop table prices;
CREATE TABLE prices (website text, query text, item text, price real, time integer, link text, search text);

--update
update prices 
set price = 12000
where query = 'Radeon RX 6800'
and trim(time) = trim(1676792796.22653)
and website = 'akakce';

delete from prices 
where trim(time) = trim(1677608290.8777);


commit;