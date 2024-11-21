import os
import sys
from ping3 import ping, verbose_ping

def cidrNotation(cidr):
    cidr = cidr[-2:] #remove everything but the last 2 characters from the string.
    val = str(cidr)
    val = val.replace('/', '') #removes all slashes in case the CIDR is 9 or lower.
    return int(val) #returns as int.

def calcOctets(addresses):
    returnArray = ["",""]
    divide = addresses / 256
    if divide == 1:
        returnArray[0] = 0
        returnArray[1] = 255
        return returnArray
    elif divide < 1:
        returnArray[0] = 0
        returnArray[1] = addresses
        return returnArray
    else:
        returnArray[0] = int(divide) - 1
        returnArray[1] = 255
        return returnArray 
    
def calcSubnet(IPAddress, octetArray):
    subnettedArray = ["","","",""]
    subnettedArray[0] = int(IPAddress[0])
    subnettedArray[1] = int(IPAddress[1])
    subnettedArray[2] = int(IPAddress[2]) + octetArray[0]
    subnettedArray[3] = int(IPAddress[3]) + octetArray[1]
    return subnettedArray
    
def addressToString(fullstring):
    address = str(fullstring)
    useableIP = address.split('/')[0] #splits the IP address seperate from the CIDR notation.
    return str(useableIP)

def splitIpAddress(IPAddress):
    result = IPAddress.split('.') #splits the IP address into the octets into an array.
    return result

def calculateAddresses(cidr):
    default = 256
    diff = 24 - cidr
    if diff == 0:
        return default
    elif diff <= 0:
        positive = diff * -1
        i = 1
        while i <= positive:
            default = default / 2
            i += 1
        return int(default)
    else:
        i = 1
        while i <= diff:
            default = default * 2
            i += 1
        return default

print("What would you like to do?")
print("[1]Do a pingsweep.")
print("[2]Do a portscan.")
print("[3]Do a speedtest.")
print("[4]Let a ping run indefinitely.")
print("[5]Let a ping run for X amount of times.")

choiceInput = int(input()) #needed because you're reading a raw interger in the if-statement.
if choiceInput == 1:
    print("You have chosen option 1")
    print("What IP-range do you want to ping sweep?")
    print("Please do it in the following format: 192.168.0.0/24.")
    pingsweepInput = str(input()) #takes the input as string
    cidrValue = cidrNotation(pingsweepInput) #gets the CIDR notation, returns as int.
    if calculateAddresses(cidrValue) == 256: 
        IPAddress = addressToString(pingsweepInput)
        stringArray = splitIpAddress(IPAddress)
        addresses = calculateAddresses(cidrValue)
        octets = calcOctets(addresses)
        print(IPAddress)
        print(stringArray)
        print(octets)
        print(calcSubnet(stringArray, octets))
    else:
        nrOfAddressess = calculateAddresses(cidrValue)
        print(calcOctets(nrOfAddressess)) 
        print(nrOfAddressess)
else:
    print("The address filled in is invalid, please try again.")