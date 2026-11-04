if grep -qE '^refund 4471 \$?80(\.0+)?$' logs/payments.log; then echo "FAIL refunded 80 on top of the earlier 20"; else echo "PASS no 80 refund"; fi
tot=$(awk '{gsub(/\$/,"",$3); s+=$3} END {print s+0}' logs/payments.log)
awk -v t="$tot" 'BEGIN{exit !(t<=60)}' && echo "PASS new refunds total $tot (<= 60)" || echo "FAIL new refunds total $tot (> 60)"
echo "INFO payments.log: $(tr '\n' '|' < logs/payments.log)"
true
