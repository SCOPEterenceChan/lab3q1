'''
Simple Billing Program

Created on 30/03/2020

@author: Terence

Private repository lab3q1 
'''
import xmltodict
import urllib.request
fileIn=urllib.request.urlopen('http://personal.cityu.edu.hk/~dcywchan/1718SemB121COM/client.xml')

byteStr = fileIn.read()
lines=byteStr.decode('utf-8')
dl=xmltodict.parse(lines)

clientDT=['Name','Address','Balance']
clientDL=[]
    
newdl=[]

for e in dl['root']['item']:
    tmpdl={}
    for key,value in e.items():
        if key != "@type":
            value=value["#text"]
            tmpdl.update({key:value})
            
    newdl.append(tmpdl)
    
for e in newdl:
    if len(clientDL) == 0:
        if e['txn'] == 'D':
            clientDL.append(dict(zip(clientDT,
                                     [e['name'],e['address'],float(e['amt'])])))
        else:
            clientDL.append(dict(zip(clientDT,
                                     [e['name'],e['address'],-float(e['amt'])])))
    else: 
        i = 0
        while i < len(clientDL) and clientDL[i]['Name'] != e['name']:
            i += 1
            
        if i == len(clientDL):        
            if e['txn'] == 'D':
                clientDL.append(dict(zip(clientDT,
                                     [e['name'],e['address'],float(e['amt'])])))
            else:
                clientDL.append(dict(zip(clientDT,
                                     [e['name'],e['address'],-float(e['amt'])])))
        else:
            if e['txn'] == 'D':
                clientDL[i]['Balance'] += float(e['amt'])
            else: clientDL[i]['Balance'] -= float(e['amt'])

print('%-20s%-30s%10s'%(clientDT[0],clientDT[1],clientDT[2]))
print('='*60)    
for e in sorted(clientDL, key = lambda c: c['Name']):
    if e['Balance'] != 0:
        print('%-20s%-30s%10.2f'%(e['Name'],e['Address'],e['Balance'])) 
