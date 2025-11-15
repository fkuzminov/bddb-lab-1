SELECT account_type, count(*) AS count
from accounts
GROUP BY account_type;