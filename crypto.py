import os, random
from Crypto.Cipher import AES
from Crypto.Hash import SHA256

def encrypt(key, filename):
    chunksize = 64*1024
    outputFile = "(encryted)"+filename
    filesize = str(os.path.getsize(filename)).zfill(16)
    IV = ''

    for i in range(16):
        IV += chr(random.randint(0, 0xFF))

    encryptor = AES.new(key, AES.MODE_CBC, IV)

    with open(filename, 'rb') as infile:
        with open(outputFile, 'wb') as outfile:
            outfile.write(filesize)
            outfile.write(IV)

            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += ' ' * (16 - (len(chunk) % 16))
                    os.remove(filename)
                    outfile.write(encryptor.encrypt(chunk))

def decrypt(key, filename):
    chunksize = 64*1024
    outputFile = filename[10:]

    with open(filename, 'rb') as infile:
        filesize = long(infile.read(16))
        IV = infile.read(16)

        decryptor = AES.new(key, AES.MODE_CBC, IV)

        with open(outputFile, 'wb') as outfile:
            while True:
                chunk = infile.read(chunksize)

                if len(chunk) == 0:
                    break
                else:
                    os.remove(filename)
                    outfile.write(decryptor.decrypt(chunk))
                    outfile.truncate(filesize)

def get_key(password):
    hasher = SHA256.new(password)
    return hasher.digest()


def Main():
    choice = raw_input("Do you want to (E)ncrypt or (D)ecrypt?: ")

    if choice == 'E' or choice == 'e':
        filename = raw_input("File to encrypt: ")
        password = raw_input("Password: ")
        try:
            encrypt(get_key(password), filename)
            print "... File encrypted"
        except:
            print "... Input file does not exist"
    elif choice == 'D' or choice == 'e':
        try:
            filename = raw_input("File to decrypt: ")
            password = raw_input("Password: ")
            decrypt(get_key(password), filename)
            print "... File decrypted"
        except:
            print "... Input file does not exist"
    else:
        print "No option selected, closing..."

if __name__ == '__main__':
    Main()
