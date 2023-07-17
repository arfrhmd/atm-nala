 #!/usr/bin/env python

from config.colors import colors

import app.rekening as rekening
import app.transaksi as transaksi
import os
import time

def banner(): 
    banner = """
   _   _   ___   _       ___   ______  ___   _   _  _   __
  | \ | | / _ \ | |     / _ \  | ___ \/ _ \ | \ | || | / /
  |  \| |/ /_\ \| |    / /_\ \ | |_/ / /_\ \|  \| || |/ / 
  | . ` ||  _  || |    |  _  | | ___ \  _  || . ` ||    \ 
  | |\  || | | || |____| | | | | |_/ / | | || |\  || |\  \\
  \_| \_/\_| |_/\_____/\_| |_/ \____/\_| |_/\_| \_/\_| \_/
                                                        
              NALA Bank - Your Saving Solution                   
    """
    
    print(banner)

def menu():
    try_again = 'y'
    
    while try_again.lower() == 'y':
        os.system("cls")
        banner()
        print("Menu ATM: ")
        print()
        print("1. Cek Saldo\t\t4. Transfer")
        print("2. Setor Tunai\t\t5. Ubah PIN")
        print("3. Tarik Tunai\t\t6. Keluar")
        print()
        option = int(input("Silakan pilih opsi: "))
        print()

        if option == 1:
            data_rek = rekening.check_balance(data['no_rekening'])
            print(f"{colors.OKBLUE}INFO: Nomor rekening Anda adalah {colors.OKCYAN}{data_rek['no_rekening']}")
            print(f"{colors.OKBLUE}INFO: Tipe rekening Anda adalah {colors.OKCYAN}{data_rek['tipe']}")
            print(f"{colors.OKBLUE}INFO: Saldo rekening Anda sebesar {colors.OKCYAN}{rekening.to_rupiah(data_rek['saldo'])}")
            print(colors.ENDC)
            try_again = input("Apakah Anda ingin menggunakannya lagi? [y/n] ")
        elif option == 2:
            saldo = int(input("Masukkan jumlah deposit: "))
            print()
            print(transaksi.deposit(data['no_rekening'], saldo))
            print()
            try_again = input("Apakah Anda ingin menggunakannya lagi? [y/n] ")
        elif option == 3:
            saldo = int(input("Masukkan jumlah tarik tunai: "))
            print()
            print(transaksi.withdraw(data['no_rekening'], saldo))
            print()
            try_again = input("Apakah Anda ingin menggunakannya lagi? [y/n] ")
        elif option == 4:
            saldo = int(input("Masukkan jumlah transfer: "))
            rek_penerima = int(input("Masukkan no. rekening tujuan: "))
            print()
            print(transaksi.transfer(data['no_rekening'], rek_penerima, saldo))
            print()
            try_again = input("Apakah Anda ingin menggunakannya lagi? [y/n] ")
        elif option == 5:
            new_pin = input("Masukkan PIN baru : ")
            nama_ibu = input("Masukkan nama ibu kandung : ")
            
            if len(new_pin) == 6:
                change = rekening.change_pin(data['no_rekening'], new_pin, nama_ibu.upper())
            else:
                change = f"{colors.FAIL}ERROR: PIN harus berjumlah 6 angka{colors.ENDC}"
            
            if change and not isinstance(change, str):
                print(f"\n{colors.OKBLUE}INFO: PIN telah berhasil diubah{colors.ENDC}")
                print()
                time.sleep(2)
                try_again = input("Apakah Anda ingin menggunakannya lagi? [y/n] ")
            else:
                print()
                print(f"{colors.FAIL}ERROR: Data yang Anda masukkan salah{colors.ENDC}")
                if isinstance(change, str):
                    print(change)
                # print(f"{colors.OKBLUE}INFO: Anda akan dikeluarkan dari aplikasi{colors.ENDC}")
                time.sleep(2)
                print()
                try_again = input("Apakah Anda ingin menggunakannya lagi? [y/n] ")
        elif option == 6:
            print("\nTerima kasih telah menggunakan ATM NALA")
            exit()
        else:
            print(f"\n{colors.FAIL}ERROR: Opsi yang Anda masukkan tidak valid. Silakan coba lagi.{colors.ENDC}")
    
    print("\nTerima kasih telah menggunakan ATM NALA")


if __name__ == "__main__":
    pin_attempts = 3
    data = None

    while pin_attempts:
        os.system("cls")
        banner()
        email = input("Masukkan email\t: ")
        pin = input("Masukkan PIN\t: ")
        print()
        data = rekening.autentikasi(email, pin)
        # print(data)
        if data:
            if 'pin' in data and not data['is_block']:
                pin_attempts = 0
                print(f"{colors.OKBLUE}INFO: Anda akan dialihkan ke menu dalam waktu 2 detik{colors.ENDC}")
                time.sleep(2)
                menu()
            elif data['is_block']:
                print(f"{colors.WARNING}WARN: Akun telah diblokir oleh sistem")
                print(f"{colors.OKBLUE}INFO: Harap hubungi CS untuk aktivasi kembali{colors.ENDC}")
                exit()
            else:
                print(f"{colors.FAIL}ERROR: Data tidak ditemukan")
                pin_attempts -= 1
                print(f"{colors.OKBLUE}INFO: Batas memasukkan akun tersisa {colors.FAIL}{pin_attempts}{colors.ENDC}")
                time.sleep(3)
                if pin_attempts < 1:
                    rekening.block_user(email)
                    print(f"{colors.WARNING}WARN: Anda salah memasukkan data 3x berturut-turut")
                    print(f"{colors.WARNING}WARN: Akun {colors.OKCYAN}{email}{colors.WARNING} telah diblokir oleh sistem")
                    print(f"{colors.OKBLUE}INFO: Harap hubungi CS untuk aktivasi kembali{colors.ENDC}")
        else:
            print(f"{colors.FAIL}ERROR: Data tidak ditemukan")
            pin_attempts -= 1
            print(f"{colors.OKBLUE}INFO: Batas memasukkan akun tersisa {colors.FAIL}{pin_attempts}{colors.ENDC}")
            time.sleep(3)
            if pin_attempts < 1:
                block = rekening.block_user(email)
                if block:
                    print(f"{colors.WARNING}WARN: Anda salah memasukkan data 3x berturut-turut")
                    print(f"{colors.WARNING}WARN: Akun {colors.OKCYAN}{email}{colors.WARNING} telah diblokir oleh sistem")
                    print(f"{colors.OKBLUE}INFO: Harap hubungi CS untuk aktivasi kembali{colors.ENDC}")