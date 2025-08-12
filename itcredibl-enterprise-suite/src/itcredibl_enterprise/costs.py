def within_budget(usage, hard_cap: float):
    c = (usage or {}).get('cost')
    return True if c is None else float(c) <= hard_cap