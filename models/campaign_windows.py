"""Campaign-ready windows: every 2026 ATP tour event FanCode holds, scored as an India viewing window.

A window is one event x one session type (day session, night session, final). Each window is
scored on: IST timing robustness, tournament tier, clash risk with F1 and football, player-story
continuity, the offer to sell, and the confidence of the timing evidence.

Reads only committed files in data/processed and analysis_config. Player draws are not scored:
they are unknown until the week of the event.
Run:  python models/campaign_windows.py   (writes outputs/tables/10_campaign_ready_windows.csv and outputs/reports/10_campaign_windows_summary.json)
"""
from pathlib import Path
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import json
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
P = ROOT / 'data/processed'
CFG = json.loads((ROOT / 'analysis_config/analysis.json').read_text())
IST = ZoneInfo('Asia/Kolkata')
ANALYSIS_DATE = pd.Timestamp('2026-09-18')

SETTINGS = {
    '_about': 'Scoring settings. Weights are choices, not estimates (A). Session start times are modelled local conventions (A) unless an official order of play is available (O).',
    'session_local_start': {'Day session': '14:00', 'Night session': '19:00', 'Final': '15:00'},
    'viewing_windows_ist': CFG['viewing_windows'],
    'delays_minutes': CFG['scheduled_delay_minutes'],
    'weights': {'timing': 0.40, 'tier': 0.30, 'continuity': 0.15, 'clash_free': 0.15},
    'tier_value': {'ATP FINALS': 1.0, 'ATP MASTERS 1000': 1.0, 'ATP 500': 0.6, 'ATP 250': 0.3},
    'list_price': {'ATP FINALS': 99, 'ATP MASTERS 1000': 99, 'ATP 500': 89, 'ATP 250': 79},
    'replay_price': 39,
    'post_slam_days': 10,
    'race_to_turin_days': 42,
    'clash_window_hours': {'before': 2, 'after': 2.5, '_note': 'A rival event overlaps if it starts up to 2h before the tennis (typical F1 race or football match length) or within 2.5h after it (median ATP duration scenario, 150 min)'},
}

# Slam finals are on rival platforms. They matter only as a follow-through trigger.
SLAM_FINALS = {'Australian Open': '2026-02-01', 'Roland Garros': '2026-06-07', 'Wimbledon': '2026-07-12', 'US Open': '2026-09-13'}
TURIN_START = pd.Timestamp('2026-11-15')

TZ = {'BRISBANE': 'Australia/Brisbane', 'HONG KONG': 'Asia/Hong_Kong', 'ADELAIDE': 'Australia/Adelaide', 'AUCKLAND': 'Pacific/Auckland',
      'MONTPELLIER': 'Europe/Paris', 'DALLAS': 'America/Chicago', 'ROTTERDAM': 'Europe/Amsterdam', 'BUENOS AIRES': 'America/Argentina/Buenos_Aires',
      'DELRAY': 'America/New_York', 'DOHA': 'Asia/Qatar', 'RIO': 'America/Sao_Paulo', 'ACAPULCO': 'America/Mexico_City', 'DUBAI': 'Asia/Dubai',
      'SANTIAGO': 'America/Santiago', 'INDIAN WELLS': 'America/Los_Angeles', 'MIAMI': 'America/New_York', 'MARRAKECH': 'Africa/Casablanca',
      'HOUSTON': 'America/Chicago', 'BUCHAREST': 'Europe/Bucharest', 'MONTE': 'Europe/Monaco', 'BARCELONA': 'Europe/Madrid', 'MUNICH': 'Europe/Berlin',
      'MADRID': 'Europe/Madrid', 'ROME': 'Europe/Rome', 'GENEVA': 'Europe/Zurich', 'HAMBURG': 'Europe/Berlin', 'STUTTGART': 'Europe/Berlin',
      'HERTOGENBOSCH': 'Europe/Amsterdam', 'HALLE': 'Europe/Berlin', 'LONDON': 'Europe/London', 'MALLORCA': 'Europe/Madrid', 'EASTBOURNE': 'Europe/London',
      'BASTAD': 'Europe/Stockholm', 'GSTAAD': 'Europe/Zurich', 'UMAG': 'Europe/Zagreb', 'KITZBUHEL': 'Europe/Vienna', 'ESTORIL': 'Europe/Lisbon',
      'LOS CABOS': 'America/Mazatlan', 'WASHINGTON': 'America/New_York', 'MONTREAL': 'America/Toronto', 'CINCINNATI': 'America/New_York',
      'WINSTON': 'America/New_York', 'CHENGDU': 'Asia/Shanghai', 'HANGZHOU': 'Asia/Shanghai', 'TOKYO': 'Asia/Tokyo', 'BEIJING': 'Asia/Shanghai',
      'SHANGHAI': 'Asia/Shanghai', 'ALMATY': 'Asia/Almaty', 'BRUSSELS': 'Europe/Brussels', 'LYON': 'Europe/Paris', 'BASEL': 'Europe/Zurich',
      'VIENNA': 'Europe/Vienna', 'PARIS': 'Europe/Paris', 'STOCKHOLM': 'Europe/Stockholm', 'TURIN': 'Europe/Rome'}
