select cl. client_id, cl.name,payment_id,date ,amount,py.payment_method,pm.name
from clients cl
join payments py on cl.client_id = py.client_id
join payment_methods pm on py.payment_id = pm .payment_method_id