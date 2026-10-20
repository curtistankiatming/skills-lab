#!/usr/bin/env node
'use strict';
const fs=require('node:fs');
const path=require('node:path');
const crypto=require('node:crypto');
const {gate}=require('./gate.cjs');
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
const value=x=>x===undefined||x===null?'UNKNOWN':String(x);
const iso=s=>typeof s==='string'&&Number.isFinite(Date.parse(s));
const q=s=>String(s).replace(/[|\r\n]/g,' ');
const identity=s=>typeof s==='string'&&s.length>0;
const pct=x=>String(Math.round(x*100)/100);
const readingId=x=>Number.isInteger(x)||(typeof x==='string'&&x.trim().length>0);
const actorId=x=>typeof x==='string'&&x.trim().length>0;
const faultText=e=>!Object.hasOwn(e,'fault')?'UNKNOWN':e.fault===null?'NONE':typeof e.fault==='string'&&e.fault.length?q(e.fault):'UNKNOWN';
const meterText=m=>{
  if(typeof m==='string') return `failure=${q(m)}`;
  if(!m||typeof m!=='object') return 'UNKNOWN reading';
  const w=m.rateLimitsByLimitId?.ordinary, p=w?.primaryWindow;
  const used=p&&Number.isFinite(p.usedPercent)?`${pct(p.usedPercent)}% used / ${pct(100-p.usedPercent)}% remaining`:'UNKNOWN';
  const secondary=w?.secondaryWindow===null?'UNKNOWN':w?.secondaryWindow===undefined?'UNKNOWN':JSON.stringify(w.secondaryWindow);
  return `account=${q(value(m.accountId))}; bucket=${q(value(m.bucketId))}; sampled=${q(value(m.observedAt))}; ordinaryAllowed=${q(value(m.ordinaryUsageAllowed))}; primary=${used}; duration=${q(value(p?.windowDurationMins))} min; resetsAt=${q(value(p?.resetsAt))}; secondary=${q(secondary)}`;
};
function formatReceipt(r, sourcePath, sourceHash) {
  const issues=[]; const lines=[]; const latched=[];
  const issue=(where,why)=>issues.push(`${where}: ${why}`);
  if(!r||typeof r!=='object') throw Error('receipt must be a JSON object');
  if(!['screening','confirmation'].includes(r.phase)) issue('receipt','unsupported phase');
  if(!['baseline','candidate'].includes(r.mode)) issue('receipt','unsupported mode');
  if(!identity(r.account)) issue('receipt','missing account identity');
  if(!identity(r.authority)) issue('receipt','missing authority');
  if(!/^[a-f0-9]{64}$/i.test(r.fixtureSha256||'')) issue('receipt','missing fixture hash');
  if(!Array.isArray(r.cases)||!r.cases.length) issue('receipt','missing cases');
  const t=r.totals||{};
  for(const k of ['accountPolls','failedAttempts','fallbackPolls','workerGates','duplicateTriggers']) if(!Number.isInteger(t[k])||t[k]<0) issue('totals',`missing or invalid ${k}`);
  const receiptRejected=issues.length>0;
  lines.push('# O2 usage-monitor replay report','',`Phase: ${q(value(r.phase))} | Mode: ${q(value(r.mode))} | Account: ${q(value(r.account))}`,
    `Authority: ${q(value(r.authority))}`,`Source receipt: ${q(sourcePath)} | SHA256 ${sourceHash}`,
    `Fixture SHA256: ${q(value(r.fixtureSha256))}`,
    'Authority rules: Check hourly while active. WORK requires known, matching account, bucket, reset, primary window and ordinary-usage permission; any missing or unsupported required fact means HOLD / review needed. Optional secondary UNKNOWN alone does not stop work. At each due boundary, further work requires a fresh source sample at/after that boundary and a passing local gate; a pre-boundary sample never extends the prior expiry. This replay gate accepts the scheduled event timestamp exactly. At <=10% ordinary remaining, stop at a safe checkpoint; STOP stays latched across reset until renewed owner authority. No reset, purchase or model switch substitutes for authority.',
    'Scope: local synthetic replay. Worker actions below are simulated receipts; live stop delivery and elapsed-time bounds are unverified.','');
  for(const [ci,c] of (Array.isArray(r.cases)?r.cases:[]).entries()) {
    const caseName=identity(c?.id)?c.id:`case-${ci+1}`;
    if(!identity(c?.id)) issue(caseName,'missing case identity');
    const caseRejected=!identity(c?.id);
    lines.push(`## ${q(caseName)}`,'');
    if(!Array.isArray(c?.events)||!c.events.length) {issue(caseName,'missing events');lines.push('HOLD / review needed: no events.','');continue;}
    const states=new Map();
    for(const [ei,e] of c.events.entries()) {
      const where=`${caseName} event ${ei+1}`;
      const eventIssueStart=issues.length;
      const computedActions=new Set();
      if(!e||typeof e!=='object') {issue(where,'missing event');continue;}
      if(!iso(e.at)||!iso(e.expectedDue)||!iso(e.reset)||!identity(e.bucket)) issue(where,'missing time, bucket or reset identity');
      if(faultText(e)==='UNKNOWN') issue(where,'fault annotation absent or unsupported');
      if(!Array.isArray(e.readings)||!e.readings.length) issue(where,'missing source readings');
      if(!Array.isArray(e.decisions)||!e.decisions.length) issue(where,'missing worker decisions');
      const reads=Array.isArray(e.readings)?e.readings:[];
      const decisions=Array.isArray(e.decisions)?e.decisions:[];
      lines.push(`### ${ei+1}. ${q(value(e.at))}`,
        `Due: ${q(value(e.expectedDue))} | Expected bucket: ${q(value(e.bucket))} | Expected reset: ${q(value(e.reset))} | Injected fault: ${faultText(e)}`,
        `Source calls: ${reads.length}; local fallbacks: ${r.mode==='candidate'?reads.filter(x=>x?.actor!=='monitor').length:0}; fallback cause: ${r.mode==='candidate'&&reads.some(x=>x?.actor!=='monitor')?faultText(e):'none'}`,
        'Readings:');
      for(const a of reads) {
        if(!readingId(a?.callId)) issue(where,'missing or invalid reading callId');
        if(!actorId(a?.actor)) issue(where,'missing or invalid reading actor');
        lines.push(`- call ${q(value(a?.callId))} by ${q(value(a?.actor))}: ${meterText(a?.result)}`);
        const m=a?.result;
        if(typeof m==='string') {if(!['source-unavailable','monitor-failure'].includes(m)) issue(where,`unsupported source failure ${m}`);}
        else if(!m||typeof m!=='object') issue(where,'missing source reading');
        else {
          const p=m.rateLimitsByLimitId?.ordinary?.primaryWindow;
          if(!identity(m.accountId)||!identity(m.bucketId)||!iso(m.observedAt)) issue(where,'missing source account, bucket or timestamp');
          if(typeof m.ordinaryUsageAllowed!=='boolean') issue(where,'ordinary flag UNKNOWN');
          if(!p||!Number.isFinite(p.usedPercent)||p.usedPercent<0||p.usedPercent>100||
             !Number.isFinite(p.windowDurationMins)||p.windowDurationMins<=0||!Number.isInteger(p.resetsAt))
            issue(where,'required primary window UNKNOWN or invalid');
        }
      }
      lines.push('Worker | Trigger | Recorded action | Reason | Deadline / expiry | Independent gate','--- | ---: | --- | --- | --- | ---');
      for(const d of decisions) {
        const worker=identity(d?.worker)?d.worker:'UNKNOWN';
        const state=states.get(worker)||{latched:false}; states.set(worker,state);
        const source=r.mode==='baseline'?reads.find(x=>x?.actor===worker):reads.find(x=>x?.actor===worker)||reads.find(x=>x?.actor==='monitor');
        let check='HOLD / review needed';
        let actual=null;
        if(state.latched) {
          actual=gate({account:r.account},{at:e.at,bucket:e.bucket,reset:e.reset},null,state,Date.parse(e.expectedDue));
        } else if(!source) issue(where,`missing source for ${worker}`);
        else if(!identity(r.account)||!iso(e.at)||!iso(e.expectedDue)||!iso(e.reset)||!identity(e.bucket)) issue(where,`unknown required identity for ${worker}`);
        else {
          actual=gate({account:r.account},{at:e.at,bucket:e.bucket,reset:e.reset},typeof source.result==='object'?source.result:null,state,Date.parse(e.expectedDue));
        }
        if(!identity(d?.worker)||!['WORK','HOLD','STOP'].includes(d?.action)||!iso(d?.deadline)||!Number.isInteger(d?.trigger)) issue(where,`invalid decision for ${worker}`);
        if(actual) {
          computedActions.add(actual.action);
          check=actual.action===d?.action&&actual.reason===d?.reason&&actual.deadline===d?.deadline?'MATCH':'HOLD / review needed';
          if(check!=='MATCH') issue(where,`${worker} recorded decision differs from source gate (computed ${actual.action}; reason ${actual.reason}; deadline ${value(actual.deadline)})`);
        }
        if(d?.action==='STOP') state.latched=true;
        lines.push(`${q(worker)} | ${q(value(d?.trigger))} | ${q(value(d?.action))} | ${q(value(d?.reason))} | ${q(value(d?.deadline))} | ${check}`);
      }
      const actions=new Set([...decisions.map(x=>x?.action),...computedActions]);
      const hasStopLatch=[...states.values()].some(s=>s.latched);
      const next=hasStopLatch||actions.has('STOP')?'Safe checkpoint and stop; owner authority required before any restart, including after reset.':receiptRejected||caseRejected||issues.length>eventIssueStart||actions.has('HOLD')?'Hold work; resolve source/identity/authority and obtain a fresh at/after-boundary reading before further work.':actions.size===1&&actions.has('WORK')?'Continue only until each listed expiry. At the next due boundary, obtain a fresh at/after-boundary source sample and pass the local gate before further work; the prior sample cannot extend expiry.':'HOLD / review needed: missing or unsupported action.';
      for(const [w,s] of states) if(s.latched&&!latched.includes(`${caseName}/${w}`)) latched.push(`${caseName}/${w}`);
      lines.push(`STOP latch: ${[...states].filter(([,s])=>s.latched).map(([w])=>w).join(', ')||'none'}`,
        `Next action: ${next}`,'');
    }
  }
  lines.push('## Totals','',`Account polls: ${value(t.accountPolls)} | Failed attempts: ${value(t.failedAttempts)} | Local fallbacks: ${value(t.fallbackPolls)} | Worker gates: ${value(t.workerGates)} | Duplicate triggers: ${value(t.duplicateTriggers)}`,
    'These counters are diagnostics, not token savings.','',`Receipt check: ${issues.length?'HOLD / REVIEW NEEDED':'MATCHED'}`,
    `STOP latched: ${latched.length?latched.map(q).join(', '):'none'}`);
  if(issues.length) lines.push(...issues.map(x=>`- ${q(x)}`));
  lines.push('');
  return {report:lines.join('\n'),status:issues.length?'HOLD':'MATCHED',stopLatched:latched,issues};
}
function main(argv) {
  const option=k=>{const i=argv.indexOf(k),v=i<0?null:argv[i+1];return typeof v==='string'&&!v.startsWith('--')?v:null;};
  const input=option('--receipt'), output=option('--out');
  if(!input||!output) throw Error('usage: node scripts/report.cjs --receipt <raw-receipt.json> --out <local-report.md>');
  const inPath=path.resolve(input), outPath=path.resolve(output);
  if(inPath===outPath) throw Error('output must differ from raw receipt');
  const raw=fs.readFileSync(inPath), result=formatReceipt(JSON.parse(raw),inPath,sha(raw));
  fs.mkdirSync(path.dirname(outPath),{recursive:true});
  fs.writeFileSync(outPath,result.report,{encoding:'utf8',flag:'wx'});
  // STOP-LATCHED is appended so a caller that reads only stdout cannot miss a latched stop;
  // it goes last so the status, path and hash keep their earlier positions.
  process.stdout.write(`${result.status} ${outPath} SHA256 ${sha(Buffer.from(result.report))}${result.stopLatched.length?' STOP-LATCHED':''}\n`);
}
if(require.main===module) try {main(process.argv.slice(2));} catch(e) {console.error(e.message);process.exitCode=1;}
module.exports={formatReceipt,meterText};
