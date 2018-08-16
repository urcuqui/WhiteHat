# Fingerprinting


**Table of Contents**

[Introduction](#introduction)
| [Tools and overview](#Tools-and-Overview)
| [Automated Tools](#Automated-Tools)

---

## Introduction ##

This is a process to get information about a target. Currently, we can access to different tools whose are automated and other not, but all of them use the open information in Internet. One practice in this is OSINT (Open Source Intelligence), whose is oriented to get information in different open sources, such as, news, Internet and television.

## Tools and Overview ##


During this process is important to get insights about the technological infrastructure, we can get an idea through the data in the communication network (packet analysis received in the web browser). Moreover, we can use other tools to make HTTP request, for example:

Netcat
```
nc taget.com.edu port
```
Telnet
```
nc IP port
```
Some HTTP requests have special data, and they depend of the server technology, in some cases the information get from an Apache server is different from an Microsoft IIS.

Sometimes, Cookies have information about the technology, and they are defined in their identification variables, such as:
* ASPSESSIONIDFBEDUWXUIB=CEUIL... that is for a ASP solution
* PHPSESSID=acfirg7v0e4... it is for PHP solution
* CFID=659356, it is for ColdFusion solution

## Automated Tools ##
* Httpprint
* Nmap
* WhatWeb
* BlindElephant
