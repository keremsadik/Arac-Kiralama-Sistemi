import json

def verileri_oku():
    try:
        f = open('araclar.json', 'r', encoding='utf-8')
        araclar = json.load(f)
        f.close()
        return araclar
    except:
        return []

def verileri_yaz(araclar):
    f = open('araclar.json', 'w', encoding='utf-8')
    json.dump(araclar, f, ensure_ascii=False, indent=2)
    f.close()