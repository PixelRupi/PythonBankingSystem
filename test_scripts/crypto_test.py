import hashlib


wynikOperacjiSHA = "55944d9ae9e4d756a6eef6f0035ebb176aa46e7cd84c4e9be4ce3a4f06043b5f"
daneDoWeryfikacji = "testowy string"

#hash_object = hashlib.sha256(daneDoWeryfikacji.encode('utf-8'))  
#hex_dig = hash_object.hexdigest()
#print(f"Hashed String: {hex_dig}")


# porownywanie:
if wynikOperacjiSHA == hashlib.sha256(daneDoWeryfikacji.encode('utf-8')).hexdigest():
    print("success")
else:
    print("failure")