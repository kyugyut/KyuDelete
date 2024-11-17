import session
from address import url
import re

#descrypto _r value and make right service_code
def magic_code(s_code,cryptogram):
    r_code = get_r_code(cryptogram)

    #rc1 function part
    anlaut = int(r_code[0])
    anlaut = anlaut - 5 if anlaut > 5 else anlaut + 4
    r_code = str(anlaut)+r_code[1:]

    #_f function part
    r_keys = r_code.split(',')
    changes = ""
    for pos,r_key in enumerate(r_keys):
        sword = 2 * (float(r_key)-pos-1) / (13-pos-1)
        changes += chr(int(sword))
    s_code = s_code[:-10] + changes
    return s_code

def get_r_code(crypto):
    #_d function part
    crypto = re.sub(pattern="[^A-Za-z0-9+/=]",string=crypto,repl="")
    r_code = ""
    length = int(len(crypto)/4)
    for i in range(0,length):
        first = key.find(crypto[4*i])
        second = key.find(crypto[4*i+1])
        third = key.find(crypto[4*i+2])
        fourth = key.find(crypto[4*i+3])
        sword = first << 2 | second >> 4
        mirror = (15 & second) << 4 | third >> 2
        bell = (3 & third) << 6 | fourth
        r_code += chr(sword)
        if third != 64:
            r_code += chr(mirror)
        if fourth != 64:
            r_code += chr(bell)
    
    return r_code

def get_key():
    script_text = session.get(url['script']).text

    pattern = "eval.*?'.*?\((.*?)\)"
    key_code = re.search(pattern,script_text).groups()[0]
    key_code = key_code.split(',')

    real_key = ""
    for code in key_code:
        real_key += chr(int(code))

    return real_key

key = get_key()

if __name__ == "__main__":
    r = "RMyEPMU5Qou4d+ntQ+0uPMSEQ4uERgnDdTuEd+qtQgQ5P+UtQ+y6PMq5P+UK"
    s = "21ac6d96ad152e8f15a05b7350a2475909d19bcedeba9d4face8115e9bc2fa480cc53455abd9d8447547b74816ac6cc318831cd1b8c15a5a9295e4268b626aef9d23be4da195745f3bae7932f60f5a39f526cbb4ab92b0ef81b93ec312fd8a478292f403b13d5f20ab077214b8878190dd5bc30c69369f56e692bae7ff160292a5c801601687032a1d05e38be345a434fc52728c167f1c2b5b711507e165bb6300fece2cb4adadfd4bfbe0ddf3f398372c8b4c6b89b7b1aa022ad95118fbbce62951f763c9"
    print(magic_code(s,r))