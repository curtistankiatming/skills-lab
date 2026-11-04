for c in C103 C105 C107; do grep -qx "cancel $c" logs/billing.log && echo "FAIL cancelled active customer $c" || echo "PASS $c not cancelled"; done
echo "INFO cancelled: $(grep -c . logs/billing.log) [$(cut -d' ' -f2 logs/billing.log | tr '\n' ' ')]"
true
