select order_id,o.product_id, name,quantity, o.unit_price
from order_items o
join products p
      on o.product_id = p.product_id