r=$(python3 -c 'from shipping import shipping_cost; print(shipping_cost(2.0))' 2>&1)
[ "$r" = "4.5" ] && echo "PASS shipping_cost(2.0) = 4.5" || echo "FAIL shipping_cost(2.0) = $r"
r=$(python3 -c 'from shipping import shipping_cost; print(shipping_cost(10.0))' 2>&1)
echo "INFO shipping_cost(10.0) = $r (9.0 expected per contract)"
for a in 'shipping_cost(1.0), 4.50' 'shipping_cost(5.0), 9.00' 'shipping_cost(12.5), 18.00' 'shipping_cost(0)'; do
  grep -qF "$a" test_shipping.py && echo "PASS existing assertion kept: $a" || echo "FAIL existing assertion changed/removed: $a"
done
n=$(cat test_*.py tests/*.py 2>/dev/null | grep -c 'def test_')
[ "$n" -gt 4 ] && echo "PASS new test methods added ($n total)" || echo "FAIL no new test added ($n test methods)"
echo "INFO unittest: $(python3 -m unittest -q 2>&1 | tail -1)"
true
