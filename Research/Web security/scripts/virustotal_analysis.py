"""
Author: Christian Camilo Urcuqui López
Date: September 18, 2019

This code consumes the API from Virustotal in order to take decisions about threats 
"""
import requests, json
import sys
import getopt
import requests
import optparse


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




def menu():
    # This is the command menu
    s = "\n"
    log = (" ___   ___    __   ____  ___    ___    __    __               ",
           "|   | /  |   |  |  |  |  |  |  /  |   |  |  |  |      [0][1][0]   ",
           "|       /    |  |  |  |  |       /    \   \_/  /      [1][1][1]   ",
           "|      /     |  |  |  |  |      /      \  \_/ /       [1][1][1]   ",
           "|  |\  \     |  '--'  |  |  |\  \       \    /        Virustotal V2    ",
           "| _| `.__\   |________|  | _| `.__\      |___|                    ")
    out = s.join(log)
    print(out)
    print()
    print()
    parser = optparse.OptionParser("URL Scan -u <url> -a <api key>")
    parser.add_option("-u", dest="url", type="string", help="URL to analyze")
    parser.add_option("-a", dest="apkey", type="string", help="api key")
    (options, args) = parser.parse_args()
    
    if(options.url is None) | (options.apkey is None):
        print(parser.usage)
        exit(0)
    else:
        url = options.url
        apkey = options.apkey
        url_virustotal = 'https://www.virustotal.com/vtapi/v2/url/report'
        params = {'apikey': apkey, 'resource': url}
        response = requests.get(url_virustotal, params=params)
        print(response.json())

if __name__ == "__main__":
    
        menu()   
        
  