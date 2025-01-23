import tkinter as tk
from tkinter import messagebox
import sqlite3


conn = sqlite3.connect("sonuclar.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS ogrenci (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ad TEXT NOT NULL,
    soyad TEXT NOT NULL,
    vize INTEGER NOT NULL,
    final INTEGER NOT NULL,
    sonuc INTEGER
)
""")
conn.commit()

def yeni_kisi_ekle():
    ad = ad_entry.get().strip()
    soyad = soyad_entry.get().strip()
    vize = vize_entry.get().strip()
    final = final_entry.get().strip()

    if not ad or not soyad or not vize or not final:
        messagebox.showwarning("Eksik Bilgi", "Lütfen ad, soyad, vize ve final alanlarını doldurun!")
        return

    vize = int(vize)
    final = int(final)
    sonuc = "G" if (vize + final) / 2 >= 50 else "K"

    cursor.execute("""
    INSERT INTO ogrenci (ad, soyad, vize, final, sonuc)
    VALUES (?, ?, ?, ?, ?)
    """, (ad, soyad, vize, final, sonuc))
    conn.commit()

    messagebox.showinfo("Başarılı", f"Kişi başarıyla eklendi! Sonuç: {sonuc}")
    temizle()

def tum_kisileri_listele():
    cursor.execute("SELECT * FROM ogrenci")
    kisiler = cursor.fetchall()

    listbox.delete(0, tk.END)

    if kisiler:
        for kisi in kisiler:
            listbox.insert(tk.END, f"ID: {kisi[0]}, Ad: {kisi[1]}, Soyad: {kisi[2]}, vize: {kisi[3]}, final: {kisi[4] },sonuc:  {kisi[5]}")
    else:
        listbox.insert(tk.END, "Adres defterinde kayıtlı kişi bulunmuyor.")


def temizle():
    ad_entry.delete(0, tk.END)
    soyad_entry.delete(0, tk.END)
    vize_entry.delete(0, tk.END)
    final_entry.delete(0, tk.END)
    
    


root = tk.Tk()
root.title("Gökşenin Adres Defteri")

tk.Label(root, text="Ad:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
ad_entry = tk.Entry(root)
ad_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="Soyad:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
soyad_entry = tk.Entry(root)
soyad_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(root, text="vize:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
vize_entry = tk.Entry(root)
vize_entry.grid(row=2, column=1, padx=5, pady=5)

tk.Label(root, text="final:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
final_entry = tk.Entry(root)
final_entry.grid(row=3, column=1, padx=5, pady=5)


tk.Button(root, text="Kişi Ekle", width=20, height=1, command=yeni_kisi_ekle).grid(row=5, column=0, padx=5, pady=5, columnspan=2)
tk.Button(root, text="Kişileri Listele", width=20, height=1, command=tum_kisileri_listele).grid(row=6, column=0, padx=5, pady=5, columnspan=2)
tk.Button(root, text="Temizle", width=20, height=1, command=temizle).grid(row=7, column=0, padx=5, pady=5, columnspan=2)

listbox = tk.Listbox(root, width=60, height=30)
listbox.grid(row=8, column=0, columnspan=2, padx=5, pady=5)

root.mainloop()
conn.close()
