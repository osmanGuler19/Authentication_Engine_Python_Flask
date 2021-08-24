from cryptography.fernet import Fernet
import keyring

def createKey():
    # key generation
    key = Fernet.generate_key()
    keyring.set_password("authenticationEngine", "secret_for_first_time", key.decode('UTF-8'))


def getKey():
    return keyring.get_password("authenticationEngine", "secret_for_first_time")



def getEndOfLine():
    return ";"


def createSharedPreferencesFile():
    fernet = Fernet(getKey())
    isFirstOpen = 'isFirstOpen:True'+getEndOfLine()
    isFirstOpenToBinary = isFirstOpen.encode('UTF-8')
    encrypted = fernet.encrypt(isFirstOpenToBinary)
    f = open("sharedPreferences.bin", "wb")
    f.write(encrypted)
    f.close

def getSharedPreferencesData(key):
    f = open("sharedPreferences.bin","rb")
    fernet = Fernet(getKey())
    encrypted = f.read()
    decreypted = fernet.decrypt(encrypted)
    decreyptedToString = decreypted.decode('UTF-8')
    f.close

    ##Searching data
    # This is done by index 
    indexOfSearchedItem = decreyptedToString.find(key)
    if indexOfSearchedItem == -1:
        return 'Couldn\'t find'

    lengthOfKey = len(key)
    dataStartingIndex = indexOfSearchedItem+lengthOfKey+1 #starting index of data 
    subStr = decreyptedToString[dataStartingIndex:]
    indexOfEndOfLine = subStr.find(getEndOfLine()) #Gets the index of endofline char.
    data = subStr[:indexOfEndOfLine]
    
    return data

def editSharedPreferencesData(key,data):
    f = open("sharedPreferences.bin","wrb")
    fernet = Fernet(getKey())
    #Read the entire encrypted data from file
    encrypted = f.read()
    decreypted = fernet.decrypt(encrypted)
    decreyptedToString = decreypted.decode('UTF-8')

    ##Searching data
    # This is done by index 
    indexOfSearchedItem = decreyptedToString.find(key)
    if indexOfSearchedItem == -1:
        return 'Couldn\'t find'

    lengthOfKey = len(key)
    dataStartingIndex = indexOfSearchedItem+lengthOfKey+1 #starting index of data 
    indexOfEndOfLine = decreyptedToString[dataStartingIndex:].find(getEndOfLine()) #Gets the index of endofline char.
    decreyptedToString[dataStartingIndex:indexOfEndOfLine] = data

    #Byte olarak yeniden yazılıp dosyaya kaydediliyor
    encryptedBinaryData = fernet.encrypt(decreyptedToString.encode('UTF-8'))
    f.write(encryptedBinaryData)
    f.close

def addSharedPreferencesData(key,data):
    f = open("sharedPreferences.bin","wrb")
    fernet = Fernet(getKey())
    encrypted = f.read()
    decreypted = fernet.decrypt(encrypted)
    decreyptedToString = decreypted.decode('UTF-8')
    indexOfSearchedItem = decreyptedToString.find(key)
    if indexOfSearchedItem != -1:
        return 'You Cant\'t add already existing key'
    addingStr = key+':'+data+getEndOfLine()
    decreyptedToString+=addingStr
    encryptedBinaryData = fernet.encrypt(decreyptedToString.encode('UTF-8'))
    f.write(encryptedBinaryData)
    f.close


def deleteSharedPreferencesData(key,data):
    f = open("sharedPreferences.bin","wrb")
    fernet = Fernet(getKey())
    encrypted = f.read()
    decreypted = fernet.decrypt(encrypted)
    decreyptedToString = decreypted.decode('UTF-8')
    indexOfSearchedItem = decreyptedToString.find(key)
    if indexOfSearchedItem == -1:
        return 'Key doesn\'t exist'
    lengthOfKey = len(key)
    dataStartingIndex = indexOfSearchedItem+lengthOfKey+1 #starting index of data 
    indexOfEndOfLine = decreyptedToString[dataStartingIndex:].find(getEndOfLine()) #Gets the index of endofline char.
    decreyptedToString[indexOfSearchedItem:indexOfEndOfLine] = ""
    decreyptedToString = decreyptedToString.replace(" ","") #in case there are some spaces
    encryptedBinaryData = fernet.encrypt(decreyptedToString.encode('UTF-8'))
    f.write(encryptedBinaryData)
    f.close


#Yukarıdaki createSharedPreferences fonksiyonu ile aynı şeyi yapıyor aslında
'''def encryptFile(filename, key):
    
    f = Fernet(key)
    with open(filename, "rb") as file:
        # read all file data
        file_data = file.read()
    
    encrypted_data = f.encrypt(file_data)
    with open(filename, "wb") as file:
        file.write(encrypted_data)'''