NAMES = {'MONTE': 'Monte-Carlo', 'HERTOGENBOSCH': "'s-Hertogenbosch", 'WINSTON': 'Winston-Salem', 'DELRAY': 'Delray Beach', 'RIO': 'Rio de Janeiro',
         'WASHINGTON': 'Washington', 'LONDON': "London (Queen's)", 'KITZBUHEL': 'Kitzbuhel'}
SLOT_NAMES = {'Winston-Salem': 'WINSTON', 'Indian Wells': 'INDIAN WELLS', 'Hong Kong': 'HONG KONG'}
TWELVE_DAY = {'INDIAN WELLS', 'MIAMI', 'MADRID', 'ROME', 'MONTREAL', 'CINCINNATI', 'SHANGHAI'}


def key_for(city):
    c = str(city).upper().replace("'", '').replace('’', '').replace('Ü', 'U')
    return next((k for k in TZ if k in c), None)


def load_events():
    e = pd.read_csv(P / 'atp_event_starts.csv')
    e = e[e.tier.isin(['ATP 250', 'ATP 500', 'ATP MASTERS 1000', 'ATP FINALS']) & e.start_date.notna()].copy()
    e['key'] = e.city.map(key_for)
    missing = e[e.key.isna()]
    assert missing.empty, f'Unmapped cities: {missing.city.tolist()}'
    e['event'] = [NAMES.get(k, k.title()) for k in e.key]
    e['start'] = pd.to_datetime(e.start_date)
    slam_starts = pd.to_datetime(['2026-01-18', '2026-05-24', '2026-06-29', '2026-08-31', '2026-11-15'])  # Slams, then Turin
    finals, basis = [], []
    fut = pd.read_csv(P / 'atp_future_windows.csv')
    fut = {key_for(r.event): pd.Timestamp(r.end_date) for r in fut.itertuples() if r.regular_atp and key_for(r.event)}
    for r in e.itertuples():
        if r.key in fut:
            finals.append(fut[r.key]); basis.append('ATP calendar end date (O)'); continue
        if r.key in TWELVE_DAY:
            finals.append(r.start + timedelta(days=11)); basis.append('Start + 11 days, 12-day Masters (A)'); continue
        pre_slam = ((slam_starts > r.start) & (slam_starts - r.start <= timedelta(days=9))).any()
        days = (6 if r.start.weekday() == 6 else 5) if pre_slam else (7 if r.start.weekday() == 6 else 6)
        finals.append(r.start + timedelta(days=days)); basis.append('Weekly event rule (A)')
    e['final_date'], e['final_basis'] = finals, basis
    slots = pd.read_csv(P / 'atp_slots.csv')
    slots = slots[slots['round'] == 'Singles final']
    verified = {SLOT_NAMES.get(r.event, r.event.upper()): r for r in slots.itertuples()}
    return e, verified


def robustness(ist_hour):
    cells = [(s <= (ist_hour + d / 60) % 24 < t) for s, t in SETTINGS['viewing_windows_ist'] for d in SETTINGS['delays_minutes']]
    return sum(cells), len(cells)


def status(passes, total, hour):
    """Campaign-ready means robust: the start sits inside every viewing window under every delay (12/12)."""
    if passes == total:
        return 'Campaign-ready: sell live'
    if passes > 0 and hour < 19:
        return 'Early evening: live with start reminder'
    if passes > 0:
        return 'Late: remind + replay'
    if hour < 7:
        return 'Overnight: replay only'
    return 'Daytime: highlights'


