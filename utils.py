import string
import random

chars = string.ascii_letters + string.digits
def generate_url() -> str:
    """
    Generates base62 string
    """
    return ''.join(random.SystemRandom().choice(chars) for _ in range(7))