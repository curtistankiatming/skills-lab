'use strict';
// Run from the example folder: node --test tests/report.test.cjs
const test=require('node:test');
const assert=require('node:assert');
const fs=require('node:fs');
const os=require('node:os');
const path=require('node:path');
const {execFileSync,spawnSync}=require('node:child_process');

const HERE=__dirname;
const REPORT=path.join(HERE,'..','scripts','report.cjs');
const fixture=name=>path.join(HERE,'fixtures',name);
const scratch=()=>fs.mkdtempSync(path.join(os.tmpdir(),'reporter-test-'));
const run=(...args)=>spawnSync(process.execPath,[REPORT,...args],{encoding:'utf8'});

test('a WORK-only receipt prints MATCHED with no STOP flag',()=>{
  const out=path.join(scratch(),'report.md');
  const r=run('--receipt',fixture('work-only.json'),'--out',out);
  assert.strictEqual(r.status,0,r.stderr);
  assert.match(r.stdout,/^MATCHED \//);
  assert.doesNotMatch(r.stdout,/STOP-LATCHED/);
});

test('a latched STOP is visible on stdout and survives a reset',()=>{
  const out=path.join(scratch(),'report.md');
  const r=run('--receipt',fixture('stop-after-reset.json'),'--out',out);
  assert.strictEqual(r.status,0,r.stderr);
  assert.match(r.stdout,/^MATCHED \/.* SHA256 [0-9a-f]{64} STOP-LATCHED\n$/);
  const report=fs.readFileSync(out,'utf8');
  assert.match(report,/STOP latched: c1\/w1/);
  const nexts=report.match(/^Next action: .*$/gm);
  assert.strictEqual(nexts.length,3);
  assert.match(nexts[2],/Safe checkpoint and stop/);
});

test('percentages are rounded for display',()=>{
  const out=path.join(scratch(),'report.md');
  run('--receipt',fixture('stop-after-reset.json'),'--out',out);
  const report=fs.readFileSync(out,'utf8');
  assert.match(report,/90\.1% used \/ 9\.9% remaining/);
});

test('an existing output, or an alias of the receipt, is refused without changes',()=>{
  const dir=scratch();
  const receipt=path.join(dir,'receipt.json');
  fs.copyFileSync(fixture('work-only.json'),receipt);
  const before=fs.readFileSync(receipt);
  const existing=path.join(dir,'old.md');
  fs.writeFileSync(existing,'old report');
  assert.strictEqual(run('--receipt',receipt,'--out',existing).status,1);
  assert.strictEqual(fs.readFileSync(existing,'utf8'),'old report');
  const alias=path.join(dir,'alias.md');
  fs.symlinkSync(receipt,alias);
  assert.strictEqual(run('--receipt',receipt,'--out',alias).status,1);
  assert.deepStrictEqual(fs.readFileSync(receipt),before);
});

test('a flag in place of a value is a usage error',()=>{
  const r=run('--receipt','--out',path.join(scratch(),'x.md'));
  assert.strictEqual(r.status,1);
  assert.match(r.stderr,/^usage:/);
});

test('the stdout hash matches the written report',()=>{
  const out=path.join(scratch(),'report.md');
  const line=execFileSync(process.execPath,[REPORT,'--receipt',fixture('work-only.json'),'--out',out],{encoding:'utf8'});
  const hash=require('node:crypto').createHash('sha256').update(fs.readFileSync(out)).digest('hex');
  assert.strictEqual(line.trim().split(' ')[3],hash);
});
