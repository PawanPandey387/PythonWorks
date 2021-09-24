'''
Pawan Pandey
'''

import os
import sys
import marshal
import array

try:
    import cPickle as pickle
except:
    import pickle

# importined by pawan
import collections # to use counter

# The max bits constent
MAX_BITS = 8

'''
Code is compatible with Python 2.7

xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
'''


'''
helper-funtions for function code and decode

xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
'''

'''
funtion to build the tree.
'''
def buildTree(frequen):

    # convert recieved frequency into a list of tuple
    alist = [(y, x) for x, y in frequen.iteritems()]
    
    # sort the tree tuple in assending order
    treeTupe = (sorted(alist, key=getKey))

    '''
    Initialization: we need a sorted list of tuple, where each tuple = (frequency, letter)
                    The goal is to build a nested tuple that that represtens huffman-tree
    Maintenance: througout the tuple list we do folloing
                    1) get the two tuples of least frequncy (the first two of the sorted list)
                    2) make a branch tupple as (comibne freequency, (char1, cahr 2)) 
                    3) put it back in the list and sort the list so that in the next loop
                       we get least two in the front
    Termination: when only one tuple is left in the list. the first element of this tuple
                    is the combine weight of all unique letters and the second element is the tree
    '''
    while len(treeTupe) > 1 :
        # the explained steps of maintenace, slice in two parts
        leastTwo = tuple(treeTupe[0:2])                  
        theRest  = treeTupe[2:]
        
         #add the frequency, elements
        weight = leastTwo[0][0] + leastTwo[1][0]
        chars = (leastTwo[0][1],leastTwo[1][1])

        #combine and sort
        temp  = treeTupe  = theRest + [(weight,chars)]
        treeTupe = sorted(temp, key=getKey)

    # Return the single treetuple
    # the first element was total count therefore return the second
    return treeTupe[0][1]

'''
get key function to facilitate sorting of the list tuple
'''
def getKey(item):
    return item[0]

'''
A recursive function that populates the codeBBook by given tree
'''
def fillCodeook(tree, pattern=''):
    codeBook ={}
    '''
    Initialization: we need huff-tree (as a nested tuple)  to populate the tree dictioary
    Maintenance: identify leafs of each branch and set its value in the code book
                 we call the the recursive fucntion on left brach and right branch until we get the leaf
                  (going to left of branch is 0 and going to the right of the branh is 1)
    Termination: when we identify each leaf of the tree and its value is being set in the codeBBook
    '''   
    if isinstance(tree , str): # A leaf. set its code
        return {tree: pattern} 
    else : #Branch point. 
        codeBook.update(fillCodeook(tree[0], pattern+"0"))# Do the left branch
        codeBook.update(fillCodeook(tree[1], pattern+"1"))# do the right branch.
        return codeBook

'''
end of all  helper funtions of funtions code and decode
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
'''

'''
The code funtion uses several other helper functions
to eventually huffman-code the passed message
after the values assigned in the codeBook according
to huffman tree,
it retuens the codeed msg and the tree as dictionary
'''
def code(msg):
    frequen = collections.Counter(msg)  # calculate the frequency
    
    tree = buildTree(frequen) # get tree   
    codeBook = fillCodeook(tree) # get a codeBook dict

     # code the message based on the codeBook's value 
    codedMsg = "" 
    for ch in msg : codedMsg += codeBook[ch]

    #convert the tree as a string
    treeAsString = str(tree)

    codedTuple = (codedMsg, treeAsString) #tuple to return
    
    return codedTuple


'''
function to decode the message by walking the tree
the pass string should be in the form of binary string.
'''
def decode(msg, decoderRing):
    
    tree = eval(decoderRing) #get the tree back as tuple
    
    decoded = []  #container for string to return
    

    '''
    Initialization: to start the loop we need a binary sting, the goal is to find the decoded message
    Maintenance: based on the value of bit walk the tree if 0 go left if 1 go right,
                    whenever leaf is found set the vale and go to the begining of tree for next char
    Termination: when all bits are being triversed
    '''
    p = tree
    for bit in msg :
        if bit == '0' : p = p[0]     # Head up the left branch
        else          : p = p[1]     # or up the right branch
        if type(p) == type("") :
            decoded.append(p)              # found a character. Add to output
            p = tree                 # and restart for next character
    return ''.join(decoded)


