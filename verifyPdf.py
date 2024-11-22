from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA

def verify_pdf_signature(pdf_file, public_key_file, signature_file):
    # Read the PDF content
    with open(pdf_file, "rb") as pdf:
        pdf_data = pdf.read()

    # Compute the hash of the PDF
    hash_value = SHA256.new(pdf_data)

    # Load the public key
    with open(public_key_file, "rb") as key_file:
        public_key = RSA.import_key(key_file.read())

    # Read the signature
    with open(signature_file, "rb") as sig_file:
        signature = sig_file.read()

    # Verify the signature
    try:
        pkcs1_15.new(public_key).verify(hash_value, signature)
        print("The signature is valid.")
        return True
    except (ValueError, TypeError):
        print("The signature is invalid.")
        return False
if __name__ == "__main__":
# Verify the PDF signature
    verify_pdf_signature("input.pdf", "public_key.pem", "signature.sig")
