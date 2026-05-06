 use sql_store;
 select *
from order_items
where  order_id = 6 and (quantity*unit_price > 30)