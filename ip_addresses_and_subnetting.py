"""This script can be used to show basic information about an IP address,
such as network address, netmask and usable host addresses.
It can also be used to subnet the given address. 
Both IPv4 and IPv6 addresses and networks are supported.
For subnetting, two modes are available: variable length subnetting and fixed length subnetting. 
Fixed length subnetting is relatively easy and straightforward but wastes a lot of address space.
Variable length subnetting is more complicated but is generally the preferred method as it wastes minimal address space.
More information about subnetting can be found at https://www.fieldengineer.com/skills/subnetting.
This script uses the ipaddress module, a fast, lightweight IPv4/IPv6 manipulation library in Python.
The ipaddress module documentation can be found at https://docs.python.org/3/library/ipaddress.html """

import ipaddress
from math import ceil, log2

#Fixed length subnetting
def flsm(ip_network, num_subnets = 2):
    prefix_diff = ceil(log2(num_subnets))
    return list(ip_network.subnets(prefixlen_diff=prefix_diff))

#Variable length subnetting
def vlsm(ip_network, hosts):

    #sort hosts in descending order
    hosts.sort(reverse=True)

    subnets = []

    for num in hosts:
        num_host_bits = ceil(log2(num + 2))   # + 2 to accomodate network address and broadcast address
        network_prefix = ip_network.max_prefixlen - num_host_bits
        subnets.append(list(ip_network.subnets(new_prefix = network_prefix))[0])
        ip_network = ip_network[0] + subnets[-1].num_addresses #get next usable address block
        ip_network = ipaddress.ip_network(str(ip_network) + "/" + str(network_prefix)) #convert address to network object
    return subnets

#error handling
def error():
    print("\nPlease check host/subnet information...")

#input
while True:
    address = input("\nEnter a valid IPv4/IPv6 address and prefix: ")
    try: #Create IP network object
        ip_network = ipaddress.ip_network(address, strict=False)
        break
    except: continue

#Basic output
print("\nNetwork address:", ip_network.network_address)
print("Netmask:", ip_network.netmask)
print("Is private network?", ip_network.is_private)
print("Is link local network?", ip_network.is_link_local)
print("Number of usable host addresses:", ip_network.num_addresses - 2)
print("First usable host address:",ip_network[1])
print("Last usable host address:",ip_network[-2] )
print("Broadcast address:", ip_network.broadcast_address)

#Get subnetting choice and inputs
while True:
    user_choice = input("\n1 - Variable length subnetting (VLSM), 2 - Fixed length subnetting (FLSM), n - None: ")
    if user_choice == "1": #vlsm
        hosts = input("\nEnter the number of hosts in each subnet (one line of text): ")
        hosts = hosts.split(" ")
        try: hosts = [int(hosts[i]) for i in range(len(hosts))]
        except:
            error()
            continue
        subnets = vlsm(ip_network, hosts)
        break
    elif user_choice == "2": #flsm
        try: num_subnets = int(input("\nEnter number of subnets to create: ")) 
        except: 
            error()
            continue
        subnets = flsm(ip_network, num_subnets)
        break
    elif user_choice.lower() == "n": break #end program

#More output
if user_choice == "1" or user_choice == "2":
    print()
    for i in range(len(subnets)):
        print("Subnet", i + 1)
        print("Network address:", subnets[i])
        print("Subnet mask:", subnets[i].netmask)
        print("Number of hosts:", subnets[i].num_addresses - 2)
        print("First usable host address:", subnets[i][1])
        print("Last usable host address:", subnets[i][-2])
        print("Broadcast address:", subnets[i].broadcast_address, "\n")

#write results  to file
with open("./ip_and_subnets.txt", "w", encoding="utf-8") as file:
    file.write("Network address: " + str(ip_network.network_address) + " " + str(ip_network.netmask) + "\n")
    file.write("Prefix: /" + str(ip_network.prefixlen) + "\n")
    file.write("Is private network? " + str(ip_network.is_private) + "\n")
    file.write("Is link local network? " + str(ip_network.is_link_local) + "\n")
    file.write("Number of usable host addresses: " + str(ip_network.num_addresses - 2) + "\n")
    file.write("First usable host address: " + str(ip_network[1]) + "\n")
    file.write("Last usable host address: " + str(ip_network[-2] ) + "\n")
    file.write("Broadcast address: " + str(ip_network.broadcast_address) + "\n\n")

    if user_choice == "1" or user_choice == "2":
        for i in range(len(subnets)):
            file.write("Subnet " + str(i + 1) + "\n")
            file.write("Network address: " + str(subnets[i].network_address) + " " + str(subnets[i].netmask) + "\n")
            file.write("Prefix: /" + str(subnets[i].prefixlen) + "\n")
            file.write("Number of hosts: " + str(subnets[i].num_addresses - 2) + "\n")
            file.write("First usable host address: " + str(subnets[i][1]) + "\n")
            file.write("Last usable host address: " + str(subnets[i][-2]) + "\n")
            file.write("Broadcast address: " + str(subnets[i].broadcast_address) + "\n\n")
