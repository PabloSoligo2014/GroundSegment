'''
Created on Jul 25, 2017

@author: ubuntumate
'''

import logging
logger = logging.getLogger(__name__)

import struct
import sys
import argparse

from bitarray import bitarray



def bit_stuff(data):
    count = 0
    for bit in data:
        if bit:
            count += 1
        else:
            count = 0
        yield bit
        # todo: do we stuff *after* fifth '1' or *before* sixth '1?'
        if count == 5:
            logger.debug("Stuffing bit")
            yield False
            count = 0

def bit_unstuff(data):
    count = 0
    skip = False
    ret_bits = bitarray(endian="little")
    for bit in data:
        if not(skip):
            if bit:
                count += 1
            else:
                count = 0
            ret_bits.append(bit)
            
            if count == 5:
                logger.debug("Unstuffing bit")
                skip = True;
                count = 0
        else:
            skip = False
    return ret_bits

class FCS(object):
    def __init__(self):
        self.fcs = 0xffff
    def update_bit(self, bit):
        check = (self.fcs & 0x1 == 1)
        self.fcs >>= 1
        if check != bit:
            self.fcs ^= 0x8408
    def update(self, bytes):
        for byte in (ord(b) for b in bytes):
            for i in range(7,-1,-1):
                self.update_bit((byte >> i) & 0x01 == 1)
    def digest(self):
#        print ~self.fcs
#        print "%r" % struct.pack("<H", ~self.fcs % 2**16)
#        print "%r" % "".join([chr((~self.fcs & 0xff) % 256), chr((~self.fcs >> 8) % 256)])
        # digest is two bytes, little endian
        return struct.pack("<H", ~self.fcs % 2**16)
        
def fcs(bits):
    '''
    Append running bitwise FCS CRC checksum to end of generator
    '''
    fcs = FCS()
    for bit in bits:
        yield bit
        fcs.update_bit(bit)


    # append fcs digest to bit stream

    # n.b. wire format is little-bit-endianness in addition to little-endian
    digest = bitarray(endian="little")
    digest.frombytes(fcs.digest())
    for bit in digest:
        yield bit

def fcs_validate(bits):
    buffer = bitarray()
    fcs = FCS()

    for bit in bits:
        buffer.append(bit)
        if len(buffer) > 16:
            bit = buffer.pop(0)
            fcs.update(bit)
            yield bit
    
    if buffer.tobytes() != fcs.digest():
        raise Exception("FCS checksum invalid.")

