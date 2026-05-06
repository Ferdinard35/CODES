select 
 customer_id,
 first_name,
 points,
 'Bronze' as type
from customers
 where points < 2000
 union
 select 
 customer_id,
 first_name,
 points,
 'Sliver' as type
from customers
 where points between 2000 and 3000
  union
 select 
 customer_id,
 first_name,
 points,
 'Gold' as type
from customers
 where points > 3000
 order by first_name