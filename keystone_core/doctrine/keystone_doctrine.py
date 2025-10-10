import json,math,pathlib
KEYS=["value_creation","ownership","compounding","long_term_thinking","financial_literacy","mindset_purpose","adaptability","risk_management","tax_legal_structures","health_time_stewardship"]
ROOT=pathlib.Path(__file__).resolve().parent
def shaped_reward(sig):
 d=json.load(open(ROOT/"doctrine.json")); w=d["weights"]; return sum(w[k]*sig.get(k,0.5) for k in KEYS)
