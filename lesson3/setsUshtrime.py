my_set ={1,2,3}
my_set.add(7)

my_set.add(7)
print(my_set)

my_set.remove(3)
print(my_set)

my_set.discard(8)
print(my_set)

print(len(my_set))

my_set.clear()
print(my_set)
print(len(my_set))


print('---------------------------------')

my_list = [1,2,2,2,2,4,5]

print(my_list)


listaUnike= set(my_list)

listaUnike2=list(listaUnike)
print(listaUnike)
print(listaUnike2)

print('---------------------------------')


user1_interest= {"music","movies","travel"}
user2_interest= {"movies","reading","cook"}

rezultati = user1_interest.intersection(user2_interest)

print(rezultati)

users = {'lisa',"erit","bob"}

personi = "bob"

print(personi in users)
