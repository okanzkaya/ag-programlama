import os
from collections import Counter

def lorem_sikistir(dosya_adi):
    # 1. Dosyayı oku
    if not os.path.exists(dosya_adi):
        return print(f"Hata: {dosya_adi} bulunamadı!")

    with open(dosya_adi, 'r', encoding='utf-8') as f:
        metin = f.read()

    # 2. Frekans ve Sözlük Oluşturma
    frekanslar = Counter(metin)
    sirali = sorted(frekanslar.items(), key=lambda x: x[1], reverse=True)
    
    # Basit bir "Prefix Code" (Önek Kodu) oluşturuyoruz
    sozluk = {}
    for i, (char, _) in enumerate(sirali):
        # En sık harfe 0, sonrakine 10, sonrakine 110...
        sozluk[char] = ('1' * i) + '0'

    # 3. Metni Bitlere Dönüştür
    bit_dizisi = "".join(sozluk[char] for char in metin)
    
    # Byte sınırına (8 bit) tamamlama
    dolgu_miktari = 8 - (len(bit_dizisi) % 8)
    bit_dizisi += '0' * dolgu_miktari

    # 4. Binary (İkilik) Dosyaya Yazma
    byte_dizisi = bytearray()
    for i in range(0, len(bit_dizisi), 8):
        byte_dizisi.append(int(bit_dizisi[i:i+8], 2))

    yeni_dosya = "lorem_compressed.bin"
    with open(yeni_dosya, 'wb') as f:
        f.write(byte_dizisi)

    # 5. Sonuçları Karşılaştır
    eski_boyut = os.path.getsize(dosya_adi)
    yeni_boyut = os.path.getsize(yeni_dosya)
    
    print(f"Orijinal Lorem Dosyası: {eski_boyut} byte")
    print(f"Sıkıştırılmış Binary Dosya: {yeni_boyut} byte")
    print(f"Kurtarılan Alan: {eski_boyut - yeni_boyut} byte")
    print(f"Sıkıştırma Oranı: %{((eski_boyut - yeni_boyut) / eski_boyut) * 100:.2f}")

# Çalıştır
lorem_sikistir("lorem.txt")