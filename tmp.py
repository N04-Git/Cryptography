import conversion

p = "data3.JPG"

with open(p, 'rb') as f:
    d = f.read()
    
    print('Read bytes :', len(d))

serialized = conversion.makeSerializable(d)

deserialized = conversion.unmakeSerializable(serialized)

with open('data2.JPG', 'wb') as f:
    f.write(deserialized)