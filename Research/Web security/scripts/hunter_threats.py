"""
Author: Christian Camilo Urcuqui López
Date: September 18, 2019

This code consumes services from some cyber threat providers, the idea of this tool is to provide utilities to make decisions about threats, for example, a malicious communication in a network
+ API from Virustotal
+ Ransomware Tracker

I would like to appreciate their help, both researchers and hackers who are collaborating with their knowledge in order to make computer systems and networks to be more secure

"""
import requests, json
import sys
import getopt
import requests
import optparse
import pandas as pd

def url_analysis(url="google.com", apkey=""):
    """
    It uses the Virustotal's service to know the reports about an URL
    
    Parameters
    ----------
    key: str
    url: str
    """
    url_virustotal = 'https://www.virustotal.com/vtapi/v2/url/report'
    params = {'apikey': apkey, 'resource': url}
    response = requests.get(url_virustotal, params=params)
    return(response.json())


def ip_virustotal_analysis(ip="google.com", apkey=""):
    """
    It uses the Virustotal's service to know the reports about an URL
    
    Parameters
    ----------
    apkey: str
    ip: str
    """
    url_virustotal = 'https://www.virustotal.com/vtapi/v2/ip-address/report'
    params = {'apikey': apkey, 'ip': ip}
    response = requests.get(url_virustotal, params=params)
    return(response.json())



def ramsomware_analysis(host="google.com", ip=""):
    """
    It uses the Ransomware Tracker CSV Feed 
    
    Parameters
    ----------
    url: str
    host: str
    """
    url_ramsomware = 'https://ransomwaretracker.abuse.ch/feeds/csv/'
    df_ram = pd.read_csv(url_ramsomware, skiprows=8, encoding="ISO-8859-1")
    return df_ram

def parser_menu():
    """
    Menu Script 
    
    Parameters
    ----------
    url: str
    host: str
    """
    parser = optparse.OptionParser("Options to do -t <tool> -u <url> -a <api key> -o <host>")    
    parser.add_option("-u", dest="url", help="URL to analyze")
    parser.add_option("-a", dest="apkey", type="string", help="api key")
    parser.add_option("-t", dest="tool", type="string", help="tool")
    parser.add_option("-o", dest="host", type="string", help="host to analyze")
    (options, args) = parser.parse_args()
    if options.tool is None:
        print(parser.usage)
        print("--------Tools-------")
        print("-v <virustotal>")
        print("-r <ransomware tracker>")
        menu = str(input("Select the tool of your preference: \n"))
        if "-v" == menu:
            url = str(input("Write the URL to analyze: \n"))
            apkey = str(input("Write the API Key from Virustotal: \n"))
            print(url_analysis(url, apkey))   
        elif "-r" == menu:
            menu_ransomware_tracker()   
    elif (options.tool == "-v"):
        url = str(input("Write the URL to analyze"))
        apkey = str(input("Write the API Key from Virustotal"))
        print(url_analysis(url, apkey)) 
    elif (options.tool == "-r"):
        host = str(input("Write the host to analyze: \n"))
        print(host)
        menu_ransomware_tracker(host)   
    else:
        exit(0)

        
def menu_ransomware_tracker(hosts=["www.google.com"]):
    url_ramsomware = 'https://ransomwaretracker.abuse.ch/feeds/csv/'
    ransomware_df = pd.read_csv(url_ramsomware, skiprows=8, encoding="ISO-8859-1")
    ransomware_df.columns = ransomware_df.columns.str.replace("-","_").str.replace("(","_").str.replace(")","_").str.lower().str.replace(" ", "_")
    ransomware_df = ransomware_df.loc[ransomware_df.ip_address_es_.isin(hosts)].copy()
    if ransomware_df.shape[0] != 0:
        print("You are compromised")
    else:
        print("Nothing right now")

if __name__ == "__main__":
    
    s = "\n"
    log = (" ___   ___    __   ____  ___    ___    __    __               ",
           "|   | /  |   |  |  |  |  |  |  /  |   |  |  |  |      [0][1][0]   ",
           "|       /    |  |  |  |  |       /    \   \ /  /      [0][0][1]   ",
           "|      /     |  |  |  |  |      /      \  \_/ /       [1][1][1]   ",
           "|  |\  \     |  '--'  |  |  |\  \       \    /        Threat Hunter    ",
           "| _| `.__\   |________|  | _| `.__\      |___|                    ")
    out = s.join(log)
    print(out)
    print()
    print()
    parser_menu()
    
  