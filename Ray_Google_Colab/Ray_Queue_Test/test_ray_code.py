import ray

ray.init()
a = 'Amrit'
b = ray.put(a)
del a
c = ray.get(b)
print(c)
del b
d = input("Enter a Value")
