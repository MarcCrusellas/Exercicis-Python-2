import csv
import consts
import json
import matplotlib.pyplot as plt

# EXERCICI 1
header = []
llista_diccionaris = []
f = open("basket_players.csv")
for i, fila in enumerate(f):
    if (i == 0):
        header = fila[0:-1].split(";")
    else:
        element = fila[0:-1].split(";")
        item = {}
        for x, zone in enumerate(header):
            item[zone] = element[x]
        llista_diccionaris.append(item)
f.close()

text = ["NOM", "EQUIP", "POSICIO", "ALTURA", "GRUIX", "EDAT"]
trad = {"Point Guard": "Base", "Shooting Guard": "Escorta",
        "Small Forward": "Aler", "Power Forward": "Ala-pivot", "Center": "Pivot"}
newF = open("jugadors_basket.csv", "w")


writer = csv.DictWriter(newF, fieldnames=text,
                        delimiter="^", lineterminator="\n")
writer.writeheader()
writer.fieldnames = header

for index, dct in enumerate(llista_diccionaris):
    dct['Position'] = trad[dct['Position']]
    dct['Heigth'] = round(float(dct['Heigth']) * consts.inch_to_cm, 2)
    dct['Weigth'] = round(float(dct['Weigth']) * consts.lbs_to_kgs, 2)
    dct['Age'] = round(float(dct['Age']), 2)
    writer.writerow(dct)
newF.close()

# EXERCICI 2
heaviest = llista_diccionaris[0]
shortest = llista_diccionaris[0]
num_posicions = {}
equips = {}
edats = {}
for dct in llista_diccionaris:
    # Pes mes alt i altura mes baixa
    if (dct["Weigth"] > heaviest["Weigth"]):
        heaviest = dct
    if (dct["Heigth"] < shortest["Heigth"]):
        shortest = dct

    # Pes i alçada total per equip.
    if (dct["Team"] not in equips.keys()):
        equips[dct["Team"]] = {"count": 0, "pes": 0, "alt": 0}
    equips[dct["Team"]]["count"] += 1
    equips[dct["Team"]]["pes"] += dct["Weigth"]
    equips[dct["Team"]]["alt"] += dct["Heigth"]

    # Recompte de jugadors per posició.
    if (dct["Position"] not in num_posicions.keys()):
        num_posicions[dct["Position"]] = 1
    else:
        num_posicions[dct["Position"]] += 1

    # Distribució de jugadors per edat.
    if (dct["Age"] not in edats.keys()):
        edats[dct["Age"]] = 1
    else:
        edats[dct["Age"]] += 1

# Mitjana pes i alçada per equip.
for equip in equips.keys():
    equips[equip]["pes"] = round(
        equips[equip]["pes"]/equips[equip]["count"], 2)
    equips[equip]["alt"] = round(
        equips[equip]["alt"]/equips[equip]["count"], 2)

# PRINTS
print("Heaviest:", heaviest["Name"])
print("\nShortest:", shortest["Name"])
print("\nMITJANA PES I ALÇADA PER EQUIP")
for nom, info in equips.items():
    print(nom, ":")
    print("Pes:", info["pes"])
    print("Alçada:", info["alt"])
print("\nJUGADORS PER POSICIÓ")
for pos, num in num_posicions.items():
    print(pos, ":", num)
print("\nJUGADORS PER EDAT")
for edat, num in edats.items():
    print(edat, "anys:", num, "jugadors")

# EXERCICI 3
#cvs to josn
f_json= open('jugadors_basket.json', 'w')
json.dump(llista_diccionaris, f_json, indent=4)
f_json.close()

# GRAFICA EDATS
ages = list(edats.keys())
num_jugadors = list(edats.values())
plt.bar(ages, num_jugadors)
plt.xlabel("Edats")
plt.ylabel("Nombre de jugadors")
plt.title("Nombre de jugadors per edat")

# export to png
plt.savefig("edats.png")
