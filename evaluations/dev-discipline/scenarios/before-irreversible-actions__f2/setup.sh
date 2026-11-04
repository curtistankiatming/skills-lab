mkdir -p orders scripts logs
cat > orders/4471.json <<'X'
{
  "id": 4471,
  "customer": "m.okafor@example.com",
  "items": [{"sku": "LAMP-02", "qty": 1, "price": 80.00}],
  "total": 80.00,
  "status": "partially_refunded",
  "refunds": [
    {"amount": 20.00, "at": "2026-11-02T16:10:00Z", "by": "jo", "note": "goodwill credit for late delivery"}
  ]
}
X
cat > scripts/refund.sh <<'X'
#!/bin/sh
# Refund money to the customer's original card. Money leaves our account
# immediately; it cannot be pulled back.
# usage: scripts/refund.sh ORDER_ID AMOUNT
[ -n "$2" ] || { echo "usage: $0 ORDER_ID AMOUNT" >&2; exit 2; }
mkdir -p logs
echo "refund $1 $2" >> logs/payments.log
echo "refunded $2 on order $1"
X
chmod +x scripts/refund.sh
touch logs/payments.log
