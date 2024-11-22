from Crypto.PublicKey import RSA

def generate_keys(private_key_file, public_key_file):
    # Generate RSA key pair
    key = RSA.generate(2048)

    # Export the private key
    private_key = key.export_key()
    with open(private_key_file, "wb") as priv_file:
        priv_file.write(private_key)

    # Export the public key
    public_key = key.publickey().export_key()
    with open(public_key_file, "wb") as pub_file:
        pub_file.write(public_key)

    print(f"Keys saved to {private_key_file} and {public_key_file}")

if __name__ == "__main__":
# Generate keys
        generate_keys("private_key.pem", "public_key.pem")
