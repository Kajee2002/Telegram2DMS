from helper.logprint import log

keys=['batchFlag','batchFileList','dmsUsername','dmsPassword']


class Usersession:
    def __init__(self):
        #initiate dictionary
        self.data={}
    def create(self,user):
        
        self.data[user]={}
        for i in keys:
            self.data[user][i]=None
        log(f'{user} created successfully!')
    def insert(self,user,key,value):
        if user not in self.data:
            self.create(user)
        self.data[user][key]=value

    def get(self,user,key):
        return self.data.get(user)[key] if self.data.get(user) else None

dataBase=Usersession()

def CreateUser(user):
    if user not in dataBase.data:
        dataBase.create(user)

def AddBatchFile(user,file,message):
    
    if GetBatchFile(user):
        prev=dataBase.get(user,'batchFileList')
        prev.append([file,message])
        dataBase.insert(user,'batchFileList',prev)
    else:
        dataBase.insert(user,'batchFileList',[[file,message]])
    #print (dataBase.get(user,'batchFileList'),"Added")

def GetBatchFile(user):
    #print(dataBase.get(user,'batchFileList'),"Get")
    return dataBase.get(user,'batchFileList') if dataBase.get(user,'batchFileList') else []
