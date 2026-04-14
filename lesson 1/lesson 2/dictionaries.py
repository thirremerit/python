numrat={
    "KS":"+383",
    "It":"+39",
    "AL":"+355",
}

kosova =numrat['KS']
print(kosova)

print(numrat['AL'])

numrat['KS']=+5
print(numrat['KS'])

del numrat['AL']

print(numrat)

numrat2 = numrat.keys()

print(numrat2)