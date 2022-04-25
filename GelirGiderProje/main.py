#-------------------KÜTÜPHANE------------------#
#----------------------------------------------#

import sys
from sqlite3 import Cursor
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from AnaSayfaUI import *
from datetime import datetime
from GirisEkraniUI import *
from Hakkinda import *
import time

#---------------UYGULAMA OLUSTUR---------------#
#----------------------------------------------#

Uygulama = QApplication(sys.argv)
penAna = QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(penAna)

penGirisEkrani = QWidget()
ui2 = Ui_Form()
ui2.setupUi(penGirisEkrani)

penHakkinda = QDialog()
ui3 = Ui_Dialog()
ui3.setupUi(penHakkinda)


penGirisEkrani.show()

#-------------KULLANICI GİRİŞ İÇİN VERİTABANI OLUŞTUR---------------#
#-------------------------------------------------------------------#

import sqlite3
global curs3
global conn3
conn3 = sqlite3.connect('veritabaniKullanici.db')
curs3 = conn3.cursor()

sorguCreTblKullaniciVerileri = ('CREATE TABLE IF NOT EXISTS kullaniciverileri(    \
                                Id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,    \
                                KullaniciAdi TEXT NOT NULL,                       \
                                Sifre TEXT NOT NULL)')

curs3.execute(sorguCreTblKullaniciVerileri)
conn3.commit()

#-------------KAYIT OL BUTONU--------------#
#------------------------------------------#

def KAYITOL():

    kullanici_adi = ui2.lneKullaniciAdi.text()
    sifre = ui2.lneSifre.text()

    curs3.execute("SELECT * FROM kullaniciverileri WHERE KullaniciAdi = ?", (kullanici_adi,))
    conn3.commit()
    veri = curs3.fetchall()

    if len(veri) == 0:
        curs3.execute("INSERT INTO kullaniciverileri(KullaniciAdi,Sifre) VALUES(?,?)", (kullanici_adi, sifre))
        conn3.commit()
        ui2.lblBilgilendirme.setText("Kayıt başarılı. Hoşgeldin "+kullanici_adi)
    else:
        ui2.lblBilgilendirme.setText("""
                    Bu kullanıcı adı ile kayıtlı
                başka bir kullanıcı bulunmakta...
        """)

#-------------GİRİŞ YAP BUTONU--------------#
#-------------------------------------------#

