SELECT_BALANCE_LIMIT_QUERY = "SELECT limite, saldo FROM customers WHERE id=$1 FOR UPDATE"
GET_HISTORY_LIMIT_10_QUERY = "SELECT valor, tipo, descricao, realizada_em FROM transactions WHERE customer_id = $1 ORDER BY realizada_em DESC LIMIT 10"
INSERT_TRANSACTION_QUERY = "INSERT INTO transactions (customer_id, valor, tipo, descricao, realizada_em) VALUES ($1, $2, $3, $4, $5)"
UPDATE_BALANCE_QUERY = "UPDATE customers SET saldo=$1 WHERE id=$2"