from PyPDF2 import PdfReader, PdfWriter
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from PyPDF2.generic import NameObject,TextStringObject
from PyPDF2 import PdfReader

def embed_signature(pdf_file, output_pdf, public_key_file, signature_file):
    # Read the original PDF
    reader = PdfReader(pdf_file)
    writer = PdfWriter()

    # Copy all pages to the writer
    for page in reader.pages:
        writer.add_page(page)

    # Compute the hash of the PDF
    with open(pdf_file, "rb") as pdf:
        pdf_data = pdf.read()
    hash_value = SHA256.new(pdf_data)

    # Load the public key
    with open(public_key_file, "rb") as key_file:
        public_key = RSA.import_key(key_file.read())

    # Load the signature
    with open(signature_file, "rb") as sig_file:
        signature = sig_file.read()

    # Verify the signature
    try:
        pkcs1_15.new(public_key).verify(hash_value, signature)
        verification_status = "Signature Verified"
        print("The signature is valid.")
    except (ValueError, TypeError):
        verification_status = "Signature Invalid"
        print("The signature is invalid.")

    # Add signature verification metadata
    metadata = reader.metadata or {}
    metadata[NameObject('/Signature')] = TextStringObject(signature.hex())
    
    
    
    # writer.add_metadata(metadata)
    # metadata["/SignatureVerification"] = verification_status
    writer.add_metadata(metadata)

    # Save the new PDF with verification metadata
    with open(output_pdf, "wb") as output_file:
        writer.write(output_file)

    print(f"Verified PDF saved as: {output_pdf}")

# Embed signature and verification result
embed_signature("input.pdf", "verified_input.pdf", "public_key.pem", "signature.sig")
