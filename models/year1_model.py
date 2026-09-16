"""Year-one plan model tying persona targets (slide 02) to channel budget (07) and P&L (05).
Inputs reuse notebook tables and case inputs. New assumptions are marked A in the deck."""
import json, pandas as pd
from zoneinfo import ZoneInfo
from datetime import datetime
R = "data/processed/"; out = {}
# ---- persona payers (same as slide 02)
reg=240e6; ibm={'football':.60,'f1':.22,'tennis':.37}; motogp=.22*(1.478431/7.223529)
pools={'football':reg*.60*.37,'f1':reg*.22*.37,'motogp':reg*motogp*.37,'slam':reg*.37-24e6*1.5}
params={'football':(.10,.015),'f1':(.15,.02),'slam':(.05,.01),'motogp':(.15,.015)}
payers={k:pools[k]*r*c for k,(r,c) in params.items()}
# ---- per-channel year-one purchase CAC at scale
cac={
 'owned': 0.8631/0.01*1.15,            # WhatsApp rate / 1pp owned lift + 15% ops (A)
 'native': 150.0,                        # native hosts zero rights cost, production only (A)
 'performance': 10/0.03,                 # CPC 10 working, 3% CVR only with D-2 timing and warm retargeting (A)
 'contests': (12000+5000*10)/(5000*0.078),# partner and prizes 12k + 5,000 clicks at CPC 10, 7.8% case CVR
 'publisher': 180.0,                     # procurement gate, fee <= 180 x expected payers
}
mix={'football':{'owned':.60,'native':.15,'performance':.15,'contests':.10},
     'f1':{'owned':.65,'native':.25,'performance':.10},
     'motogp':{'owned':.70,'native':.20,'performance':.10},
     'slam':{'performance':.45,'contests':.30,'publisher':.25}}
ch_pay={c:0 for c in cac}; flows=[]
for p,m in mix.items():
    for c,s in m.items():
        ch_pay[c]+=payers[p]*s; flows.append({'persona':p,'channel':c,'payers':round(payers[p]*s)})
ch_cost={c:ch_pay[c]*cac[c] for c in cac}
acq=sum(ch_cost.values()); total=acq/0.90; brand_meas=total-acq
out['channels']={c:{'cac':round(cac[c],1),'payers':round(ch_pay[c]),'cost_cr':round(ch_cost[c]/1e7,3),'share':round(ch_cost[c]/total,3)} for c in cac}
out['channels']['brand_measurement']={'cost_cr':round(brand_meas/1e7,3),'share':0.10}
out['budget']={'acquisition_cr':round(acq/1e7,3),'total_cr':round(total/1e7,3),'payers':round(sum(payers.values())),
  'blended_media_cac':round(acq/sum(payers.values()),1),'blended_loaded_cac':round(total/sum(payers.values()),1),
  'icac_at_60pct':round(total/sum(payers.values())/0.6,1),'icac_at_875pct':round(total/sum(payers.values())/0.875,1)}
out['flows']=flows
# ---- year-one P&L and cohort payback
pass_c=43.32332881355933; season_c=298.719193220339; exp=1+.6+.36
new_contrib=sum(payers.values())*exp*pass_c
credit_net=44.5/1.18; upg=21.6e6*.2*.02
upg_contrib=upg*(season_c-exp*pass_c-credit_net)
retention_cost=21.6e6*.2*0.8631*0.5*1.15   # half of reached core messaged on WhatsApp, rest push (A)
y1=new_contrib+upg_contrib-total-retention_cost
y2=sum(payers.values())*0.40*exp*pass_c + upg*0.90*(season_c-exp*pass_c)
spend=total+retention_cost; payback_m=12+max(0,spend-(new_contrib+upg_contrib))/(y2/12)
out['pnl']={'new_gross_cr':round(sum(payers.values())*89*exp/1e7,3),'new_contrib_cr':round(new_contrib/1e7,3),'upgrades':round(upg),
 'upg_gross_cr':round(upg*399/1e7,3),'upg_contrib_cr':round(upg_contrib/1e7,3),'acq_cr':round(total/1e7,3),'retention_cr':round(retention_cost/1e7,3),
 'y1_net_cr':round(y1/1e7,3),'y2_retained_contrib_cr':round(y2/1e7,3),'cum24_net_cr':round((y1+y2)/1e7,3),'payback_months':round(payback_m,1),
 'per_upgrade_contrib':round(season_c-exp*pass_c-credit_net,2)}
# ---- retention: expected passes
def e(p,n): return sum(p**k for k in range(n))
out['passes']={f'{p}_{n}':round(e(p,n),2) for p,n in [(.6,3),(.65,3),(.65,5),(.7,5)]}
out['passes_contrib']={k:round(v*pass_c,1) for k,v in out['passes'].items()}
# ---- remaining season price today and price per event
rip=pd.read_csv('outputs/tables/03_remaining_inventory_price.csv'); rip['date']=pd.to_datetime(rip['date'])
row=rip[rip.date<=pd.Timestamp('2026-09-16')].iloc[-1]; out['remaining_price']={'date':str(row.date.date()),'events':int(row.remaining_event_starts),'price':int(row.candidate_rounded_price)}
out['per_event']={'fancode_season_jan':round(399/54,1),'fancode_remaining_now':round(row.candidate_rounded_price/row.remaining_event_starts,1),'tennistv_annual':round(4499/55,1),'tournament_89':89}
# ---- calendar: Slam spillover and time-zone buckets
ev=pd.read_csv(R+'atp_event_starts.csv'); ev['start']=pd.to_datetime(ev['start_date'],errors='coerce'); ev=ev.dropna(subset=['start'])
regd=ev[ev.tier.isin(['ATP 250','ATP 500','ATP MASTERS 1000','ATP FINALS'])].copy()
slam_finals={'Australian Open':'2026-02-01','Roland Garros':'2026-06-07','Wimbledon':'2026-07-12','US Open':'2026-09-13'}
spill=[]
for s,d in slam_finals.items():
    d=pd.Timestamp(d); w=regd[(regd.start>d)&(regd.start<=d+pd.Timedelta(days=10))]
    spill.append({'slam':s,'final':str(d.date()),'next':[f"{c.title()} ({t.replace('ATP ','').replace('MASTERS 1000','Masters')})" for c,t in zip(w.city,w.tier)]})
