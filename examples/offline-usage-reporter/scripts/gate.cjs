'use strict';
const HOUR=3600000;const stamp=s=>Date.parse(s);
function gate(f, e, reading, workerState, due) {
  if (workerState.latched) return {action:'STOP', reason:'latched-stop', deadline:e.at};
  if (!reading) return {action:'HOLD', reason:'source-unavailable', deadline:e.at};
  if (stamp(e.at) !== due || stamp(reading.observedAt) !== stamp(e.at)) return {action:'HOLD', reason:'stale-or-missed-due', deadline:e.at};
  if (reading.accountId !== f.account || reading.bucketId !== e.bucket ||
      reading.rateLimitsByLimitId?.ordinary?.primaryWindow?.resetsAt !== Math.floor(stamp(e.reset)/1000))
    return {action:'HOLD', reason:'identity-or-reset-mismatch', deadline:e.at};
  const p = reading.rateLimitsByLimitId.ordinary.primaryWindow;
  if (reading.ordinaryUsageAllowed !== true || !p || !Number.isFinite(p.usedPercent) || p.usedPercent < 0 || p.usedPercent > 100)
    return {action:'HOLD', reason:'required-primary-or-ordinary-unknown', deadline:e.at};
  if (100-p.usedPercent <= 10) {workerState.latched=true; return {action:'STOP', reason:'remaining<=10', deadline:e.at};}
  return {action:'WORK', reason:'fresh-authorized', deadline:new Date(due+HOUR).toISOString()};
}

module.exports={gate};
