from json import dumps
from pyeda.inter import *

master_league_pvp = ["togekiss", "dragonite", "snorlax", "metagross", "excadrill", "mamoswine", "garchomp", "zarude"]
ultra_league_pvp = ["jellicent", "stunfisk", "abomasnow", "sirfetch", "walrein", "cressaelia", "lickilicky", "swampert", "skarmory", "trevenant", "dragonite", "muk"] 
cool_guys = ["lucario", "gardevoir", "eevee"]

good_pokemon = sorted(list(set(master_league_pvp + ultra_league_pvp + cool_guys)))

pvs = []
for pmon in good_pokemon:
    pv = exprvar("PMON_" + pmon)
    pvs.append(pv)

all_good = Or(*pvs)

is_legendary =  exprvar("ZZ_legendary")
is_shiny =  exprvar("ZZ_shiny")
is_traded =  exprvar("ZZ_traded")
is_trade_evolve =  exprvar("ZZ_tradeevolve")
is_shadow =  exprvar("ZZ_shadow")
is_cp1500_ =  exprvar("ZZ_cp1500_")
is_lucky =  exprvar("ZZ_lucky")

is_4_star = exprvar("ZZ_4_star")

is_0_1_attack = exprvar("ZZ_0_1_attack")
is_3_4_attack = exprvar("ZZ_3_4_attack")
is_3_4_defense = exprvar("ZZ_3_4_defense")
is_3_4_hp = exprvar("ZZ_3_4_hp")

expr_attack_ivs = is_0_1_attack & is_3_4_defense & is_3_4_hp
expr_3_4_all = is_3_4_attack & is_3_4_defense & is_3_4_hp

pok_good_attack_iv = all_good & expr_attack_ivs
pok_good_3_4_star = all_good & expr_3_4_all

pok_bad_attack_iv_not_traded = all_good & ~expr_attack_ivs & ~is_traded

final_expr = ~(pok_good_3_4_star | pok_good_3_4_star | pok_bad_attack_iv_not_traded | is_legendary | is_shiny | is_trade_evolve | is_shadow | is_cp1500_ | is_lucky | is_4_star)



c1 = final_expr.to_cnf()
print(c1.simple)
print(c1, len(str(c1)))
print("----------")
mapping, asdf = expr2dimacscnf(c1)

obj = {}
for (k, v) in mapping.items():
    print(str(k))
    if not isinstance(k, int) and v >= 0:
        obj[str(k)] = v


print(dumps(obj, indent=2))
print("-------")
print(asdf)

# print(final_expr.to_cnf())
f1m, = espresso_exprs(final_expr.to_dnf())
c2 = f1m.to_cnf()

# c2 = f1m.to_cnf()

# print(c2, len(str(c2)))
