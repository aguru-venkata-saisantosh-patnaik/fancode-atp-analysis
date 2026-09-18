"""ATP on FanCode: the single economics model behind every figure in the deck.

Two mutually exclusive cohorts, each measured against its own holdout:
  1. Acquisition: new ATP pass buyers, bought through owned, native, contest,
     publisher and paid channels. Counted on an incremental basis.
  2. Upgrade: EXISTING ATP pass buyers in the reached core audience, moved to a
     season pass. Only upgrades above the control rate are credited, and the
     upgrade credit is charged to every treated upgrader, including those who
     would have upgraded anyway (leakage).

All inputs live in models/model_inputs.json with a C/O/D/A evidence tag.
Run:  python models/atp_economics.py   (writes models/atp_economics.json)
"""
from pathlib import Path
import json, math

HERE = Path(__file__).resolve().parent
INPUTS = json.loads((HERE / 'model_inputs.json').read_text())


def v(section, key):
    return INPUTS[section][key]['value']


# ---------------------------------------------------------------- unit economics
def contribution(price):
    """What FanCode keeps from one purchase, before marketing. Rights excluded."""
    gst, fee, fee_tax = v('unit_economics', 'gst_rate'), v('unit_economics', 'gateway_fee'), v('unit_economics', 'gateway_fee_tax')
    return price / (1 + gst) - price * fee * (1 + fee_tax) - v('unit_economics', 'variable_cost_per_purchase')


PASS_PRICE, SEASON_PRICE = v('unit_economics', 'tournament_pass_price'), v('unit_economics', 'season_pass_price')
PASS_C, SEASON_C = contribution(PASS_PRICE), contribution(SEASON_PRICE)
CREDIT = v('unit_economics', 'upgrade_credit')
CREDIT_COST = SEASON_C - contribution(SEASON_PRICE - CREDIT)  # contribution given up per credited upgrade

REPEAT = v('acquired_payers', 'purchases_per_buyer')
Y2_RETURN = v('acquired_payers', 'year2_return_rate')
PER_BUYER_24M = REPEAT * PASS_C * (1 + Y2_RETURN)  # contribution of one incremental acquired payer over 24 months

# ---------------------------------------------------------------- channels
b = INPUTS['acquisition_budget_inr']
cb = INPUTS['channel_cac_build']
OWNED_CAC = v('channel_cac_build', 'whatsapp_rate_inr') / v('channel_cac_build', 'owned_conversion') * (1 + v('channel_cac_build', 'owned_operations_uplift'))
PAID_CAC = v('channel_cac_build', 'paid_cpc_inr') / v('channel_cac_build', 'paid_click_conversion')
CONTEST_CAC = (v('channel_cac_build', 'contest_clicks') * v('channel_cac_build', 'contest_cpc_inr') + v('channel_cac_build', 'contest_fees_and_prizes_inr')) / (v('channel_cac_build', 'contest_clicks') * v('channel_cac_build', 'contest_conversion'))

CHANNELS = [  # key, label, budget, attributed CAC, how the CAC is built, evidence status
    ('owned_lifecycle', 'Owned lifecycle', b['owned_lifecycle']['value'], OWNED_CAC,
     'INR 0.8631 per WhatsApp message (O) / 1% conversion (A) x 1.15 operations (A)', 'Calculated'),
    ('native_personalities', 'Native personalities', b['native_personalities']['value'], v('channel_cac_build', 'native_cac_test_ceiling'),
     'No public cost basis. Zero incremental rights cost (C). Ceiling: attributed CAC <= INR 150, holdout incremental CAC <= INR 200', 'Test ceiling'),
    ('contests', 'Contests', b['contests']['value'], CONTEST_CAC,
     '(5,000 clicks x INR 10 CPC (O) + INR 12,000 fees and prizes (A)) / (5,000 x 7.8% conversion (C))', 'Calculated'),
    ('publisher_takeovers', 'Publisher takeovers', b['publisher_takeovers']['value'], v('channel_cac_build', 'publisher_cac_test_ceiling'),
     'No ESPN.in quote. Ceiling: fee <= INR 180 x expected payers; clears INR 200 incremental only at 90%+ incrementality', 'Test ceiling'),
    ('paid_media_test', 'Paid media (capped test)', b['paid_media_test']['value'], PAID_CAC,
     'INR 10 CPC (O) / 3% click-to-purchase (A)', 'Calculated'),
]
BRAND = b['brand_and_measurement']['value']
ENVELOPE = b['envelope_total']['value']
COMMITTED_ACQ = sum(c[2] for c in CHANNELS)
RESERVE = ENVELOPE - COMMITTED_ACQ - BRAND
PAYERS = {c[0]: c[2] / c[3] for c in CHANNELS}
TOTAL_PAYERS = sum(PAYERS.values())
ATTRIBUTED_BLENDED_CAC = (COMMITTED_ACQ + BRAND) / TOTAL_PAYERS
ICAC_CEILING = v('cac_target', 'incremental_cac_ceiling')
INCREMENTALITY_NEEDED = ATTRIBUTED_BLENDED_CAC / ICAC_CEILING

