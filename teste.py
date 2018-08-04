from datetime import datetime
a = datetime.now()

for i in range(1000):
    pass

b = datetime.now()
c = b - a

print(c.microseconds)