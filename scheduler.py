import datetime as dt
from typing import List

def spaced_intervals(n: int) -> List[int]:
    """Retorna lista de intervalos (em dias) para n revisões.
    Base: [1, 3, 7, 14, 30, 60, 120] e, se necessário, dobra a partir daí.
    """
    base = [1, 3, 7, 14, 30, 60, 120]
    if n <= len(base):
        return base[:n]
    more = []
    last = base[-1]
    while len(base) + len(more) < n:
        last *= 2
        more.append(last)
    return base + more

def schedule_dates(start_date: dt.date, n: int) -> List[dt.date]:
    ivals = spaced_intervals(n)
    return [start_date + dt.timedelta(days=d) for d in ivals]

# --- SM-2 for flashcards ---
def sm2_update(ease_factor: float, repetitions: int, interval: int, quality: int):
    """Atualiza parâmetros SM-2 (ease_factor, repetitions, interval dias) baseado em quality (0..5)."""
    if quality < 3:
        repetitions = 0
        interval = 1
    else:
        if repetitions == 0:
            interval = 1
            repetitions = 1
        elif repetitions == 1:
            interval = 6
            repetitions = 2
        else:
            interval = int(round(interval * ease_factor))
            repetitions += 1

    # atualizar ease factor
    ef = ease_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
    if ef < 1.3:
        ef = 1.3
    return ef, repetitions, interval
