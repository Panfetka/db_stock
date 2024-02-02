--Выдать данные о поставках заготовок в указанном пользователем году по форме: Месяц, уникальный код заготовки, объем поставок.
-- select * from shipper where year(sh_date) = $sh_year;
select month(in_date), pr_id, sum(il_quantity) from rk6.invoice a  join rk6.invoice_line b
on a.in_id = b.in_id where year(in_date) = $pr_year group by month(in_date), pr_id;
