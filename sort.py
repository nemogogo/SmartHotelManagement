

# def insert_sort(li):
# 	for i in range(len(li)):
# 		temp=li[i]
# 		j=i-1
# 		while li[j]>temp and j>=0:
# 			li[j+1]=li[j]
# 			j=j-1
#
# 		li[j+1]=temp
# 	return li
		
# def bubbule_sort(li):
# 	for i in range(len(li)-1):
# 		exchange=False
# 		for j in range(len(li)-i-1):
# 			if li[j+1]<li[j]:
# 				exchange=True
# 				li[j+1],li[j]=li[j],li[j+1]
# 		if not exchange:
# 			return li
# 	return li
#

# def select_sort(li):
# 	for i in range(len(li)-1):
# 		min_loc=i
# 		for j in range(i+1,len(li)):
# 			if li[min_loc]>li[j]:
# 				min_loc=j
# 		if min_loc!=i:
# 			li[min_loc],li[i]=li[i],li[min_loc]
# 	return li
# def partion(li,left,right):
# 	temp=li[left]
# 	while left<right:
# 		while left<right and li[right]>=temp:
# 			right-=1
# 		li[left]=li[right]
# 		while left<right and li[left]<=temp:
# 			left+=1
# 		li[right]=li[left]
# 	li[left]=temp
# 	return left
#
# def quick_sort(li,left,right):
# 	if left<right:
# 		mid=partion(li,left,right)
# 		quick_sort(li,mid+1,right)
# 		quick_sort(li,left,mid-1)
# 	return li
def shift(li,low,high):
	i=low
	j=2*i+1
	temp=li[i]
	while low<high:
		if j+1<high and li[j+1]>li[j]:
			j=j+1
		if j<high and li[j]>temp:
			li[i]=li[j]
			i=j
			j=2*i+1
		else:
			li[i]=temp
			break
	else:
		li[i]=temp
		
def heap_sort(li):
	n=len(li)
	for i in range((n-2)//2,-1,-1):
		shift(li,i,n-1)
	for i in range(n-1,-1,-1):
		li[i],li[0]=li[0],li[i]
		shift(li,0,i)
	return li
	
	

li=list(range(20))
print(li)
for i in range(len(li)-1):
	print(li[i])
		
		
		
import random
li=list(range(20))
random.shuffle(li)
print(li)
print(heap_sort(li))