import os
import requests

# Define your API endpoints
SIGN_API_URL = "https://example.com/api/sign"
VERIFY_API_URL = "https://example.com/api/verify"

# Directory setup
INPUT_DIR = "pdfs/input"         # Directory containing input PDF files
SIGNED_DIR = "pdfs/signed"       # Directory to save signed PDFs
VERIFIED_DIR = "pdfs/verified"   # Directory to save verified PDFs

# API Key or Authorization (if required)
API_KEY = "your_api_key_here"  # Replace with your actual API key

# Ensure directories exist
os.makedirs(SIGNED_DIR, exist_ok=True)
os.makedirs(VERIFIED_DIR, exist_ok=True)

def sign_pdf(file_path):
    """
    Send a PDF file to the API for signing.
    """
    with open(file_path, "rb") as pdf_file:
        response = requests.post(
            SIGN_API_URL,
            headers={"Authorization": f"Bearer {API_KEY}"},
            files={"file": pdf_file}
        )
    if response.status_code == 200:
        return response.content  # Return signed PDF content
    else:
        print(f"Failed to sign {file_path}: {response.text}")
        return None

def verify_pdf(file_path):
    """
    Send a PDF file to the API for verification.
    """
    with open(file_path, "rb") as pdf_file:
        response = requests.post(
            VERIFY_API_URL,
            headers={"Authorization": f"Bearer {API_KEY}"},
            files={"file": pdf_file}
        )
    if response.status_code == 200:
        return response.json()  # Return verification result
    else:
        print(f"Failed to verify {file_path}: {response.text}")
        return None

def process_pdfs():
    """
    Automate signing and verifying multiple PDF files.
    """
    for pdf_name in os.listdir(INPUT_DIR):
        input_file = os.path.join(INPUT_DIR, pdf_name)

        # Step 1: Sign the PDF
        signed_content = sign_pdf(input_file)
        if signed_content:
            signed_file = os.path.join(SIGNED_DIR, pdf_name)
            with open(signed_file, "wb") as signed_pdf:
                signed_pdf.write(signed_content)
            print(f"Signed PDF saved: {signed_file}")

            # Step 2: Verify the signed PDF
            verification_result = verify_pdf(signed_file)
            if verification_result:
                print(f"Verification result for {pdf_name}: {verification_result}")

                # Save the verified PDF
                if verification_result.get("status") == "valid":
                    verified_file = os.path.join(VERIFIED_DIR, pdf_name)
                    os.rename(signed_file, verified_file)
                    print(f"Verified PDF moved to: {verified_file}")
            else:
                print(f"Verification failed for {pdf_name}.")
        else:
            print(f"Signing failed for {pdf_name}.")

if __name__ == "__main__":
    process_pdfs()
