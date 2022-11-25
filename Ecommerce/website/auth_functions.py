from passlib.hash import sha256_crypt
# Create password hash
def hash_User_Password(user_Password):
    user_Password = sha256_crypt.encrypt(user_Password)
    return user_Password

# Compare password hash
def verify_User_Password(user_Password, db_User_password):
    if sha256_crypt.verify(user_Password, db_User_password):
        return True
    else:
        return False

passwd = hash_User_Password("1234")

print (len(passwd))