# ---------------------------------------------------------------- audience and personas
AUD = INPUTS['audience']
F1 = AUD['fancode_f1_engaged']['value']
POOLS = {}
for i, case in enumerate(['low', 'base', 'high']):
    t = AUD['tennis_follow_rate']['value'][i]
    POOLS[case] = {'f1': F1 * t, 'football': F1 * AUD['football_to_f1_multiplier']['value'][i] * t,
                   'motogp': F1 * AUD['motogp_to_f1_ratio']['value'] * t}
BASE_POOL_TOTAL = sum(POOLS['base'].values())
IN_APP = ['owned_lifecycle', 'native_personalities']          # reach portfolio fans already on FanCode
EXTERNAL = ['contests', 'publisher_takeovers', 'paid_media_test']  # reach tennis intent outside the app
PERSONA_PAYERS = {'Grid Strategist (F1)': 0.0, 'Matchday Loyalist (football)': 0.0, 'Throttle Rider (MotoGP)': 0.0, 'Slam Tourist (external)': 0.0}
for key in IN_APP:  # in-app payers split in proportion to the base sport pools (D)
    PERSONA_PAYERS['Grid Strategist (F1)'] += PAYERS[key] * POOLS['base']['f1'] / BASE_POOL_TOTAL
    PERSONA_PAYERS['Matchday Loyalist (football)'] += PAYERS[key] * POOLS['base']['football'] / BASE_POOL_TOTAL
    PERSONA_PAYERS['Throttle Rider (MotoGP)'] += PAYERS[key] * POOLS['base']['motogp'] / BASE_POOL_TOTAL
for key in EXTERNAL:
    PERSONA_PAYERS['Slam Tourist (external)'] += PAYERS[key]

CORE = AUD['ordinary_week_viewers']['value'] * AUD['core_share_of_ordinary_week']['value']
U = INPUTS['upgrade_cohort']
REACHED = CORE * U['core_reached_share']['value']
CONTROL = U['control_upgrade_rate']['value']
RENEWAL = U['season_renewal_new_upgrader']['value']
RETENTION_COST = REACHED * v('channel_cac_build', 'whatsapp_rate_inr') * U['retention_messaging_share_whatsapp']['value'] * (1 + v('channel_cac_build', 'owned_operations_uplift'))
UPGRADE_VALUE_Y1 = SEASON_C - REPEAT * PASS_C  # season contribution minus the passes they would have bought anyway
UPGRADE_VALUE_Y2 = RENEWAL * UPGRADE_VALUE_Y1
Y2_MONTHS = v('payback', 'year2_earning_months')


def eligible(pass_buyer_share=None):
    return REACHED * (U['active_pass_buyer_share']['value'] if pass_buyer_share is None else pass_buyer_share)


