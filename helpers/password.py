import bcrypt

def generate_password(password):
        byte_passw = password.encode('utf-8')
        salt_gen = bcrypt.gensalt()
        hash_passw = bcrypt.hashpw(byte_passw, salt_gen)
        hash_passw = bcrypt.hashpw(byte_passw, salt_gen)
        password = str(hash_passw.decode('utf-8'))
        return password