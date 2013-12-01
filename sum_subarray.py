import math
INF = 100001
n = int(raw_input())
v = raw_input().split()

for i in range(0,n):
	v[i] = int(v[i])

print len(v)
Sum = [0 for i in range(0,n)]
Sum[0] = v[0]%n

for i in range(1,n):
	Sum[i] = (Sum[i-1] + v[i])%n

minhash = {}

for i in range(0,n):
	minhash[Sum[i]] = INF

for i in range(0,n):
	val = Sum[i]
	min_value = min(dict[val],i)
	dict[val] = min_value

for i in range(0,n):
	if Sum[i]%n == 0:
		print 0,i
	else:
		start = Sum[i]
		if start!= INF and start!=i:
			print start+1,i