# ---------------------------------------------------------------- P&L
def pnl(treatment, incrementality, pass_buyer_share=None, renewal=None, reserve_deployed=False, upgrades_on=True):
    """24-month campaign P&L in INR. Rights fee excluded: this is an incremental campaign P&L."""
    ren = RENEWAL if renewal is None else renewal
    elig = eligible(pass_buyer_share)
    inc_payers = TOTAL_PAYERS * incrementality
    acq_y1 = inc_payers * REPEAT * PASS_C
    acq_y2 = inc_payers * Y2_RETURN * REPEAT * PASS_C
    spend = COMMITTED_ACQ + BRAND + RETENTION_COST
    if reserve_deployed:  # reserve spent at exactly the INR 200 incremental CAC ceiling
        extra = RESERVE / ICAC_CEILING
        acq_y1 += extra * REPEAT * PASS_C
        acq_y2 += extra * Y2_RETURN * REPEAT * PASS_C
        spend += RESERVE
    if upgrades_on:
        inc_upgrades = max(0.0, treatment - CONTROL) * elig
        credit_cost = treatment * elig * CREDIT_COST  # every treated upgrader receives the credit
        upg_y1 = inc_upgrades * UPGRADE_VALUE_Y1 - credit_cost
        upg_y2 = inc_upgrades * ren * UPGRADE_VALUE_Y1
    else:
        inc_upgrades = credit_cost = upg_y1 = upg_y2 = 0.0
    y1 = acq_y1 + upg_y1 - spend
    y2 = acq_y2 + upg_y2
    net24 = y1 + y2
    if net24 < 0 or y2 <= 0:
        payback = None  # does not repay inside 24 months
    else:
        payback = 12 + max(0.0, spend - (acq_y1 + upg_y1)) / (y2 / Y2_MONTHS)
    return dict(treatment_rate=treatment, incrementality=incrementality, eligible_pass_buyers=elig,
                incremental_upgrades=inc_upgrades, credit_cost=credit_cost, acquisition_y1=acq_y1,
                upgrade_y1=upg_y1, spend=spend, y1_net=y1, acquisition_y2=acq_y2, upgrade_y2=upg_y2,
                y2=y2, net_24m=net24, payback_months=payback)


def break_even_treatment(incrementality, pass_buyer_share=None, renewal=None, reserve_deployed=False):
    """Treatment upgrade rate at which 24-month net = 0 (net is linear in the rate)."""
    lo, hi = pnl(CONTROL, incrementality, pass_buyer_share, renewal, reserve_deployed), pnl(1.0, incrementality, pass_buyer_share, renewal, reserve_deployed)
    slope = (hi['net_24m'] - lo['net_24m']) / (1.0 - CONTROL)
    return CONTROL - lo['net_24m'] / slope


def treatment_for_payback(months, incrementality, pass_buyer_share=None):
    """Lowest treatment upgrade rate at which payback falls to the given number of months (bisection)."""
    lo, hi = CONTROL, 1.0
    for _ in range(100):
        mid = (lo + hi) / 2
        pb = pnl(mid, incrementality, pass_buyer_share)['payback_months']
        if pb is not None and pb <= months:
            hi = mid
        else:
            lo = mid
    return hi


# ---------------------------------------------------------------- experiments
Z_A, Z_B = 1.959963984540054, 0.8416212335729143


def n_lower_bound(p0, p_true, p_threshold):
    """Users per arm so the 95% lower bound of (treatment - control) clears (threshold - control) with 80% power."""
    se = ((p_true - p0) - (p_threshold - p0)) / (Z_A + Z_B)
    return math.ceil((p0 * (1 - p0) + p_true * (1 - p_true)) / se ** 2)


OWNED_MSG_COST = v('channel_cac_build', 'whatsapp_rate_inr') * (1 + v('channel_cac_build', 'owned_operations_uplift'))
OWNED_LIFT_THRESHOLD = OWNED_MSG_COST / ICAC_CEILING  # lift at which owned incremental CAC equals INR 200


