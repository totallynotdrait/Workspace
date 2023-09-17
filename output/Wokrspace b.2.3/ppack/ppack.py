"""
ppack 1.1
============================

ppack is a file packaging system to store any type of files

    * write_pack() is the function that writes the files into the ppack file
    * read_pack() is the function that reads the files inside the ppack file, returns all the stored files into a list

In this version:
    * Changed write_pack to make_pack
    * ppack does now encrypt files inside the ppack file
"""
import os
import struct
import base64
from cryptography.fernet import Fernet

def make_pack(filename, files):
    # Generate a key
    key = Fernet.generate_key()
    cipher_suite = Fernet(key)

    with open(filename + ".ppack", 'wb') as f:
        # Write the key to the pack
        f.write(struct.pack('I', len(key)))
        f.write(key)

        # Write the number of files
        f.write(struct.pack('I', len(files)))

        # Write each file to the pack
        for file in files:
            with open(file, 'rb') as af:
                data = af.read()
                encrypted_data = cipher_suite.encrypt(data)
                encoded_data = base64.b64encode(encrypted_data)
                f.write(struct.pack('I', len(encoded_data)))  # Write the size of the encoded file
                f.write(encoded_data)

def read_pack(filename):
    if os.path.exists(filename):
        if filename.endswith(".ppack"):
            with open(filename, 'rb') as f:
                # Read the key from the pack
                key_size = struct.unpack('I', f.read(4))[0]
                key = f.read(key_size)
                cipher_suite = Fernet(key)

                # Read the number of files
                num_files = struct.unpack('I', f.read(4))[0]

                # Read each file from the pack
                files = []
                for _ in range(num_files):
                    size = struct.unpack('I', f.read(4))[0]  # Read the size of the encoded file
                    encoded_data = f.read(size)
                    encrypted_data = base64.b64decode(encoded_data)
                    data = cipher_suite.decrypt(encrypted_data)
                    files.append(data)
        else:
            print(f"PPACK:ERROR: {filename} is not a ppack file")
    else:
        print(f"PPACK:ERROR: file not found : {filename}")
    return files
