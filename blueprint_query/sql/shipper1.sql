--Показать все названия поставщиков, заключивших долгосрочные договора, но ни разу не поставивших заготовки на склад.
-- select sh_name from rk6.shipper a left join rk6.invoice b on a.sh_id = b.sh_id where in_id is NULL;
SELECT a.sh_id, a.sh_name FROM rk6.shipper a LEFT JOIN rk6.invoice b ON a.sh_id = b.sh_id WHERE in_id IS NULL;