class AX25(object):
    def __init__(
        self,
        destination=b"APRS", 
        source=b"", 
        digipeaters=(b"RELAY", b"WIDE2-1"), 
        info=b"\""
    ):
        self.flag = b"\x7e"

        self.destination = destination
        self.source = source
        self.digipeaters = digipeaters

        self.info = info
    
    @classmethod
    def callsign_encode(self, callsign):
        callsign = callsign.upper()
        if callsign.find(b"-") > 0:
            callsign, ssid = callsign.split(b"-")
        else:
            ssid = b"0"

        assert(len(ssid) == 1)
        assert(len(callsign) <= 6)

        callsign = b"{callsign:6s}{ssid}".format(callsign=callsign, ssid=ssid)

        # now shift left one bit, argh
        return b"".join([chr(ord(char) << 1) for char in callsign])


    def callsign_decode(self, callbits):
        callstring = callbits.tobytes()

        return b"".join([chr(ord(char) >> 1) for char in callstring])


    def encoded_addresses(self):
        address_bytes = bytearray(b"{destination}{source}{digis}".format(
            destination = AX25.callsign_encode(self.destination),
            source = AX25.callsign_encode(self.source),
            digis = b"".join([AX25.callsign_encode(digi) for digi in self.digipeaters])
        ))


        # set the low order (first, with eventual little bit endian encoding) bit
        # in order to flag the end of the address string
        address_bytes[-1] |= 0x01


        return address_bytes

    def header(self):
        
        return b"{addresses}{control}{protocol}".format(
            addresses = self.encoded_addresses(),
            control = self.control_field, # * 8,
            protocol = self.protocol_id,
        )
    def packet(self):
        return b"{header}{info}{fcs}".format(
            flag = self.flag,
            header = self.header(),
            info = self.info,
            fcs = self.fcs()
        )
    def unparse(self):
        flag = bitarray(endian="little")
        flag.frombytes(self.flag)

        bits = bitarray(endian="little")
        bits.frombytes("".join([self.header(), self.info, self.fcs()]))

        return flag + bit_stuff(bits) + flag
    
    def parse(self,bits):
        flag = bitarray(endian="little")
        flag.frombytes(self.flag)

        # extract bits from the first to second flag
        try:
            flag_loc = bits.search(flag)
            bits_noflag = bits[ flag_loc[0]+8:flag_loc[1] ]
       
            # Bit unstuff
            bits_unstuff = bit_unstuff(bits_noflag)
    
            # Chop to length
            bits_bytes = bits_unstuff.tobytes()
    
            # Split bits
            
     #       header = bits_unstuff[:240]
            h_dest = bits_unstuff[:56]
            h_src  = bits_unstuff[56:112]
            for n in range(14,len(bits_bytes)-1):
                if bits_bytes[n:n+2]=="\x03\xF0":
                    break
            if n==len(bits_bytes)-1 :
                self.destination = "no decode"
                self.source = "no decode"
                self.info = "no decode"
                self.digis = "no decode"
                return 
    
            
            digilen = (n-14)*8/7
            h_digi = bits_unstuff[112:112+(n-14)*8]
            h_len = 112 + (n-14)*8 + 16
            fcs = bits_unstuff[-16:]
            info = bits_unstuff[h_len:-16]
    
    
            # Decode addresses
            destination = self.callsign_decode(h_dest)
            source = self.callsign_decode(h_src)
        
            if digilen == 0:
                digipeaters = ()
            else:
                digipeters =  self.callsign_decode(h_digi)
                #     digipeaters = (self.callsign_decode(header[112:168]), self.callsign_decode(header[168:224]))
                print( "Destination:\t", destination[:-1])
                print( "Source:\t\t", source[:-1])
                #       print "Digipeater1:\t", digipeaters[0][:-1], "-", digipeaters[0][-1]
                print( "Digipeaters:\t", digipeaters)
                print( "Info:\t\t", info.tobytes())
            
            self.destination = destination
            self.source = source
            self.info = info.tobytes()
            self.digis = digipeaters 
        except:
            self.destination = "no decode"
            self.source = "no decode"
            self.info = "no decode"
            self.digis = "no decode"
            return 


    
    def __repr__(self):
        return self.__str__()
    
    def __str__(self):
        """
        return b"{source}>{destination},{digis}:{info}".format(
            destination = self.destination,
            source = self.source,
            digis = b",".join(self.digipeaters),
            info = self.info
        )"""
        
        digis = b",".join(self.digipeaters)
        return self.__showAsHex(self.destination)+self.__showAsHex(self.source)+self.__showAsHex(digis)+self.__showAsHex(self.info)
        
    def __showAsHex(self ,ba):
    
        result = ""
        for b in ba:
            result = result+hex(b)+" "
     
        return result
    
    
    def fcs(self):
        content = bitarray(endian="little")
        content.frombytes("".join([self.header(), self.info]))

        fcs = FCS()
        for bit in content:
            fcs.update_bit(bit)
#        fcs.update(self.header())
#        fcs.update(self.info)
        return fcs.digest()

class UI(AX25):
    def __init__(
        self,
        destination=b"APRS", 
        source=b"", 
        digipeaters=(b"WIDE1-1", b"WIDE2-1"),
        info=b""
    ):
        AX25.__init__(
            self, 
            destination, 
            source, 
            digipeaters,
            info
        )
        self.control_field = b"\x03"
        self.protocol_id = b"\xf0"
            