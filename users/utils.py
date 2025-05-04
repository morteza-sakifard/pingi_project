import random
import logging

logger = logging.getLogger(__name__)

def generate_otp():
    """Generate a 6-digit OTP"""
    return str(random.randint(100000, 999999))

def log_otp(mobile, otp):
    """Log OTP for a given mobile number"""
    print(f"OTP [{mobile}] -> [{otp}]")  # Print directly to console for visibility
    logger.info(f"OTP [{mobile}] -> [{otp}]")