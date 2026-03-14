from datetime import datetime
def gun_hesapla(baslangic, bitis):
    try:
        bas = datetime.strptime(baslangic, "%d-%m-%Y")
        bit = datetime.strptime(bitis, "%d-%m-%Y")
        
        fark = (bit - bas).days
        if fark <= 0:
            fark = 1
        return fark
    except:
        return None

def ucret_hesapla(gun_sayisi, gunluk_ucret):
    return gun_sayisi * gunluk_ucret

def tarih_kontrol(baslangic, bitis):
    try:
        bas = datetime.strptime(baslangic, "%d-%m-%Y")
        bit = datetime.strptime(bitis, "%d-%m-%Y")
        
        if bit < bas:
            return False
        return True
    except:
        return None