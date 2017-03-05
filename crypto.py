import os, random
from Crypto.Cipher import AES
from Crypto.Hash import SHA256

# Make it do something when user inputs wrong pass 


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
ALL = EXTENSIONS.get("OFFICE")+EXTENSIONS.get("IMAGE")+EXTENSIONS.get("AUDIO")+EXTENSIONS.get("VIDEO")
OFFICE = EXTENSIONS.get("OFFICE")
IMAGE = EXTENSIONS.get("IMAGE")
AUDIO = EXTENSIONS.get("AUDIO")
VIDEO = EXTENSIONS.get("VIDEO")

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

def encrypt_all(key, directory, file_type):
    sub_directories = [x[0] for x in os.walk(directory)]

    for sub_directory in sub_directories:
        files = os.walk(sub_directory).next()[2]
        if (len(files) > 0):
            for file in files:
                for extension in file_type:
                    if file.endswith(extension):
                        path = sub_directory + "/"
                        encrypt(get_key(key), path, file)
                    else:
                        pass

def decrypt_all(key, directory, file_type):
    sub_directories = [x[0] for x in os.walk(directory)]

    for sub_directory in sub_directories:
        files = os.walk(sub_directory).next()[2]
        if (len(files) > 0):
            for file in files:
                for extension in file_type:
                    if file.endswith(extension):
                        path = sub_directory + "/"
                        decrypt(get_key(key), path, file)
                    else:
                        pass

def get_file_type(user_input):
    option = int(user_input)
    file_type = None

    if option is 0:
        file_type = ALL
    elif option is 1:
        file_type = OFFICE
    elif option is 2:
        file_type = IMAGE
    elif option is 3:
        file_type = AUDIO
    elif option is 4:
        file_type = VIDEO
    else:
        print "[-] Error: Input value is not correct"

    return file_type

def Main():

    choice = raw_input("Do you want to (E)ncrypt or (D)ecrypt?: ")
    if choice is "E" or choice is "e" or choice is "D" or choice is "d":
        password = raw_input("Password: ")
        directory = raw_input("Directory: ")
        option = raw_input("""
    [0] All
    [1] Office
    [2] Image
    [3] Audio
    [4] Video

File type: """)

        try:
            if choice is "E" or choice is "e":
                encrypt_all(get_key(password), directory, get_file_type(option))
                print "[+] Encryption completed"

            elif choice is "D" or choice is "d":
                decrypt_all(get_key(password), directory, get_file_type(option))
                print "[+] Decryption completed"
        except:
            print "[-] Cannot find directory path: "+str(directory)

    else:
        print "[-] Wrong option"


if __name__ == '__main__':
    Main()
