import bcrypt

class cript_utils ():
    def cript(password):
        # Generazione della salt
        salt = bcrypt.gensalt()
        # Hash della password con salt
        hashed_password = bcrypt.hashpw(password.encode(), salt)
        return hashed_password
    
    def check_cript(password, hashed_password):
        # Verifica se la password fornita corrisponde all'hash
        return bcrypt.checkpw(password.encode(), hashed_password)