out['spillover']=spill
tz={'BRISBANE':'Australia/Brisbane','HONG KONG':'Asia/Hong_Kong','ADELAIDE':'Australia/Adelaide','AUCKLAND':'Pacific/Auckland','MONTPELLIER':'Europe/Paris','DALLAS':'America/Chicago',
 'ROTTERDAM':'Europe/Amsterdam','BUENOS AIRES':'America/Argentina/Buenos_Aires','DELRAY':'America/New_York','DOHA':'Asia/Qatar','RIO':'America/Sao_Paulo','MARSEILLE':'Europe/Paris',
 'ACAPULCO':'America/Mexico_City','DUBAI':'Asia/Dubai','SANTIAGO':'America/Santiago','INDIAN WELLS':'America/Los_Angeles','MIAMI':'America/New_York','MARRAKECH':'Africa/Casablanca',
 'HOUSTON':'America/Chicago','BUCHAREST':'Europe/Bucharest','MONTE':'Europe/Monaco','BARCELONA':'Europe/Madrid','MUNICH':'Europe/Berlin','MADRID':'Europe/Madrid','ROME':'Europe/Rome',
 'GENEVA':'Europe/Zurich','HAMBURG':'Europe/Berlin','STUTTGART':'Europe/Berlin','HERTOGENBOSCH':'Europe/Amsterdam','HALLE':'Europe/Berlin','LONDON':'Europe/London','MALLORCA':'Europe/Madrid',
 'EASTBOURNE':'Europe/London','BASTAD':'Europe/Stockholm','GSTAAD':'Europe/Zurich','UMAG':'Europe/Zagreb','KITZBUHEL':'Europe/Vienna','LOS CABOS':'America/Mazatlan','WASHINGTON':'America/New_York',
 'TORONTO':'America/Toronto','MONTREAL':'America/Toronto','CINCINNATI':'America/New_York','WINSTON':'America/New_York','CHENGDU':'Asia/Shanghai','HANGZHOU':'Asia/Shanghai','BEIJING':'Asia/Shanghai',
 'TOKYO':'Asia/Tokyo','SHANGHAI':'Asia/Shanghai','ALMATY':'Asia/Almaty','STOCKHOLM':'Europe/Stockholm','ANTWERP':'Europe/Brussels','BRUSSELS':'Europe/Brussels','LYON':'Europe/Paris','VIENNA':'Europe/Vienna',
 'BASEL':'Europe/Zurich','PARIS':'Europe/Paris','METZ':'Europe/Paris','ATHENS':'Europe/Athens','TURIN':'Europe/Rome','BELGRADE':'Europe/Belgrade','LAS VEGAS':'America/Los_Angeles','CHARLESTON':'America/New_York'}
ist=ZoneInfo('Asia/Kolkata'); rows=[]; unm=[]
for _,r in regd.iterrows():
    z=next((v for k,v in tz.items() if k in str(r.city).upper().replace("'",'').replace('Ü','U')),None)
    if not z: unm.append(r.city); continue
    loc=datetime(r.start.year,r.start.month,r.start.day,15,0,tzinfo=ZoneInfo(z)); i=loc.astimezone(ist)
    off=(i.utcoffset()-loc.utcoffset()).total_seconds()/3600
    b='Europe and Middle East' if z.startswith(('Europe','Asia/Dubai','Asia/Qatar','Africa')) else ('Asia and Oceania' if z.startswith(('Asia','Australia','Pacific')) else 'Americas')
    rows.append({'city':r.city,'tier':r.tier,'bucket':b,'ist_of_15_local':i.strftime('%H:%M'),'offset':off})
df=pd.DataFrame(rows); out['unmapped']=unm
out['tz_buckets']=df.groupby('bucket').agg(events=('city','count'),masters=('tier',lambda s:(s=='ATP MASTERS 1000').sum())).reset_index().to_dict('records')
out['ist_15_by_bucket']=df.groupby('bucket')['ist_of_15_local'].agg(lambda s: sorted(set(s))).to_dict()
# ---- portfolio occasions for passport
f1=pd.read_csv(R+'f1_races.csv'); f1=f1[pd.to_datetime(f1.start_ist.str[:19])>=pd.Timestamp('2026-09-16')]
out['f1_next']=[{'event':e_,'ist':s[:16]} for e_,s in zip(f1.event,f1.start_ist)]
out['owned_test_cost']=round(85214*0.8631)
json.dump(out,open('presentation/html_draft/analysis_additions/year1_model.json','w'),indent=1)
print(json.dumps(out,indent=1))
