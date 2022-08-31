list1 = [13,11,9,5,2]
list2 = [15,12,7,6,1]

output = [] 
m = len(list1)
n = len(list2)

i = m - 1 
j = n - 1

while i >= 0 and j >= 0 :
    
	if list1[i] <= list2[j]:
		output += [list1[i]]
		i -= 1
	else:
		output += [list2[j]]
		j -= 1

    
    





print(output)