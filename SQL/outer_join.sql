use sql_store;
select pr.product_id,name,quantity from products pr
 left join order_items oi on pr.product_id =oi.product_id