def GIRISYAP():

    kullanici_adi = ui2.lneKullaniciAdi.text()
    sifre = ui2.lneSifre.text()

    curs3.execute("SELECT * FROM kullaniciverileri WHERE KullaniciAdi = ?", (kullanici_adi,))
    conn3.commit()
    kullanicidata = curs3.fetchall()

    if len(kullanicidata) != 0:

        curs3.execute("SELECT * FROM kullaniciverileri WHERE KullaniciAdi = ?", (kullanici_adi,))
        conn3.commit()
        kullanicidata = curs3.fetchall()

        curs3.execute("Select * from kullaniciverileri where KullaniciAdi = ? and Sifre = ?",(kullanici_adi,sifre))
        conn3.commit()

        kullanicidata2 = curs3.fetchall()

        if len(kullanicidata2) != 0:
            ui2.lblBilgilendirme.setText("Giriş Başarılı")
            penGirisEkrani.close()
            penAna.show()

            # -------------VERİTABANI OLUŞTUR---------------#
            # ----------------------------------------------#
            kullaniciadiCuzdan = (kullanici_adi + "cuzdan")

            import sqlite3
            global curs
            global conn
            conn = sqlite3.connect('veritabani.db')
            curs = conn.cursor()
            conn2 = sqlite3.connect('veritabani.db')
            curs2 = conn2.cursor()

            sorguCreTblVeriler = (f'CREATE TABLE IF NOT EXISTS {kullanici_adi}(                         \
                                      Id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,           \
                                      GelirGider TEXT NOT NULL,                                \
                                      Miktar TEXT NOT NULL,                                    \
                                      Aciklama TEXT NOT NULL,                                  \
                                      Tarih TEXT NOT NULL)')
            sorguCreTblCuzdan = (f'CREATE TABLE IF NOT EXISTS {kullaniciadiCuzdan}(cuzdanmiktar)')
            sorguAramaTblCuzdan = (f"SELECT * FROM {kullaniciadiCuzdan} WHERE cuzdanmiktar")
            sorguInsTblCuzdan = (f'INSERT INTO {kullaniciadiCuzdan} VALUES (0)')
            curs.execute(sorguCreTblVeriler)
            curs2.execute(sorguCreTblCuzdan)
            curs2.execute(sorguAramaTblCuzdan)
            cuzdanverisi = curs2.fetchall()
            if len(cuzdanverisi) != 0:
                pass
            else:
                curs2.execute(sorguInsTblCuzdan)
            conn.commit()
            conn2.commit()

            # -------------------KAYDET---------------------#
            # ----------------------------------------------#

            def KAYDET():

                _secenek = ''
                if ui.rdbtnGelir.isChecked():
                    _secenek = 'Gelir'
                elif ui.rdbtnGider.isChecked():
                    _secenek = 'Gider'
                _spinMiktar = ui.spinMiktar.value()
                _lneAciklama = ui.lneAciklama.text()
                _clndrTarih = ui.clndrTarih.selectedDate().toString(QtCore.Qt.ISODate)

                curs.execute(f"INSERT INTO {kullanici_adi}(GelirGider,Miktar,Aciklama,Tarih) VALUES(?,?,?,?)",
                             (_secenek, _spinMiktar, _lneAciklama, _clndrTarih))
                conn.commit()

                if _secenek == "Gelir":
                    curs2.execute(f"SELECT * FROM {kullaniciadiCuzdan}")
                    data = curs2.fetchall()
                    data = data[0][0]
                    data = float(data)
                    data += (_spinMiktar)
                    curs2.execute(f"DELETE FROM {kullaniciadiCuzdan}")
                    curs2.execute(f"REPLACE INTO {kullaniciadiCuzdan}(cuzdanmiktar) VALUES(?)", (data,))
                    conn2.commit()
                elif _secenek == "Gider":
                    curs2.execute(f"SELECT * FROM {kullaniciadiCuzdan}")
                    data = curs2.fetchall()
                    data = data[0][0]
                    data = float(data)
                    data -= (_spinMiktar)
                    curs2.execute(f"DELETE FROM {kullaniciadiCuzdan}")
                    curs2.execute(f"REPLACE INTO {kullaniciadiCuzdan}(cuzdanmiktar) VALUES(?)", (data,))
                    conn2.commit()

            # ---------------------LİSTELE----------------------#
            # --------------------------------------------------#

            def LISTELE():

                curs2.execute(f"SELECT * FROM {kullaniciadiCuzdan}")
                deneme = curs2.fetchall()
                deneme = (str(deneme[0][0]) + " TL")
                ui.lblCuzdan.setText(deneme)

                ui.tblVeriler.clear()
                ui.tblVeriler.setHorizontalHeaderLabels(('No', 'Tip', 'Miktar[TL]', 'Açıklama', 'Tarih'))
                ui.tblVeriler.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

                curs.execute(f"SELECT * FROM {kullanici_adi}")
                for satirIndeks, satirVeri in enumerate(curs):
                    for sutunIndeks, sutunVeri in enumerate(satirVeri):
                        ui.tblVeriler.setItem(satirIndeks, sutunIndeks, QTableWidgetItem(str(sutunVeri)))

            LISTELE()

            # ----------------CÜZDAN BELİRLE-----------------#
            # -----------------------------------------------#

            def CUZDANBELIRLE():

                if len(ui.lneCuzdanMiktari.text()) != 0:
                    miktar = ui.lneCuzdanMiktari.text()
                    curs2.execute(f"SELECT * FROM {kullaniciadiCuzdan}")
                    data = curs2.fetchall()
                    if len(data) == 0:
                        curs2.execute(f"INSERT INTO {kullaniciadiCuzdan}(cuzdanmiktar) VALUES(?)", (miktar,))
                        conn2.commit()
                    else:
                        curs2.execute(f"DELETE FROM {kullaniciadiCuzdan}")
                        curs2.execute(f"REPLACE INTO {kullaniciadiCuzdan}(cuzdanmiktar) VALUES(?)", (miktar,))
                        conn2.commit()
                    ui.lblCuzdan.setText(miktar + " TL")
                    ui.lneCuzdanMiktari.clear()
                else:
                    ui.lblUyari.setText("                  Miktar girmediniz!!!")

            # ----------------KAYITLI GİDER EKLE-----------------#
            # ---------------------------------------------------#

            def KAYITLIGIDEREKLE():
                liste = ui.lblCuzdan.text().split(" ")
                anlik = liste[0]
                anlik = float(anlik)
                try:
                    if (ui.listwHazirGiderTipi.currentItem().text())[0] == "1":
                        if anlik < 40:
                            ui.statusbar.showMessage("Cüzdan eksiye düşeceği için bu kayıtlı gider eklenemez!", 10000)
                        else:
                            _secenek = 'Gider'
                            _spinMiktar = "40"
                            _lneAciklama = "Netflix"
                            _clndrTarih = (datetime.now().replace(microsecond=0).isoformat()[0:10])
                            curs.execute(f"INSERT INTO {kullanici_adi}(GelirGider,Miktar,Aciklama,Tarih) VALUES(?,?,?,?)",
                                         (_secenek, _spinMiktar, _lneAciklama, _clndrTarih))
                            conn.commit()
                            curs2.execute(f"SELECT * FROM {kullaniciadiCuzdan}")
                            data = curs2.fetchall()
                            data = data[0][0]
                            data = float(data)
                            data -= (float(_spinMiktar))
                            curs2.execute(f"DELETE FROM {kullaniciadiCuzdan}")
                            curs2.execute(f"REPLACE INTO {kullaniciadiCuzdan}(cuzdanmiktar) VALUES(?)", (data,))
                            conn2.commit()
                            LISTELE()
                    elif (ui.listwHazirGiderTipi.currentItem().text())[0] == "2":
                        if anlik < 4.5:
                            ui.statusbar.showMessage("Cüzdan eksiye düşeceği için bu kayıtlı gider eklenemez!", 10000)
                        else:
                            _secenek = 'Gider'
                            _spinMiktar = "4.5"
                            _lneAciklama = "Spotify"
                            _clndrTarih = (datetime.now().replace(microsecond=0).isoformat()[0:10])
                            curs.execute(f"INSERT INTO {kullanici_adi}(GelirGider,Miktar,Aciklama,Tarih) VALUES(?,?,?,?)",
                                         (_secenek, _spinMiktar, _lneAciklama, _clndrTarih))
                            conn.commit()
                            curs2.execute(f"SELECT * FROM {kullaniciadiCuzdan}")
                            data = curs2.fetchall()
                            data = data[0][0]
                            data = float(data)
                            data -= (float(_spinMiktar))
                            curs2.execute(f"DELETE FROM {kullaniciadiCuzdan}")
                            curs2.execute(f"REPLACE INTO {kullaniciadiCuzdan}(cuzdanmiktar) VALUES(?)", (data,))
                            conn2.commit()
                            LISTELE()
                    elif (ui.listwHazirGiderTipi.currentItem().text())[0] == "3":
                        if anlik < 16:
                            ui.statusbar.showMessage("Cüzdan eksiye düşeceği için bu kayıtlı gider eklenemez!", 10000)
                        else:
                            _secenek = 'Gider'
                            _spinMiktar = "16"
                            _lneAciklama = "Youtube"
                            _clndrTarih = (datetime.now().replace(microsecond=0).isoformat()[0:10])
                            curs.execute(f"INSERT INTO {kullanici_adi}(GelirGider,Miktar,Aciklama,Tarih) VALUES(?,?,?,?)",
                                         (_secenek, _spinMiktar, _lneAciklama, _clndrTarih))
                            conn.commit()
                            curs2.execute(f"SELECT * FROM {kullaniciadiCuzdan}")
                            data = curs2.fetchall()
                            data = data[0][0]
                            data = float(data)
                            data -= (float(_spinMiktar))
                            curs2.execute(f"DELETE FROM {kullaniciadiCuzdan}")
                            curs2.execute(f"REPLACE INTO {kullaniciadiCuzdan}(cuzdanmiktar) VALUES(?)", (data,))
                            conn2.commit()
                            LISTELE()
                except AttributeError:
                    ui.statusbar.showMessage("Önce seçim yapmanız gerekmektedir...", 10000)

            # ----------------ÇIKIŞ-----------------#
            # --------------------------------------#

            def CIKIS():
                cevap = QMessageBox.question(penAna, "ÇIKIŞ", "Programdan çıkmak istediğinize emin misiniz?", \
                                             QMessageBox.Yes | QMessageBox.No)
                if cevap == QMessageBox.Yes:
                    conn.close()
                    sys.exit(Uygulama.exec_())
                else:
                    penAna.show()

            # ----------------SİL-----------------#
            # ------------------------------------#

            def SİL():
                cevap = QMessageBox.question(penAna, "KAYIT SİL", "Kaydı silmek istediğinize emin misiniz?", \
                                             QMessageBox.Yes | QMessageBox.No)
                if cevap == QMessageBox.Yes:
                    secili = ui.tblVeriler.selectedItems()
                    silinecek = secili[0].text()
                    silinecek = str(silinecek)
                    try:
                        curs.execute(f"DELETE FROM {kullanici_adi} WHERE Id = ?", [silinecek, ])
                        conn.commit()
                        LISTELE()
                        ui.statusbar.showMessage("KAYIT SİLME İŞLEMİ BAŞARIYLA GERÇEKLEŞTİ...", 10000)
                    except Exception as Hata:
                        Hata = str(Hata)
                        ui.statusbar.showMessage("Şöyle bir hata ile karşılaşıldı: " + Hata, 10000)
                else:
                    ui.statusbar.showMessage("SİLME İŞLEMİ İPTAL EDİLDİ...", 10000)

            # -------------HAKKINDA---------------#
            # ------------------------------------#

            def HAKKINDA():
                penHakkinda.show()

            # -------------SİNYAL-SLOT---------------#
            # ---------------------------------------#

            ui.btnKaydet.clicked.connect(lambda: KAYDET())
            ui.btnListele.clicked.connect(lambda: LISTELE())
            ui.btnCuzdanBelirle.clicked.connect(lambda: CUZDANBELIRLE())
            ui.btnHazirGiderEkle.clicked.connect(lambda: KAYITLIGIDEREKLE())
            ui.btnCikis.clicked.connect(lambda: CIKIS())
            ui.btnSil.clicked.connect(lambda: SİL())
            ui.menuYardim.triggered.connect(lambda : HAKKINDA())


        else:
            ui2.lblBilgilendirme.setText("            Yanlış kullanıcı adı veya şifre girdiniz!")

    else:
        ui2.lblBilgilendirme.setText("          Maalesef böyle bir kullanıcı bulunamadı.")


#-------------SİNYAL-SLOT---------------#
#---------------------------------------#

ui2.btnKayitOl.clicked.connect(lambda : KAYITOL())
ui2.btnGirisYap.clicked.connect(lambda : GIRISYAP())

sys.exit(Uygulama.exec_())