 select pa.date,
cl.name, cl.client_id,pa.payment_id,
amount, pm.name
from payments pa
join clients cl on pa.client_id = cl.client_id
join payment_methods pm on pa.payment_method = pm.payment_method_id