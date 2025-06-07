from cryptography.fernet import Fernet

def encrypt(text, key):
    f = Fernet(key)
    encrypted_text = f.encrypt(text.encode())
    return encrypted_text

def decrypt(encrypted_text, key):
    f = Fernet(key)
    decrypted_text = f.decrypt(encrypted_text).decode()
    return decrypted_text

text = "user_text"
key = Fernet.generate_key()
encrypted_text = encrypt(text, key)
print("Encrypted text: ", encrypted_text)

decrypted_text = decrypt(encrypted_text, key)
print("Decrypted text: ", decrypted_text)
