#-------------------KÜTÜPHANE------------------#
#----------------------------------------------#

import sys
from sqlite3 import Cursor
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from AnaSayfaUI import *
from datetime import datetime

#---------------UYGULAMA OLUSTUR---------------#
#----------------------------------------------#

Uygulama = QApplication(sys.argv)
penAna = QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(penAna)
penAna.show()


#-------------VERİTABANI OLUŞTUR---------------#
#----------------------------------------------#

import sqlite3
global curs
global conn
conn = sqlite3.connect('veritabani.db')
curs = conn.cursor()
conn2 = sqlite3.connect('veritabani.db')
curs2 = conn2.cursor()

sorguCreTblVeriler = ('CREATE TABLE IF NOT EXISTS veriler(                     \
                      Id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,           \
                      GelirGider TEXT NOT NULL,                                \
                      Miktar TEXT NOT NULL,                                    \
                      Aciklama TEXT NOT NULL,                                  \
                      Tarih TEXT NOT NULL)')

sorguCreTblCuzdan = ('CREATE TABLE IF NOT EXISTS cuzdan(cuzdanmiktar)')
curs.execute(sorguCreTblVeriler)
curs2.execute(sorguCreTblCuzdan)
conn.commit()
conn2.commit()
#-------------------KAYDET---------------------#
#----------------------------------------------#

def KAYDET():

    _secenek = ''
    if ui.rdbtnGelir.isChecked():
        _secenek = 'Gelir'
    elif ui.rdbtnGider.isChecked():
        _secenek = 'Gider'
    _spinMiktar = ui.spinMiktar.value()
    _lneAciklama = ui.lneAciklama.text()
    _clndrTarih = ui.clndrTarih.selectedDate().toString(QtCore.Qt.ISODate)

    curs.execute("INSERT INTO veriler(GelirGider,Miktar,Aciklama,Tarih) VALUES(?,?,?,?)",(_secenek,_spinMiktar,_lneAciklama,_clndrTarih))
    conn.commit()

    if _secenek == "Gelir":
        curs2.execute("SELECT * FROM cuzdan")
        data = curs2.fetchall()
        data = data[0][0]
        data = float(data)
        data += (_spinMiktar)
        curs2.execute("DELETE FROM cuzdan")
        curs2.execute("REPLACE INTO cuzdan(cuzdanmiktar) VALUES(?)", (data,))
        conn2.commit()
    elif _secenek == "Gider":
        curs2.execute("SELECT * FROM cuzdan")
        data = curs2.fetchall()
        data = data[0][0]
        data = float(data)
        data -= (_spinMiktar)
        curs2.execute("DELETE FROM cuzdan")
        curs2.execute("REPLACE INTO cuzdan(cuzdanmiktar) VALUES(?)", (data,))
        conn2.commit()

#---------------------SİL----------------------#
#----------------------------------------------#

def LISTELE():

    curs2.execute("SELECT * FROM cuzdan")
    deneme = curs2.fetchall()
    deneme = (str(deneme[0][0]) + " TL")
    ui.lblCuzdan.setText(deneme)

    ui.tblVeriler.clear()
    ui.tblVeriler.setHorizontalHeaderLabels(('No','Tip','Miktar[TL]','Açıklama','Tarih'))
    ui.tblVeriler.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    curs.execute("SELECT * FROM veriler")
    for satirIndeks,satirVeri in enumerate(curs):
        for  sutunIndeks,sutunVeri in enumerate (satirVeri):
            ui.tblVeriler.setItem(satirIndeks,sutunIndeks,QTableWidgetItem(str(sutunVeri)))

LISTELE()

#----------------CÜZDAN BELİRLE-----------------#
#-----------------------------------------------#

def CUZDANBELIRLE():

    if len(ui.lneCuzdanMiktari.text()) != 0:
        miktar = ui.lneCuzdanMiktari.text()
        curs2.execute("SELECT * FROM cuzdan")
        data = curs2.fetchall()
        if len(data) == 0:
            curs2.execute("INSERT INTO cuzdan(cuzdanmiktar) VALUES(?)",(miktar,))
            conn2.commit()
        else:
            curs2.execute("DELETE FROM cuzdan")
            curs2.execute("REPLACE INTO cuzdan(cuzdanmiktar) VALUES(?)",(miktar,))
            conn2.commit()
        ui.lblCuzdan.setText(miktar + " TL")
    else:
        ui.lblUyari.setText("                  Miktar girmediniz!!!")

#----------------KAYITLI GİDER EKLE-----------------#
#---------------------------------------------------#

