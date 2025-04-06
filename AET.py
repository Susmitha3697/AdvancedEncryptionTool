import os
import sys
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2

KEY_LENGTH = 32
SALT = b'some_salt_123'

def get_key(password):
    return PBKDF2(password, SALT, dkLen=KEY_LENGTH)

def encrypt_file(file_path, password):
    key = get_key(password)
    cipher = AES.new(key, AES.MODE_EAX)

    with open(file_path, 'rb') as f:
        data = f.read()

    ciphertext, tag = cipher.encrypt_and_digest(data)
    encrypted_file = file_path + '.enc'

    with open(encrypted_file, 'wb') as f:
        f.write(cipher.nonce)
        f.write(tag)
        f.write(ciphertext)

    print(f"[✔] File encrypted and saved as: {encrypted_file}")

def decrypt_file(file_path, password):
    key = get_key(password)

    with open(file_path, 'rb') as f:
        nonce = f.read(16)
        tag = f.read(16)
        ciphertext = f.read()

    cipher = AES.new(key, AES.MODE_EAX, nonce)

    try:
        data = cipher.decrypt_and_verify(ciphertext, tag)
        output_file = file_path.replace('.enc', '.dec')

        with open(output_file, 'wb') as f:
            f.write(data)

        print(f"[✔] File decrypted and saved as: {output_file}")
    except ValueError:
        print("[✘] Decryption failed! Wrong password or file is corrupted.")

def main():
    print("\n=== Advanced Encryption Tool (CMD Version) ===")
    print("1. Encrypt a file")
    print("2. Decrypt a file")
    choice = input("Choose (1/2): ")

    file_path = input("Enter full file path: ").strip('"')
    if not os.path.exists(file_path):
        print("[✘] File not found.")
        return

    password = input("Enter password: ")

    if choice == '1':
        encrypt_file(file_path, password)
    elif choice == '2':
        decrypt_file(file_path, password)
    else:
        print("[✘] Invalid option.")

if __name__ == "__main__":
    main()
