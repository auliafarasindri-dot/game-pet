"""
Game Hewan Peliharaan Virtual - Project OOP Python
Materi OOP yang dicakup:
1. Class & Object
2. Encapsulation (atribut private + property getter/setter)
3. Inheritance (Kucing, Anjing, Burung turunan Hewan)
4. Polymorphism (suara() dan bermain() beda tiap hewan)
5. Abstract class
6. Class method & Static method
7. Magic method (__str__, __eq__, __len__)
8. Composition (Game punya Rumah, Rumah punya banyak Hewan)
"""

import random
from abc import ABC, abstractmethod


# ======================= ABSTRACT CLASS =======================
class Hewan(ABC):
    jumlah_hewan = 0  # class attribute

    def __init__(self, nama, umur=1):
        self.nama = nama
        self.umur = umur
        self.__lapar = 50      # private: 0 = kenyang, 100 = sangat lapar
        self.__senang = 50     # private: 0 = sedih, 100 = sangat senang
        Hewan.jumlah_hewan += 1

    # ---------- property ----------
    @property
    def lapar(self):
        return self.__lapar

    @lapar.setter
    def lapar(self, nilai):
        self.__lapar = self._batasi(nilai)

    @property
    def senang(self):
        return self.__senang

    @senang.setter
    def senang(self, nilai):
        self.__senang = self._batasi(nilai)

    @property
    def status(self):
        if self.lapar > 80:
            return "Kelaparan"
        if self.senang < 20:
            return "Sedih"
        if self.senang > 80 and self.lapar < 40:
            return "Bahagia"
        return "Biasa saja"

    # ---------- static method ----------
    @staticmethod
    def _batasi(nilai):
        """Batasi nilai antara 0 sampai 100."""
        return max(0, min(100, nilai))

    # ---------- class method ----------
    @classmethod
    def total_hewan(cls):
        return cls.jumlah_hewan

    @classmethod
    def dari_input(cls, nama):
        """Membuat hewan dengan umur acak."""
        return cls(nama, umur=random.randint(1, 5))

    # ---------- method biasa ----------
    def beri_makan(self):
        self.lapar -= 30
        self.senang += 5
        print(f"{self.nama} makan dengan lahap. Nyam!")

    def waktu_berlalu(self):
        self.lapar += random.randint(5, 15)
        self.senang -= random.randint(3, 10)

    # ---------- abstract method ----------
    @abstractmethod
    def suara(self):
        pass

    @abstractmethod
    def bermain(self):
        pass

    # ---------- magic method ----------
    def __str__(self):
        return (f"{self.nama} ({self.__class__.__name__}, {self.umur} th) | "
                f"Lapar: {self.lapar} | Senang: {self.senang} | {self.status}")

    def __eq__(self, other):
        return isinstance(other, Hewan) and self.nama.lower() == other.nama.lower()


# ======================= INHERITANCE + POLYMORPHISM =======================
class Kucing(Hewan):
    def suara(self):
        return "Meong~"

    def bermain(self):
        self.senang += 20
        self.lapar += 10
        print(f"{self.nama} mengejar bola benang. {self.suara()}")


class Anjing(Hewan):
    def suara(self):
        return "Guk guk!"

    def bermain(self):
        self.senang += 25
        self.lapar += 15
        print(f"{self.nama} berlari mengejar frisbee. {self.suara()}")


class Burung(Hewan):
    def suara(self):
        return "Cuit cuit!"

    def bermain(self):
        self.senang += 15
        self.lapar += 5
        print(f"{self.nama} terbang berkeliling ruangan. {self.suara()}")

    # override: burung kenyang lebih cepat
    def beri_makan(self):
        super().beri_makan()
        self.lapar -= 10


# ======================= COMPOSITION =======================
class Rumah:
    def __init__(self, kapasitas=3):
        self.kapasitas = kapasitas
        self.__penghuni = []

    def tambah(self, hewan):
        if len(self) >= self.kapasitas:
            print("Rumah penuh!")
            return False
        if hewan in self.__penghuni:
            print(f"Sudah ada hewan bernama {hewan.nama}!")
            return False
        self.__penghuni.append(hewan)
        return True

    def semua(self):
        return list(self.__penghuni)

    def __len__(self):
        return len(self.__penghuni)


class Game:
    JENIS = {"1": Kucing, "2": Anjing, "3": Burung}

    def __init__(self):
        self.rumah = Rumah(kapasitas=3)
        self.hari = 1

    def adopsi(self):
        print("\nJenis hewan: 1. Kucing  2. Anjing  3. Burung")
        pilih = input("Pilih jenis: ").strip()
        kelas = self.JENIS.get(pilih)
        if not kelas:
            print("Pilihan tidak valid.")
            return
        nama = input("Beri nama: ").strip() or "Tanpa Nama"
        hewan = kelas.dari_input(nama)
        if self.rumah.tambah(hewan):
            print(f"Selamat! Kamu mengadopsi {hewan.nama}. Dia bilang: {hewan.suara()}")

    def pilih_hewan(self):
        daftar = self.rumah.semua()
        if not daftar:
            print("Belum punya hewan. Adopsi dulu!")
            return None
        for i, h in enumerate(daftar, 1):
            print(f"  {i}. {h}")
        try:
            return daftar[int(input("Pilih nomor hewan: ")) - 1]
        except (ValueError, IndexError):
            print("Nomor tidak valid.")
            return None

    def menu(self):
        print(f"\n===== HARI {self.hari} | Hewan: {len(self.rumah)}/{self.rumah.kapasitas} =====")
        print("1. Adopsi hewan")
        print("2. Beri makan")
        print("3. Ajak bermain")
        print("4. Dengarkan semua suara")
        print("5. Lihat status")
        print("6. Ganti hari")
        print("0. Keluar")

    def mulai(self):
        print("=== SIMULASI HEWAN PELIHARAAN (OOP PYTHON) ===")
        while True:
            self.menu()
            aksi = input("Pilih: ").strip()
            if aksi == "1":
                self.adopsi()
            elif aksi == "2":
                h = self.pilih_hewan()
                if h:
                    h.beri_makan()
            elif aksi == "3":
                h = self.pilih_hewan()
                if h:
                    h.bermain()
            elif aksi == "4":
                for h in self.rumah.semua():
                    print(f"{h.nama}: {h.suara()}")  # polymorphism
            elif aksi == "5":
                for h in self.rumah.semua():
                    print(h)
            elif aksi == "6":
                self.hari += 1
                for h in self.rumah.semua():
                    h.waktu_berlalu()
                print("Hari berganti...")
            elif aksi == "0":
                print(f"Sampai jumpa! Total hewan yang pernah dibuat: {Hewan.total_hewan()}")
                break
            else:
                print("Menu tidak dikenal.")


if __name__ == "__main__":
    Game().mulai()
