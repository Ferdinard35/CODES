select 
order_date,
order_id ,first_name as customer,
sh.name as shipper ,
 oru.name as status 
from customers cu
 join orders ors on cu.customer_id = ors.customer_id
 left join shippers sh on ors.shipper_id = sh.shipper_id
 left join order_statuses oru on ors.status = oru. order_status_id