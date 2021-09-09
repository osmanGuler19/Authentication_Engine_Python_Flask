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


def getSharedPreferencesAllData():
    f = open("sharedPreferences.bin","rb")
    fernet = Fernet(getKey())
    encrypted = f.read()
    decreypted = fernet.decrypt(encrypted)
    decreyptedToString = decreypted.decode('UTF-8')
    f.close
    return decreyptedToString

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
    indexOfEndOfLine = subStr.find(';') #Gets the index of endofline char.
    data = subStr[:indexOfEndOfLine]
    
    return "".join(data)
     

def editSharedPreferencesData(key,data):
    f = open("sharedPreferences.bin","rb")
    fernet = Fernet(getKey())
    #Read the entire encrypted data from file
    encrypted = f.read()
    f.close()
    decreypted = fernet.decrypt(encrypted)
    decreyptedToString = decreypted.decode('UTF-8')

    ##Searching data
    # This is done by index 
    indexOfSearchedItem = decreyptedToString.find(key)
    if indexOfSearchedItem == -1:
        return 'Couldn\'t find'

    lengthOfKey = len(key)
    dataStartingIndex = indexOfSearchedItem+lengthOfKey+1 #starting index of data 
    subStr = decreyptedToString[dataStartingIndex:]
    indexOfEndOfLine = subStr.find(';') #Gets the index of endofline char.
    oldData = subStr[:indexOfEndOfLine]
    c1 = key+':'+oldData+';'
    c2 = key+':'+data+';'
    decreyptedToString = decreyptedToString.replace(c1,c2)

    #decreyptedToString[dataStartingIndex:indexOfEndOfLine] = data
    f = open("sharedPreferences.bin","wb")
    #Byte olarak yeniden yazılıp dosyaya kaydediliyor
    encryptedBinaryData = fernet.encrypt(decreyptedToString.encode('UTF-8'))
    f.write(encryptedBinaryData)
    f.close

def addSharedPreferencesData(key,data):
    f = open("sharedPreferences.bin","rb")
    fernet = Fernet(getKey())
    encrypted = f.read()
    f.close()

    decreypted = fernet.decrypt(encrypted)
    decreyptedToString = decreypted.decode('UTF-8')
    indexOfSearchedItem = decreyptedToString.find(key)
    if indexOfSearchedItem != -1:
        return 'You Cant\'t add already existing key'
    addingStr = key+':'+data+';'
    decreyptedToString+=addingStr
    encryptedBinaryData = fernet.encrypt(decreyptedToString.encode('UTF-8'))
    f = open("sharedPreferences.bin","wb")
    f.write(encryptedBinaryData)
    f.close


def deleteSharedPreferencesData(key):
    f = open("sharedPreferences.bin","rb")
    fernet = Fernet(getKey())
    encrypted = f.read()
    f.close()
    decreypted = fernet.decrypt(encrypted)
    decreyptedToString = decreypted.decode('UTF-8')
    indexOfSearchedItem = decreyptedToString.find(key)
    if indexOfSearchedItem == -1:
        return 'Key doesn\'t exist'
    lengthOfKey = len(key)
    dataStartingIndex = indexOfSearchedItem+lengthOfKey+1 #starting index of data 
    indexOfEndOfLine = decreyptedToString[dataStartingIndex:].find(getEndOfLine()) #Gets the index of endofline char.
    fullLength = indexOfSearchedItem+lengthOfKey+indexOfEndOfLine+2
    deletingData = decreyptedToString[indexOfSearchedItem:fullLength]
    decreyptedToString = decreyptedToString.replace(deletingData,'')
    decreyptedToString = decreyptedToString.replace(" ","") #in case there are some spaces
    encryptedBinaryData = fernet.encrypt(decreyptedToString.encode('UTF-8'))
    f = open("sharedPreferences.bin","wb")
    f.write(encryptedBinaryData)
    f.close
