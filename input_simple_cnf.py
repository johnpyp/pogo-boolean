import json
from pyeda.inter import *

good_pokemon = ["lucario", "togepi", "dratini", "ralts", "eevee"]

pvs = []
for pmon in good_pokemon:
    pv = exprvar("PMON_" + pmon)
    pvs.append(pv)

all_good = Or(*pvs)

is_legendary =  exprvar("ZZ_legendary")
is_shiny =  exprvar("ZZ_shiny")
is_pokemon =  exprvar("ZZ_shiny")
is_traded =  exprvar("ZZ_traded")
is_trade_evolve =  exprvar("ZZ_tradeevolve")

is_4_star = exprvar("ZZ_4_star")

is_0_1_attack = exprvar("ZZ_0_1_attack")
is_3_4_attack = exprvar("ZZ_3_4_attack")
is_3_4_defense = exprvar("ZZ_3_4_defense")
is_3_4_hp = exprvar("ZZ_3_4_hp")

real_mappings = {

}

def map_pmon(v: str):
    v = v.replace("PMON_", "")
    return "+" + v

zz_mappings = {
  "ZZ_traded": "traded",
  "ZZ_4_star": "4*",
  "ZZ_0_1_attack": "0-1attack",
  "ZZ_3_4_attack": "3-4attack",
  "ZZ_3_4_defense": "3-4defense",
  "ZZ_3_4_hp": "3-4hp",
  "ZZ_legendary": "legendary",
  "ZZ_tradeevolve": "tradeevolve",
  "ZZ_shadow": "shadow",
  "ZZ_shiny": "shiny",
  "ZZ_cp1500_": "cp1500-",
  "ZZ_lucky": "lucky"
}

def map_zz(v: str):
    if not v.startswith("ZZ"):
        raise RuntimeError("Str %s not a ZZ str" % v)
    if not v in zz_mappings:
        raise RuntimeError("ZZ str %s not in zz_mappings" % v)
    return zz_mappings[v]

def get_real(lookup_str: str):
    if lookup_str.startswith("PMON"): return map_pmon(lookup_str)
    if lookup_str.startswith("ZZ"): return map_zz(lookup_str)
    raise RuntimeError("Str %s not valid prefix mapping or found in any mappings" % lookup_str)

f = open('input.json')
  
# returns JSON object as 
# a dictionary
init_mapping = json.load(f)

f.close()

lookup_mapping = {}
real_mapping = {}

def create_lookup_mapping():
    for (k, v) in init_mapping.items():
        n = v
        exp = exprvar(k)
        lookup_mapping[n] = exp
        real_mapping[n] = get_real(k)
        lookup_mapping[-n] = ~exp
        real_mapping[-n] = "!" + get_real(k)


def read():
    file_path = "./input.txt"
    print('reading: ' + file_path)
    file = open(file_path, 'r').read()
    rows = file.strip().split('\n')

    ns_list = list()
    clause_list = list()
    for row in rows:
        if row[0] != 'c' and row[0] != 'p':
            var_list = list()
            n_list = list()
            if ' ' in row:
                for var in row.split(' '):
                    if int(var) != 0:
                        var_list.append(lookup_mapping[int(var)])
                        n_list.append(int(var))
            if '\t' in row:
                for var in row.split('\t'):
                    if int(var) != 0:
                        var_list.append(lookup_mapping[int(var)])
                        n_list.append(int(var))
            clause_list.append(Or(*var_list))
            ns_list.append(n_list)


    exp = And(*clause_list)

    return exp, ns_list

create_lookup_mapping()

c, n_list = read()
print(c)

segments = []
for ns in n_list:
    reals = []
    for n in ns:
        real = real_mapping[n]
        reals.append(real)

    segment = ",".join(reals)
    segments.append(segment)
final = "&".join(segments)
print("------------")
print(final)

