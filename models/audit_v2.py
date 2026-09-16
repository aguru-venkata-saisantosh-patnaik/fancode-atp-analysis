"""Audit and rebuild of the year-one claims.
Fixes: (1) no subtraction across different population bases, (2) survey shares used as
relative weights anchored on FanCode's own reported F1 number, (3) repeat purchase read as
"ever repurchases" rather than a per-event hazard, (4) pilot sized on the lift that pays and
on evidence strong enough to release money, (5) purchase CAC and incremental CAC kept apart."""
import json, math

out={}
# ---------- 1. POPULATIONS. Anchored on FanCode's own reported number, not on 240M registered.
F1_ENGAGED=21e6                      # reported company claim, "21M+ engaged F1 fans"  [O]
TENNIS_RATE={'low':.25,'base':.37,'high':.45}   # share who follow tennis, IBM survey 37% [O], widened [A]
FOOT_MULT={'low':1.0,'base':1.8,'high':2.7}     # football engaged vs F1 engaged. 2.7 = survey 60/22 ceiling
MOTO_MULT=1.478431/7.223529                     # MotoGP vs F1 from 2026 India search ratio [D]
pools={}
for k in ['low','base','high']:
    t=TENNIS_RATE[k]
    pools[k]={'f1':F1_ENGAGED*t,'football':F1_ENGAGED*FOOT_MULT[k]*t,'motogp':F1_ENGAGED*MOTO_MULT*t}
out['pools_m']={k:{s:round(v/1e6,1) for s,v in d.items()} for k,d in pools.items()}

# ---------- 2. REPEAT PURCHASE. Brief: match-pass buyers return at 60-65%. Read as "ever repurchase".
PASS_C=43.32332881355933; SEASON_C=298.719193220339
rep={'low':1+.60,'base':1+.625,'high':1+.65+.65*.5}   # high adds a partial third purchase [A]
out['purchases_per_buyer']={k:round(v,2) for k,v in rep.items()}
out['contribution_per_new_buyer']={k:round(v*PASS_C,1) for k,v in rep.items()}

# ---------- 3. CAPACITY CHECK. Budget is the decision. Pools only test whether it is reachable.
BUDGET_ACQ=2.736e7; BRAND=0.304e7; TOTAL=BUDGET_ACQ+BRAND
mix={'owned':.302,'performance':.336,'native':.140,'contests':.083,'publisher':.039}
cac_purchase={'owned':99.3,'performance':333.3,'native':150.0,'contests':159.0,'publisher':180.0}
payers={c:TOTAL*s/cac_purchase[c] for c,s in mix.items()}
tot_payers=sum(payers.values())
out['payers_by_channel']={c:round(v) for c,v in payers.items()}
out['total_payers']=round(tot_payers)
out['blended_purchase_cac']=round(TOTAL/tot_payers,1)
# capacity: can the pools supply these payers at 5-15% reach?
for k in ['low','base','high']:
    need=tot_payers; pool=sum(pools[k].values())
    out.setdefault('capacity_need_share_of_pool',{})[k]=round(need/pool*100,2)

# ---------- 4. UPGRADES. Expressed against a stated core-fan scenario, not an implied headcount.
CORE={'low':10e6,'base':21.6e6,'high':30e6}    # 21.6M = brief's illustrative 24M week x 90% [C, illustrative]
UPG_REACH=.20; UPG_RATE=.02
credit_net=44.5/1.18
upg={k:CORE[k]*UPG_REACH*UPG_RATE for k in CORE}
out['upgrades']={k:round(v) for k,v in upg.items()}

# ---------- 5. YEAR ONE P&L AND PAYBACK, three scenarios, seasonality-aware payback.
RET_COST={k:CORE[k]*UPG_REACH*0.8631*0.5*1.15 for k in CORE}
res={}
for k in ['low','base','high']:
    new_c=tot_payers*rep[k]*PASS_C
    up_c=upg[k]*(SEASON_C-rep[k]*PASS_C-credit_net)
    spend=TOTAL+RET_COST[k]
    y1=new_c+up_c-spend
    ret_rate={'low':.30,'base':.40,'high':.50}[k]; ren={'low':.75,'base':.85,'high':.90}[k]
    y2=tot_payers*ret_rate*rep[k]*PASS_C + upg[k]*ren*(SEASON_C-rep[k]*PASS_C)
    # payback: year-two contribution earned over the 8 busiest months, not spread evenly
    monthly=y2/8
    pb=12+max(0.,spend-(new_c+up_c))/monthly if y2>0 else None
    res[k]={'new_contrib_cr':round(new_c/1e7,2),'upgrade_contrib_cr':round(up_c/1e7,2),
            'spend_cr':round(spend/1e7,2),'y1_net_cr':round(y1/1e7,2),
            'y2_contrib_cr':round(y2/1e7,2),'payback_months':round(pb,1) if pb else None,
            'net_24m_cr':round((y1+y2)/1e7,2)}
out['pnl']=res

# ---------- 6. PILOT. Break-even lift, sizing lift, and the lift needed to release money.
MSG=0.8631; OPS=1.15; CEIL=200.
be_lift=MSG*OPS/CEIL                      # lift at which incremental CAC equals the ceiling
out['break_even_lift_pp']=round(be_lift*100,3)
def n_per_arm(p0,d,z_a=1.959964,z_b=0.8416212):
    p1=p0+d; return math.ceil((z_a+z_b)**2*(p0*(1-p0)+p1*(1-p1))/d**2)
p0=.01
out['sizing']={}
for d in [0.002,0.005,0.008]:
    n=n_per_arm(p0,d)
    out['sizing'][f'lift_{d*100:.1f}pp']={'per_arm':n,'total':2*n,'messaged_cost_inr':round(n*MSG),
        'implied_icac_inr':round(MSG*OPS/d)}
# evidence to release money: 95% lower bound on lift must clear break-even, with 80% power
def n_for_release(p0,d_true,d_be):
    se=(d_true-d_be)/(1.959964+0.8416212); p1=p0+d_true
    return math.ceil((p0*(1-p0)+p1*(1-p1))/se**2)
for d_true in [0.008,0.01]:
    n=n_for_release(p0,d_true,be_lift)
    out.setdefault('release_grade',{})[f'true_lift_{d_true*100:.1f}pp']={'per_arm':n,'total':2*n,
        'messaged_cost_inr':round(n*MSG),'point_icac_inr':round(MSG*OPS/d_true)}

# ---------- 7. INCREMENTAL BASIS for the whole budget, stated apart from purchase CAC.
for share in [.6,.875]:
    out.setdefault('blended_icac',{})[f'{int(share*100)}pct_incremental']=round(TOTAL/tot_payers/share,0)
json.dump(out,open('presentation/html_draft/analysis_additions/audit_v2.json','w'),indent=1)
print(json.dumps(out,indent=1))
