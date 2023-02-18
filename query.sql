select rowid, prices.*
from prices;

with ana as(
    select query,
        datetime(time, 'unixepoch', 'localtime') time,
        rowid,
        min(price)
    from prices
    group by query, time
)
select pices.website,
    ana.*
from ana
    join prices on prices.rowid = ana.rowid;