import json
from msilib.schema import File
file = open("data_json.txt","a")

dados = { 100000001: "Luz Canto Bonito", 
100000002: "Vitória Cortês Vigário",
100000003: "Esperança Carvalho Dinis",
100000004: "Nikita Berenguer Barbalho", 
100000005: "Ícaro Narvais Salazar", 
100000006: "Angélico Peseiro Varela", 
100000007: "Elisama Caetano Cardim", 
100000008: "Kevyn Adarga Breia", 
100000009: "Keyla Castilhos Ribeiro", 
100000010: "Samoa Cerveira Rufino", 
100000011: "Yi Ponte Parente", 
100000012: "Anderson Matos Chainho", 
100000013: "Jorge Teles Rebelo", 
100000014: "Humberto Areosa Rabelo", 
100000015: "Lília Amado Fontes", 
100000016: "Máximo Mariz Frajuca", 
100000017: "Valdemar Caeiro Proença", 
100000018: "Gaia Boga Esparteiro", 
100000019: "Benjamin Freire Portugal", 
100000020: "Tobias Bezerril Lagos", 
100000021: "Neide Saldanha Aguiar", 
100000022: "Diogo Frajuca Valadim", 
100000023: "Louis Fialho Assis", 
100000024: "Adelaide Figueiredo Azenha", 
100000025: "Yaroslav Escobar Amarante", 
100000026: "Eduardo Galvão Grilo", 
100000027: "Nicolau Pestana Raminhos", 
100000028: "Piedade Machado Vieira"
}
print(dados)

data_json = json.dumps(dados)
file.write(data_json)
file.close()