def run():
    out = {'_about': 'Generated by models/atp_economics.py from models/model_inputs.json. INR unless stated. Scenario outputs, not observed company results.'}
    out['unit_economics'] = {'pass_contribution': PASS_C, 'season_contribution': SEASON_C, 'credit_cost_per_upgrade': CREDIT_COST,
                             'credit_hurdle_rate_at_10pct_control': CONTROL * SEASON_C / contribution(SEASON_PRICE - CREDIT),
                             'discount_10pct_volume_hurdle': 1 / 0.9 - 1,
                             'purchases_per_buyer': REPEAT, 'contribution_per_buyer_year1': REPEAT * PASS_C,
                             'contribution_per_acquired_payer_24m': PER_BUYER_24M,
                             'passes_to_repay_175': 175 / PASS_C, 'seasons_to_repay_175': 175 / SEASON_C}
    ch = []
    for key, label, budget, cac, build, status in CHANNELS:
        ch.append({'channel': key, 'label': label, 'budget': budget, 'share_of_envelope': budget / ENVELOPE, 'attributed_cac': cac,
                   'cac_basis': status, 'cac_build': build, 'attributed_payers': PAYERS[key],
                   'incremental_cac_at_100': cac, 'incremental_cac_at_87_5': cac / 0.875, 'incremental_cac_at_60': cac / 0.6,
                   'clears_200_at_87_5': cac / 0.875 <= ICAC_CEILING,
                   'net_per_payer_24m_at_100': PER_BUYER_24M - cac, 'net_per_payer_24m_at_87_5': PER_BUYER_24M * 0.875 - cac,
                   'channel_net_24m_at_100': PAYERS[key] * (PER_BUYER_24M - cac)})
    out['channels'] = ch
    out['envelope'] = {'total': ENVELOPE, 'committed_acquisition': COMMITTED_ACQ, 'brand_and_measurement': BRAND, 'performance_reserve': RESERVE,
                       'reserve_share': RESERVE / ENVELOPE, 'attributed_payers': TOTAL_PAYERS,
                       'attributed_blended_cac_incl_brand': ATTRIBUTED_BLENDED_CAC,
                       'attributed_blended_cac_media_only': COMMITTED_ACQ / TOTAL_PAYERS,
                       'incrementality_needed_for_200': INCREMENTALITY_NEEDED,
                       'incremental_cac_at': {str(q): ATTRIBUTED_BLENDED_CAC / q for q in v('acquired_payers', 'incrementality_scenarios')},
                       'owned_half_response_cac': OWNED_CAC * 2, 'owned_half_response_incrementality_needed': OWNED_CAC * 2 / ICAC_CEILING,
                       'owned_sends_funded': b['owned_lifecycle']['value'] / OWNED_MSG_COST,
                       'owned_sends_share_of_base_pools': b['owned_lifecycle']['value'] / OWNED_MSG_COST / BASE_POOL_TOTAL}
    out['personas'] = {'pools_m': {k: {s: x / 1e6 for s, x in d.items()} for k, d in POOLS.items()},
                       'payers': PERSONA_PAYERS, 'payer_share': {k: x / TOTAL_PAYERS for k, x in PERSONA_PAYERS.items()},
                       'capacity_share_of_pools': {k: TOTAL_PAYERS / sum(d.values()) for k, d in POOLS.items()},
                       'rule': 'In-app channels (owned, native) split by base sport-pool size; external channels (contests, publisher, paid) reach the Slam Tourist'}
    out['upgrade_cohort'] = {'core': CORE, 'reached': REACHED, 'eligible_pass_buyers': eligible(), 'control_rate': CONTROL,
                             'control_upgrades': CONTROL * eligible(), 'value_per_incremental_upgrade_y1': UPGRADE_VALUE_Y1,
                             'value_per_incremental_upgrade_y2': UPGRADE_VALUE_Y2, 'retention_messaging_cost': RETENTION_COST}
    qs = v('acquired_payers', 'incrementality_scenarios')
    out['without_upgrades'] = {str(q): pnl(CONTROL, q, upgrades_on=False)['net_24m'] for q in qs}
    out['break_even_treatment'] = {str(q): break_even_treatment(q) for q in qs}
    ceiling = INPUTS['gates_inr']['payback_ceiling_months']['value']
    out['treatment_for_15m_payback'] = {str(q): treatment_for_payback(ceiling, q) for q in qs}
    out['break_even_treatment_by_pass_buyer_share'] = {str(s): {str(q): break_even_treatment(q, pass_buyer_share=s) for q in qs}
                                                       for s in U['active_pass_buyer_share_sensitivity']['value']}
    out['break_even_treatment_by_renewal'] = {str(r): break_even_treatment(v('acquired_payers', 'reference_incrementality'), renewal=r)
                                              for r in U['season_renewal_sensitivity']['value']}
    out['break_even_treatment_reserve_deployed'] = {str(q): break_even_treatment(q, reserve_deployed=True) for q in qs}
    grid = [pnl(t, q) for q in qs for t in U['treatment_upgrade_scenarios']['value']]
    out['pnl_grid'] = grid
    ref_q, ref_t = v('acquired_payers', 'reference_incrementality'), U['reference_treatment_rate']['value']
    out['reference_case'] = pnl(ref_t, ref_q)
    out['scenarios'] = {'low': pnl(0.12, 0.6), 'reference': pnl(ref_t, ref_q), 'high': pnl(0.20, 1.0)}
    out['reference_case_reserve_deployed'] = pnl(ref_t, ref_q, reserve_deployed=True)
    # experiments
    p0, lift = v('experiments', 'owned_pilot_baseline_conversion'), v('experiments', 'owned_pilot_true_lift_pp')
    n1 = n_lower_bound(p0, p0 + lift, p0 + OWNED_LIFT_THRESHOLD)
    out['gate1_owned_pilot'] = {'lift_threshold_pp': OWNED_LIFT_THRESHOLD * 100, 'true_lift_pp': lift * 100, 'per_arm': n1, 'total_users': 2 * n1,
                                'treatment_messages_cost': n1 * v('channel_cac_build', 'whatsapp_rate_inr'),
                                'treatment_cost_with_operations': n1 * OWNED_MSG_COST, 'implied_incremental_cac_at_true_lift': OWNED_MSG_COST / lift}
    g2 = []
    for q in qs:
        thresholds = {'24m_break_even': break_even_treatment(q), '15m_payback': treatment_for_payback(ceiling, q)}
        for rule, threshold in thresholds.items():
            for pt in v('experiments', 'upgrade_true_rates'):
                if pt <= threshold:
                    g2.append({'incrementality': q, 'threshold_rule': rule, 'threshold_rate': threshold, 'true_rate': pt,
                               'per_arm': None, 'total_users': None, 'message_cost': None, 'credit_face_value_paid': None,
                               'note': 'Not provable: true rate is at or below the threshold'})
                    continue
                n = n_lower_bound(CONTROL, pt, threshold)
                g2.append({'incrementality': q, 'threshold_rule': rule, 'threshold_rate': threshold, 'true_rate': pt, 'per_arm': n,
                           'total_users': 2 * n, 'message_cost': n * OWNED_MSG_COST, 'credit_face_value_paid': n * pt * CREDIT, 'note': ''})
    out['gate2_upgrade_test'] = g2
    out['gates'] = {k: INPUTS['gates_inr'][k]['value'] for k in ['gate1', 'gate2', 'gate3']}
    budgets = {c[0]: c[2] for c in CHANNELS}
    budgets['brand_and_measurement'] = BRAND
    budgets['performance_reserve'] = RESERVE
    g1_owned = out['gate1_owned_pilot']['treatment_cost_with_operations']
    g1 = {k: 0.0 for k in budgets}
    g1['owned_lifecycle'] = g1_owned
    g1['brand_and_measurement'] = out['gates']['gate1'] - g1_owned  # access, ledger and pass-buyer count
    g2 = {k: float(INPUTS['gates_inr']['gate2_split']['value'].get(k, 0)) for k in budgets}
    g3 = {k: budgets[k] - g1[k] - g2[k] for k in budgets}
    out['gate_allocation'] = [{'line': k, 'gate1': g1[k], 'gate2': g2[k], 'gate3': g3[k], 'total': budgets[k], 'share_of_envelope': budgets[k] / ENVELOPE} for k in budgets]
    assert abs(sum(g1.values()) - out['gates']['gate1']) < 1e-6 and abs(sum(g2.values()) - out['gates']['gate2']) < 1e-6
    assert abs(sum(g3.values()) - out['gates']['gate3']) < 1e-6 and min(g3.values()) >= 0
    return out


if __name__ == '__main__':
    result = run()
    (HERE / 'atp_economics.json').write_text(json.dumps(result, indent=1, default=float) + '\n')
    print(json.dumps({k: result[k] for k in ['envelope', 'without_upgrades', 'break_even_treatment', 'reference_case']}, indent=1, default=float))
