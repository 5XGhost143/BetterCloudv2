from fastapi import FastAPI
import uvicorn
import sys
import platform
import os
from pathlib import Path
from endpoints.root_endpoint import router as root_router

current_systemos = platform.system()

if current_systemos not in ["Windows", "Linux"]:
    print(f"Nicht unterstütztes Betriebssystem: {current_systemos}")
    sys.exit(1)

app = FastAPI()
app.include_router(root_router)

def check_ssl_certificates():
    ssl_dir = Path("ssl")
    
    if not ssl_dir.exists():
        return None, None
    
    cert_file = ssl_dir / "fullchain.pem"
    key_file = ssl_dir / "privkey.pem"
    
    if cert_file.exists() and key_file.exists():
        return str(cert_file), str(key_file)
    else:
        print("No SSL Certs were found (PLEASE ADD THEM FOR PRODUCTION)")
        return None, None

def print_windows_logo():
    print("""
    ██╗    ██╗██╗███╗   ██╗██████╗  ██████╗ ██╗    ██╗███████╗
    ██║    ██║██║████╗  ██║██╔══██╗██╔═══██╗██║    ██║██╔════╝
    ██║ █╗ ██║██║██╔██╗ ██║██║  ██║██║   ██║██║ █╗ ██║███████╗
    ██║███╗██║██║██║╚██╗██║██║  ██║██║   ██║██║███╗██║╚════██║
    ╚███╔███╔╝██║██║ ╚████║██████╔╝╚██████╔╝╚███╔███╔╝███████║
     ╚══╝╚══╝ ╚═╝╚═╝  ╚═══╝╚═════╝  ╚═════╝  ╚══╝╚══╝ ╚══════╝
    """)

def print_linux_logo():
    print("""
    ██╗     ██╗███╗   ██╗██╗   ██╗██╗  ██╗
    ██║     ██║████╗  ██║██║   ██║╚██╗██╔╝
    ██║     ██║██╔██╗ ██║██║   ██║ ╚███╔╝
    ██║     ██║██║╚██╗██║██║   ██║ ██╔██╗
    ███████╗██║██║ ╚████║╚██████╔╝██╔╝ ██╗
    ╚══════╝╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═╝
    """)

if __name__ == "__main__":
    if current_systemos == "Windows":
        print_windows_logo()
    elif current_systemos == "Linux":
        print_linux_logo()
    
    # Check if SSL
    ssl_cert, ssl_key = check_ssl_certificates()
    
    if ssl_cert and ssl_key:
        uvicorn.run(
            "cloud:app", 
            host="0.0.0.0", 
            port=9562, 
            reload=True,
            ssl_certfile=ssl_cert,
            ssl_keyfile=ssl_key
        )
    else:
        uvicorn.run(
            "cloud:app", 
            host="0.0.0.0", 
            port=9562, 
            reload=True
        )