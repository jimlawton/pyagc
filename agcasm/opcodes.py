#!/usr/bin/env python

# Copyright 2010 Jim Lawton <jim dot lawton at gmail dot com>
# 
# This file is part of pyagc. 
#
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this software; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

from architecture import Architecture
from opcode import OpcodeType, OperandType
from memory import AddressType
from instruction import Instruction
from directive import Directive
from interpretive import Interpretive

OPCODES = { 
    Architecture.AGC4_B2 : {
        # In AGC4 architecture, all instructions are single-word.
        OpcodeType.BASIC: {
            # Name                Method    Opcode   Operand Type               Address Type 
            "AD":     Instruction("AD",     060000,  OperandType.EXPRESSION,    AddressType.ERASABLE_12), 
            "CA":     Instruction("CA",     030000,  OperandType.EXPRESSION,    AddressType.GENERAL_12),
            "CAE":    Instruction("CAE",    030000,  OperandType.EXPRESSION,    AddressType.ERASABLE_12),
            "CAF":    Instruction("CAF",    030000,  OperandType.EXPRESSION,    AddressType.FIXED_12),
            "CCS":    Instruction("CCS",    010000,  OperandType.EXPRESSION,    AddressType.ERASABLE_10),
            "COM":    Instruction("COM",    040000),
            "CS":     Instruction("CS",     040000,  OperandType.EXPRESSION,    AddressType.GENERAL_12),
            "DAS":    Instruction("DAS",    020001,  OperandType.EXPRESSION,    AddressType.ERASABLE_10),
            "DDOUBL": Instruction("DDOUBL", 020001),
            "DOUBLE": Instruction("DOUBLE", 060000),
            "DTCB":   Instruction("DTCB",   052006),
            "DTCF":   Instruction("DTCF",   052005),
            "DV":     Instruction("DV",     010000,  OperandType.EXPRESSION,    AddressType.GENERAL_12),
            "DXCH":   Instruction("DXCH",   050001,  OperandType.EXPRESSION,    AddressType.ERASABLE_10),
            "EXTEND": Instruction("EXTEND", 000006),
            "INCR":   Instruction("INCR",   024000),
            "INDEX":  Instruction("INDEX",  050000,  OperandType.EXPRESSION,    AddressType.ERASABLE_10),
            "INHINT": Instruction("INHINT", 000004),
            "LXCH":   Instruction("LXCH",   022000,  OperandType.EXPRESSION,    AddressType.ERASABLE_10),
            "MASK":   Instruction("MASK",   070000,  OperandType.EXPRESSION,    AddressType.GENERAL_12),
            "MSK":    Instruction("MASK",   070000,  OperandType.EXPRESSION,    AddressType.GENERAL_12),
            "NDX":    Instruction("INDEX",  050000,  OperandType.EXPRESSION,    AddressType.ERASABLE_10),
            "NOOP":   Instruction("NOOP",   010000),           # TODO: For fixed memory only. Handle erasable case.
            "OVSK":   Instruction("OVSK",   054000),
            "RELINT": Instruction("RELINT", 000003),
            "RESUME": Instruction("RESUME", 050017),
            "RETURN": Instruction("RETURN", 000002),
            "TC":     Instruction("TC",     000000,  OperandType.EXPRESSION,    AddressType.GENERAL_12),
            "TCAA":   Instruction("TCAA",   054005),
            "TCF":    Instruction("TCF",    010000,  OperandType.EXPRESSION,    AddressType.FIXED_12),
            "TCR":    Instruction("TC",     000000,  OperandType.EXPRESSION,    AddressType.GENERAL_12),
            "TS":     Instruction("TS",     054000,  OperandType.EXPRESSION,    AddressType.ERASABLE_10),
            "XCH":    Instruction("XCH",    056000,  OperandType.EXPRESSION,    AddressType.ERASABLE_10),
            "XLQ":    Instruction("XLQ",    000001),
            "XXALQ":  Instruction("XXALQ",  000000),
            "ZL":     Instruction("ZL",     022007)
        },
        OpcodeType.EXTENDED: {
            # Name                Method    Opcode   Operand
            "ADS":    Instruction("ADS",    026000,  OperandType.EXPRESSION,    AddressType.ERASABLE_10),
            "AUG":    Instruction("AUG",    024000,  OperandType.EXPRESSION,    AddressType.ERASABLE_10), 
            "BZF":    Instruction("BZF",    010000,  OperandType.EXPRESSION,    AddressType.FIXED_12),  
            "BZMF":   Instruction("BZMF",   060000,  OperandType.EXPRESSION,    AddressType.FIXED_12),
            "DCA":    Instruction("DCA",    030001,  OperandType.EXPRESSION,    AddressType.GENERAL_12),
            "DCOM":   Instruction("DCOM",   040001),
            "DIM":    Instruction("DIM",    026000,  OperandType.EXPRESSION,    AddressType.ERASABLE_10),
            "EDRUPT": Instruction("EDRUPT", 007000,  OperandType.EXPRESSION,    AddressType.FIXED_9),
            "INDEX":  Instruction("INDEX",  050000,  OperandType.EXPRESSION,    AddressType.GENERAL_12),
            "MP":     Instruction("MP",     070000,  OperandType.EXPRESSION,    AddressType.GENERAL_12),
            "MSU":    Instruction("MSU",    020000,  OperandType.EXPRESSION,    AddressType.ERASABLE_10),
            "NDX":    Instruction("INDEX",  050000,  OperandType.EXPRESSION,    AddressType.GENERAL_12),
            "QXCH":   Instruction("QXCH",   022000,  OperandType.EXPRESSION,    AddressType.ERASABLE_10),
            "RAND":   Instruction("RAND",   002000,  OperandType.EXPRESSION,    AddressType.CHANNEL),
            "READ":   Instruction("READ",   000000,  OperandType.EXPRESSION,    AddressType.CHANNEL),
            "ROR":    Instruction("ROR",    004000,  OperandType.EXPRESSION,    AddressType.CHANNEL),
            "RXOR":   Instruction("RXOR",   006000,  OperandType.EXPRESSION,    AddressType.CHANNEL),
            "SQUARE": Instruction("SQUARE", 070000),
            "SU":     Instruction("SU",     060000,  OperandType.EXPRESSION,    AddressType.ERASABLE_10),
            "WAND":   Instruction("WAND",   003000,  OperandType.EXPRESSION,    AddressType.CHANNEL),
            "WOR":    Instruction("WOR",    005000,  OperandType.EXPRESSION,    AddressType.CHANNEL),
            "WRITE":  Instruction("WRITE",  001000,  OperandType.EXPRESSION,    AddressType.CHANNEL),
            "ZQ":     Instruction("ZQ",     022007)
        },
        OpcodeType.DIRECTIVE: {
            # Name                Method            Mnemonic    Operand Type            Words
            "-1DNADR":  Directive("Minus1DNADR",    "-1DNADR",  OperandType.EXPRESSION, 1),
            "-2CADR":   Directive("Minus2CADR",     "-2CADR",   OperandType.EXPRESSION, 1),
            "-2DNADR":  Directive("Minus2DNADR",    "-2DNADR",  OperandType.EXPRESSION, 1),
            "-3DNADR":  Directive("Minus3DNADR",    "-3DNADR",  OperandType.EXPRESSION, 1),
            "-4DNADR":  Directive("Minus4DNADR",    "-4DNADR",  OperandType.EXPRESSION, 1),
            "-5DNADR":  Directive("Minus5DNADR",    "-5DNADR",  OperandType.EXPRESSION, 1),
            "-6DNADR":  Directive("Minus6DNADR",    "-6DNADR",  OperandType.EXPRESSION, 1),
            "-DNCHAN":  Directive("MinusDNCHAN",    "-DNCHAN",  1),
            "-DNPTR":   Directive("MinusDNPTR",     "-DNPTR",   1),
            "-GENADR":  Directive("MinusGENADR",    "-GENADR",  1),
            "1DNADR":   Directive("1DNADR",         None,       OperandType.EXPRESSION, 1),
            "2BCADR":   Directive("2BCADR",         None,       OperandType.EXPRESSION, 2),
            "2CADR":    Directive("2CADR",          None,       OperandType.EXPRESSION, 2),
            "2DEC":     Directive("2DEC",           None,       OperandType.DECIMAL,    2),
            "2DEC*":    Directive("2DEC",           "2DEC*",    OperandType.DECIMAL,    2),
            "2DNADR":   Directive("2DNADR",         None,       OperandType.EXPRESSION, 2),
            "2FCADR":   Directive("2FCADR",         None,       OperandType.EXPRESSION, 2), 
            "2OCT":     Directive("2OCT",           None,       OperandType.OCTAL,      2),
            "3DNADR":   Directive("3DNADR",         None,       OperandType.EXPRESSION, 1),
            "4DNADR":   Directive("4DNADR",         None,       OperandType.EXPRESSION, 1),
            "5DNADR":   Directive("5DNADR",         None,       OperandType.EXPRESSION, 1),
            "6DNADR":   Directive("6DNADR",         None,       OperandType.EXPRESSION, 1),
            "=":        Directive("EqualsSign",     "=",        OperandType.EXPRESSION, 0),
            "=ECADR":   Directive("EqualsECADR",    "=ECADR",   OperandType.EXPRESSION, 0),
            "=MINUS":   Directive("EqualsMINUS",    "=MINUS",   OperandType.EXPRESSION, 0),
            "ADRES":    Directive("ADRES",          None,       OperandType.EXPRESSION, 1),
            "BANK":     Directive("BANK",           None,       OperandType.OCTAL,      0),
            "BBCON":    Directive("BBCON",          None,       OperandType.EXPRESSION, 1),
            "BBCON*":   Directive("BBCON",          "BBCON*",   OperandType.EXPRESSION, 1),
            "BLOCK":    Directive("BLOCK",          None,       OperandType.OCTAL,      0),
            "BNKSUM":   Directive("BNKSUM",         None,       OperandType.NONE,       0),
            "CADR":     Directive("CADR",           None,       OperandType.EXPRESSION, 1),
            "CHECK=":   Directive("CHECKEquals",    "CHECK=",   OperandType.EXPRESSION, 0),
            "COUNT":    Directive("COUNT",          None,       OperandType.EXPRESSION, 0),
            "COUNT*":   Directive("COUNT",          "COUNT*",   OperandType.EXPRESSION, 0),
            "DEC":      Directive("DEC",            None,       OperandType.DECIMAL,    1),
            "DEC*":     Directive("DEC",            "DEC*",     OperandType.DECIMAL,    1),
            "DNCHAN":   Directive("DNCHAN",         None,       OperandType.OCTAL,      1),
            "DNPTR":    Directive("DNPTR",          None,       OperandType.EXPRESSION, 1),
            "EBANK=":   Directive("EBANKEquals",    "EBANK=",   OperandType.EXPRESSION, 0),
            "ECADR":    Directive("ECADR",          None,       OperandType.EXPRESSION, 1),
            "EQUALS":   Directive("EQUALS",         None,       OperandType.EXPRESSION, 0),
            "ERASE":    Directive("ERASE",          None,       OperandType.EXPRESSION, 0),
            "FCADR":    Directive("FCADR",          None,       OperandType.EXPRESSION, 1),
            "GENADR":   Directive("GENADR",         None,       OperandType.EXPRESSION, 1),
            "MEMORY":   Directive("MEMORY",         None,       OperandType.EXPRESSION, 0),
            "MM":       Directive("MM",             None,       OperandType.DECIMAL,    1),
            "NV":       Directive("NV",             None,       OperandType.DECIMAL,    1),
            "OCT":      Directive("OCT",            None,       OperandType.OCTAL,      1),
            "OCTAL":    Directive("OCTAL",          None,       OperandType.OCTAL,      1),
            "REMADR":   Directive("REMADR",         None,       OperandType.EXPRESSION, 1),
            "SBANK=":   Directive("SBANKEquals",    "SBANK=",   OperandType.EXPRESSION, 0),
            "SETLOC":   Directive("SETLOC",         None,       OperandType.EXPRESSION, 0),
            "SUBRO":    Directive("SUBRO",          None,       OperandType.SYMBOLIC,   0),
            "VN":       Directive("VN",             None,       OperandType.DECIMAL,    1)
        },
        OpcodeType.INTERPRETIVE: {
            # Name                 Method           Mnemonic    Opcode
            "ABS":    Interpretive("ABS",           "ABS",      000000), 
            "ABVAL":  Interpretive("ABVAL",         "ABVAL",    000000), 
            "ACOS":   Interpretive("ACOS",          "ACOS",     000000), 
            "ARCCOS": Interpretive("ACOS",          "ARCCOS",   000000), 
            "ASIN":   Interpretive("ASIN",          "ASIN",     000000), 
            "ARCSIN": Interpretive("ASIN",          "ARCSIN",   000000), 
            "AXC,1":  Interpretive("AXC",           "AXC,1",    000000), 
            "AXC,2":  Interpretive("AXC",           "AXC,2",    000000), 
            "AXT,1":  Interpretive("AXT",           "AXT,1",    000000), 
            "AXT,2":  Interpretive("AXT",           "AXT,2",    000000), 
            "BDDV":   Interpretive("BDDV",          "BDDV",     000000), 
            "BDDV*":  Interpretive("BDDV",          "BDDV*",    000000), 
            "BDSU":   Interpretive("BDSU",          "BDSU",     000000), 
            "BDSU*":  Interpretive("BDSU",          "BDSU*",    000000), 
            "BHIZ":   Interpretive("BHIZ",          "BHIZ",     000000), 
            "BMN":    Interpretive("BMN",           "BMN",      000000), 
            "BOFCLR": Interpretive("BOFCLR",        "BOFCLR",   000000), 
            "BOF":    Interpretive("BOF",           "BOF",      000000), 
            "BOFF":   Interpretive("BOFF",          "BOFF",     000000), 
            "BOFINV": Interpretive("BOFINV",        "BOFINV",   000000), 
            "BOFSET": Interpretive("BOFSET",        "BOFSET",   000000), 
            "BON":    Interpretive("BON",           "BON",      000000), 
            "BONCLR": Interpretive("BONCLR",        "BONCLR",   000000), 
            "BONINV": Interpretive("BONINV",        "BONINV",   000000), 
            "BONSET": Interpretive("BONSET",        "BONSET",   000000), 
            "BOV":    Interpretive("BOV",           "BOV",      000000), 
            "BOVB":   Interpretive("BOVB",          "BOVB",     000000), 
            "BPL":    Interpretive("BPL",           "BPL",      000000), 
            "BVSU":   Interpretive("BVSU",          "BVSU",     000000), 
            "BVSU*":  Interpretive("BVSU",          "BVSU*",    000000), 
            "BZE":    Interpretive("BZE",           "BZE",      000000), 
            "CALL":   Interpretive("CALL",          "CALL",     000000), 
            "CALRB":  Interpretive("CALRB",         "CALRB",    000000), 
            "CCALL":  Interpretive("CCALL",         "CCALL",    000000), 
            "CCALL*": Interpretive("CCALL",         "CCALL*",   000000), 
            "CGOTO":  Interpretive("CGOTO",         "CGOTO",    000000), 
            "CGOTO*": Interpretive("CGOTO",         "CGOTO*",   000000), 
            "CLEAR":  Interpretive("CLEAR",         "CLEAR",    000000), 
            "CLR":    Interpretive("CLR",           "CLR",      000000), 
            "CLRGO":  Interpretive("CLRGO",         "CLRGO",    000000), 
            "COS":    Interpretive("COS",           "COS",      000000), 
            "COSINE": Interpretive("COS",           "COSINE",   000000), 
            "DAD":    Interpretive("DAD",           "DAD",      000000), 
            "DAD*":   Interpretive("DAD",           "DAD*",     000000), 
            "DCOMP":  Interpretive("DCOMP",         "DCOMP",    000000), 
            "DDV":    Interpretive("DDV",           "DDV",      000000), 
            "DDV*":   Interpretive("DDV",           "DDV*",     000000), 
            "DLOAD":  Interpretive("DLOAD",         "DLOAD",    000000), 
            "DLOAD*": Interpretive("DLOAD",         "DLOAD*",   000000), 
            "DMP":    Interpretive("DMP",           "DMP",      000000), 
            "DMP*":   Interpretive("DMP",           "DMP*",     000000), 
            "DMPR":   Interpretive("DMPR",          "DMPR",     000000), 
            "DMPR*":  Interpretive("DMPR",          "DMPR*",    000000), 
            "DOT":    Interpretive("DOT",           "DOT",      000000), 
            "DOT*":   Interpretive("DOT",           "DOT*",     000000), 
            "DSQ":    Interpretive("DSQ",           "DSQ",      000000), 
            "DSU":    Interpretive("DSU",           "DSU",      000000), 
            "DSU*":   Interpretive("DSU",           "DSU*",     000000), 
            "EXIT":   Interpretive("EXIT",          "EXIT",     000000), 
            "GOTO":   Interpretive("GOTO",          "GOTO",     000000), 
            "INCR,1": Interpretive("INCR",          "INCR,1",   000000), 
            "INCR,2": Interpretive("INCR",          "INCR,2",   000000), 
            "INVERT": Interpretive("INVERT",        "INVERT",   000000), 
            "INVGO":  Interpretive("INVGO",         "INVGO",    000000), 
            "ITA":    Interpretive("ITA",           "ITA",      000000), 
            "LXA,1":  Interpretive("LXA",           "LXA,1",    000000), 
            "LXA,2":  Interpretive("LXA",           "LXA,2",    000000), 
            "LXC,1":  Interpretive("LXC",           "LXC,1",    000000), 
            "LXC,2":  Interpretive("LXC",           "LXC,2",    000000), 
            "MXV":    Interpretive("MXV",           "MXV",      000000), 
            "MXV*":   Interpretive("MXV",           "MXV*",     000000), 
            "NORM":   Interpretive("NORM",          "NORM",     000000), 
            "NORM*":  Interpretive("NORM",          "NORM*",    000000), 
            "PDDL":   Interpretive("PDDL",          "PDDL",     000000), 
            "PDDL*":  Interpretive("PDDL",          "PDDL*",    000000), 
            "PDVL":   Interpretive("PDVL",          "PDVL",     000000), 
            "PDVL*":  Interpretive("PDVL",          "PDVL*",    000000), 
            "PUSH":   Interpretive("PUSH",          "PUSH",     000000), 
            "ROUND":  Interpretive("ROUND",         "ROUND",    000000), 
            "RTB":    Interpretive("RTB",           "RTB",      000000), 
            "RVQ":    Interpretive("RVQ",           "RVQ",      000000), 
            "SET":    Interpretive("SET",           "SET",      000000), 
            "SETGO":  Interpretive("SETGO",         "SETGO",    000000), 
            "SETPD":  Interpretive("SETPD",         "SETPD",    000000), 
            "SIGN":   Interpretive("SIGN",          "SIGN",     000000), 
            "SIGN*":  Interpretive("SIGN",          "SIGN*",    000000), 
            "SIN":    Interpretive("SIN",           "SIN",      000000), 
            "SINE":   Interpretive("SIN",           "SINE",     000000), 
            "SL1":    Interpretive("SL",            "SL1",      000000), 
            "SL1R":   Interpretive("SL",            "SL1R",     000000), 
            "SL2":    Interpretive("SL",            "SL2",      000000), 
            "SL2R":   Interpretive("SL",            "SL2R",     000000), 
            "SL3":    Interpretive("SL",            "SL3",      000000), 
            "SL3R":   Interpretive("SL",            "SL3R",     000000), 
            "SL4":    Interpretive("SL",            "SL4",      000000), 
            "SL4R":   Interpretive("SL",            "SL4R",     000000), 
            "SL":     Interpretive("SL",            "SL",       000000), 
            "SL*":    Interpretive("SL",            "SL*",      000000), 
            "SLOAD":  Interpretive("SLOAD",         "SLOAD",    000000), 
            "SLOAD*": Interpretive("SLOAD",         "SLOAD*",   000000), 
            "SLR":    Interpretive("SLR",           "SLR",      000000), 
            "SLR*":   Interpretive("SLR",           "SLR*",     000000), 
            "SQRT":   Interpretive("SQRT",          "SQRT",     000000), 
            "SR1":    Interpretive("SR",            "SR1",      000000), 
            "SR1R":   Interpretive("SR",            "SR1R",     000000), 
            "SR2":    Interpretive("SR",            "SR2",      000000), 
            "SR2R":   Interpretive("SR",            "SR2R",     000000), 
            "SR3":    Interpretive("SR",            "SR3",      000000), 
            "SR3R":   Interpretive("SR",            "SR3R",     000000), 
            "SR4":    Interpretive("SR",            "SR4",      000000), 
            "SR4R":   Interpretive("SR",            "SR4R",     000000), 
            "SR":     Interpretive("SR",            "SR",       000000), 
            "SR*":    Interpretive("SR",            "SR*",      000000), 
            "SRR":    Interpretive("SRR",           "SRR",      000000), 
            "SRR*":   Interpretive("SRR",           "SRR*",     000000), 
            "SSP":    Interpretive("SSP",           "SSP",      000000), 
            "SSP*":   Interpretive("SSP",           "SSP*",     000000), 
            "STADR":  Interpretive("STADR",         "STADR",    000000), 
            "STCALL": Interpretive("STCALL",        "STCALL",   000000), 
            "STODL":  Interpretive("STODL",         "STODL",    000000), 
            "STODL*": Interpretive("STODL",         "STODL*",   000000), 
            "STORE":  Interpretive("STORE",         "STORE",    000000), 
            "STOVL":  Interpretive("STOVL",         "STOVL",    000000), 
            "STOVL*": Interpretive("STOVL",         "STOVL*",   000000), 
            "STQ":    Interpretive("STQ",           "STQ",      000000), 
            "SXA,1":  Interpretive("SXA",           "SXA,1",    000000), 
            "SXA,2":  Interpretive("SXA",           "SXA,2",    000000), 
            "TAD":    Interpretive("TAD",           "TAD",      000000), 
            "TAD*":   Interpretive("TAD",           "TAD*",     000000), 
            "TIX,1":  Interpretive("TIX",           "TIX,1",    000000), 
            "TIX,2":  Interpretive("TIX",           "TIX,2",    000000), 
            "TLOAD":  Interpretive("TLOAD",         "TLOAD",    000000), 
            "TLOAD*": Interpretive("TLOAD",         "TLOAD*",   000000), 
            "UNIT":   Interpretive("UNIT",          "UNIT",     000000), 
            "UNIT*":  Interpretive("UNIT",          "UNIT*",    000000), 
            "V/SC":   Interpretive("VSC",           "V/SC",     000000), 
            "V/SC*":  Interpretive("VSC",           "V/SC*",    000000), 
            "VAD":    Interpretive("VAD",           "VAD",      000000), 
            "VAD*":   Interpretive("VAD",           "VAD*",     000000), 
            "VCOMP":  Interpretive("VCOMP",         "VCOMP",    000000), 
            "VDEF":   Interpretive("VDEF",          "VDEF",     000000), 
            "VLOAD":  Interpretive("VLOAD",         "VLOAD",    000000), 
            "VLOAD*": Interpretive("VLOAD",         "VLOAD*",   000000), 
            "VPROJ":  Interpretive("VPROJ",         "VPROJ",    000000), 
            "VPROJ*": Interpretive("VPROJ",         "VPROJ*",   000000), 
            "VSL":    Interpretive("VSL",           "VSL",      000000), 
            "VSL*":   Interpretive("VSL",           "VSL*",     000000), 
            "VSL1":   Interpretive("VSL",           "VSL1",     000000), 
            "VSL2":   Interpretive("VSL",           "VSL2",     000000), 
            "VSL3":   Interpretive("VSL",           "VSL3",     000000), 
            "VSL4":   Interpretive("VSL",           "VSL4",     000000), 
            "VSL5":   Interpretive("VSL",           "VSL5",     000000), 
            "VSL6":   Interpretive("VSL",           "VSL6",     000000), 
            "VSL7":   Interpretive("VSL",           "VSL7",     000000), 
            "VSL8":   Interpretive("VSL",           "VSL8",     000000), 
            "VSQ":    Interpretive("VSQ",           "VSQ",      000000), 
            "VSR":    Interpretive("VSR",           "VSR",      000000), 
            "VSR*":   Interpretive("VSR",           "VSR*",     000000), 
            "VSR1":   Interpretive("VSR",           "VSR1",     000000), 
            "VSR2":   Interpretive("VSR",           "VSR2",     000000), 
            "VSR3":   Interpretive("VSR",           "VSR3",     000000), 
            "VSR4":   Interpretive("VSR",           "VSR4",     000000), 
            "VSR5":   Interpretive("VSR",           "VSR5",     000000), 
            "VSR6":   Interpretive("VSR",           "VSR6",     000000), 
            "VSR7":   Interpretive("VSR",           "VSR7",     000000), 
            "VSR8":   Interpretive("VSR",           "VSR8",     000000), 
            "VXM":    Interpretive("VXM",           "VXM",      000000), 
            "VXM*":   Interpretive("VXM",           "VXM*",     000000), 
            "VXSC":   Interpretive("VXSC",          "VXSC",     000000), 
            "VXSC*":  Interpretive("VXSC",          "VXSC*",    000000), 
            "VXV":    Interpretive("VXV",           "VXV",      000000), 
            "VXV*":   Interpretive("VXV",           "VXV*",     000000), 
            "XAD,1":  Interpretive("XAD",           "XAD,1",    000000), 
            "XAD,2":  Interpretive("XAD",           "XAD,2",    000000), 
            "XCHX,1": Interpretive("XCHX",          "XCHX,1",   000000), 
            "XCHX,2": Interpretive("XCHX",          "XCHX,2",   000000), 
            "XSU,1":  Interpretive("XSU",           "XSU,1",    000000), 
            "XSU,2":  Interpretive("XSU",           "XSU,2",    000000)
        }
    }
}