'''
function compresses the passed message using bbitWise manipulation
the passed message should be only as a binary string
it returns a tuple that contains (compressed message, decoding tree)
'''
def compress(msg):
  
    # Initializes an array to hold the compressed message.
    compressed = array.array('B')

    #get the huffCode and the tree
    huff_code, tree = code(msg)
  
    buff = 0 # for bitwise manipulation
    count = 0 # to keep track loop
    
    total_length = 0 #to keep trak oftotal length, will be used in decompressing

    '''
    Initialization:we need binary string to start the loop, the goal is to compress this string
                    using bit manipulation
    Maintenance: In each loop we need to do the following
                    1) update value of buff based on the value of current bit if 0 update it
                          shift ting left, if 1 update it by (shifting left or 1)
                    2)keep track of the count of the loop whenever it reaches
                        Max_bits(8)
                    3) keep track of total lenght
                        
    Termination: when the all bits have been triverced in binary string
    '''
    for bit in huff_code:
      # shifting based on the value of bit
      if(bit == '0'):
        buff = (buff << 1) 
      else:
        buff = (buff << 1)| 1
        
      count += 1
      # whe we reach 8 loops time to append the compressed
      if(count == MAX_BITS):
          
        compressed.append(buff)
        
        # keep track of total length
        total_length += count
        
        # for next roud
        count = 0
        buff = 0

    # in last round if cound couldn't reach to 8th loop
    if(count != 0): 
      compressed.append(buff << (MAX_BITS-count))
      
      # update the totallength (I waited my 2 days becouse of this single line)
      total_length += count

    #reate the decoder ring
    treeAsString = str(tree)
    decding_ring = {'t' : treeAsString}
    decding_ring['l'] = total_length
    

    tupleToReturn = (compressed, decding_ring) # tuple to return
      
    return tupleToReturn 
    
    raise NotImplementedError


'''
the decompression function
'''
def decompress(msg, decoderRing):

    # Represent the message as an array
    byteArray = array.array('B',msg)

    # get the tree and code length from docoderRing
    tree = eval(decoderRing['t'])
    code_length = decoderRing['l']

    decoded = [] # container for decoded message

    total_length = 0 # to keep track of total lenght.
    

    
    p = tree # helper to walk the tree
    for code in byteArray:
        '''
        Initialization:fort each code of ourbyteArry  our goal is to decompress
                   the message to the original; we also need a contaion to hold the decoded
                   message, a tree to walk and total length of of of commressed message.
        Maintenance: for each code in the bite arrary check if code shiffted right by (MAX_BITS - i) & 1
                  where i = {1,2,...8}. if yes walk right on tree other wise go to the left.
                  whenever we reach to a leaf we
                      1)append the container with decoded value.
                      2go back to biging of the tree for the next char.
                      
                Important: It is possible that in the last round we didn't completed the 8th loop
                           there fore to prevent the extra right shifing we will process it
                           only up code_lengh that we have it in decoderRing
                  
                  
                        
       Termination: either buf_length =  8 or total_length == code_length.  
        '''
        buf_length = 0 
        while(buf_length < MAX_BITS and total_length != code_length):
            
            #keep track of buffer length and total length
            buf_length += 1
            total_length += 1
            
            if code >> (MAX_BITS - buf_length) & 1:
                p = p[1]
                if type(p) == type(""):
                    decoded.append(p)
                    p = tree
            else:
                p = p[0]
                if type(p) == type(""):
                    decoded.append(p)
                    p = tree
                   
    return ''.join(decoded)        
    raise NotImplementedError


'''
Function that run's the show.
'''
def usage():
    sys.stderr.write("Usage: {} [-c|-d|-v|-w] infile outfile\n".format(sys.argv[0]))
    exit(1)

if __name__=='__main__':
    if len(sys.argv) != 4:
        usage()
    opt = sys.argv[1]
    compressing = False
    decompressing = False
    encoding = False
    decoding = False
    if opt == "-c":
        compressing = True
    elif opt == "-d":
        decompressing = True
    elif opt == "-v":
        encoding = True
    elif opt == "-w":
        decoding = True
    else:
        usage()

    infile = sys.argv[2]
    outfile = sys.argv[3]
    assert os.path.exists(infile)

    if compressing or encoding:
        fp = open(infile, 'rb')
        msg = fp.read()
        fp.close()
        if compressing:
            compr, tree = compress(msg)
            fcompressed = open(outfile, 'wb')
            marshal.dump((pickle.dumps(tree), compr), fcompressed)
            fcompressed.close()
        else:
            enc, tree = code(msg)
            print(msg)
            fcompressed = open(outfile, 'wb')
            marshal.dump((pickle.dumps(tree), enc), fcompressed)
            fcompressed.close()
    else:
        fp = open(infile, 'rb')
        pickleRick, compr = marshal.load(fp)
        tree = pickle.loads(pickleRick)
        fp.close()
        if decompressing:
            msg = decompress(compr, tree)
        else:
            msg = decode(compr, tree)
            print(msg)
        fp = open(outfile, 'wb')
        fp.write(msg)
        fp.close()

