'use strict';
const $ = id => document.getElementById(id);
let cases = [], selected = null, current = null, mode = 'base', busy = false;
const currency = n => new Intl.NumberFormat('en-US', {style:'currency', currency:'USD', maximumFractionDigits:2}).format(n / 100);
const decimal = n => (n / 100).toFixed(2);
const date = s => new Date(s + 'T12:00:00').toLocaleDateString('en-US', {month:'short', day:'numeric', year:'numeric'});
function text(id, value) { $(id).textContent = value; }
function node(tag, className, value) { const n = document.createElement(tag); if (className) n.className = className; if (value !== undefined) n.textContent = value; return n; }
function cents(value, allowZero) {
  const s = value.trim();
  if (!/^\d{1,11}(\.\d{1,2})?$/.test(s)) throw new Error('Enter money as digits with at most two decimal places, for example 1200.00.');
  const [whole, fraction = ''] = s.split('.');
  const n = Number(whole) * 100 + Number(fraction.padEnd(2, '0'));
  if (n > 1000000000000 || n < (allowZero ? 0 : 1)) throw new Error('Invoice amount must be positive; starting balance cannot be negative. Maximum amount is $10 billion.');
  return n;
}
async function api(path, options) {
  const res = await fetch(path, options); const data = await res.json();
  if (!res.ok) throw new Error(data.error || 'The review could not be completed.');
  return data;
}
function error(message) { text('error', message); $('error').hidden = !message; }
function pending() {
  if (!selected) return;
  document.body.dataset.pending = 'true'; $('download').disabled = true;
  text('status', 'NOT REVIEWED'); $('status').className = 'status PENDING';
  text('decision-title', 'Inputs changed. Review again.');
  text('decision-description', 'The findings below belong to the previous review. Run the checks to assess your edited invoice.');
  text('next-action', 'Run payment review with the current values.'); text('review-caption', 'Previous results are dimmed until reassessed.');
}
function loadCase(c) {
  if (busy) return;
  selected = c; mode = 'base'; error('');
  for (const button of $('scenarios').children) button.setAttribute('aria-current', String(button.dataset.id === c.id));
  text('scenario-title', c.title); text('supplier-name', c.supplier.name); text('invoice-number', c.invoice.invoice_number + ' · ' + c.invoice.supplier_id);
  $('amount').value = decimal(c.invoice.amount_cents); $('recipient').value = c.invoice.account_ref; $('balance').value = decimal(c.company.balance_cents);
  text('pay-date', date(c.invoice.pay_on)); text('trusted-account', c.supplier.approved_account_ref);
  text('purchase-order', c.purchase_order ? c.purchase_order.id + ' · ' + currency(c.purchase_order.amount_cents) : 'Unavailable — requires review');
  text('approval-limit', currency(c.company.approval_limit_cents)); text('paid-ledger', c.paid_invoices.length ? c.paid_invoices.map(p => p.invoice_number).join(', ') : 'No matching paid invoice in this sample');
  pending(); runReview();
}
const titles = {READY:'Available checks passed.', HOLD:'Pause this payment.', BLOCK:'Do not pay this invoice again.', REVIEW:'A closer look is required.'};
const descriptions = {READY:'The supporting records match and scheduled cash remains above the configured reserve.', HOLD:'Resolve the evidence or cash exception before taking the next payment step.', BLOCK:'A matching invoice is already in the paid ledger. Reconcile it before proceeding.', REVIEW:'A reviewer needs to assess the cited evidence, policy, or receipt assumptions.'};
async function runReview(event) {
  if (event) event.preventDefault(); if (busy || !selected) return;
  pending(); error('');
  let overrides;
  try { overrides = {amount_cents:cents($('amount').value, false), account_ref:$('recipient').value.trim(), balance_cents:cents($('balance').value, true)};
    if (!overrides.account_ref) throw new Error('Enter a recipient account reference.');
  } catch (e) { error(e.message); return; }
  busy = true; $('results').setAttribute('aria-busy', 'true'); text('run', 'Checking evidence…');
  for (const n of document.querySelectorAll('input, #run, #reset, .scenario-button')) n.disabled = true;
  try {
    current = await api('/api/review', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({case_id:selected.id, overrides})});
    render(current); document.body.dataset.pending = 'false'; $('download').disabled = false;
  } catch (e) { error(e.message); }
  finally { busy = false; $('results').setAttribute('aria-busy', 'false'); text('run', 'Run payment review'); for (const n of document.querySelectorAll('input, #run, #reset, .scenario-button')) n.disabled = false; }
}
function render(data) {
  const r = data.result;
  text('status', r.status); $('status').className = 'status ' + r.status;
  text('decision-title', titles[r.status] || 'Review complete.'); text('decision-description', descriptions[r.status] || 'Inspect the evidence below.');
  text('next-action', r.next_action); text('review-caption', 'Reviewed just now · Independent synthetic scenario · No funds reserved or transferred');
  text('finding-count', r.findings.length + (r.findings.length === 1 ? ' finding' : ' findings'));
  $('findings').replaceChildren();
  for (const f of r.findings) {
    const item = node('article', 'finding'); const badge = node('span', 'finding-symbol ' + f.severity, f.severity === 'info' ? '✓' : '!'); badge.setAttribute('aria-hidden', 'true');
    const content = node('div'); content.append(node('span', 'finding-role', f.role + ' check'), node('h3', '', f.code.toLowerCase().replaceAll('_', ' ').replace(/^./, a => a.toUpperCase())), node('p', '', f.explanation), node('p', 'evidence', 'Evidence: ' + f.evidence));
    item.append(badge, content); $('findings').append(item);
  }
  text('reserve', currency(data.case.company.minimum_cash_cents));
  for (const key of ['base', 'stress']) { text(key + '-min', r[key] ? currency(r[key].minimum_cents) : 'Not assessed'); $(key + '-min').classList.toggle('below', !!r[key] && r[key].minimum_cents < data.case.company.minimum_cash_cents); }
  timeline();
}
function svgNode(tag, attributes, value) { const n = document.createElementNS('http://www.w3.org/2000/svg', tag); for (const [key,val] of Object.entries(attributes)) n.setAttribute(key, val); if (value !== undefined) n.textContent = value; return n; }
function timeline() {
  if (!current) return; const data = current.result[mode], company = current.case.company;
  $('base-tab').setAttribute('aria-pressed', String(mode === 'base')); $('stress-tab').setAttribute('aria-pressed', String(mode === 'stress'));
  $('timeline').replaceChildren(); $('cash-chart').replaceChildren();
  if (!data) { $('cash-chart').append(node('p', 'cash-note', 'Cash was not assessed for this review.')); return; }
  const rows = [{date:company.as_of, label:'Starting company balance', amount_cents:null, balance_cents:company.balance_cents}, ...data.timeline];
  for (const e of rows) {
    const tr = node('tr'); const label = node('td', '', e.label);
    if (e.amount_cents > 0 && !e.confirmed) label.append(node('small', '', 'Unconfirmed receipt'));
    tr.append(node('td', '', date(e.date)), label, node('td', '', e.amount_cents === null ? '—' : (e.amount_cents > 0 ? '+' : '') + currency(e.amount_cents)), node('td', '', currency(e.balance_cents))); $('timeline').append(tr);
  }
  const w=650, h=180, left=65, right=12, top=18, bottom=28, floor=company.minimum_cash_cents;
  const values = rows.map(e=>e.balance_cents); const lo = Math.min(...values, floor, 0), hi = Math.max(...values, floor, 1) * 1.12;
  const y = value => top + (hi-value)/(hi-lo)*(h-top-bottom);
  const start = Date.parse(company.as_of), end = Date.parse(company.horizon_end), span = Math.max(end-start, 86400000);
  const x = day => left + (Date.parse(day)-start)/span*(w-left-right);
  const svg = svgNode('svg', {viewBox:`0 0 ${w} ${h}`, role:'img', 'aria-label':`${mode === 'base' ? 'Base' : 'Stress'} cash timeline. Minimum ${currency(data.minimum_cents)} against reserve ${currency(floor)}.`});
  for (const val of [hi/1.12, floor, lo]) {
    svg.append(svgNode('line', {x1:left,y1:y(val),x2:w-right,y2:y(val),stroke:val===floor?'#b68743':'#e8eef1','stroke-dasharray':val===floor?'5 4':'0'}));
    svg.append(svgNode('text', {x:left-9,y:y(val)+4,'text-anchor':'end',fill:'#718796','font-size':10}, '$'+(val/100).toLocaleString('en-US',{maximumFractionDigits:0})));
  }
  let path=`M ${left} ${y(company.balance_cents)}`;
  for (let i=1;i<rows.length;i++) path+=` H ${x(rows[i].date)} V ${y(rows[i].balance_cents)}`;
  path+=` H ${w-right}`;
  svg.append(svgNode('path', {d:path,fill:'none',stroke:'#329b84','stroke-width':2.5,'stroke-linejoin':'round'}));
  for (const e of rows) { const point=svgNode('circle', {cx:x(e.date),cy:y(e.balance_cents),r:3.5,fill:'#329b84',stroke:'white','stroke-width':1.5}); point.append(svgNode('title', {}, `${e.label}: ${currency(e.balance_cents)}`)); svg.append(point); }
  for (const [day, anchor] of [[company.as_of,'start'],[company.horizon_end,'end']]) svg.append(svgNode('text', {x:x(day),y:h-5,'text-anchor':anchor,fill:'#718796','font-size':10}, date(day)));
  $('cash-chart').append(svg);
}
$('review-form').addEventListener('submit', runReview);
$('reset').addEventListener('click', ()=>loadCase(selected));
for (const id of ['amount','recipient','balance']) $(id).addEventListener('input', pending);
for (const key of ['base','stress']) $(key+'-tab').addEventListener('click',()=>{mode=key;timeline();});
$('download').addEventListener('click',()=>{ if (!current || $('download').disabled) return; const blob = new Blob([JSON.stringify({...current, exported_at:new Date().toISOString(), note:'Synthetic independent review. No payment approval or execution.'},null,2)],{type:'application/json'}); const url=URL.createObjectURL(blob), a=node('a');a.href=url;a.download='finality-'+current.case.id+'-decision.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000); });
async function init() {
  try { cases = await api('/api/scenarios'); if (!cases.length) throw new Error('No sample scenarios are available.');
    cases.forEach((c,i)=>{ const b=node('button','scenario-button');b.type='button';b.dataset.id=c.id;b.append(node('span','scenario-number',String(i+1).padStart(2,'0')),node('span','',c.title));b.addEventListener('click',()=>loadCase(c));$('scenarios').append(b); }); loadCase(cases[0]);
  } catch(e) { error('Unable to load the demo. '+e.message); text('status','UNAVAILABLE'); text('decision-title','Review unavailable.'); text('decision-description','Check that the local FINALITY server is running, then reload this page.'); $('results').setAttribute('aria-busy','false'); $('run').disabled=true; }
}
init();
