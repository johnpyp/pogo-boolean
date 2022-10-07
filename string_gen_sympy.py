from sympy.core import symbol
from sympy.logic import simplify_logic
from sympy import symbols, Symbol
from sympy.logic.boolalg import Or
# from pyeda.inter import *

good_pokemon = ["lucario", "togepi", "dratini", "ralts", "eevee"]

pvs = []
for pmon in good_pokemon:
    pv = symbols("PMON_" + pmon)
    pvs.append(pv)

all_good = Or(*pvs)

is_legendary =  symbols("ZZ_legendary")
is_shiny =  symbols("ZZ_shiny")
is_pokemon =  symbols("ZZ_shiny")
is_traded =  symbols("ZZ_traded")
is_trade_evolve =  symbols("ZZ_tradeevolve")

is_4_star = symbols("ZZ_4_star")

is_0_1_attack = symbols("ZZ_0_1_attack")
is_3_4_attack = symbols("ZZ_3_4_attack")
is_3_4_defense = symbols("ZZ_3_4_defense")
is_3_4_hp = symbols("ZZ_3_4_hp")

expr_attack_ivs = is_0_1_attack & is_3_4_defense & is_3_4_hp
expr_3_4_all = is_3_4_attack & is_3_4_defense & is_3_4_hp

pok_good_attack_iv = all_good & expr_attack_ivs
pok_good_3_4_star = all_good & expr_3_4_all

pok_bad_attack_iv_not_traded = all_good & ~expr_attack_ivs & ~is_traded

pok_4_star = is_4_star

final_expr = ~(pok_good_3_4_star | pok_good_3_4_star | pok_4_star | pok_bad_attack_iv_not_traded)


print(final_expr)
simplified = simplify_logic(final_expr, 'cnf', True, True)
print(simplified)


# c1 = final_expr.to_cnf()
# print(c1.simple)
# print(c1, len(str(c1)))
# print("----------")
# print(expr2dimacscnf(c1))

# # print(final_expr.to_cnf())
# f1m, = espresso_exprs(final_expr.to_dnf())
# c2 = f1m.to_cnf()

# # c2 = f1m.to_cnf()

# # print(c2, len(str(c2)))
