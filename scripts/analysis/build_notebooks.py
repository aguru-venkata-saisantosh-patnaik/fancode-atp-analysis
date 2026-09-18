"""Create transparent analysis notebooks. Execution is a separate command."""
from pathlib import Path
import nbformat as nbf
import textwrap,json,hashlib
R=Path(__file__).resolve().parents[2]
SETUP='''from pathlib import Path
import sys
ROOT = next(p for p in [Path.cwd(), *Path.cwd().parents] if (p/'data/manifests/release.json').exists())
sys.path.insert(0, str(ROOT))
from src.analysis_common import *
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
rng = np.random.default_rng(CFG['seed'])
print('Offline inputs:', CFG['raw_release'], '| Author: Chanakya')'''
def md(s):return nbf.v4.new_markdown_cell(textwrap.dedent(s).strip())
def code(s):return nbf.v4.new_code_cell(textwrap.dedent(s).strip())
def notebook(name,title,intro,sections):
 source_ids={x['id'] for x in json.loads((R/'data/manifests/sources.json').read_text())+json.loads((R/'data/manifests/manual_captures.json').read_text())}
 joined=' '.join(body for _,body in sections)
 refs=sorted(i for i in source_ids if i in joined)
 if name.startswith('01'):refs=sorted(set(refs)|{x['source_id'] for x in json.loads((R/'analysis_config/session_transcriptions.json').read_text())})
 if name.startswith('02'):refs=sorted(set(refs)|{i for i in source_ids if i.startswith('v4_motogp_sessions_') or i.startswith('v4_motogp_report_')})
 if name.startswith('04'):refs=sorted(set(refs)|{i for i in source_ids if i.startswith('fancode_ios_reviews_page')})
 if name.startswith('07'):refs=sorted(set(refs)|{'v5_gst_council_rates','v3_razorpay_pricing','v3_cloudflare_stream_pricing','v3_fancode_terms'})
 setup=SETUP+'\nimport src.analysis_common as shared\nshared.ACTIVE_NOTEBOOK='+repr(name)+'\nshared.ACTIVE_SOURCES='+repr(refs)
 cells=[md('# '+title+'\n\n**Author: Chanakya**\n\n'+intro),code(setup)]
 for kind,body in sections:cells.append(md(body) if kind=='md' else code(body))
 if refs:
  cells += [md('## Source references\nThese IDs resolve to the preserved bodies, URLs and capture timestamps. Derived tables also retain row-level source IDs where applicable. Case inputs refer to the supplied brief, physical PDF pages 9–14. Review source files resolve through the review collection log. Scenario parameters are in analysis_config.'),code('references=source_table('+repr(refs)+')\ndisplay(table(references,'+repr(name[:2]+'_source_references')+'))')]
 for k,c in enumerate(cells):c['id']=hashlib.sha256((name+str(k)+c.source).encode()).hexdigest()[:12]
 nb=nbf.v4.new_notebook(cells=cells,metadata={'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},'language_info':{'name':'python','version':'3.10'},'authors':[{'name':'Chanakya'}]})
 nbf.write(nb,R/'notebooks/source'/f'{name}.ipynb')
notebook('00_evidence_and_case','00 | Evidence, scope and the case logic','Start here. Audit the locked inputs, establish units and map the brief before fitting models. A source download is not a verified operating metric.',[
('md','## 1. Verify the frozen research inputs\nThe checksum verifier is read-only. It also checks provenance records locked at collection close.'),
('code', '''import subprocess
v = subprocess.run([sys.executable, str(ROOT/'scripts/verify_release.py')], capture_output=True, text=True, check=True)
print(v.stdout)
inv = pd.DataFrame(json.loads((ROOT/'data/manifests/raw_inventory.json').read_text()))
quality = pd.DataFrame(json.loads((ROOT/'data/manifests/source_validation.json').read_text()))
coverage = inv.groupby('format').agg(files=('file','size'),MB=('bytes',lambda x:x.sum()/1e6)).reset_index()
display(table(coverage,'00_raw_coverage'))
plt.figure(figsize=(9,4));plt.barh(coverage['format'],coverage['files']);plt.xlabel('Preserved files');plt.title('Evidence volume is not evidence strength');fig('00_evidence_coverage','Source: locked raw-v5 inventory. Includes failed-response bodies.')'''),
('md','## 2. Brief inputs and denominator controls\nPage numbers below are physical PDF pages. The illustrative audience bars are deliberately excluded from market sizing. The repurchase horizon and renewal cohort are undefined. ₹89 is a midpoint tournament-price scenario, not an observed single-match price.'),
('code', '''brief = PdfReader(ROOT/'data/raw/case_inputs/case_brief/BGCC_FANCODE_R3.pdf')
inputs=[('registered_users',240e6,'users, cumulative',9,'Not active or reachable audience'),('watch_minutes',90,'minutes per sport/tour',9,'No payer or session denominator'),('masters_uplift',.5,'relative uplift',9,'Association, not causal timing effect'),('noncore_share',.1,'ordinary-week tennis viewers',9,'Not platform conversion'),('repeat_low',.60,'repurchase proportion',10,'Horizon unknown'),('repeat_high',.65,'repurchase proportion',10,'Not a stationary repeat hazard'),('renewal',.9,'season renewal proportion',10,'Cohort and period unspecified'),('cac_low',150,'INR per paying subscriber target',11,'Not observed incremental CAC'),('cac_high',200,'INR per paying subscriber target',11,'Target may exceed product contribution'),('contest_cvr',.078,'click-to-purchase proportion',11,'Historical case channel only'),('tournament_low',79,'INR per tournament',11,'Case input, current checkout unverified'),('tournament_high',99,'INR per tournament',11,'Case input'),('season_price',399,'INR per season',11,'Declines late season, not rolling 365 days'),('performance_share_low',.65,'fraction of total marketing spend',11,'Current case baseline, not proposed allocation'),('performance_share_high',.70,'fraction of total marketing spend',11,'Current case baseline, not proposed allocation'),('attention_lead_days',2,'days before match',11,'Approximate engagement peak, not measured purchase-conversion peak'),('weekly_inventory',200,'tour-level matches or sessions per week',9,'Case input, not independently counted')]
b = pd.DataFrame(inputs,columns=['input_id','value','unit','pdf_page','limitation']);b['source_id']='supplied_BGCC_FANCODE_R3'
table(b,'case_inputs',True);display(table(b,'00_case_dictionary'))
operating=pd.DataFrame([
('performance_marketing','65–70% of total marketing spend','Current baseline'),
('brand_other','30–35% of total marketing spend, chart illustrates 68/32','Complementary current baseline'),
('campaign_attention','Engagement peaks roughly two days before the match','Plan occasion-led activation around D-2, do not claim a purchase peak'),
('contest_conversion','7.8% contest link-click to pass purchase, recurring','Use supplied rate for this channel, not every acquisition channel'),
('publisher_takeovers','ESPN.in inventory takeovers already used','Improve the existing channel rather than propose it as new'),
('native_personalities','Effectively zero incremental media-rights cost','Do not add an ATP rights surcharge. Production, talent and distribution costs are separate'),
('portfolio_growth','Incremental subscription gains skew toward F1 and football','Accepted case fact, no external corroboration required for its use'),
('season_price','Typically INR399, declining toward season end','Use remaining-season coverage, not rolling annual validity')],columns=['case_fact','supplied_value','decision_use']);operating['source_id']='supplied_BGCC_FANCODE_R3';display(table(operating,'00_case_operating_facts'))
assert '7.8%' in brief.pages[10].extract_text()
assert '65-70%' in brief.pages[10].extract_text()
assert '2 days' in brief.pages[10].extract_text()
comparison=pd.DataFrame({'reading':['Stated uplift','Illustrative bars'],'ordinary_index':[100,100],'spike_index':[150,500]})
comparison['uplift_pct']=(comparison.spike_index/comparison.ordinary_index-1)*100
display(table(comparison,'00_spike_definition_audit'))
print('The bar uplift is 8 times the stated uplift, but the bars are explicitly illustrative. Neither is a measured acquisition multiplier.')'''),
('md','## 3. External evidence stays in its own ledger\nThird-party estimates differ in population and period. No addition of subscribers, subscriptions, households and fans. Vendor rates can inform costs but cannot measure FanCode conversion.'),
('code', '''external=pd.DataFrame(list(METRICS.values()))
display(table(external,'00_external_evidence_register')[['metric_id','value','unit','evidence_type','limitations']])
requirements=[('Q1','Portfolio segmentation: F1, football, MotoGP','10','02,03,04,05,06','2'),('Q2','Passes, player/event bundles, rental, dynamic pricing, competitors','03,07','01,06','4,5'),('Q3','Retention and sustained-growth KPIs','09,10','01,02,04','6,8'),('Q4','Marketing percentages and estimated channel costs/CAC','08','07,09','7,8')]
req=pd.DataFrame(requirements,columns=['question','requirement','primary_notebooks','supporting_notebooks','planned_slides']);display(table(req,'00_requirement_map'))
check('00_evidence',{'locked_raw_pass':json.loads(v.stdout)['status']=='PASS','all_source_ids_reviewed':len(quality)==len(SOURCES),'case_inputs_unique':b.input_id.is_unique})'''),
('md','## Decision passed forward\nUse audience state × occasion × entitlement as the analytical unit. Calendar, pricing and cost evidence can support decisions. Public data cannot establish segment sizes, willingness to pay, internal rights profitability or causal acquisition lift. These become explicit scenarios and pilot gates, not fabricated datasets.')])
notebook('01_viewing_calendar','01 | India viewing occasions','Build a primary annual event-start ledger and a transparent ATP singles-slot sample. This is a timing-opportunity analysis, not an estimate of demand or an actual-start census.',[
('md','## 1. Parse the primary annual guide\nPreserve the entire original line and physical page. Multiweek continuation lines without draw counts are excluded. Dates inherited within a week are explicitly marked. The guide includes events outside the ATP rights package. Unresolved TBC entries remain visible.'),
('code', '''events=[];current=None
for page in [15,16]:
 for line in text('v5_atp_media_guide_lta',page).splitlines():
  date=re.search(r'\\b(\\d{2}) (JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC)\\b',line)
  if date:current=datetime.strptime(date.group(0)+' 2026','%d %b %Y').date().isoformat()
  cat=re.search(r'(ATP MASTERS 1000|ATP 500|ATP 250|GRAND SLAM|ATP FINALS|UNITED CUP|LAVER CUP)',line)
  if not cat or not re.search(r'(?:\\d+|TEAMS)$',line.strip()):continue
  prefix=line[:cat.start()];city=re.sub(r'^\\d+\\s+','',prefix);city=re.sub(r'\\b\\d{2} (?:JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC)\\s*','',city);city=re.sub(r'[\\d,]+\\s*$','',city).strip()
  unknown='TBC' in line
  events.append(dict(event_id='G'+str(len(events)+1).zfill(3),city=city,tier=cat.group(0),start_date=None if unknown else current,date_inherited=not bool(date),source_line=line,pdf_page=page,source_id='v5_atp_media_guide_lta',rights_scope='ATP regular tour candidate' if cat.group(0) in ['ATP 250','ATP 500','ATP MASTERS 1000'] else 'Requires separate rights confirmation'))
events=pd.DataFrame(events);table(events,'atp_event_starts',True);display(events[['event_id','city','tier','start_date','date_inherited']])
display(table(events.groupby('tier').size().rename('event_rows').reset_index(),'01_calendar_tiers'))
# Exact dates for a bounded future journey are read from the saved current calendar capture.
future=[]
for line in text('atp_future_calendar_rendered_v2').splitlines():
 label,datepart=line.split(' | ');m=re.search(r'(\\d+) - (\\d+) (\\w+), (\\d+)',datepart)
 if m:a,b,month,year=m.groups();start=datetime.strptime(f'{a} {month} {year}','%d %B %Y');end=datetime.strptime(f'{b} {month} {year}','%d %B %Y')
 else:
  m=re.search(r'(\\d+) (\\w+) - (\\d+) (\\w+), (\\d+)',datepart);a,ma,b,mb,year=m.groups();start=datetime.strptime(f'{a} {ma} {year}','%d %B %Y');end=datetime.strptime(f'{b} {mb} {year}','%d %B %Y')
 future.append(dict(event=label,start_date=start.date().isoformat(),end_date=end.date().isoformat(),source_id='atp_future_calendar_rendered_v2',regular_atp=not any(x in label for x in ['Davis','Laver'])))
future=pd.DataFrame(future);table(future,'atp_future_windows',True)
plt.figure(figsize=(11,4));d=events.dropna(subset=['start_date']).copy();d['month']=pd.to_datetime(d.start_date).dt.month
d.groupby(['month','tier']).size().unstack(fill_value=0).plot.bar(stacked=True,ax=plt.gca(),width=.85);plt.title('Published tournament starts across the year');plt.ylabel('Event starts');plt.xlabel('Month');plt.legend(fontsize=8,ncol=3);fig('01_event_calendar','Annual guide snapshot. TBC rows excluded from monthly chart. Rights scope differs by event.')'''),
('md','## 2. Convert a fixed 12-final sample and selected additional singles slots\nManual transcriptions are processed inputs with locators, not raw feeds. All clocks use IANA city timezones with date-aware daylight saving. Not-before times are lower bounds. Several source release stamps follow the planned match time, so this is retrospective schedule evidence, not proof of ex-ante campaign knowledge.'),
('code', '''slots=pd.DataFrame(json.loads((ROOT/'analysis_config/session_transcriptions.json').read_text()))
slots['start_utc']=[pd.Timestamp(f'{r.date_local} {r.time_local}',tz=r.timezone).tz_convert('UTC') for r in slots.itertuples()]
slots['start_ist']=pd.to_datetime(slots.start_utc,utc=True).dt.tz_convert('Asia/Kolkata')
slots['hour_ist']=slots.start_ist.dt.hour+slots.start_ist.dt.minute/60
slots['date_ist']=slots.start_ist.dt.date.astype(str);slots['weekday_ist']=slots.start_ist.dt.day_name()
slots['source_url']=[SOURCES[i]['url'] for i in slots.source_id]
table(slots,'atp_slots',True);display(table(slots[['event','round','date_local','time_local','timezone','start_ist','time_semantics','source_id']],'01_verified_slot_ledger'))
finals=slots[slots['round']=='Singles final'].copy()
plt.figure(figsize=(10,5));ax=plt.gca();ax.axvspan(18,23,color=COLORS[1],alpha=.13,label='Assumed 18:00–23:00 window')
for tier,g in finals.groupby('tier'):ax.scatter(g.hour_ist,g.event,s=90,label=tier,zorder=3)
ax.set(xlim=(0,24),xticks=range(0,25,3),xlabel='Scheduled / not-before start in IST',title='Tournament tier alone does not determine usable timing');ax.legend(fontsize=8,loc='lower left');fig('01_final_start_times','One final per preselected edition, n=12. Not-before is not actual start. Date rollover retained in table.')'''),
('md','## 3. Window and delay sensitivity\nThe preferred window is unknown. Test three declared windows and 0–120 minute delays. This shifts a start marker only, not a match-duration estimate. Report sample counts, not population confidence intervals.'),
('code', '''sens=[]
for start,end in CFG['viewing_windows']:
 for delay in CFG['scheduled_delay_minutes']:
  hours=(finals.hour_ist+delay/60)%24
  for event,tier,ok in zip(finals.event,finals.tier,(hours>=start)&(hours<end)):
   sens.append(dict(event=event,tier=tier,window=f'{start}:00–{end}:00',delay_minutes=delay,starts_in_window=bool(ok)))
sens=pd.DataFrame(sens);table(sens,'01_window_delay_sensitivity')
rob=sens.groupby('event').starts_in_window.agg(['sum','count','mean']).reset_index().rename(columns={'mean':'fraction_of_design_cells'})
display(table(rob,'01_timing_robustness'))
piv=sens[sens.delay_minutes==0].pivot(index='event',columns='window',values='starts_in_window').astype(int)
plt.figure(figsize=(8,5));plt.imshow(piv,aspect='auto',cmap='YlGnBu',vmin=0,vmax=1);plt.xticks(range(len(piv.columns)),piv.columns);plt.yticks(range(len(piv)),piv.index);plt.title('Does the final start fit the assumed window?');cb=plt.colorbar(ticks=[0,1]);cb.ax.set_yticklabels(['Outside','Inside']);fig('01_window_sensitivity','Binary scheduled-start fit. Unknown preference, not measured audience propensity.')
# Coverage is sparse by construction. A blank week is missing evidence, not zero tennis.
heat=np.full((53,24),np.nan)
for r in slots.itertuples():
 w=int(r.start_ist.isocalendar().week)-1;h=int(r.hour_ist);heat[w,h]=0 if np.isnan(heat[w,h]) else heat[w,h];heat[w,h]+=1
plt.figure(figsize=(11,4));plt.imshow(heat.T,aspect='auto',origin='lower',cmap='viridis');plt.colorbar(label='Known selected singles starts');plt.xlabel('ISO week index (week 1 at zero)');plt.ylabel('IST hour');plt.title('Coverage-aware sampled timing heatmap');fig('01_sampled_week_hour','White cells are unobserved, not absence of tennis. Use the final comparison for balanced tier analysis.')
check('01_calendar',{'twelve_distinct_finals':len(finals)==12 and finals.event.nunique()==12,'unique_slots':slots.slot_id.is_unique,'all_times_timezone_aware':all(x.tzinfo is not None for x in slots.start_utc),'dubai_ist_2030':float(finals.set_index('event').loc['Dubai','hour_ist'])==20.5,'indian_wells_next_day':finals.set_index('event').loc['Indian Wells','date_ist']=='2026-03-16'})
report('01_calendar_findings',f'{len(events)} guide rows retained, including unresolved dates and events outside the regular ATP package. {len(slots)} selected singles slots across 12 editions. Timing robustness is a design-grid fraction, not a probability. Source locators and full date rollover are preserved. Use clear included-access messaging and a live/replay choice before assuming a higher tier deserves more spend.')'''),
('md','## Decision passed forward\nTarget declared viewing occasions rather than a blanket “Asian events are prime-time” rule. The next notebook tests conflicts. Do not sell a player-specific live promise until participation and a usable slot are confirmed.')])
notebook('02_portfolio_clashes','02 | Portfolio conflicts and next occasions','Combine dated F1 and football evidence with the ATP slot sample. MotoGP offsets remain quarantined where a circuit-specific clock interpretation has not been validated.',[
('md','## 1. F1 and football clocks\nF1 feed fields are scheduled UTC. Football-Data clocks use a Europe/London interpretation supported by winter and summer official fixture checks. Retain that interpretation as a documented inference.'),
('code', '''f1=pd.DataFrame([dict(event=r['raceName'],round=r['round'],start_utc=pd.Timestamp(r['date']+'T'+r['time']),source_id='v3_jolpica_races_2026',sport='F1') for r in rawjson('v3_jolpica_races_2026')['MRData']['RaceTable']['Races']])
f1['start_ist']=pd.to_datetime(f1.start_utc,utc=True).dt.tz_convert('Asia/Kolkata');table(f1,'f1_races',True)
football=[]
for sid in ['v4_laliga_2526','v4_laliga_2627']:
 d=pd.read_csv(path(sid));d['start_utc']=pd.to_datetime(d.Date+' '+d.Time,format='%d/%m/%Y %H:%M').dt.tz_localize('Europe/London',ambiguous='raise',nonexistent='raise').dt.tz_convert('UTC');d['source_id']=sid;football.append(d)
football=pd.concat(football,ignore_index=True);football=football[(football.start_utc>=pd.Timestamp('2026-01-01',tz='UTC'))&(football.start_utc<pd.Timestamp('2026-09-13',tz='UTC'))].copy()
football['event']=football.HomeTeam+' vs '+football.AwayTeam;football['sport']='La Liga';football['start_ist']=football.start_utc.dt.tz_convert('Asia/Kolkata')
football=football[['event','HomeTeam','AwayTeam','start_utc','start_ist','sport','source_id']];table(football,'football_fixtures',True)
display(pd.DataFrame({'sport':['F1','La Liga'],'rows':[len(f1),len(football)],'coverage':['Current 2026 schedule','2026 observations through 7 September']}))'''),
('md','## 2. MotoGP: expose the timezone defect before using the data\nAll 177 session records are retained. The Assen race is independently checked against its official UTC+2 timetable. Other session offsets are not silently corrected. All 29 report excerpts are exported as local-clock evidence with restarts preserved.'),
('code', '''moto=[]
for sid,src in SOURCES.items():
 if sid.startswith('v4_motogp_sessions_') and src.get('extension')=='json':
  for r in rawjson(sid):moto.append(dict(session_id=r['id'],event=r['event']['name'],event_code=r['event']['short_name'],type=r['type'],date_literal=r['date'],status=r['status'],source_id=sid,utc_usable=False))
moto=pd.DataFrame(moto);table(moto,'motogp_sessions_quarantined',True)
qa=json.loads((ROOT/'data/manifests/recovery_v4_qa.json').read_text());logs=[]
for r in qa['motogp']['official_reports']:
 for p in r['race_start_evidence']:
  for clock in p['race_start_clocks']:logs.append(dict(source_id=r['source_id'],pdf_page=p['page'],local_clock=clock,semantics='Race-control clock, possible repeated restart history'))
table(pd.DataFrame(logs),'02_motogp_actual_clock_evidence')
assen=moto[(moto.event_code=='NED')&(moto.type=='RAC')].iloc[0]
literal=pd.Timestamp(assen.date_literal);correct=pd.Timestamp(literal.tz_localize(None),tz='Europe/Amsterdam').tz_convert('UTC')
comparison=pd.DataFrame({'interpretation':['Literal API offset','Official local-time interpretation'],'IST':[literal.tz_convert('Asia/Kolkata'),correct.tz_convert('Asia/Kolkata')]});display(table(comparison,'02_assen_timezone_audit'))
display(table(moto.groupby(['type','status']).size().rename('sessions').reset_index(),'02_motogp_coverage'))'''),
('md','## 3. ATP/F1/football overlap sensitivity\nNo actual ATP durations are available. Compute overlap under 90/150/210-minute ATP and alternative rival duration scenarios. A clash exists only for the selected fixture basket, not all fans of that sport. Weekend co-occurrence is a separate, weaker measure.'),
('code', '''slots=read('atp_slots');slots['start_utc']=pd.to_datetime(slots.start_utc,utc=True)
rivals=pd.concat([f1[['event','sport','start_utc','source_id']],football[['event','sport','start_utc','source_id']]],ignore_index=True)
clashes=[]
for a in slots[slots['round']=='Singles final'].itertuples():
 nearby=rivals[(rivals.start_utc-a.start_utc).abs()<=pd.Timedelta(hours=8)]
 for b in nearby.itertuples():
  for da in CFG['atp_duration_scenarios_minutes']:
   for db in (CFG['f1_duration_scenarios_minutes'] if b.sport=='F1' else CFG['football_duration_scenarios_minutes']):
    overlap=max(0,(min(a.start_utc+pd.Timedelta(minutes=da),b.start_utc+pd.Timedelta(minutes=db))-max(a.start_utc,b.start_utc)).total_seconds()/60)
    clashes.append(dict(atp_event=a.event,rival=b.event,sport=b.sport,atp_duration=da,rival_duration=db,overlap_minutes=overlap,atp_source=a.source_id,rival_source=b.source_id))
clashes=pd.DataFrame(clashes);table(clashes,'02_clash_scenarios')
cs=clashes.groupby(['atp_event','rival','sport']).overlap_minutes.agg(['min','max']).reset_index();display(table(cs,'02_clash_bounds'))
base=clashes[(clashes.atp_duration==150)&(((clashes.sport=='F1')&(clashes.rival_duration==120))|((clashes.sport=='La Liga')&(clashes.rival_duration==105)))]
plt.figure(figsize=(10,5));g=base[base.overlap_minutes>0].sort_values('overlap_minutes').tail(12);plt.barh(g.atp_event+' / '+g.rival,g.overlap_minutes);plt.xlabel('Scenario overlap minutes');plt.title('Selected finals can compete with specific football fixtures');fig('02_selected_clashes','Assumed durations, scheduled starts. Partial final and football sample, no actual viewing or audience overlap.')
# Event-date co-occurrence does not imply hourly overlap.
ev=rawjson('v4_motogp_finished_events')+rawjson('v4_motogp_future_events');ev={r['id']:r for r in ev if not r['test']}
co=[]
for a in slots[slots['round']=='Singles final'].itertuples():
 local=pd.Timestamp(a.date_local).date()
 for e in ev.values():
  if pd.Timestamp(e['date_start']).date()<=local<=pd.Timestamp(e['date_end']).date():co.append(dict(atp_event=a.event,motogp_event=e['name'],type='Event-date co-occurrence only',atp_source=a.source_id))
display(table(pd.DataFrame(co),'02_motogp_weekend_cooccurrence'))
check('02_portfolio',{'f1_23_rounds':len(f1)==23,'football_250_rows':len(football)==250,'motogp_177_unique':len(moto)==177 and moto.session_id.is_unique,'assen_offset_difference_2h':(literal-correct).total_seconds()==7200,'no_negative_overlap':bool((clashes.overlap_minutes>=0).all())})'''),
('md','## Decision passed forward\nUse sport-specific conflict suppression with the customer’s chosen race or club. A shared weekend may offer a bundle opportunity, but hourly overlap can make the bundle less usable. Broad MotoGP hourly clash claims remain outside the verified evidence. F1/football overlap tables are sensitivity results, not realized collisions.')])
notebook('03_offers_and_baskets','03 | Entitlements, baskets and dynamic pricing','Compare what each customer can actually consume. Prices are date- and channel-specific observations or labelled case inputs. Intended viewing baskets are scenarios, not observed customer demand.',[
('md','## 1. Audited product menu\nNo monthly ATP entitlement is assumed. The yearly description explicitly includes tennis. Competitors differ in rights, devices and term. Comparing rupees per month does not make their content interchangeable.'),
('code', '''offers=[
('FanCode tournament','ATP',79,99,'tournament','case input','supplied_BGCC_FANCODE_R3','PDF p11. Current checkout unverified'),
('FanCode season','ATP',399,399,'2026 season','case input','supplied_BGCC_FANCODE_R3','Declining late-season price not observed'),
('FanCode monthly list','ATP uncertain',199,199,'30 days','public observation','fancode_monthly_final_v5','Explicit F1/MotoGP, ATP unresolved'),
('FanCode monthly promo','ATP uncertain',116,116,'30 days','public observation','fancode_monthly_final_v5','SEPT10 applied, renewal price not verified'),
('FanCode yearly list','Portfolio including tennis',999,999,'365 days','public observation','fancode_yearly_rendered','Device and scope per captured description'),
('FanCode yearly promo','Portfolio including tennis',899,899,'365 days','public observation','fancode_yearly_rendered','Coupon snapshot, not permanent policy'),
('Sony LIV Premium monthly','Different rights basket',399,399,'month','public listing','sonyliv_subscription','Not an ATP-equivalent substitute'),
('Sony LIV Premium annual','Different rights basket',1499,1499,'year','public listing','sonyliv_subscription','Not an ATP-equivalent substitute'),
('Sony LIV mobile annual','Mobile only',699,699,'year','public listing','sonyliv_subscription','Device restriction matters'),
('Tennis TV monthly IAP','ATP product',449,449,'month','India App Store listing','v3_tennistv_india_iap','Not web checkout or purchased entitlement'),
('Tennis TV six-month IAP','ATP product',2500,2500,'six months','India App Store listing','v3_tennistv_india_iap','Not directly equivalent to FanCode season'),
('Tennis TV annual IAP','ATP product',4499,4499,'year','India App Store listing','v3_tennistv_india_iap','Grand Slams excluded from ATP comparison'),
('JioHotstar Mobile','Different rights basket',79,79,'month','January announcement','jiohotstar_2026_price_release','Dated launch price, not September checkout'),
('JioHotstar Super','Different rights basket',149,149,'month','January announcement','jiohotstar_2026_price_release','Rights basket differs'),
('JioHotstar Premium','Different rights basket',299,299,'month','January announcement','jiohotstar_2026_price_release','Rights basket differs')]
offers=pd.DataFrame(offers,columns=['product','scope','low_price','high_price','validity','evidence_type','source_id','limitation']);table(offers,'offers',True);display(table(offers,'03_offer_audit'))
print('Two INR99 tournament passes cost INR198. Monthly list costs INR1 more, while observed promotion costs INR82 less, only if ATP is included and dates fit the term.')'''),
('md','## 2. Minimum-cost coverage over explicit dated baskets\nSolve a small weighted set-cover problem exactly using a bitmask dynamic programme. Each required viewing date must be covered. Monthly validity is 30 days from purchase, yearly 365. The buyer can start a pass on a demand date. Tournament access covers that event. Existing ownership is modelled as zero-cost coverage. This is product arithmetic, not an elasticity or choice model.'),
('code', '''from itertools import product
future=read('atp_future_windows');f1=read('f1_races')
# Dated ATP occasions are event-window endpoints, not promised match times.
selected=[]
for name in ['Chengdu','Tokyo','Shanghai','Basel','Paris','Nitto']:
 r=future[future.event.str.contains(name)].iloc[0];selected.append((name,pd.Timestamp(r.end_date),'ATP'))
races=[(r.event,pd.Timestamp(r.start_ist).tz_localize(None).normalize(),'F1') for r in f1.itertuples() if pd.Timestamp(r.start_ist)>=pd.Timestamp('2026-09-23',tz='Asia/Kolkata')]
baskets={'One tennis event':selected[:1],'Two tennis events within 30d':[selected[1],selected[2]],'Late-season tennis six':selected,'Tennis plus two race weekends':selected[:3]+races[:2],'Portfolio to season end':selected+races}
def cheapest(demands,monthly_atp,monthly_price,yearly_price,owned=False,tournament_price=99):
 n=len(demands);full=(1<<n)-1
 if owned:return 0.,'Existing covering entitlement'
 candidates=[]
 for j,(event,date,sport) in enumerate(demands):
  if sport=='ATP':candidates.append((tournament_price,1<<j,'Tournament '+event))
 atp_mask=sum(1<<j for j,d in enumerate(demands) if d[2]=='ATP')
 candidates.append((399,atp_mask,'ATP season'))
 for _,start,_ in demands:
  mask=sum(1<<j for j,(_,dt,sp) in enumerate(demands) if start<=dt<start+pd.Timedelta(days=30) and (sp!='ATP' or monthly_atp))
  candidates.append((monthly_price,mask,'Monthly '+start.date().isoformat()))
  ymask=sum(1<<j for j,(_,dt,_) in enumerate(demands) if start<=dt<start+pd.Timedelta(days=365))
  candidates.append((yearly_price,ymask,'Yearly '+start.date().isoformat()))
 dp={0:(0.,[])}
 for mask in range(full+1):
  if mask not in dp:continue
  for price,cover,label in candidates:
   new=mask|cover
   if new!=mask and (new not in dp or dp[mask][0]+price<dp[new][0]):dp[new]=(dp[mask][0]+price,dp[mask][1]+[label])
 return dp[full][0],'; '.join(dp[full][1])
rows=[];basketrows=[]
for name,demands in baskets.items():
 for event,date,sport in demands:basketrows.append(dict(basket=name,event=event,date=date.date(),sport=sport,interpretation='Scenario intention, source-dated event occasion'))
 for inclusion,mp,yp,tp in product([False,True],[116,199],[899,999],[79,89,99]):
  cost,choice=cheapest(demands,inclusion,mp,yp,tournament_price=tp);rows.append(dict(basket=name,monthly_atp=inclusion,monthly_price=mp,yearly_price=yp,tournament_price=tp,total_cost=cost,choice=choice))
result=pd.DataFrame(rows);table(pd.DataFrame(basketrows),'03_basket_definitions');table(result,'03_minimum_cost_baskets');table(result,'basket_results',True)
base=result[(result.yearly_price==999)&(result.tournament_price==99)];display(base[['basket','monthly_atp','monthly_price','total_cost','choice']])
plot=base.assign(scenario=base.monthly_atp.map({False:'ATP excluded',True:'ATP included'})+' / INR'+base.monthly_price.astype(str)).pivot(index='basket',columns='scenario',values='total_cost')
plot.plot.barh(figsize=(11,5));plt.xlabel('Minimum new payment (INR)');plt.title('The same viewing basket can imply a different pass');plt.legend(fontsize=8);fig('03_basket_switch_map','Scenario intentions on source-dated events. Monthly ATP inclusion unresolved. No customer demand inferred.')'''),
('md','## 3. Transparent pricing rules and dominance checks\nTest tier, timing and remaining season sequentially. A player pass cannot promise unplayed matches. Replay INR39 is a feasibility-dependent test, not an existing SKU. Remaining season is priced here using event-start opportunities as an explicitly coarse inventory proxy. It is not viewer value or a precise remaining-live-days measure.'),
('code', '''events=read('atp_event_starts');regular=events[events.tier.isin(['ATP 250','ATP 500','ATP MASTERS 1000']) & events.start_date.notna()].copy();regular['start_date']=pd.to_datetime(regular.start_date)
curve=[]
for date in pd.date_range('2026-01-01','2026-11-23',freq='7D'):
 remaining=int((regular.start_date>=date).sum());inventory_price=399*remaining/len(regular);curve.append(dict(date=date,remaining_event_starts=remaining,reference_price=399,raw_inventory_price=inventory_price,candidate_rounded_price=round(min(inventory_price,99*remaining)),proxy='Equal-weight event starts, excludes ongoing event replays'))
curve=pd.DataFrame(curve);table(curve,'03_remaining_inventory_price')
plt.figure(figsize=(10,3.8));plt.step(curve.date,curve.candidate_rounded_price,where='post');plt.ylabel('Candidate season price (INR)');plt.title('An inventory-based declining price is a test rule, not WTP');fig('03_remaining_season_rule','Guide dates, equal event-start weights. Current declining season checkout is unknown. Validate before testing.')
formats=pd.DataFrame([
('Single match','Proposed INR49 test','One identified match, replay expiry specified before launch','Do not lead with paid acquisition at INR150–200 CAC. Test total cohort contribution and displacement.'),
('Tournament','Case INR79–99','Covered event, scope and replays must be clear','Default low-commitment entry when it is the cheapest covering basket.'),
('Season','Case INR399, declines late season','Remaining ATP coverage, not 365 days','Use actual current price and intended remaining events.'),
('Replay rental','Proposed INR39 test','One selected replay, candidate 48-hour viewing window after activation','Rights and playback enforcement unverified. Reject if substitution loss exceeds induced contribution.'),
('Player or event bundle','Price via existing minimum-cost basket first','Confirmed appearances or flexible event access, explicit withdrawal/refund treatment','Do not promise progression or invent a player premium from video views.'),
('Portfolio bundle','Observed monthly/yearly menu','Dates, devices and ATP inclusion checked','Monthly ATP scope is a two-branch analysis. Annual requires sufficient intended portfolio value.')],columns=['format','price_status','coverage_rule','lead_decision']);display(table(formats,'03_format_decisions'))
check('03_offers',{'two_events_list_comparison':2*99==198,'promotion_gap':198-116==82,'yearly_cannot_win_pure_six_tennis_at_list':cheapest(selected,False,199,999)[0]<=399,'ownership_suppresses_sale':cheapest(selected,True,199,999,owned=True)[0]==0,'adding_atp_access_never_raises_cost':bool((result.pivot(index=['basket','monthly_price','yearly_price','tournament_price'],columns='monthly_atp',values='total_cost')[True]<=result.pivot(index=['basket','monthly_price','yearly_price','tournament_price'],columns='monthly_atp',values='total_cost')[False]).all())})
report('03_offer_findings','Do not automatically push every multi-sport user to a yearly pass. The exact covering basket and existing entitlement decide. Short monthly access may dominate a tennis mini-bundle if ATP is included. Publish complete coverage and suppress redundant sales. Player-specific products require participation protection or refund terms. Test replay and credit on total portfolio contribution.')''')])
notebook('07_contribution_and_pricing','07 | Contribution, repeat buying and pricing risk','Separate marginal acquisition economics from fixed-rights viability. All unobserved costs and behavioural persistence are explicit scenarios. No revenue coverage is called profit.',[
('md','## 1. Contribution bridge\nFor tax-inclusive price P: net revenue = P/(1+tax). Gateway charge uses an illustrative external 2% list fee plus 18% fee tax, conservatively expensed with no input-tax recovery. Other variable cost is additional to that fee. Rights cost is excluded from marginal contribution and assessed separately. Tax-exclusive prices are a separate ledger: tax charged to customers is not revenue.'),
('code', '''def contribution(price,tax=.18,variable=30,fee=.02,fee_tax=.18):
 return price/(1+tax)-price*fee*(1+fee_tax)-variable
rows=[]
for price in [39,49,79,89,99,116,199,399,899,999]:
 for tax in CFG['gst_scenarios']:
  for variable in CFG['variable_cost_scenarios']:
   c=contribution(price,tax,variable)
   for cac in CFG['acquisition_cost_scenarios']:rows.append(dict(price=price,tax=tax,other_variable_cost=variable,cac=cac,net_sales=price/(1+tax),gateway_cost=price*.02*1.18,pre_marketing_contribution=c,after_acquisition=c-cac,contribution_pct_receipts=c/price,scope='Assumption scenario, not observed FanCode margin'))
econ=pd.DataFrame(rows);table(econ,'07_contribution_grid');table(econ,'contribution_grid',True)
base=econ[(econ.tax==.18)&(econ.other_variable_cost==30)&(econ.cac==175)];display(base)
plt.figure(figsize=(10,4));plt.bar(base.price.astype(str),base.pre_marketing_contribution,label='Before acquisition');plt.axhline(175,color=COLORS[3],linestyle='--',label='INR175 acquisition scenario');plt.ylabel('INR per purchase');plt.xlabel('Customer price (INR)');plt.title('Short passes cannot bear the same acquisition cost as seasons');plt.legend();fig('07_contribution_bridge','18% tax-inclusive scenario, 2% gateway + fee tax, INR30 other variable cost. Rights excluded.')
# Explicit tax-exclusive alternative changes customer payable as well as revenue.
exclusive=pd.DataFrame([dict(list_before_tax=p,payable=p*1.18,net_sales=p,contribution=p-p*1.18*.02*1.18-30) for p in [89,399,999]])
display(table(exclusive,'07_tax_exclusive_alternative'))'''),
('md','## 2. Repeat purchase, with horizon definitions kept separate\nThe supplied 60–65% is only a repurchase proportion. First show exactly one possible repeat. Then separately test a stationary geometric process capped at K purchase opportunities. E[purchases] = sum(p^j, j=0..K-1). This is a sensitivity model, not an estimated lifetime.'),
('code', '''repeat=[]
for p in [.60,.65]:
 for k in [2,3,5,10]:
  purchases=sum(p**j for j in range(k))
  for v in [10,30,60]:
   c=contribution(89,variable=v);repeat.append(dict(repurchase_probability=p,opportunity_cap=k,expected_purchases=purchases,net_revenue=89/1.18*purchases,contribution_before_acquisition=c*purchases,contribution_after_175=c*purchases-175,variable=v))
repeat=pd.DataFrame(repeat);display(table(repeat,'07_repeat_horizons'))
plt.figure(figsize=(9,4))
for p,g in repeat[repeat.variable==30].groupby('repurchase_probability'):plt.plot(g.opportunity_cap,g.contribution_after_175,marker='o',label=f'p={p:.0%}')
plt.axhline(0,color='black',lw=.8);plt.xlabel('Maximum purchase opportunities');plt.ylabel('Expected contribution after INR175 CAC');plt.title('Repeat purchases help only if per-order contribution survives');plt.legend();fig('07_repeat_sensitivity','INR89 midpoint tournament scenario. Constant repeat probability is unverified. No infinite lifetime claim.')
ltv=[]
for start in [2026,2027,2028]:
 for r in CFG['renewal_scenarios']:
  for d in CFG['discount_rate_scenarios']:
   years=2028-start+1;c=contribution(399);pv=sum(c*r**j/(1+d)**j for j in range(years));ltv.append(dict(acquisition_year=start,renewal=r,discount_rate=d,covered_seasons=years,pre_marketing_pv=pv,after_175=pv-175))
ltv=pd.DataFrame(ltv);display(table(ltv,'07_rights_horizon_ltv'))
print('Full-season INR399 receipts even for late-2026 acquisition would be optimistic. Use actual remaining-season receipts before launch. Post-2028 value is excluded, not asserted to be zero for the whole company.')'''),
('md','## 3. Credit leakage and discount hurdle\nFor qualifying tournament price E and season price S, control upgrade probability u0 and treatment u1, entry contribution cancels. Delta = u1*C(S-credit) - u0*C(S). Break-even u1/u0 = C(S)/C(S-credit). This assumes the same entry cohort and one upgrade maximum. Full randomized portfolio contribution is the operational primary outcome.'),
('code', '''leak=[]
for credit in [0,39,44.5,50,89]:
 for u0 in [.05,.10,.20,.40]:
  c0=contribution(399);c1=contribution(399-credit);threshold=u0*c0/c1
  leak.append(dict(credit=credit,control_upgrade=u0,required_treatment_upgrade=threshold,required_relative_lift=c0/c1-1,leakage_per_organic_upgrade=c0-c1,qualifier='Same entry cohort and costs'))
leak=pd.DataFrame(leak);display(table(leak,'07_credit_break_even'))
discounts=[]
for price in [39,79,89,99,399]:
 for v in [0,10,30,60]:
  old=contribution(price,variable=v);new=contribution(price*.9,variable=v);discounts.append(dict(price=price,variable=v,old_contribution=old,new_contribution=new,required_volume_uplift=old/new-1 if old>0 and new>0 else np.nan))
discounts=pd.DataFrame(discounts);table(discounts,'07_discount_hurdles')
p=discounts.pivot(index='variable',columns='price',values='required_volume_uplift');plt.figure(figsize=(9,3.5));plt.imshow(p,aspect='auto',cmap='YlOrRd');plt.xticks(range(len(p.columns)),p.columns);plt.yticks(range(len(p)),p.index);plt.colorbar(label='Required relative volume uplift');plt.xlabel('Original price (INR)');plt.ylabel('Other variable cost (INR)');plt.title('A 10% price cut can need much more than 11.1% extra volume');fig('07_discount_hurdles','NaN means the positive-contribution hurdle is not defined. No elasticity measured.')'''),
('md','## 4. Usage and reward costs can reverse the result\nThe Cloudflare public delivery rate is an external stress benchmark, not FanCode procurement evidence. INR80/90/100 per USD are FX scenarios, not current exchange-rate claims. Do not add this delivery estimate to a variable-cost scenario that already includes delivery. Referral voucher face value is not necessarily cash cost.'),
('code', '''usage=[]
for price in [89,399,999]:
 for minutes in [90,600,1800,3600]:
  for fx in [80,90,100]:
   delivery=minutes/1000*float(METRICS['stream_delivery']['value'])*fx
   net=price/1.18-price*.02*1.18-10-delivery
   usage.append(dict(price=price,watch_minutes=minutes,usd_inr_assumption=fx,delivery_benchmark_cost=delivery,other_operations_assumption=10,pre_marketing_contribution=net,after_175=net-175))
usage=pd.DataFrame(usage);display(table(usage,'07_usage_cost_stress'))
plt.figure(figsize=(9,4))
for price,g in usage[usage.usd_inr_assumption==90].groupby('price'):plt.plot(g.watch_minutes,g.after_175,marker='o',label=f'INR{price} receipt')
plt.axhline(0,color='black',lw=.8);plt.xlabel('Delivered watch minutes per buyer over the evaluated term');plt.ylabel('Contribution after INR175 acquisition');plt.title('More viewing also carries a delivery-cost obligation');plt.legend();fig('07_usage_cost_stress','External USD1/1,000-minute benchmark, assumed FX90, INR10 operations. No FanCode contract inference.')
rewards=[]
for price,face in [(89,150),(399,500)]:
 for redemption in [.25,.5,1]:
  for procurement_fraction in [.1,.5,1]:
   reward_cost=face*redemption*procurement_fraction;rewards.append(dict(price=price,voucher_face=face,redemption_assumption=redemption,procurement_fraction_assumption=procurement_fraction,expected_reward_cost=reward_cost,contribution_after_reward=contribution(price)-reward_cost,source_id='v3_fancode_terms'))
display(table(pd.DataFrame(rewards),'07_referral_reward_stress'))
print('Reward funding, redemption and procurement terms are unknown. Published voucher face value must not be described as CAC or cash expense.')'''),
('md','## 5. Fixed-cost coverage and true acquisition\nThe supplied INR150–200 target concerns acquired paying subscribers. The brief does not define a causal incremental denominator. Applying INR200 to incremental CAC is a proposed additional hurdle. Attributed INR175 below is illustrative, not achieved performance. A normalized INR1 crore fixed budget is not the ATP rights fee. Required payers = fixed cost / positive contribution after acquisition. If the denominator is zero or negative, no finite payer scale covers the fixed cost in that scenario.'),
('code', '''fixed=[]
for c in [0,150,175,200]:
 for v in [10,30,60]:
  net=contribution(399,variable=v)-c;fixed.append(dict(fixed_cost=1e7,cac=c,variable=v,contribution_per_payer=net,required_new_payers=np.ceil(1e7/net) if net>0 else np.nan))
display(table(pd.DataFrame(fixed),'07_fixed_cost_coverage'))
inc=pd.DataFrame([dict(reported_cac=c,incremental_fraction=q,true_icac=c/q) for c in [150,175,200] for q in np.arange(.1,1.01,.05)]);table(inc,'07_incrementality_cac')
plt.figure(figsize=(9,4))
for c,g in inc.groupby('reported_cac'):plt.plot(g.incremental_fraction,g.true_icac,label=f'Attributed INR{c}')
plt.axhline(200,color='black',ls='--');plt.ylim(0,1200);plt.xlabel('Fraction of credited payers who are incremental new payers');plt.ylabel('Incremental CAC (INR)');plt.title('Attribution efficiency is not acquisition efficiency');plt.legend();fig('07_incrementality_frontier','Attributed INR175 is hypothetical. 87.5% incrementality is required for a proposed INR200 incremental-CAC hurdle, not a supplied causal target.')
check('07_economics',{'tax_bridge':abs(399/1.18*1.18-399)<1e-8,'credit_no_effect_at_zero':bool((leak[leak.credit==0].required_relative_lift==0).all()),'discount_proportional_hurdle':abs((1/.9-1)-.1111111111)<1e-8,'incremental_fraction_hurdle':175/200==.875,'cost_grid_identity':bool(np.allclose(econ.pre_marketing_contribution-econ.cac,econ.after_acquisition)),'finite_repeat_below_infinite':all(r.expected_purchases<1/(1-r.repurchase_probability) for r in repeat.itertuples())})
report('07_economics_findings',f'Base scenario season contribution before acquisition is INR{contribution(399):.2f}, after INR175 acquisition is INR{contribution(399)-175:.2f}. These are scenario outputs, not company margins. Attributed INR175 requires 87.5% incremental new payers to meet INR200 iCAC. Capped credits need additional upgrades to offset leakage. Rights costs remain a normalized coverage frontier.')''')])
notebook('04_review_friction','04 | Review friction and first-session risks','Use public reviews to discover product friction, not to estimate the prevalence of problems among subscribers. Store audiences, collection windows and review-update behavior differ. No names or original review IDs are exported.',[
('md','## 1. Parse preserved review responses and apply the registered window\nDeduplicate by store and source review ID, retaining the latest encountered snapshot. Use source timestamps in Asia/Kolkata. The same person may appear across stores. Text stays in a local processed file and must be reviewed before redistribution.'),
('code', '''from google_play_scraper.constants.regex import Regex
from google_play_scraper.constants.element import ElementSpecs
reviews={}
for log in [json.loads(x) for x in (ROOT/'data/manifests/review_collection_log.jsonl').read_text().splitlines()]:
 if str(log['http_status'])!='200':continue
 payload=json.loads(Regex.REVIEWS.findall((ROOT/log['file']).read_text())[0]);body=json.loads(payload[0][2])
 for item in body[0] if body and body[0] else []:
  rid=ElementSpecs.Review['reviewId'].extract_content(item);key=log['app_id']+':'+rid
  reviews[key]=dict(review_key=hashlib.sha256(key.encode()).hexdigest()[:20],store='Android mobile' if log['app_id']=='com.dream11sportsguru' else 'Android TV',date=pd.Timestamp(item[5][0],unit='s',tz='UTC').tz_convert('Asia/Kolkata'),rating=ElementSpecs.Review['score'].extract_content(item),text=ElementSpecs.Review['content'].extract_content(item) or '',source_file=log['file'])
for sid in SOURCES:
 if not sid.startswith('fancode_ios_reviews_page'):continue
 entries=rawjson(sid)['feed'].get('entry',[])
 if isinstance(entries,dict):entries=[entries]
 for e in entries:
  if 'im:rating' not in e:continue
  key='iOS:'+e['id']['label'];reviews[key]=dict(review_key=hashlib.sha256(key.encode()).hexdigest()[:20],store='iOS',date=pd.Timestamp(e['updated']['label']).tz_convert('Asia/Kolkata'),rating=int(e['im:rating']['label']),text=e.get('title',{}).get('label','')+' '+e['content']['label'],source_file=SOURCES[sid]['file'])
r=pd.DataFrame(reviews.values());r=r[(r.date>=pd.Timestamp('2025-01-01',tz='Asia/Kolkata'))&(r.date<pd.Timestamp('2026-09-13',tz='Asia/Kolkata'))].copy()
r['text']=r.text.str.replace(r'https?://\\S+|\\S+@\\S+|\\b\\d{10,}\\b','[redacted]',regex=True);r['month']=r.date.dt.strftime('%Y-%m');r['year']=r.date.dt.year;r['low_rating']=r.rating<=2
lex=json.loads((ROOT/'analysis_config/review_lexicon.json').read_text())
for name,pattern in {**lex['patterns'],**{'sport_'+k:v for k,v in lex['sport_patterns'].items()}}.items():r[name]=r.text.str.contains(pattern,case=False,regex=True,na=False)
table(r,'review_features_local_only',True)
counts=r.groupby('store').agg(reviews=('review_key','size'),mean_rating=('rating','mean'),low_rating_share=('low_rating','mean'),tennis_mentions=('sport_tennis','sum'),first_date=('date','min'),last_date=('date','max')).reset_index();display(table(counts,'04_store_coverage'))'''),
('md','## 2. Issue mentions, not automatically complaints\nThe lexicon is deliberately transparent and frozen in analysis_config. “Pass” or “quality” can appear in praise. Report mention rates inside low-rated reviews separately, and never convert mentions into churn or lost revenue. Wilson intervals describe binomial uncertainty conditional on this review sample, not selection bias.'),
('code', '''from statsmodels.stats.proportion import proportion_confint
mention=[]
for store,g in r.groupby('store'):
 for subset,h in [('All',g),('Rating 1–2',g[g.low_rating])]:
  for topic in lex['patterns']:
   k=int(h[topic].sum());n=len(h);lo,hi=proportion_confint(k,n,method='wilson') if n else (np.nan,np.nan)
   mention.append(dict(store=store,subset=subset,topic=topic,mentions=k,review_denominator=n,share=k/n if n else np.nan,wilson_low=lo,wilson_high=hi))
mention=pd.DataFrame(mention);display(table(mention,'04_issue_mentions'))
g=mention[(mention.store=='Android mobile')&(mention.subset=='Rating 1–2')].sort_values('share')
plt.figure(figsize=(9,4));plt.barh(g.topic.str.replace('_',' '),g.share*100);plt.errorbar(g.share*100,range(len(g)),xerr=[(g.share-g.wilson_low)*100,(g.wilson_high-g.share)*100],fmt='none',ecolor='black',capsize=3);plt.xlabel('Percent of low-rated mobile reviews');plt.title('First-session friction deserves a place in the growth strategy');fig('04_friction_mentions','Heuristic topic mentions, overlapping categories. Conditional Wilson intervals do not remove review selection bias.')
monthly=r.groupby(['store','month']).agg(reviews=('review_key','size'),rating=('rating','mean'),low_share=('low_rating','mean'),tennis_mentions=('sport_tennis','sum')).reset_index();table(monthly,'04_monthly_review_diagnostics')
figx,ax=plt.subplots(2,1,figsize=(11,6),sharex=True)
for store,g in monthly.groupby('store'):
 ax[0].plot(pd.to_datetime(g.month),g.rating,marker='.',label=store);ax[1].plot(pd.to_datetime(g.month),g.reviews,label=store)
ax[0].set(ylabel='Mean review rating',title='Review composition changes over time');ax[0].legend();ax[1].set(ylabel='Reviews collected');fig('04_review_time_series','Public storefront sample, not a before/after causal ATP-launch evaluation. iOS is a latest-500 window.')
# Fairer calendar alignment: only Jan-Aug in both years, mobile store only.
matched=r[(r.store=='Android mobile')&(r.date.dt.month<=8)].groupby('year').agg(n=('review_key','size'),low_share=('low_rating','mean'),tennis_mentions=('sport_tennis','sum'),access_mentions=('stream_access','mean')).reset_index();display(table(matched,'04_matched_month_comparison'))'''),
('md','## 3. Exploratory themes with a chronological holdout\nFit TF-IDF and six nonnegative matrix factorization components on 2025 mobile reviews only. Transform 2026 without refitting. This checks whether a vocabulary is still usable, not whether topics are true customer segments. NMF components are overlapping latent themes. No cluster is assigned a market size.'),
('code', '''from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF
train=r[(r.store=='Android mobile')&(r.year==2025)&(r.text.str.len()>=25)]
hold=r[(r.store=='Android mobile')&(r.year==2026)&(r.text.str.len()>=25)]
vectorizer=TfidfVectorizer(stop_words='english',min_df=5,max_df=.8,max_features=2500,ngram_range=(1,2),token_pattern=r'(?u)\\b[a-zA-Z][a-zA-Z]+\\b')
X=vectorizer.fit_transform(train.text);Y=vectorizer.transform(hold.text)
nmf=NMF(n_components=6,init='nndsvda',random_state=CFG['seed'],max_iter=700)
W=nmf.fit_transform(X);H=nmf.transform(Y);words=vectorizer.get_feature_names_out()
topics=pd.DataFrame([dict(component=k,top_terms=', '.join(words[np.argsort(row)[-10:][::-1]]),train_documents=len(train),holdout_documents=len(hold),mean_train_weight=W[:,k].mean(),mean_holdout_weight=H[:,k].mean()) for k,row in enumerate(nmf.components_)])
display(table(topics,'04_exploratory_themes'))
print('Holdout documents with no training vocabulary:',int((Y.getnnz(axis=1)==0).sum()))
# Export only aggregate sport-mention diagnostics, not claims of sport-specific customer prevalence.
sports=pd.DataFrame([dict(sport=k,mentions=int(r['sport_'+k].sum()),low_rated_mentions=int((r['sport_'+k]&r.low_rating).sum())) for k in lex['sport_patterns']]);display(table(sports,'04_sport_mention_counts'))
check('04_reviews',{'deduplicated_review_keys':r.review_key.is_unique,'mobile_window_count':int(counts.set_index('store').loc['Android mobile','reviews'])==14665,'tv_window_count':int(counts.set_index('store').loc['Android TV','reviews'])==64,'ios_window_count':int(counts.set_index('store').loc['iOS','reviews'])==500,'ratings_valid':bool(r.rating.between(1,5).all()),'train_before_holdout':train.date.max()<hold.date.min()})
report('04_review_findings','Prioritize a measurable pay-to-play reliability and entitlement journey. Topic counts are mentions, not adjudicated complaints, and no causal pre/post claim is made. NMF is exploratory with a chronological holdout. Sport labels are keyword signals, not customer identities. Raw and row-level review text remain local-only. Formal classifier validation and subscriber-level incidence require other data.')''')])
notebook('05_search_attention','05 | Search attention and competing explanations','Use relative search interest to challenge the growth narrative. These are search terms in India, not topics, unique viewers or subscription attribution. Separate requests have separate normalization.',[
('md','## 1. Reconstruct the saved query tables\nThe 2026 four-term request shares one scale. The football pair and 2025 weekly pair do not share that scale. Preserve query context, rounding and boundary weeks. No extrapolation to absolute searches.'),
('code', '''daily=pd.read_csv(path('google_trends_daily_table_v2'),sep='\\t');daily.columns=['date','tennis','FanCode','Formula 1','MotoGP'];daily['date']=pd.to_datetime(daily.date)
football=pd.read_csv(path('google_trends_football_table_v5'),sep='\\t');football.columns=['date','football','FanCode'];football['date']=pd.to_datetime(football.date)
s=text('v4_trends_2025_timeline');weeklyraw=json.loads(s[s.index('{'):])['default']['timelineData']
weekly=pd.DataFrame([dict(week=pd.to_datetime(int(x['time']),unit='s',utc=True),label=x['formattedTime'],tennis=x['value'][0],FanCode=x['value'][1]) for x in weeklyraw])
table(daily,'trends_daily_four_terms',True);table(football,'trends_football_pair',True);table(weekly,'trends_2025_weekly',True)
print(text('google_trends_query_context_v2'))
figx,axes=plt.subplots(2,1,figsize=(11,6))
for col in daily.columns[1:]:axes[0].plot(daily.date,daily[col].rolling(7,min_periods=7).mean(),label=col)
axes[0].set(title='Within-request 7-day mean search interest',ylabel='Relative interest');axes[0].legend(ncol=4,fontsize=8)
axes[1].plot(football.date,football.football,label='football');axes[1].plot(football.date,football.FanCode,label='FanCode');axes[1].set(title='Separate football pair: different scale and rounding',ylabel='Relative interest');axes[1].legend();fig('05_search_series','Google Trends India web search, Jan1–Sep12 2026. Context contains noisy related queries. No subscriber inference.')'''),
('md','## 2. Association and a temporal placebo check\nReport rank correlation in levels and first differences. Circular shifts preserve each series’ shape but displace its alignment. The comparison is a sensitivity diagnostic, not a valid randomization p-value under guaranteed exchangeability. Avoid selecting a preferred lag after inspecting outcomes.'),
('code', '''from scipy.stats import spearmanr
assoc=[]
for label,df,cols in [('four_term',daily,['tennis','Formula 1','MotoGP']),('football_pair',football,['football'])]:
 for sport in cols:
  x=df[sport].to_numpy();y=df.FanCode.to_numpy();rho=spearmanr(x,y).statistic;diff=spearmanr(np.diff(x),np.diff(y)).statistic
  shifted=np.array([spearmanr(x,np.roll(y,k)).statistic for k in range(8,len(y)-7)])
  assoc.append(dict(request=label,sport=sport,level_rho=rho,difference_rho=diff,circular_shift_abs_exceedance=float((np.abs(shifted)>=abs(rho)).mean()),zero_share=float((x==0).mean()),n=len(x)))
assoc=pd.DataFrame(assoc);display(table(assoc,'05_search_associations'))
plt.figure(figsize=(8,4));x=np.arange(len(assoc));plt.bar(x-.17,assoc.level_rho,.34,label='Levels');plt.bar(x+.17,assoc.difference_rho,.34,label='First differences');plt.xticks(x,assoc.sport);plt.axhline(0,color='black',lw=.8);plt.ylabel('Spearman correlation with FanCode');plt.title('Associations depend on the request and time-series treatment');plt.legend();fig('05_search_associations','Descriptive correlations. Broad terms and cricket/other events confound interpretation. No causal sport contribution.')
peaks=daily.nlargest(15,'FanCode').copy();f1=read('f1_races');fdates=pd.to_datetime(f1.start_utc,utc=True).dt.tz_convert('Asia/Kolkata').dt.tz_localize(None).dt.normalize();slots=read('atp_slots');adates=pd.to_datetime(slots.date_ist)
peaks['days_to_nearest_F1_race']=[min(abs((fdates-date).dt.days)) for date in peaks.date];peaks['days_to_nearest_sampled_ATP_slot']=[min(abs((adates-date).dt.days)) for date in peaks.date];display(table(peaks,'05_peak_date_context'))
zero=pd.DataFrame([dict(request='football pair',term='FanCode',zero_days=int((football.FanCode==0).sum()),days=len(football)),dict(request='four term',term='FanCode',zero_days=int((daily.FanCode==0).sum()),days=len(daily))]);display(table(zero,'05_rounding_diagnostic'))
check('05_trends',{'daily_dates_255':len(daily)==255 and daily.date.is_unique,'football_dates_identical':daily.date.equals(football.date),'weekly_bins_53':len(weekly)==53,'bounded_values':bool(daily.iloc[:,1:].apply(lambda c:c.between(0,100).all()).all())})
report('05_search_findings','Google Trends cannot independently verify which sport drives paid subscriptions. Noisy related queries and request-level rounding materially constrain interpretation. Use the series for timing exploration and creative hypotheses, with observed peak dates explicitly separated from causal explanations. The 2025 pair provides historical within-request seasonality only, not a comparable YoY level.')''')])
notebook('06_player_and_video_risk','06 | Player dependence and public content signals','Test the risk in selling access around a popular player, using a clean historical results archive and bounded official-channel video metadata. Completed participation cannot guarantee future appearances.',[
('md','## 1. Results audit and a conservative historical baseline\nThe 2026 alternative files have date/key inconsistencies. Use the documented 2025 archive for the quantitative player-risk baseline. Grand Slams and team events are excluded from the regular-tour comparison. The season file includes Brisbane and Hong Kong starting in December 2024. These are retained as 2025-season events, with original dates. United Cup is explicitly excluded even though its level code resembles a tour event. A player-event entry means at least one recorded match, not a complete entrants list including byes or withdrawn-before-play players.'),
('code', '''audit=pd.DataFrame(json.loads((ROOT/'data/manifests/results_source_qa.json').read_text()));display(table(audit,'06_results_source_audit'))
d=pd.read_csv(path('sackmann_archive_2025'));d['source_id']='sackmann_archive_2025'
# Remove byte-equivalent duplicate rows only, never a reused incomplete match key.
d=d.drop_duplicates();regular=d[d.tourney_level.isin(['A','M','F']) & ~d.tourney_name.str.contains('United Cup|Laver Cup',case=False,na=False)].copy();regular['tourney_date']=pd.to_datetime(regular.tourney_date.astype(str),format='%Y%m%d')
table(regular,'results_2025_regular',True)
appear=[]
for side in ['winner','loser']:
 z=regular[['tourney_id','tourney_name','tourney_date','round',side+'_name']].rename(columns={side+'_name':'player'});appear.append(z)
appear=pd.concat(appear,ignore_index=True)
rounds={'R128':1,'R64':2,'R32':3,'R16':4,'QF':5,'SF':6,'F':7,'RR':0}
appear['round_order']=appear['round'].map(rounds)
pe=appear.groupby(['player','tourney_id','tourney_name']).agg(matches=('round','size'),max_round=('round_order','max')).reset_index();pe['reached_SF']=pe.max_round>=6
players=pe.groupby('player').agg(events_played=('tourney_id','nunique'),matches=('matches','sum'),SF_events=('reached_SF','sum')).reset_index();players['SF_share_of_played_events']=players.SF_events/players.events_played
# Top ten by recorded match count is an explicit, reproducible retrospective selection rule.
top=players.nlargest(10,'matches');display(table(top,'06_player_progression'));table(pe,'player_event_2025',True)
plt.figure(figsize=(10,4));plt.barh(top.sort_values('SF_share_of_played_events').player,top.sort_values('SF_share_of_played_events').SF_share_of_played_events*100);plt.xlabel('Percent of recorded played events reaching semifinal');plt.title('Even busy players do not guarantee a weekend appearance');fig('06_player_appearance_risk','2025 regular-tour archive. Retrospective top ten by matches, not popular-player WTP or 2026 prediction.')
# Compare single-player and two-player coverage within observed event universe.
universe=set(regular.tourney_id);names=top.player.iloc[:3].tolist();bundle=[]
from itertools import combinations
for k in [1,2,3]:
 for chosen in combinations(names,k):
  x=pe[pe.player.isin(chosen)];bundle.append(dict(players=' + '.join(chosen),events_with_any_recorded_appearance=x.tourney_id.nunique(),events_with_any_SF=x[x.reached_SF].tourney_id.nunique(),archive_event_universe=len(universe)))
display(table(pd.DataFrame(bundle),'06_player_bundle_coverage'))'''),
('md','## 2. Parse bounded FanCode video-search metadata\nDeduplicate video IDs across two ranked keyword searches. Views are displayed cumulative counts, not India-specific viewers. Relative publication labels do not support exact views-per-day normalization. Do not correlate publication hour with match start.'),
('code', '''videos={}
def walk(obj):
 if isinstance(obj,dict):
  for key,value in obj.items():
   if key in ['videoRenderer','channelVideoPlayerRenderer']:yield value
   yield from walk(value)
 elif isinstance(obj,list):
  for value in obj:yield from walk(value)
def label(x):return x.get('simpleText',''.join(r.get('text','') for r in x.get('runs',[])))
for sid in ['fancode_youtube_tennis_search','fancode_youtube_atp_search']:
 raw=path(sid).read_text();m=re.search(r'(?:var )?ytInitialData\\s*=\\s*',raw);obj,_=json.JSONDecoder().raw_decode(raw[m.end():])
 assert obj['metadata']['channelMetadataRenderer']['externalId']=='UCF10AG_t1AYW3mlmX7g1VJA'
 for v in walk(obj.get('contents',{})):
  vid=v['videoId'];title=label(v.get('title',{}));views=label(v.get('viewCountText',{}));age=label(v.get('publishedTimeText',{}))
  count=re.search(r'([\\d,]+) views?',views);videos[vid]=dict(video_id=vid,title=title,displayed_views=views,views=int(count.group(1).replace(',','')) if count else np.nan,publication_label=age,source_id=sid)
v=pd.DataFrame(videos.values());v['star_mention']=v.title.str.contains('Alcaraz|Sinner|Djokovic|Nadal',case=False,regex=True);v['highlight_mention']=v.title.str.contains('highlight',case=False)
table(v,'video_metadata',True);display(table(v.nlargest(15,'views'),'06_top_displayed_videos'))
summary=v.groupby('star_mention').agg(videos=('video_id','size'),median_views=('views','median'),total_views=('views','sum')).reset_index();display(table(summary,'06_video_star_diagnostic'))
plt.figure(figsize=(8,4))
for k,g in v.groupby('star_mention'):plt.scatter(np.repeat(int(k),len(g))+rng.normal(0,.025,len(g)),np.log10(g.views+1),alpha=.55,label='Star-name title' if k else 'Other title')
plt.xticks([0,1],['Other title','Selected star mentioned']);plt.ylabel('log10(displayed views + 1)');plt.title('Content popularity is highly dispersed');fig('06_video_views','Keyword-selected metadata, cumulative views, mixed ages and competitions. Title association is not player causal effect.')
check('06_player_video',{'video_ids_unique':v.video_id.is_unique,'video_count_53':len(v)==53,'only_2025_season_ids':bool(regular.tourney_id.str.startswith('2025-').all()),'player_event_unique':not pe.duplicated(['player','tourney_id']).any(),'progression_bounded':bool(players.SF_share_of_played_events.between(0,1).all())})
report('06_player_video_findings','Prefer event or flexible access over an unconditional player-final promise. Historical played-event progression shows appearance risk and does not count pre-event withdrawals. Videos provide a creative prioritization proxy, not willingness to pay or a price premium. Replays, alternative-player options and clear refunds should be evaluated before testing a player-specific SKU.')''')])
notebook('09_retention_and_experiments','09 | Retention, opportunity gaps and causal tests','Design a measurement system rather than inventing cohort outcomes. No survey, experiment or internal event stream exists in this package. Numerical power results are planning calculations.',[
('md','## 1. Opportunity-adjusted journeys\nUse the next dated regular-tour window as an example of a return opportunity. A source-dated tournament window is not a confirmed player appearance or usable hour. Keep first-ever, reactivated, new-entitlement and already-covered users separate.'),
('code', '''future=read('atp_future_windows');future=future[future.regular_atp.astype(str).str.lower()=='true'].copy();future['start_date']=pd.to_datetime(future.start_date);future['end_date']=pd.to_datetime(future.end_date)
journeys=[]
for r in future.itertuples():
 nexts=future[future.start_date>r.end_date].sort_values('start_date')
 if len(nexts):
  n=nexts.iloc[0];journeys.append(dict(acquiring_event=r.event,end_date=r.end_date,next_event=n.event,next_start=n.start_date,gap_days=(n.start_date-r.end_date).days,trigger='After successful play, show time and coverage; confirm usable slot',source_id='atp_future_calendar_rendered_v2'))
journeys=pd.DataFrame(journeys);display(table(journeys,'09_next_event_journeys'))
states=pd.DataFrame([
('First-ever payer','First successful ATP payment, no previous FanCode payment','Pay-to-play, next included event, relevant upgrade','Incremental new payer and portfolio contribution'),
('Reactivated payer','Prior payment but no active access','Restore entitlement clarity, chosen next occasion','Incremental reactivation contribution, not new-payer CAC'),
('Existing payer, ATP uncovered','Current other-sport pass does not cover ATP','Cheapest relevant additional coverage','Incremental total portfolio contribution'),
('ATP already covered','Verified active covering pass','Suppress redundant sale, relevant live/replay nudge','Renewal at genuine expiry and contribution')],columns=['state','eligibility','treatment','primary_outcome']);display(table(states,'09_lifecycle_treatments'))
kpis=pd.DataFrame([
('Incremental new-payer CAC','Incremental campaign cost / treatment-induced first-ever payers','30/60/90 days','Undefined if estimated lift <=0'),
('Portfolio contribution per eligible user','All portfolio net receipts minus variable costs / all randomized users','90 days plus renewal followup','Include non-buyers as zero, refunds and displacement'),
('Second-event engagement','Cohort users watching a different event / all mature eligible cohort users','30 days and next available relevant opportunity','Pre-register 5/15/30-minute sensitivity, not universal habit threshold'),
('Repeat payment','Users making a separate subsequent payment / mature paid cohort','30/60/90 days','Exclude initial prepaid validity and separate ATP/other-sport payment'),
('Renewal','Passes renewed / passes reaching genuine expiry plus grace','Term-specific','Do not call day30 active season access a renewal'),
('Playback failure','Paid viewing attempts failing to start / paid viewing attempts','First session and ongoing','Repeated attempts need user and attempt views'),
('Opt-out','Users opting out / messaged users','7/30 days','Include all treatment contacts'),
('Opportunity-adjusted return','Users returning at next relevant available event / eligible users with that opportunity','Next event plus fixed grace','Report users with no opportunity separately')],columns=['kpi','definition','horizon','guardrail']);display(table(kpis,'09_kpi_dictionary'))'''),
('md','## 2. Power calculation for binary acquisition\nTwo-sided 5% alpha and 80% power, equal randomized arms, independent users. Conversion baselines and lifts are planning scenarios. Clustered allocation needs a design effect. Multiple primary tests require a revised error budget. Powering acquisition does not automatically power contribution or annual renewal.'),
('code', '''from statsmodels.stats.power import NormalIndPower
from statsmodels.stats.proportion import proportion_effectsize
power=[]
for p0 in [.005,.01,.02,.05]:
 for relative in [.1,.2,.3,.5]:
  p1=p0*(1+relative);effect=abs(proportion_effectsize(p1,p0));n=int(np.ceil(NormalIndPower().solve_power(effect_size=effect,alpha=.05,power=.8,ratio=1)))
  power.append(dict(baseline=p0,relative_lift=relative,treatment_rate=p1,absolute_lift=p1-p0,users_per_arm=n,total_users=2*n))
power=pd.DataFrame(power);display(table(power,'09_binary_power_grid'))
plt.figure(figsize=(9,4))
for p0,g in power.groupby('baseline'):plt.plot(g.relative_lift*100,g.total_users,marker='o',label=f'Baseline {p0:.1%}')
plt.yscale('log');plt.xlabel('Relative acquisition lift to detect (%)');plt.ylabel('Total randomized users (log scale)');plt.title('A small media budget cannot guarantee a decisive lift test');plt.legend();fig('09_power_requirements','Analytical planning approximation, 80% power, two-sided 5% alpha. Not an experiment result.')
clusters=pd.DataFrame([dict(mean_cluster_size=m,icc=rho,design_effect=1+(m-1)*rho) for m in [50,200,1000] for rho in [.001,.01,.05]]);display(table(clusters,'09_cluster_design_effect'))'''),
('md','## 3. Contribution uncertainty and mature outcomes\nUse a minimum detectable change in mean contribution, not a conversion-only proxy. Required sample depends on the unknown variance. A ratio such as iCAC becomes unstable when incremental payers approach zero. Do not calculate a profitable-looking ratio after conditioning on purchasers only.'),
('code', '''from scipy.stats import norm
z=norm.ppf(.975)+norm.ppf(.8)
contrib=pd.DataFrame([dict(sd_per_eligible_user=sd,minimum_detectable_contribution=delta,users_per_arm=int(np.ceil(2*z*z*sd*sd/(delta*delta)))) for sd in [20,50,100,200] for delta in [1,2,5,10]])
display(table(contrib,'09_contribution_power'))
# Maturity example is calendar arithmetic, not simulated retention data.
acq=pd.date_range('2026-06-01','2026-09-12',freq='7D');cut=pd.Timestamp(CFG['cutoff']);maturity=pd.DataFrame({'acquisition_date':acq,'days_observed':(cut-acq).days})
for horizon in [30,60,90]:maturity[f'eligible_{horizon}d']=maturity.days_observed>=horizon
table(maturity,'09_followup_maturity_example')
pilot=pd.DataFrame([
('0','Instrumentation and entitlement','Verify access, define first-ever payer and payment ledger, assign user IDs','Do not start price tests with unresolved access or missing refunds'),
('1','One acquisition treatment','User-level persistent holdout, separate paid/owned eligibility, fixed horizon','Scale only positive incremental portfolio contribution with acceptable uncertainty'),
('2','One offer treatment','Randomize within event and ownership strata, keep media constant','Reject if discount/credit displaces higher-value purchases'),
('3','Retention nudge','After successful play, relevant next occasion versus holdout','Engagement is leading evidence only, renewal needs term maturity'),
('4','Expansion','Increase only where measured marginal contribution and reachable capacity support it','Pause at nonpositive marginal contribution or worsening playback/refund guardrails')],columns=['stage','test','design','stop_or_scale_rule']);display(table(pilot,'09_pilot_design'))
check('09_experiments',{'positive_sample_sizes':bool((power.users_per_arm>0).all()),'larger_lift_requires_fewer_users':all(g.sort_values('relative_lift').users_per_arm.is_monotonic_decreasing for _,g in power.groupby('baseline')),'cluster_design_effect_at_least_one':bool((clusters.design_effect>=1).all()),'mature_90_subset_30':bool((~maturity.eligible_90d|maturity.eligible_30d).all())})
report('09_retention_findings','Sequence the pilot instead of splitting a small budget across many underpowered tests. Fix and instrument pay-to-play first. Primary business outcome is total portfolio contribution per randomized eligible user. Define mature repeat and genuine renewal separately. Opportunity-adjusted return complements calendar-day return, but cannot hide unavailable events or selectively exclude disengaged users.')''')])
notebook('08_economics_model','08 | The economics model: two cohorts, channel CAC, break-even and gates','The single source of truth for every economic figure in the recommendation. Two mutually exclusive cohorts are each measured against their own holdout. **Acquisition** buys new ATP pass buyers and is counted on an incremental basis. **Upgrade** moves existing ATP pass buyers to a season pass, and only upgrades above the control rate are credited, with the credit charged to every treated upgrader. The model lives in `models/atp_economics.py`; every input, with its evidence tag, is in `models/model_inputs.json`. Rights fees are excluded: this is an incremental campaign P&L, not a claim about total rights ROI.',[
('code', '''sys.path.insert(0, str(ROOT/'models'))
import atp_economics as m
res = m.run()
rows=[]
for section,items in m.INPUTS.items():
 if section.startswith('_'):continue
 for key,x in items.items():
  if key.startswith('_'):continue
  rows.append(dict(section=section,input=key,value=json.dumps(x['value']) if isinstance(x['value'],(list,dict)) else x['value'],tag=x.get('tag',''),source=x.get('source',''),note=x.get('note','')))
inputs=pd.DataFrame(rows);display(table(inputs,'08_model_inputs'))
print('Evidence tags:',inputs.tag.value_counts().to_dict())'''),
('md','## 1. Unit economics\nContribution = price / 1.18 GST, less a 2% gateway fee plus GST on the fee, less INR 30 variable cost. The upgrade credit costs less than its INR 44.50 face value because GST and the gateway fee fall with the price.'),
('code', '''u=pd.DataFrame([dict(item=k,value=v) for k,v in res['unit_economics'].items()]);display(table(u,'08_unit_economics'))'''),
('md','## 2. Channel economics and the INR 3.04 Cr conditional envelope\nChannels that clear the brief’s INR 150–200 target on attributed CAC keep their envelope. Paid media, at INR 333, is capped to a INR 25 lakh external-audience test. The freed money is not moved into owned messaging, because owned reach is finite and its incremental CAC rises with depth. It becomes a **performance reserve**, released only to a channel whose measured marginal incremental CAC is at or below INR 200. Test-ceiling channels have no public cost basis; their CAC is a purchasing rule, not an estimate.'),
('code', '''ch=pd.DataFrame(res['channels']);display(table(ch,'08_channel_cac_and_net'))
env=pd.DataFrame([dict(item=k,value=v) for k,v in res['envelope'].items() if not isinstance(v,dict)]);display(table(env,'08_envelope_summary'))
gates=pd.DataFrame(res['gate_allocation']);display(table(gates,'08_gate_allocation'))
fig_,ax=plt.subplots(figsize=(10,4.2))
order=ch.sort_values('net_per_payer_24m_at_100')
ax.barh(order.label,order.net_per_payer_24m_at_100,color=[COLORS[3] if x< -1 else COLORS[1] for x in order.net_per_payer_24m_at_100],label='All attributed payers incremental')
ax.scatter(order.net_per_payer_24m_at_87_5,order.label,color='black',zorder=3,label='87.5% incremental')
ax.axvline(0,color='black',lw=.8);ax.set_xlabel('24-month contribution minus attributed CAC, INR per payer, before any upgrade')
ax.set_title('No acquisition channel pays back on pass purchases alone. Owned comes closest');ax.legend(loc='lower right',fontsize=8)
fig('08_channel_net_per_payer','Contribution per acquired payer over 24 months = 1.625 purchases x INR 43.32 x (1 + 40% year-two return) = INR 98.56. Scenario, not observed.')'''),
('md','## 3. Personas and capacity\nIn-app channels (owned, native) reach portfolio fans already on FanCode and are split in proportion to the base sport pools. External channels (contests, publisher, paid) reach the Slam Tourist. Pools can overlap and are a capacity check, not a forecast.'),
('code', '''pp=pd.DataFrame([dict(persona=k,attributed_payers=v,share=res['personas']['payer_share'][k]) for k,v in res['personas']['payers'].items()]);display(table(pp,'08_persona_payers'))
pools=pd.DataFrame([dict(scenario=k,**{s+'_m':x for s,x in d.items()}) for k,d in res['personas']['pools_m'].items()]);pools['payer_target_share_of_pools']=[res['personas']['capacity_share_of_pools'][k] for k in pools.scenario];display(table(pools,'08_sport_pools_capacity'))'''),
('md','## 4. The upgrade cohort and the 24-month P&L\nEligible pass buyers = 24M ordinary-week viewers x 90% core (C, illustrative) x 20% reached (A) x 20% active ATP pass buyers (A) = 864k. The control upgrade rate is 10% (A). An incremental upgrade is worth the season contribution less the passes that buyer would have bought anyway, in year one and again at 85% renewal in year two. The credit is paid to every treated upgrader, including the 10% who would have upgraded anyway.'),
('code', '''uc=pd.DataFrame([dict(item=k,value=v) for k,v in res['upgrade_cohort'].items()]);display(table(uc,'08_upgrade_cohort'))
grid=pd.DataFrame(res['pnl_grid']);display(table(grid,'08_pnl_grid'))
scen=pd.DataFrame([dict(scenario=k,**v) for k,v in res['scenarios'].items()]);display(table(scen,'08_pnl_scenarios'))
ref=res['reference_case']
steps=[('Acquired payers\\nyear 1',ref['acquisition_y1']),('Upgrades, net\\nof credit, year 1',ref['upgrade_y1']),('Committed spend\\nincl. retention',-ref['spend']),('Year-one\\nnet',None),('Year-two\\ncontribution',ref['y2']),('Net at\\n24 months',None)]
fig_,ax=plt.subplots(figsize=(10,4.6));run=0;tops=[0]
for i,(label,val) in enumerate(steps):
 if val is None:
  ax.bar(i,run/1e7,color='#193047',width=.6);ax.annotate(f'{run/1e7:+.2f}',(i,run/1e7),xytext=(0,4 if run>=0 else -12),textcoords='offset points',ha='center',fontsize=9);tops.append(run);continue
 ax.bar(i,val/1e7,bottom=run/1e7,color=COLORS[1] if val>=0 else COLORS[3],width=.6);end=run+val
 ax.annotate(f'{val/1e7:+.2f}',(i,max(run,end)/1e7),xytext=(0,4),textcoords='offset points',ha='center',fontsize=9);tops+= [run,end];run=end
ax.set_ylim(min(tops)/1e7-.35,max(tops)/1e7+.35)
ax.axhline(0,color='black',lw=.8);ax.set_xticks(range(len(steps)));ax.set_xticklabels([s[0] for s in steps],fontsize=8.5);ax.set_ylabel('INR crore')
ax.set_title(f"Reference case: 16% upgrade rate, 87.5% incrementality. Payback {ref['payback_months']:.1f} months",fontsize=12)
fig('08_reference_waterfall','Reference scenario only. It clears 24-month break-even but not the 15-month payback gate. Rights fee excluded.')'''),
('md','## 5. What the upgrade rate has to be\nTwo thresholds matter. **24-month break-even** is where the campaign repays its committed spend. **15-month payback** is the Gate 3 rule. Both are treatment upgrade rates against a 10% control.'),
('code', '''be=[]
for q in m.v('acquired_payers','incrementality_scenarios'):
 be.append(dict(incrementality=q,net_without_upgrades=res['without_upgrades'][str(q)],break_even_rate=res['break_even_treatment'][str(q)],rate_for_15m_payback=res['treatment_for_15m_payback'][str(q)],break_even_if_reserve_deployed=res['break_even_treatment_reserve_deployed'][str(q)]))
be=pd.DataFrame(be);display(table(be,'08_break_even_rates'))
sens=pd.DataFrame([dict(active_pass_buyer_share=float(s),incrementality=float(q),break_even_rate=r) for s,d in res['break_even_treatment_by_pass_buyer_share'].items() for q,r in d.items()]);display(table(sens,'08_break_even_by_pass_buyer_share'))
ren=pd.DataFrame([dict(season_renewal=float(k),break_even_rate_at_87_5=v) for k,v in res['break_even_treatment_by_renewal'].items()]);display(table(ren,'08_break_even_by_renewal'))
fig_,ax=plt.subplots(figsize=(10,4.2));rates=np.linspace(.10,.24,57)
for q,c in zip([1.0,.875,.6],[COLORS[1],COLORS[0],COLORS[3]]):ax.plot(rates*100,[m.pnl(t,q)['net_24m']/1e7 for t in rates],color=c,label=f'{q:.1%} of acquired payers incremental')
ax.axhline(0,color='black',lw=.8);ax.axvline(10,color='grey',ls=':');ax.text(10.2,ax.get_ylim()[1]*.85,'control 10%',fontsize=8,color='grey')
ax.set_xlabel('Treatment upgrade rate among eligible pass buyers (%)');ax.set_ylabel('Net at 24 months, INR crore');ax.legend(fontsize=8)
b_,p_=res['break_even_treatment'],res['treatment_for_15m_payback']
ax.set_title(f"Break-even at {b_['1.0']:.1%}-{b_['0.6']:.1%}; 15-month payback only at {p_['1.0']:.1%}-{p_['0.6']:.1%}")
fig('08_break_even_curve','Base assumptions: 20% of reached core are active pass buyers, 85% renewal, INR 36.66 credit cost on every treated upgrader. Performance reserve unspent.')'''),
('md','## 6. Sizing the gates to the economic test, not to mere detection\nGate 1 proves owned acquisition is incremental: the 95% lower bound on the lift must clear the lift at which incremental CAC equals INR 200. Gate 2 proves the upgrade engine: the 95% lower bound of (treatment − control) must clear the threshold minus the control rate. Both use 80% power. A true rate close to the threshold cannot be proved at any sensible cost; then the decision is continue or reallocate, never scale.'),
('code', '''g1=pd.DataFrame([res['gate1_owned_pilot']]);display(table(g1,'08_gate1_owned_pilot'))
g2=pd.DataFrame(res['gate2_upgrade_test']);display(table(g2,'08_gate2_upgrade_test'))'''),
('md','## 7. Independent checks\nKey outputs are recomputed with Decimal arithmetic outside the model code.'),
('code', '''from decimal import Decimal as D
pass_c=D(89)/D('1.18')-D(89)*D('0.02')*D('1.18')-D(30)
season_c=D(399)/D('1.18')-D(399)*D('0.02')*D('1.18')-D(30)
credit=season_c-(D('354.5')/D('1.18')-D('354.5')*D('0.02')*D('1.18')-D(30))
owned=D('0.8631')/D('0.01')*D('1.15')
payers=D(9200000)/owned+D(4300000)/D(150)+D(2500000)/((D(50000)+D(12000))/D(390))+D(1200000)/D(180)+D(2500000)/(D(10)/D('0.03'))
spend=D(19700000)+D(3000000)+D(4320000)*D('0.8631')*D('0.5')*D('1.15')
acq24=payers*D('0.875')*D('1.625')*pass_c*D('1.4')
inc=D('0.06')*D(864000);upg=inc*(season_c-D('1.625')*pass_c)*(1+D('0.85'))-D('0.16')*D(864000)*credit
ref_net=acq24+upg-spend
checks={'pass_contribution':abs(float(pass_c)-res['unit_economics']['pass_contribution'])<1e-9,
 'season_contribution':abs(float(season_c)-res['unit_economics']['season_contribution'])<1e-9,
 'credit_cost':abs(float(credit)-res['unit_economics']['credit_cost_per_upgrade'])<1e-9,
 'attributed_payers':abs(float(payers)-res['envelope']['attributed_payers'])<1e-6,
 'reference_net_24m':abs(float(ref_net)-res['reference_case']['net_24m'])<1e-3,
 'break_even_is_zero':abs(m.pnl(res['break_even_treatment']['0.875'],0.875)['net_24m'])<1e-3,
 'payback_threshold_is_15':abs(m.pnl(res['treatment_for_15m_payback']['0.875'],0.875)['payback_months']-15)<1e-6,
 'envelope_reconciles':abs(sum(g['total'] for g in res['gate_allocation'])-30400000)<1e-6,
 'gates_reconcile':abs(gates.gate1.sum()-1e5)<1e-6 and abs(gates.gate2.sum()-75e5)<1e-6 and abs(gates.gate3.sum()-228e5)<1e-6,
 'only_owned_native_contests_clear_200_at_87_5':set(ch[ch.clears_200_at_87_5].channel)=={'owned_lifecycle','native_personalities','contests'},
 'upgrades_exclude_control':res['reference_case']['incremental_upgrades']==0.06*864000}
check('08_economics_model',checks)
r=res;ref=r['reference_case']
report('08_economics_findings',f"Committed acquisition of INR {r['envelope']['committed_acquisition']/1e7:.2f} Cr buys {r['envelope']['attributed_payers']/1e3:.1f}k attributed payers at INR {r['envelope']['attributed_blended_cac_incl_brand']:.0f} blended attributed CAC including brand and measurement, which meets INR 200 incremental CAC only at {r['envelope']['incrementality_needed_for_200']:.0%} incrementality or better. Each acquired payer contributes INR {r['unit_economics']['contribution_per_acquired_payer_24m']:.2f} over 24 months, so no channel repays its CAC on pass purchases alone; owned is closest. Without upgrades the campaign loses INR {-r['without_upgrades']['1.0']/1e7:.2f} to {-r['without_upgrades']['0.6']/1e7:.2f} Cr over 24 months. Against a 10% control upgrade rate among 864k eligible pass buyers, 24-month break-even needs a treatment upgrade rate of {r['break_even_treatment']['1.0']:.1%} to {r['break_even_treatment']['0.6']:.1%}, and 15-month payback needs {r['treatment_for_15m_payback']['1.0']:.1%} to {r['treatment_for_15m_payback']['0.6']:.1%}. The reference case (16%, 87.5%) nets INR {ref['net_24m']/1e7:.2f} Cr at 24 months with {ref['payback_months']:.1f}-month payback, so it would not pass Gate 3. Scale therefore waits for Gate 2 evidence. The performance reserve of INR {r['envelope']['performance_reserve']/1e7:.2f} Cr is released only on measured marginal incremental CAC at or below INR 200.")'''),
])

notebook('10_campaign_ready_windows','10 | Campaign-ready windows: the 2026 ATP calendar scored for India','Every 2026 ATP tour event in FanCode’s package, split into three viewing windows (day session, night session, final) and scored for an Indian audience. A window is **campaign-ready** only if its start sits inside every one of the three viewing windows under every start delay from 0 to 120 minutes (12 of 12 tests), the same standard applied to the verified finals in notebook 01. Each window carries its clash check, player-story trigger, offer and timing confidence. The logic lives in `models/campaign_windows.py`. Player draws are not scored: they are unknown until the week of the event.',[
('code', '''sys.path.insert(0, str(ROOT/'models'))
import campaign_windows as cw
windows, events = cw.build()
summary = cw.summarise(windows, events)
display(table(windows,'10_campaign_ready_windows'))
(ROOT/'outputs/reports/10_campaign_windows_summary.json').write_text(json.dumps({'settings':cw.SETTINGS,'summary':summary},indent=1,default=str)+'\\n')
settings=pd.DataFrame([dict(setting=k,value=json.dumps(v) if not isinstance(v,str) else v) for k,v in cw.SETTINGS.items()]);display(table(settings,'10_window_scoring_settings'))'''),
('md','## 1. How the season divides'),
('code', '''counts=windows.groupby(['session','status']).size().unstack(fill_value=0);display(counts)
st=windows.status.value_counts().rename_axis('status').reset_index(name='windows');display(table(st,'10_window_status_counts'))
print(f"{summary['campaign_ready_live']} of {summary['windows']} windows across {summary['events']} events are campaign-ready; {summary['upcoming_live_windows']} are still ahead after 18 September 2026.")'''),
('code', '''colors={'Campaign-ready: sell live':COLORS[1],'Early evening: live with start reminder':COLORS[0],'Late: remind + replay':COLORS[2],'Overnight: replay only':COLORS[3],'Daytime: highlights':COLORS[5]}
size={'Finals':140,'Masters 1000':110,'500':70,'250':40}
fig_,ax=plt.subplots(figsize=(12,4.8))
w=windows.copy();w['d']=pd.to_datetime(w.window_date);w['h']=[int(x[:2])+int(x[3:])/60 for x in w.ist_start]
for s_,g in w.groupby('status'):ax.scatter(g.d,g.h,s=[size[t] for t in g.tier],color=colors[s_],alpha=.8,label=s_,edgecolor='white',linewidth=.5)
ax.axhspan(18,23,color=COLORS[1],alpha=.08);ax.set_ylim(0,24);ax.set_yticks(range(0,25,3));ax.set_ylabel('Start, IST hour');ax.legend(fontsize=8,loc='upper center',bbox_to_anchor=(.5,-.08),ncol=5,frameon=False)
ax.axvline(pd.Timestamp('2026-09-18'),color='black',ls=':');ax.text(pd.Timestamp('2026-09-20'),1,'today',fontsize=8)
ax.set_title('The Europe and Gulf swing lands in Indian prime time; the Americas and Asia do not')
fig('10_campaign_windows_calendar','Marker size = tier. Shaded band = 18:00-23:00 IST. Session times are modelled local conventions except the 12 finals verified from official orders of play.')'''),
('md','## 2. The list: campaign-ready windows, ranked\nWindows are ranked by status first, then by score. Score out of 100 = 40% timing robustness + 30% tier + 15% player-story continuity (post-Slam follow-through, race to Turin, season finale) + 15% clash-free. Weights are settings, not estimates. A clash does not disqualify a window: it changes who receives the send.'),
('code', '''ready=windows[windows.status=='Campaign-ready: sell live'][['rank','event','tier','session','window_date','ist_start','clash_check','continuity_trigger','offer','timing_confidence','upcoming','score']]
display(table(ready,'10_campaign_ready_list'))
ahead=ready[ready.upcoming];display(table(ahead,'10_campaign_ready_upcoming'))'''),
('md','## 3. Checks'),
('code', '''checks={'fifty_five_dated_events':summary['events']==55,
 'three_windows_per_event':len(windows)==3*summary['events'],
 'status_counts_reconcile':sum(v for k,v in summary.items() if k in ['campaign_ready_live','early_evening_live','late_remind_replay','daytime_highlights','overnight_replay'])==len(windows),
 'verified_finals_used':summary['high_confidence_windows']==12,
 'rotterdam_final_2000_ist':windows[(windows.event=='Rotterdam')&(windows.session=='Final')].ist_start.iloc[0]=='20:00',
 'indian_wells_final_overnight':windows[(windows.event=='Indian Wells')&(windows.session=='Final')].status.iloc[0]=='Overnight: replay only',
 'six_verified_finals_robust':int(((windows.session=='Final')&windows.timing_confidence.str.startswith('High')&(windows.status=='Campaign-ready: sell live')).sum())==6,
 'unique_ranks':windows['rank'].is_unique}
check('10_campaign_windows',checks)
top=', '.join(f"{r.event} {r.session.lower()} {r.window_date} {r.ist_start} IST" for r in ahead.head(8).itertuples())
report('10_campaign_windows_findings',f"Of {summary['windows']} windows across {summary['events']} 2026 ATP events in FanCode's package, {summary['campaign_ready_live']} are campaign-ready: their start holds inside Indian prime time under every timing test. {summary['early_evening_live']} more start in the early evening and can be sold live with a start reminder; {summary['late_remind_replay']} are late and get reminders plus the INR 39 replay; {summary['overnight_replay']} are overnight and {summary['daytime_highlights']} daytime. {summary['upcoming_live_windows']} campaign-ready windows are still ahead this season: {top}. Timing confidence is high only for the 12 finals verified from official orders of play; the rest use modelled local session times and must be confirmed from each week's order of play before a send. Football clashes after 8 September 2026 are not yet checked because 2026-27 fixtures were not captured.")'''),
])
