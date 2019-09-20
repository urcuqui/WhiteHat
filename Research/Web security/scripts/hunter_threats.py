"""
Author: Christian Camilo Urcuqui López
Date: September 18, 2019

This code consumes services from providers of cyber threats in order to analyze them
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
    
    # This is the virtual total command menu
  
    parser = optparse.OptionParser("Options to do -t <tool> -u <url> -a <api key> -h <host>")    
    parser.add_option("-u", dest="url", help="URL to analyze")
    parser.add_option("-a", dest="apkey", type="string", help="api key")
    parser.add_option("-t", dest="tool", type="string", help="tool")
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
        menu_ransomware_tracker()   
    else:
        exit(0)
#         url = options.url
#         apkey = options.apkey
#         url_virustotal = 'https://www.virustotal.com/vtapi/v2/url/report'
#         params = {'apikey': apkey, 'resource': url}
#         response = requests.get(url_virustotal, params=params)
#         print(response.json())

        
def menu_ransomware_tracker():
    print("developing")


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
    
  