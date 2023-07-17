from config.database import Database
from config.colors import colors
from app.rekening import check_balance, to_rupiah
from datetime import datetime

db = Database()

def deposit(no_rekening, saldo_deposit):
    # Hubungkan MySQL
    db.connect()
    
    try :
        if saldo_deposit < 10000:
            output = f"{colors.WARNING}WARN: Jumlah deposit Anda kurang dari batas minimum.\n"
            output += f"WARN: Batas minimum deposit sebesar {to_rupiah(10000)}{colors.ENDC}"
            
            return output
        else:
            # Mulai transaksi MySQL
            db.conn.start_transaction()
            
            # Baca saldo saat ini
            data = check_balance(no_rekening)
            
            # print(data)
            
            # Jumlahkan dengan saldo deposit
            saldo = data['saldo'] + saldo_deposit
            
            # Tambah saldo ke database
            sql = 'UPDATE rekening SET saldo=%s WHERE no_rekening=%s'
            val = (saldo, no_rekening)
            
            db.update(sql, val)
            
            # Buat data transaksi
            tipe = 'Setor Tunai'
            created_at = datetime.now()
            
            # Tambah data transaksi
            sql = 'INSERT INTO transaksi (rek_pengirim, tipe, saldo, created_at) ' \
                'VALUES (%s, %s, %s, %s)'
            val = (no_rekening, tipe, saldo_deposit, created_at)
            
            db.update(sql, val)
            
            # Tutup koneksi
            db.close()
            
            output = f"{colors.OKBLUE}INFO: Berhasil melakukan setor tunai " \
                f"sebesar {colors.OKCYAN}{to_rupiah(saldo_deposit)}\n"
            output += check_balance(no_rekening, show=True)
            
            return output
    except Exception as err:
        # Membatalkan transaksi
        db.conn.rollback()
        # Tutup koneksi
        if db.conn.is_connected:
            db.close()
        return f"{colors.FAIL}ERROR: {err}{colors.ENDC}"
        
        
def withdraw(no_rekening, saldo_penarikan):
    # Hubungkan MySQL
    db.connect()
    
    try :
        # Mulai transaksi MySQL
        db.conn.start_transaction()
        
        # Baca saldo saat ini
        data = check_balance(no_rekening)
        
        # Jika saldo tidak mencukupi
        if saldo_penarikan > data['saldo']:
            output = f"{colors.FAIL}ERROR: Maaf, saldo Anda tidak mencukupi.\n"
            output += check_balance(no_rekening, show=True)
            
            # Tutup koneksi
            db.close()
            
            return output
        else:
            # Tambah saldo ke database
            sql = 'UPDATE rekening SET saldo=%s WHERE no_rekening=%s'
            val = ((data['saldo'] - saldo_penarikan), no_rekening)
            
            db.update(sql, val)
            
            # Buat data transaksi
            tipe = 'Tarik Tunai'
            created_at = datetime.now()
            
            # Tambah data transaksi
            sql = 'INSERT INTO transaksi (rek_pengirim, tipe, saldo, created_at) ' \
                'VALUES (%s, %s, %s, %s)'
            val = (no_rekening, tipe, saldo_penarikan, created_at)
            
            db.insert(sql, val)
            
            output = f"{colors.OKBLUE}INFO: Anda telah menarik tunai " \
                f"sebesar {colors.OKCYAN}{to_rupiah(saldo_penarikan)}\n"
            output += check_balance(no_rekening, show=True)
            
            # Tutup koneksi
            if db.conn.is_connected:
                db.close()
            
            return output
    except Exception as err:
        # Membatalkan transaksi
        db.conn.rollback()
        # Tutup koneksi
        if db.conn.is_connected:
            db.close()
        return f"{colors.FAIL}ERROR: {err}{colors.ENDC}"
    
    
def transfer(rek_pengirim, rek_penerima, saldo_transfer):
    # Hubungkan MySQL
    db.connect()
    
    try:
        # Memulai transaksi
        db.conn.start_transaction()
        
        sql = 'SELECT pengirim.saldo AS saldo_pengirim, penerima.saldo AS saldo_penerima ' \
            'FROM rekening ' \
            'JOIN rekening pengirim ON pengirim.no_rekening = %s ' \
            'JOIN rekening penerima ON penerima.no_rekening = %s ' \
            'LIMIT 0,1'
        val = (rek_pengirim, rek_penerima)
        
        data = db.read('one', sql, val)
        saldo_pengirim = data['saldo_pengirim']
        saldo_penerima = data['saldo_penerima']
        
        # Cek saldo pengirim
        if saldo_transfer > saldo_pengirim:
            output = f"{colors.FAIL}ERROR: Maaf, saldo Anda tidak mencukupi.\n"
            output += check_balance(rek_pengirim, show=True)
            
            # Tutup koneksi
            db.close()
            return output
        else:            
            # Update data rekening pengirim
            sql = 'UPDATE rekening SET saldo=%s WHERE no_rekening=%s'
            val = ((saldo_pengirim - saldo_transfer), rek_pengirim)
            
            db.update(sql, val)
            
            # Update data rekening penerima
            sql = 'UPDATE rekening SET saldo=%s WHERE no_rekening=%s'
            val = ((saldo_penerima + saldo_transfer), rek_penerima)
            
            db.update(sql, val)
            
            # Buat data transaksi
            tipe = 'Transfer'
            created_at = datetime.now()
            
            # Tambah data transaksi
            sql = 'INSERT INTO transaksi (rek_pengirim, rek_penerima, tipe, saldo, created_at) ' \
                'VALUES (%s, %s, %s, %s, %s)'
            val = (rek_pengirim, rek_penerima, tipe, saldo_transfer, created_at)
            
            db.insert(sql, val)
            
            output = f"{colors.OKBLUE}INFO: Berhasil melakukan transfer ke {colors.OKCYAN}{rek_penerima}{colors.OKBLUE} " \
                f"sebesar {colors.OKCYAN}{to_rupiah(saldo_transfer)}\n"
            output += check_balance(rek_pengirim, show=True)
            
            # Tutup koneksi
            if db.conn.is_connected:
                db.close()
            
            return output
    except Exception as err:
        # Membatalkan transaksi
        db.conn.rollback()
        # Tutup koneksi
        if db.conn.is_connected:
            db.close()
        return f"{colors.FAIL}ERROR: {err}{colors.ENDC}"