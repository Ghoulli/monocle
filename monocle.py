import socket
import time
from ping3 import ping, verbose_ping

def cidrNotation(cidr):
    cidr = cidr[-2:] #remove everything but the last 2 characters from the string.
    val = str(cidr)
    val = val.replace('/', '') #removes all slashes in case the CIDR is 9 or lower.
    return int(val) #returns as int.

def calcOctets(addresses):
    returnArray = ["",""]
    divide = addresses / 256
    if divide == 1: #when the subnet is a /24.
        returnArray[0] = 0
        returnArray[1] = 255
        return returnArray
    elif divide < 1: #incase the subnet is a /25 or smaller.
        returnArray[0] = 0
        returnArray[1] = addresses
        return returnArray
    else: #the subnet is a /23 or bigger.
        returnArray[0] = int(divide) - 1
        returnArray[1] = 255
        return returnArray 
    
def calcEndRange(IPAddress, octetArray): #ugly function, but it works. Does nothing but sets the end of the range to an array and adds the first two host octets to it. Converts it to int.
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
    default = 256 #default amount. corrosponding to /24 subnet.
    diff = 24 - cidr
    if diff == 0:
        return default
    elif diff <= 0:
        positive = diff * -1 #makes the negative difference into a positive to do some maths with.
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

def loopAddresses(startIP, endIP):
    x = int(startIP[3])
    while int(startIP[2]) < int(endIP[2]) or (int(startIP[2]) == int(endIP[2]) and x <= int(endIP[3])):
        if x > 255:
            startIP[2] = str(int(startIP[2]) + 1) #startIP to int to add it up, back to str to get into the array again.
            x = 0
        concag = startIP[0] + "." + startIP[1] + "." + startIP[2] + "." + str(x)
        pingResponse =  ping(concag, timeout=2)
        if pingResponse == False:
            print('Host ' + concag + " offline")
        elif pingResponse == None:
            print('Host ' + concag + " offline")
        else:
            print('Host ' + concag + " is online")
        x += 1
    startIP[3] = str(x)      

def safeToFile(bool, onlineHosts):
        print("Would you like to safe the currently online devices to a .txt file?")
        print("[0] for No, [1] for Yes.")
        bool = int(input())
        if bool == 1:
            fileName = time.ctime()
            f = open(fileName + ".txt", "x")
            f.write(onlineHosts)
            f.close()

def pingsweep():
    print("You have chosen option [1]")
    time.sleep(0.5)
    print("What IP-range do you want to ping sweep?")
    time.sleep(0.5)
    print("Please give the IP-range in the following format: 192.168.0.0/24.")
    time.sleep(0.5)
    inputSweep = input() #takes the input as string
    pingsweepInput = str(inputSweep)
    if pingsweepInput == '':
        print("No IP-address specified, please do this again.")
        time.sleep(1)
        print("==============================================")
        pingsweep()
    else:
        cidrValue = cidrNotation(pingsweepInput) #gets the CIDR notation, returns as int.
        IPAddress = addressToString(pingsweepInput)
        stringArray = splitIpAddress(IPAddress)
        addresses = calculateAddresses(cidrValue)
        octets = calcOctets(addresses)
        endRangeIP = calcEndRange(stringArray, octets)
        loopAddresses(stringArray, endRangeIP)
        print("The pingsweep has finished. Now returning to the initial menu.")
        print("==============================================================")
        time.sleep(3)
        main()

def main(): #Main function calls the program to run. Needs to stay in main to call main again when a wrong input is given somewhere.
    print("What would you like to do?")
    print("[1]Do a pingsweep.")
    print("[2]Do a portscan.")
    print("[3]Do a speedtest.")
    print("[4]Let a ping run indefinitely.")
    print("[5]Let a ping run for X amount of times.")
    print("[6]Exit.")

    choiceInput = input() #needed because you're reading a raw interger in the if-statement.
    if int(choiceInput) == 1:
        time.sleep(0.5)
        pingsweep()
    elif int(choiceInput) == 6:
        exit
    else:
        print("The option filled in is invalid, please try again.")
        time.sleep(0.5)
        main()

main()
