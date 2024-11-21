def cidrToBin(hosts): #Important to 
    cidrBin = bin(hosts)
    #cidrBin = f'{int(hosts):08b}'
    return cidrBin

def stringToBinary(array):
    binArray = ["","","",""]
    x = 0
    while x < 4:
        binArray[x] = bin(int(array[x]))
#        binArray[x] = f'{int(array[x]):08b}' #the for loop translates all the IP address octets into binary.
        x += 1
    return binArray

def addBin(binaryArray, hosts):
    if hosts >= str(0b11111110):
        return None
    else:
        print(binaryArray[3])
        print(hosts)
        #sum = str(binaryArray[3]) + hosts #Currently adds the text version of the binaries together.
        return sum