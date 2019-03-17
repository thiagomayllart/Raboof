# Raboof
Framework for testing common web application vulnerabilities

# Description

Raboof was created with the intention of being a framework for testing web application vulnerabilities. Raboof is structured in a way that implementing new techniques/payloads for the same vulnerability or new vulnerabilities becomes easy.

# Functions Available:

-HTTP Parameter Pollution

# Scheduled Updates: 

-SOAP Injection 
-Local/Remote File Inclusion
-Path Traversal 
-Dynamic Execution 
-OS Command Injection

# How to use

**First you need to setup the request file**

This tool is integrated with the output produced using Burp Suite. You **MUST USE BURP SUITE**

1) Produce an output of the request containing the key/token/string/etc you want to test:
  In the **Site Map** interface in Burp Suite -> Right Click the request -> Save Item -> **UNCHECK Base64 encode requests and responses**
2) Change the extension: .xml to .txt.

**HTTP Parameter Pollution Parameters:**
    
     -f | The location of your .txt request
     -o | Select 'pp' as Parameter Pollution option
     -th | quantity of threads used
     -d | delay between each request
 
 Example:
 
    raboof.py -f [FILE LOCATION] -o pp
    raboof.py -f [FILE LOCATION] -o pp -th [QUANTITY OF THREADS] -d [DELAY BETWEEN THREADS]

