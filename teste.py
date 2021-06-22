import bcrypt

print(bcrypt.hashpw(str('rrestofados').encode(),bcrypt.gensalt()))

