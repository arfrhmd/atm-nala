from config.database import Database
from config.colors import colors
import locale

db = Database()

def autentikasi(email, pin):
    try:
        # Hubungkan MySQL
        db.connect()
        
        # SQL Query
        sql = 'SELECT user.email, no_rekening, user.is_block ' \
            'FROM rekening, user ' \
            'WHERE rekening.user_id = user.user_id ' \
            'AND user.email = %s'
        val = (email,)
        
        data = db.read('one', sql, val)
        
        if data['email'] == email:
            sql = 'SELECT email, pin ' \
                'FROM rekening, user ' \
                'WHERE rekening.user_id = user.user_id ' \
                'AND email = %s AND pin = %s'
            val = (email,pin,)
            
            data_pin = db.read('one', sql, val)
            
            if data_pin:
                data.update(data_pin)
                
                if data['pin'] == pin:
                    if db.conn.is_connected:
                        db.close()
                    return data
                else:
                    if db.conn.is_connected:
                        db.close()
                    return data
            else:
                if db.conn.is_connected:
                    db.close()
                return data
        else:
            if db.conn.is_connected:
                db.close()
            return False
    except Exception as err:
        if db.conn.is_connected:
            db.close()
        return False


def block_user(email):
    try:
        # Hubungkan MySQL
        db.connect()
        
        # SQL Query - check email
        sql = 'SELECT user_id, email FROM user WHERE email = %s'
        val = (email,)
        data = db.read('one', sql, val)
        
        if data:
            # SQL Query - block user
            sql = 'UPDATE user ' \
                'JOIN rekening ON user.user_id = rekening.user_id ' \
                'SET is_block = 1 ' \
                'WHERE rekening.user_id = %s'
            val = (data['user_id'],)
            db.update(sql, val)
            
            db.close()
            return True
        else:
            db.close()
            return False
    except:
        db.close()
        return False


def check_balance(no_rekening, show=False):
    # Hubungkan MySQL
    db.connect()
    
    # SQL Query
    sql = 'SELECT no_rekening, tipe, saldo ' \
        'FROM rekening ' \
        'WHERE no_rekening = %s'
    val = (no_rekening,)
    
    # Membaca saldo rekening dari {user_id}
    data = db.read('one', sql, val)
    
    # Menutup koneksi
    db.close()
    
    if show:
        output = f"{colors.OKBLUE}INFO: Saldo Anda saat ini adalah " \
            f"{colors.OKCYAN}{to_rupiah(data['saldo'])}{colors.ENDC}"
            
        return output
    else:
        return data


def change_pin(no_rekening, pin_baru, nama_ibu):
    try:
        # Hubungkan MySQL
        db.connect()
        
        # SQL Query
        sql = 'SELECT user.nm_ibu ' \
            'FROM rekening, user ' \
            'WHERE rekening.user_id = user.user_id ' \
            'AND rekening.no_rekening = %s ' \
            'AND user.nm_ibu = %s'
        val = (no_rekening, nama_ibu)
        
        # Read data
        data = db.read('one', sql, val)
        
        # Validasi nama ibu
        if data['nm_ibu'] == nama_ibu:
            # SQL Query
            sql = 'UPDATE rekening SET pin=%s WHERE no_rekening=%s'
            val = (pin_baru, no_rekening)
            
            # Update data
            db.update(sql, val)
            
            # Tutup koneksi
            db.close()
            return True
        else:
            # Tutup koneksi
            db.close()
            return False
    except Exception as err:
        if db.conn.is_connected:
            db.close()
        return False
    
    
def to_rupiah(saldo_decimal):
    locale.setlocale(locale.LC_ALL, 'id_ID')

    # Menggunakan fungsi locale.format_string() untuk mengubah nilai menjadi format rupiah
    saldo_rupiah = locale.format_string("%.2f", saldo_decimal, grouping=True)
    
    return "Rp " + saldo_rupiah