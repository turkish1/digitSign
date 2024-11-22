from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA

def sign_pdf(pdf_file, private_key_file, signature_file):
    # Read the PDF content
    with open(pdf_file, "rb") as pdf:
        pdf_data = pdf.read()

    # Compute the hash of the PDF
    hash_value = SHA256.new(pdf_data)

    # Load the private key
    with open(private_key_file, "rb") as key_file:
        private_key = RSA.import_key(key_file.read())

    # Sign the hash
    signature = pkcs1_15.new(private_key).sign(hash_value)

    # Save the signature to a file
    with open(signature_file, "wb") as sig_file:
        sig_file.write(signature)

    print(f"PDF signed. Signature saved to {signature_file}")

if __name__ == "__main__":
# Sign a PDF
    sign_pdf("input.pdf", "private_key.pem", "signature.sig")
