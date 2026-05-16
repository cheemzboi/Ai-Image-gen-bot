from gen import Key
import re
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("desidiffusionbot-firebase-adminsdk-j84hf-a4c27fab37.json")
firebase_admin.initialize_app(cred,{'databaseURL':'https://desidiffusionbot-default-rtdb.asia-southeast1.firebasedatabase.app/'})


ref = db.reference("/")
ref.get()
key_ref = ref.child('codes')
print(ref.get())


def keymaker(hrstoadd):
    
    # hrstoadd=(input("Enter hours to add:"))
    p=Key()
    print(p)
    p=str(p)
    p=p.split(':')[0]
    new_key = str(p)
    new_value = hrstoadd

    key_ref.update({new_key: new_value})
    return str(p)
# def codedel(codetodel):
#     key_to_delete = codetodel
#     code_node_ref = ref.child("codes")

#     # Use the delete method to delete the specific key within the "code" node
#     code_node_ref.child(key_to_delete).delete()

    # print(f'Key "{key_to_delete}" deleted successfully.')


def keychecker(keytocheck=str):
    #keytocheck=(input("Enter Your Key :"))  
    p=Key(key=keytocheck)
    
    
    #m=p.verify(keytocheck)
    if 'Valid' in str(p):
        p=str(p)
        p=p.split(':')[0]
        hr=key_ref.child(p).get()
        
        # print("HRSTOADD:\n"+str(hr))
        # print('Found it!')
        return hr 
    else:
        return False
    
    
    
###############################################  OLD CODE ####################################################################        
###############################################  OLD CODE ####################################################################
# def keymaker():
#     hrstoadd=str(input("Enter hours to add:"))
#     chatid=str(input("Enter chat id :"))
#     p=Key()
#     print(p)
#     with open('licenses.txt', 'a') as f:
#         f.write(f'{hrstoadd}:{chatid}:{p}'+'\n')


# def keychecker(keytocheck=str):
#     #keytocheck=(input("Enter Your Key :"))  
#     p=Key(key=keytocheck)
#     #m=p.verify(keytocheck)
#     if 'Valid' in str(p):
#         with open('licenses.txt', 'r') as f:
#             mkk=f.read()
#             if re.search(f'{keytocheck}', mkk):
#                 print('Found it!')
#                 return True 
#     else:
#         return False            
###############################################  OLD CODE ####################################################################
###############################################  OLD CODE ####################################################################
        
if __name__ == '__main__':        
    # anso=keymaker()
    k=keychecker('RE8S-RPS2-J2RR-3969-SR8K')
    print(k)
    
    
    