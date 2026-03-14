import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import dosya_islemleri
import hesaplamalar

class AracKiralamaSistemi:
    def __init__(self):
        self.araclar = []
        self.pencere = tk.Tk()
        self.pencere.title("Araç Kiralama Sistemi")
        self.pencere.geometry("1100x600") 
        self.pencere.configure(bg="lightgray")
        self.araclar = dosya_islemleri.verileri_oku()
        self.arayuz_olustur()
        self.listeyi_guncelle()
    
    def arayuz_olustur(self):
        form_cerceve = tk.Frame(self.pencere, bg="lightgray")
        form_cerceve.pack(pady=20)
        
        tk.Label(form_cerceve, text="Plaka:", bg="lightgray").grid(row=0, column=0, padx=2)
        self.plaka_kutu = tk.Entry(form_cerceve, width=10)
        self.plaka_kutu.grid(row=0, column=1, padx=5)
        
        tk.Label(form_cerceve, text="Marka:", bg="lightgray").grid(row=0, column=2, padx=2)
        self.marka_kutu = tk.Entry(form_cerceve, width=12)
        self.marka_kutu.grid(row=0, column=3, padx=5)
        
        tk.Label(form_cerceve, text="Model:", bg="lightgray").grid(row=0, column=4, padx=2)
        self.model_kutu = tk.Entry(form_cerceve, width=12)
        self.model_kutu.grid(row=0, column=5, padx=5)
        
        tk.Label(form_cerceve, text="Günlük Ücret:", bg="lightgray").grid(row=0, column=6, padx=2)
        self.ucret_kutu = tk.Entry(form_cerceve, width=8)
        self.ucret_kutu.grid(row=0, column=7, padx=5)

        tk.Button(form_cerceve, text="Araç Ekle", command=self.arac_ekle, width=10, bg="deepskyblue", fg="black", font=('Arial', 9, 'bold')).grid(row=0, column=8, padx=10)
        buton_cerceve = tk.Frame(self.pencere, bg="lightgray")
        buton_cerceve.pack(pady=10)
        
        tk.Button(buton_cerceve, text="Düzenle", command=self.arac_duzenle, width=12, bg="lightblue").pack(side=tk.LEFT, padx=5)
        tk.Button(buton_cerceve, text="Kiralama Başlat", command=self.kiralama_baslat, width=12, bg="lightblue").pack(side=tk.LEFT, padx=5)
        tk.Button(buton_cerceve, text="Aracı İade Al", command=self.arac_iade, width=12, bg="lightblue").pack(side=tk.LEFT, padx=5)
        tk.Button(buton_cerceve, text="Sil", command=self.arac_sil, width=12, bg="#C90000", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(buton_cerceve, text="Kaydet", command=self.kaydet, width=12, bg="green", fg="white").pack(side=tk.LEFT, padx=5)
        
        liste_cerceve = tk.Frame(self.pencere)
        liste_cerceve.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        sutunlar = ("plaka", "marka", "model", "günlük ücret", "durum", "kiralayan", "başlangıç", "bitiş")
        self.tablo = ttk.Treeview(liste_cerceve, columns=sutunlar, show="headings", height=15)
        self.tablo.tag_configure("musait_tag", background="#DFF0D8") 
        self.tablo.tag_configure("kirada_tag", background="#F2DEDE") 

        for s in sutunlar:
            self.tablo.heading(s, text=s.title())
            self.tablo.column(s, width=120, anchor="center")
        
        self.tablo.pack(fill=tk.BOTH, expand=True)

    def listeyi_guncelle(self):
        for item in self.tablo.get_children():
            self.tablo.delete(item)

        for arac in self.araclar:
            durum_tag = "musait_tag" if arac["durum"] == "müsait" else "kirada_tag"

            self.tablo.insert("", "end", values=(
                arac["plaka"].upper(),
                arac["marka"].title(),
                arac["model"].title(),
                f"{arac['ucret']} TL",
                arac["durum"].title(),
                arac.get("kiralayan", "").title(),
                arac.get("baslangic_tarihi", ""),
                arac.get("bitis_tarihi", "")
            ), tags=(durum_tag,)) 
            
    def arac_duzenle(self):
        secili = self.tablo.selection()
        if not secili:
            messagebox.showerror("Hata", "Düzenlemek için bir araç seçin!")
            return
        
        index = self.tablo.index(secili[0])
        arac = self.araclar[index]
        duzenle_pencere = tk.Toplevel(self.pencere)
        duzenle_pencere.title("Aracı Düzenle")
        duzenle_pencere.geometry("300x320")
        
        tk.Label(duzenle_pencere, text="Plaka:").pack(pady=(10,0))
        e_plaka = tk.Entry(duzenle_pencere)
        e_plaka.insert(0, arac["plaka"])
        e_plaka.pack(pady=2)
        
        tk.Label(duzenle_pencere, text="Marka:").pack()
        e_marka = tk.Entry(duzenle_pencere)
        e_marka.insert(0, arac["marka"])
        e_marka.pack(pady=2)
        
        tk.Label(duzenle_pencere, text="Model:").pack()
        e_model = tk.Entry(duzenle_pencere)
        e_model.insert(0, arac["model"])
        e_model.pack(pady=2)
        
        tk.Label(duzenle_pencere, text="Günlük Ücret:").pack()
        e_ucret = tk.Entry(duzenle_pencere)
        e_ucret.insert(0, arac["ucret"])
        e_ucret.pack(pady=2)
        
        def guncelle_kaydet():
            try:
                yeni_ucret = float(e_ucret.get())
                arac["plaka"] = e_plaka.get()
                arac["marka"] = e_marka.get()
                arac["model"] = e_model.get()
                arac["ucret"] = yeni_ucret
                
                self.listeyi_guncelle()
                duzenle_pencere.destroy()
                messagebox.showinfo("Başarılı", "Araç bilgileri güncellendi.")
            except ValueError:
                messagebox.showerror("Hata", "Ücret geçerli bir sayı olmalı!")

        tk.Button(duzenle_pencere, text="Güncelle", command=guncelle_kaydet, bg="green", fg="white", width=15).pack(pady=20)

    def arac_ekle(self):
        plaka = self.plaka_kutu.get()
        marka = self.marka_kutu.get()
        model = self.model_kutu.get()
        ucret = self.ucret_kutu.get()
        
        if not (plaka and marka and model and ucret):
            messagebox.showerror("Hata", "Lütfen tüm alanları doldurun!")
            return
        
        try:
            ucret = float(ucret)
        except:
            messagebox.showerror("Hata", "Ücret sayı olmalı!")
            return
        
        yeni_arac = {
            "plaka": plaka, "marka": marka, "model": model, "ucret": ucret,
            "durum": "müsait", "kiralayan": "", "baslangic_tarihi": "", "bitis_tarihi": ""
        }
        
        self.araclar.append(yeni_arac)
        for kutu in [self.plaka_kutu, self.marka_kutu, self.model_kutu, self.ucret_kutu]:
            kutu.delete(0, tk.END)
            
        self.listeyi_guncelle()
        messagebox.showinfo("Başarılı", "Araç başarıyla eklendi.")

    def kiralama_baslat(self):
        secili = self.tablo.selection()
        if not secili:
            messagebox.showerror("Hata", "Lütfen bir araç seçin!")
            return
        
        index = self.tablo.index(secili[0])
        arac = self.araclar[index]
        
        if arac["durum"] != "müsait":
            messagebox.showerror("Hata", "Bu araç şu an müsait değil!")
            return
        
        kiralama_pencere = tk.Toplevel(self.pencere)
        kiralama_pencere.title("Kiralama İşlemi")
        kiralama_pencere.geometry("300x280")
        
        tk.Label(kiralama_pencere, text="Müşteri Adı:").pack(pady=5)
        musteri_kutu = tk.Entry(kiralama_pencere, width=30); musteri_kutu.pack()
        
        tk.Label(kiralama_pencere, text="Başlangıç Tarihi (GG-AA-YYYY):").pack(pady=5)
        baslangic_kutu = tk.Entry(kiralama_pencere, width=30); baslangic_kutu.pack()
        
        tk.Label(kiralama_pencere, text="Bitiş Tarihi (GG-AA-YYYY):").pack(pady=5)
        bitis_kutu = tk.Entry(kiralama_pencere, width=30); bitis_kutu.pack()
        
        def tamamla():
            musteri = musteri_kutu.get(); baslangic = baslangic_kutu.get(); bitis = bitis_kutu.get()
            if not (musteri and baslangic and bitis):
                messagebox.showerror("Hata", "Tüm alanları doldurun!"); return
            
            tarih_sonuc = hesaplamalar.tarih_kontrol(baslangic, bitis)
            if tarih_sonuc is None:
                messagebox.showerror("Hata", "Tarih formatı hatalı!"); return
            if tarih_sonuc is False:
                messagebox.showerror("Hata", "Bitiş tarihi başlangıçtan önce olamaz!"); return
            
            gun_sayisi = hesaplamalar.gun_hesapla(baslangic, bitis)
            toplam_ucret = hesaplamalar.ucret_hesapla(gun_sayisi, arac["ucret"])
        
            arac.update({"durum": "kirada", "kiralayan": musteri, "baslangic_tarihi": baslangic, "bitis_tarihi": bitis})
            self.listeyi_guncelle()
            kiralama_pencere.destroy()
            messagebox.showinfo("Başarılı", f"Kiralama tamamlandı.\nÜcret: {toplam_ucret} TL")
        
        tk.Button(kiralama_pencere, text="Kirala", command=tamamla, bg="green", fg="white").pack(pady=20)
    
    def arac_iade(self):
        secili = self.tablo.selection()
        if not secili:
            messagebox.showerror("Hata", "Bir araç seçin!"); return
        
        index = self.tablo.index(secili[0]); arac = self.araclar[index]
        if arac["durum"] != "kirada":
            messagebox.showerror("Hata", "Bu araç kirada değil!"); return
        
        arac.update({"durum": "müsait", "kiralayan": "", "baslangic_tarihi": "", "bitis_tarihi": ""})
        self.listeyi_guncelle()
        messagebox.showinfo("Başarılı", "Araç iade edildi.")
    
    def arac_sil(self):
        secili = self.tablo.selection()
        if not secili:
            messagebox.showerror("Hata", "Bir araç seçin!"); return
        
        if messagebox.askyesno("Onay", "Bu aracı silmek istediğinizden emin misiniz?"):
            index = self.tablo.index(secili[0])
            self.araclar.pop(index)
            self.listeyi_guncelle()
            messagebox.showinfo("Başarılı", "Araç silindi.")
    
    def kaydet(self):
        dosya_islemleri.verileri_yaz(self.araclar)
        messagebox.showinfo("Bilgi", "Bilgiler dosyaya kaydedildi.")
    
    def kapat(self):
        dosya_islemleri.verileri_yaz(self.araclar)
        self.pencere.destroy()
    
    def calistir(self):
        self.pencere.protocol("WM_DELETE_WINDOW", self.kapat)
        self.pencere.mainloop()
