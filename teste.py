import bcrypt
st = '123456789'

print(str.encode(st))
hash = bcrypt.hashpw(st.encode(), bcrypt.gensalt())

print(hash)