def clashes(start_ist, days, f1, football):
    b, a = SETTINGS['clash_window_hours']['before'], SETTINGS['clash_window_hours']['after']
    f1_hits, fb_hits, fb_checked = [], 0, True
    for d in range(days):
        s = start_ist + timedelta(days=d)
        lo, hi = s - timedelta(hours=b), s + timedelta(hours=a)
        f1_hits += [r.event for r in f1.itertuples() if lo <= r.t <= hi]
        fb_hits += sum(1 for t in football.t if lo <= t <= hi)
        if s.tz_localize(None) > football.t.max().tz_localize(None) + timedelta(days=1):
            fb_checked = False
    return sorted(set(f1_hits)), fb_hits, fb_checked


def build():
    events, verified = load_events()
    f1 = pd.read_csv(P / 'f1_races.csv'); f1['t'] = pd.to_datetime(f1.start_ist)
    fb = pd.read_csv(P / 'football_fixtures.csv'); fb['t'] = pd.to_datetime(fb.start_ist)
    slam_final = {k: pd.Timestamp(v) for k, v in SLAM_FINALS.items()}
    rows = []
    for r in events.itertuples():
        tz = ZoneInfo(TZ[r.key])
        post_slam = [s for s, d in slam_final.items() if timedelta(0) < r.start - d <= timedelta(days=SETTINGS['post_slam_days'])]
        race = r.tier != 'ATP FINALS' and timedelta(0) <= TURIN_START - r.start <= timedelta(days=SETTINGS['race_to_turin_days'])
        continuity = ('Post-Slam follow-through: ' + ', '.join(post_slam)) if post_slam else ('Race to Turin' if race else ('Season finale' if r.tier == 'ATP FINALS' else 'No trigger'))
        early_days = max(1, (r.final_date - r.start).days)
        mid = r.start + timedelta(days=early_days // 2)
        for session in ['Day session', 'Night session', 'Final']:
            if session == 'Final':
                v = verified.get(r.key)
                if v is not None:
                    start_ist = pd.Timestamp(v.start_ist); time_conf = 'High: official order of play (O)'
                    local = f'{v.time_local} ({v.time_semantics.replace("_", " ")})'
                    final_date, final_basis = pd.Timestamp(v.date_local), 'Official order of play (O)'
                else:
                    loc = datetime.combine(r.final_date.date(), datetime.strptime(SETTINGS['session_local_start']['Final'], '%H:%M').time(), tz)
                    start_ist = pd.Timestamp(loc.astimezone(IST)); local = SETTINGS['session_local_start']['Final'] + ' (modelled)'
                    time_conf = 'Medium: published date, modelled time (A)' if not r.date_inherited else 'Low: inherited date, modelled time (A)'
                    final_date, final_basis = r.final_date, r.final_basis
                window_date, days = final_date, 1
            else:
                final_date, final_basis = r.final_date, r.final_basis
                loc = datetime.combine(mid.date(), datetime.strptime(SETTINGS['session_local_start'][session], '%H:%M').time(), tz)
                start_ist = pd.Timestamp(loc.astimezone(IST)); local = SETTINGS['session_local_start'][session] + ' (modelled)'
                time_conf = 'Medium: published date, modelled time (A)' if not r.date_inherited else 'Low: inherited date, modelled time (A)'
                window_date, days = r.start, early_days
                start_ist = start_ist - timedelta(days=(mid - r.start).days)  # first day of the early rounds, same clock time
            hour = start_ist.hour + start_ist.minute / 60
            passes, total = robustness(hour)
            st = status(passes, total, hour)
            f1_hits, fb_hits, fb_checked = clashes(start_ist, days, f1, fb)
            clash_free = 1.0 if not f1_hits and fb_hits == 0 else (0.5 if not f1_hits else 0.0)
            if not fb_checked and not f1_hits:
                clash_free = 0.5  # unknown football fixtures are not treated as clear
            tier_v = SETTINGS['tier_value'][r.tier]
            w = SETTINGS['weights']
            score = 100 * (w['timing'] * passes / total + w['tier'] * tier_v + w['continuity'] * (0.0 if continuity == 'No trigger' else 1.0) + w['clash_free'] * clash_free)
            price = SETTINGS['list_price'][r.tier]
            if st == 'Campaign-ready: sell live':
                offer = f'INR {price} tournament pass at list'
            elif st == 'Early evening: live with start reminder':
                offer = f'INR {price} tournament pass at list; reminder at start; replay for late joiners'
            elif st == 'Late: remind + replay':
                offer = f'Reminder; INR {SETTINGS["replay_price"]} replay default; 10% late discount only as a test arm'
            elif st == 'Overnight: replay only':
                offer = f'INR {SETTINGS["replay_price"]} replay where rights permit'
            else:
                offer = 'Highlights and next-occasion prompt; no live acquisition spend'
            clash_text = '; '.join(filter(None, [('F1: ' + ', '.join(f1_hits)) if f1_hits else '',
                                                 f'La Liga fixtures overlapping: {fb_hits}' if fb_hits else '',
                                                 '' if fb_checked else 'Football not checked (no 2026-27 fixture data captured)'])) or 'No overlap found'
            rows.append({'event': r.event, 'tier': r.tier.replace('ATP ', '').replace('MASTERS 1000', 'Masters 1000').title().replace('Masters 1000', 'Masters 1000'),
                         'event_start': r.start.date().isoformat(), 'final_date': final_date.date().isoformat(), 'final_date_basis': final_basis,
                         'session': session, 'local_start': local, 'local_timezone': TZ[r.key],
                         'window_date': window_date.date().isoformat(), 'ist_start': start_ist.strftime('%H:%M'),
                         'timing_cells_passed': f'{passes}/{total}', 'status': st, 'clash_check': clash_text,
                         'continuity_trigger': continuity, 'offer': offer, 'rights': 'Covered: ATP Tour package (C)',
                         'timing_confidence': time_conf, 'upcoming': final_date >= ANALYSIS_DATE, 'score': round(score, 1)})
    order = {'Campaign-ready: sell live': 0, 'Early evening: live with start reminder': 1, 'Late: remind + replay': 2, 'Overnight: replay only': 3, 'Daytime: highlights': 4}
    df = pd.DataFrame(rows)
    df['_o'] = df.status.map(order)
    df = df.sort_values(['_o', 'score', 'window_date'], ascending=[True, False, True]).drop(columns='_o').reset_index(drop=True)  # status first, then score
    df.insert(0, 'rank', range(1, len(df) + 1))
    return df, events


def summarise(df, events):
    live = df[df.status == 'Campaign-ready: sell live']
    return {
        'events': int(len(events)), 'windows': int(len(df)),
        'campaign_ready_live': int(len(live)),
        'early_evening_live': int((df.status == 'Early evening: live with start reminder').sum()),
        'late_remind_replay': int((df.status == 'Late: remind + replay').sum()),
        'daytime_highlights': int((df.status == 'Daytime: highlights').sum()), 'overnight_replay': int((df.status == 'Overnight: replay only').sum()),
        'events_with_a_live_window': int(live.event.nunique()),
        'live_windows_by_tier': live.tier.value_counts().to_dict(),
        'live_windows_by_session': live.session.value_counts().to_dict(),
        'live_windows_with_f1_clash': int(live.clash_check.str.contains('F1:').sum()),
        'live_windows_with_football_clash': int(live.clash_check.str.contains('La Liga').sum()),
        'upcoming_live_windows': int(live.upcoming.sum()),
        'high_confidence_windows': int(df.timing_confidence.str.startswith('High').sum()),
        'top_upcoming': df[df.upcoming & (df.status == 'Campaign-ready: sell live')].head(10)[['rank', 'event', 'session', 'window_date', 'ist_start', 'score']].to_dict('records'),
    }


if __name__ == '__main__':
    df, events = build()
    df.to_csv(ROOT / 'outputs/tables/10_campaign_ready_windows.csv', index=False)
    summary = summarise(df, events)
    (ROOT / 'outputs/reports/10_campaign_windows_summary.json').write_text(json.dumps({'settings': SETTINGS, 'summary': summary}, indent=1, default=str) + '\n')
    print(json.dumps(summary, indent=1, default=str))
