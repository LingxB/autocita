from dotenv import load_dotenv, find_dotenv
import os

def get_envar(key):
    """Get environment variable form .env file"""
    load_dotenv(find_dotenv(raise_error_if_not_found=True, usecwd=True))
    return os.environ.get(key)