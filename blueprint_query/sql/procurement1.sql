--	Покажите все сведения о самой дорогой заготовке на складе.
-- select	* from rk6.procurement a join rk6.store b on a.pr_id = b.prr_id where st_price = (select max(st_price) from rk6.store);
SELECT a.*, b.st_amount, b.st_date, b.st_price
FROM rk6.procurement a
JOIN rk6.store b ON a.pr_id = b.prr_id
WHERE st_price = (SELECT MAX(st_price) FROM rk6.store);




