# YesWeWaf

## Description
YesWeWaf is a Web Application Firewall Tester designed to help identify vulnerabilities in web applications.

## Installation

1. Ensure you have Python 3 installed on your system. If not, please download and install it from [the official Python website](https://www.python.org/).

2. Clone this Git repository to your machine using the following command:

    ```bash
    git clone https://github.com/Squ3D/YesWeWaf.git
    ```

3. Navigate to the YesWeWaf directory:

    ```bash
    cd YesWeWaf
    ```

4. Install the required dependencies by running the following command:

    ```bash
    pip3 install -r requirements.txt
    ```

## Usage

To use YesWeWaf, run the `YesWeWaf.py` script from the command line and specify the necessary options.

```bash
python3 YesWeWaf.py <url> [--test-rce] [--test-sql] [--test-rfi-rce] [--payloads-file <file_path>] [--export-csv]
