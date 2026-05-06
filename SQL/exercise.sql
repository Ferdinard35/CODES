 use sql_store;
 select o.order_id,o.product_id,name,quantity_in_stock,p.unit_price
 from order_items o
 join products p on o.product_id = p.product_id