def KAYITLIGIDEREKLE():
    liste = ui.lblCuzdan.text().split(" ")
    anlik = liste[0]
    anlik = float(anlik)
    try:
        if (ui.listwHazirGiderTipi.currentItem().text())[0] == "1":
            if anlik < 40:
                ui.statusbar.showMessage("Cüzdan eksiye düşeceği için bu kayıtlı gider eklenemez!",10000)
            else:
                _secenek = 'Gider'
                _spinMiktar = "40"
                _lneAciklama = "Netflix"
                _clndrTarih = (datetime.now().replace(microsecond=0).isoformat()[0:10])
                curs.execute("INSERT INTO veriler(GelirGider,Miktar,Aciklama,Tarih) VALUES(?,?,?,?)",
                             (_secenek, _spinMiktar, _lneAciklama, _clndrTarih))
                conn.commit()
                curs2.execute("SELECT * FROM cuzdan")
                data = curs2.fetchall()
                data = data[0][0]
                data = float(data)
                data -= (float(_spinMiktar))
                curs2.execute("DELETE FROM cuzdan")
                curs2.execute("REPLACE INTO cuzdan(cuzdanmiktar) VALUES(?)", (data,))
                conn2.commit()
                LISTELE()
        elif (ui.listwHazirGiderTipi.currentItem().text())[0] == "2":
            if anlik < 4.5:
                ui.statusbar.showMessage("Cüzdan eksiye düşeceği için bu kayıtlı gider eklenemez!",10000)
            else:
                _secenek = 'Gider'
                _spinMiktar = "4.5"
                _lneAciklama = "Spotify"
                _clndrTarih = (datetime.now().replace(microsecond=0).isoformat()[0:10])
                curs.execute("INSERT INTO veriler(GelirGider,Miktar,Aciklama,Tarih) VALUES(?,?,?,?)",
                             (_secenek, _spinMiktar, _lneAciklama, _clndrTarih))
                conn.commit()
                curs2.execute("SELECT * FROM cuzdan")
                data = curs2.fetchall()
                data = data[0][0]
                data = float(data)
                data -= (float(_spinMiktar))
                curs2.execute("DELETE FROM cuzdan")
                curs2.execute("REPLACE INTO cuzdan(cuzdanmiktar) VALUES(?)", (data,))
                conn2.commit()
                LISTELE()
        elif (ui.listwHazirGiderTipi.currentItem().text())[0] == "3":
            if anlik < 16:
                ui.statusbar.showMessage("Cüzdan eksiye düşeceği için bu kayıtlı gider eklenemez!",10000)
            else:
                _secenek = 'Gider'
                _spinMiktar = "16"
                _lneAciklama = "Youtube"
                _clndrTarih = (datetime.now().replace(microsecond=0).isoformat()[0:10])
                curs.execute("INSERT INTO veriler(GelirGider,Miktar,Aciklama,Tarih) VALUES(?,?,?,?)",
                             (_secenek, _spinMiktar, _lneAciklama, _clndrTarih))
                conn.commit()
                curs2.execute("SELECT * FROM cuzdan")
                data = curs2.fetchall()
                data = data[0][0]
                data = float(data)
                data -= (float(_spinMiktar))
                curs2.execute("DELETE FROM cuzdan")
                curs2.execute("REPLACE INTO cuzdan(cuzdanmiktar) VALUES(?)", (data,))
                conn2.commit()
                LISTELE()
    except AttributeError:
        ui.statusbar.showMessage("Önce seçim yapmanız gerekmektedir...",10000)
#----------------ÇIKIŞ-----------------#
#--------------------------------------#

def CIKIS():
    cevap = QMessageBox.question(penAna,"ÇIKIŞ","Programdan çıkmak istediğinize emin misiniz?",\
                                 QMessageBox.Yes  | QMessageBox.No)
    if cevap == QMessageBox.Yes:
        conn.close()
        sys.exit(Uygulama.exec_())
    else:
        penAna.show()

#----------------SİL-----------------#
#------------------------------------#

def SİL():
    cevap = QMessageBox.question(penAna, "KAYIT SİL", "Kaydı silmek istediğinize emin misiniz?",\
                                 QMessageBox.Yes | QMessageBox.No)
    if cevap == QMessageBox.Yes:
        secili = ui.tblVeriler.selectedItems()
        silinecek = secili[0].text()
        silinecek = str(silinecek)
        try:
            curs.execute("DELETE FROM veriler WHERE Id = ?",silinecek)
            conn.commit()
            LISTELE()
            ui.statusbar.showMessage("KAYIT SİLME İŞLEMİ BAŞARIYLA GERÇEKLEŞTİ...",10000)
        except Exception as Hata:
            Hata = str(Hata)
            ui.statusbar.showMessage("Şöyle bir hata ile karşılaşıldı: "+Hata,10000)
    else:
        ui.statusbar.showMessage("SİLME İŞLEMİ İPTAL EDİLDİ...", 10000)


#-------------SİNYAL-SLOT---------------#
#---------------------------------------#

ui.btnKaydet.clicked.connect(lambda: KAYDET())
ui.btnListele.clicked.connect(lambda : LISTELE())
ui.btnCuzdanBelirle.clicked.connect(lambda : CUZDANBELIRLE())
ui.btnHazirGiderEkle.clicked.connect(lambda : KAYITLIGIDEREKLE())
ui.btnCikis.clicked.connect(lambda : CIKIS())
ui.btnSil.clicked.connect(lambda : SİL())

sys.exit(Uygulama.exec_())