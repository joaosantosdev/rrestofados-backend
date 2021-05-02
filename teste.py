import bcrypt

print(bcrypt.hashpw(str('12345678').encode(),bcrypt.gensalt()))