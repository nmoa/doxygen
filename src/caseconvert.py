# python3 script to generate caseconvert.h.
# It uses difference in lower() and upper() on a character to make a mapping
# that maps a given unicode point to either a lower or upper case UTF-8 character.
# this also include multi-byte characters.

import codecs
import unicodedata

toupper = {}
tolower = {}

def writeMapping(file,mapping):
    for k,v in sorted(mapping.items()):
        file.write(u"    case %s /* %s */: BSEQ(%s) /* %s */\n" %
               (hex(ord(k[0])), k, ",".join(f"0x{b:02x}" for b in v.encode('utf-8')), v))

def writePunctuationCodes(file):
    for codeValue in range(0,0x1FFFF):
        if unicodedata.category(chr(codeValue)).startswith(tuple(['P','S'])): # punctuation and symbols
            file.write(u"    case %s: return true; /* %s */\n" % (hex(codeValue), chr(codeValue)))

# create mappings of characters whose upper and lower case differ
for codeValue in range(0,0x1FFFF):
        s = chr(codeValue)
        sl = s.lower()
        su = s.upper()
        if ord(s[0])!=ord(sl[0]):
            tolower[s]=sl
        if ord(s[0])!=ord(su[0]):
            toupper[s]=su

file = codecs.open("caseconvert.h", "w", "utf-8")
file.write(r'''/** This file is generated by python3 caseconvert.py. DO NOT EDIT! */

#ifndef CASECONVERT_H
#define CASECONVERT_H

#include <cstdint>
#include <string>

#define BSEQ(...) { static unsigned char s[] = { __VA_ARGS__, 0x00 }; \
                    return reinterpret_cast<const char *>(s); }

inline const char *convertUnicodeToUpper(uint32_t code)
{
  switch(code)
  {
''');
writeMapping(file,toupper);
file.write(r'''    default: return nullptr;
  }
}

inline const char *convertUnicodeToLower(uint32_t code)
{
  switch(code)
  {
''');
writeMapping(file,tolower);
file.write(r'''    default: return nullptr;
  }
}

inline bool isPunctuationCharacter(uint32_t code)
{
  switch(code)
  {
''');
writePunctuationCodes(file);
file.write(r'''    default: return false;
  }
  return false;
}

#endif
''');
