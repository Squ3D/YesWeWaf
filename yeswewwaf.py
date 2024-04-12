import argparse
import csv
import requests
import time
from termcolor import colored
from urllib.parse import urljoin, urlparse, urlunparse

def test_sql_injection(url, payloads, headers):
    results = []
    for payload in payloads:
        result = {}
        full_url = url + payload
        response = requests.get(full_url, headers=headers)
        result['payload'] = payload
        
        if response.status_code == 403 or 'ATTACK DETECTED BY CLOUDFLARE' in response.headers.get('server', '').lower():
            result['vulnerability'] = 'SQL Injection'
            result['result'] = 'Bypass Failed'
            print(colored(f"{result['payload']} - Bypass Failed", 'red'))
        elif "error" in response.text:
            result['vulnerability'] = 'SQL Injection'
            result['result'] = 'Detected'
            print(result)
        else:
            result['vulnerability'] = 'SQL Injection'
            result['result'] = 'Bypass Succeed'
            print(colored(f"{result['payload']} - Bypass Succeed", 'green'))
        results.append(result)
    return results


def test_xss(url, payloads, headers):
    results = []
    parsed_url = urlparse(url)
    base_url = urlunparse(parsed_url[:3] + ('', '', ''))  # Remove fragment identifier
    
    for payload in payloads:
        result = {}
        full_url = urljoin(base_url, payload)  # Use base_url without fragment identifier
        response = requests.get(full_url, headers=headers, params=parsed_url.fragment)
        result['payload'] = payload
        result['time'] = time.strftime("%Y-%m-%d %H:%M:%S")  # Capture the current time when the attack was launched
        result['user_agent'] = headers['User-Agent']  # Include the user agent used in the request
        result['hostname'] = response.url.split('/')[2]  # Extract hostname from the response URL
        
        if response.status_code == 403:
            result['vulnerability'] = 'XSS'
            result['result'] = 'Bypass Failed'
            print(colored(f"Request for payload {result['payload']} was blocked (403 Forbidden)", 'red'))
        elif payload in response.text:
            result['vulnerability'] = 'XSS'
            result['result'] = 'Detected'
            print(result)
        else:
            result['vulnerability'] = 'XSS'
            result['result'] = f'{result["payload"]} - Bypass Succeed'
            print(colored(f"XSS bypass attempt with payload {result['payload']} - Bypass Succeed", 'green'))
        results.append(result)
    return results

def test_rfi(url, payloads, headers):
    results = []
    parsed_url = urlparse(url)
    base_url = urlunparse(parsed_url[:3] + ('', '', ''))  # Remove fragment identifier
    
    for payload in payloads:
        result = {}
        full_url = urljoin(base_url, payload)  # Use base_url without fragment identifier
        response = requests.get(full_url, headers=headers, params=parsed_url.fragment)
        result['payload'] = payload
        result['time'] = time.strftime("%Y-%m-%d %H:%M:%S")  # Capture the current time when the attack was launched
        result['user_agent'] = headers['User-Agent']  # Include the user agent used in the request
        result['hostname'] = response.url.split('/')[2]  # Extract hostname from the response URL
        
        if response.status_code == 403:
            result['vulnerability'] = 'RCE-RFI-LFI'
            result['result'] = 'Bypass Failed'
            print(colored(f"Request for payload {result['payload']} was blocked (403 Forbidden)", 'red'))
        else:
            result['vulnerability'] = 'RCE-RFI-LFI'
            result['result'] = f'{result["payload"]} - Bypass Succeed'
            print(colored(f"RCE-RFI-LFI bypass attempt with payload {result['payload']} - Bypass Succeed", 'green'))
        results.append(result)
    return results

def read_payloads_from_file(filename):
    with open(filename, 'r') as file:
        payloads = file.read().splitlines()
    return payloads

def no_tamper(payload):
    return payload

def write_results_to_csv(results, filename):
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = results[0].keys() if results else []
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for result in results:
            writer.writerow(result)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="YesWeWaf: Web Application Firewall Tester")
    parser.add_argument("url", help="URL of the web application to test")
    parser.add_argument("--test-xss", action="store_true", help="Test for XSS vulnerabilities")
    parser.add_argument("--test-sql", action="store_true", help="Test for SQL Injection vulnerabilities")
    parser.add_argument("--test-rfi", action="store_true", help="Test for Remote File Inclusion / RCE  vulnerabilities")
    parser.add_argument("--payloads-file", help="Path to the file containing payloads")
    parser.add_argument("--export-csv", action="store_true", help="Export results to a CSV file")
    args = parser.parse_args()

    print("""
 

██╗░░░██╗███████╗░██████╗░██╗░░░░░░░██╗███████╗░██╗░░░░░░░██╗░█████╗░███████╗
╚██╗░██╔╝██╔════╝██╔════╝░██║░░██╗░░██║██╔════╝░██║░░██╗░░██║██╔══██╗██╔════╝
░╚████╔╝░█████╗░░╚█████╗░░╚██╗████╗██╔╝█████╗░░░╚██╗████╗██╔╝███████║█████╗░░
░░╚██╔╝░░██╔══╝░░░╚═══██╗░░████╔═████║░██╔══╝░░░░████╔═████║░██╔══██║██╔══╝░░
░░░██║░░░███████╗██████╔╝░░╚██╔╝░╚██╔╝░███████╗░░╚██╔╝░╚██╔╝░██║░░██║██║░░░░░
░░░╚═╝░░░╚══════╝╚═════╝░░░░╚═╝░░░╚═╝░░╚══════╝░░░╚═╝░░░╚═╝░░╚═╝░░╚═╝╚═╝░░░░░
 

 Version 0.1
 Decathlon
 @author N. Gallouj

    """)

    if args.payloads_file:
        payloads = read_payloads_from_file(args.payloads_file)
    else:
        payloads_file = input("Enter the path to the file containing payloads: ")
        payloads = read_payloads_from_file(payloads_file)

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NAIMWAF 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}

    results = []

    if args.test_xss:
        print("\nTesting for XSS vulnerability:")
        results.extend(test_xss(args.url, payloads, headers))
    
    if args.test_sql:
        print("\nTesting for SQL Injection vulnerability:")
        results.extend(test_sql_injection(args.url, payloads, headers))
    
    if args.test_rfi:
        print("\nTesting for Remote File Inclusion vulnerability: (Not implemented)")
        results.extend(test_rfi(args.url, payloads, headers))

    if not args.test_xss and not args.test_sql and not args.test_rfi:
        print("No vulnerability type selected. Exiting.")

    if args.export_csv:
        if results:
            write_results_to_csv(results, 'test_results.csv')
            print("Results exported to test_results.csv")
        else:
            print("No vulnerability type selected or no results to export.")
