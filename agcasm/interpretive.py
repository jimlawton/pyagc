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

from opcode import Opcode, OpcodeType
from record_type import RecordType
from expression import AddressExpression

class InterpretiveType:
    NORMAL = 0
    SWITCH = 1
    SHIFT  = 2
    INDEX  = 3
    BRANCH = 4

    @classmethod
    def toString(cls, type):
        if type == InterpretiveType.SWITCH:
            return '[SW]'
        elif type == InterpretiveType.SHIFT:
            return '[SH]'
        elif type == InterpretiveType.INDEX:
            return '[IX]'
        elif type == InterpretiveType.BRANCH:
            return '[BR]'
        else:
            return '    '

class PackingType:
    "Specifies the packing type of a line of interpretive code, i.e. whether a left word only, right word only, or a packed pair (2 opcodes, or opcode/operand)."
    OPCODE_ONLY    = 0  # Left.
    OPERAND_ONLY   = 1  # Right.
    OPCODE_PAIR    = 2  # Pair.
    OPCODE_OPERAND = 3  # Pair.

# NOTE: Must be a new-style class.
class Interpretive(Opcode):

    def __init__(self, methodName, mnemonic, opcode, numOperands=1, increment=False, interpType=InterpretiveType.NORMAL, switchcode=None):
        Opcode.__init__(self, methodName, mnemonic, opcode, None, False, None, 1)
        self.numOperands = numOperands
        self.switchcode = switchcode
        self.type = RecordType.INTERP
        self.interpType = interpType
        self.interpArgType = None
        self.complement = True          # Default is to complement the generated code.
        self.increment = increment

    def parse(self, context, operands):
        # Case 1: One interpretive opcode.
        # Case 2: Two packed interpretive opcodes.
        # Case 3: Interpretive opcode, simple operand.
        # Case 4: Interpretive opcode, operand expression with 2 components (e.g. ['A', '+1']).
        # Case 5: Interpretive opcode, operand expression with 3 components (e.g. ['A', '-', '1']).

        exitInterp = False
        numArgs = self.numOperands

        context.interpArgs = 0
        context.interpArgCount = 0
        context.interpArgTypes = [ None, None, None, None ]
        context.interpArgCodes = [ 0, 0, 0, 0 ]
        context.interpArgIncrement = [ False, False, False, False ]

        # Increment flag for operand(s) of first opcode.
        if self.numOperands > 0:
            if self.methodName == "StoreLoad":
                # Store/loads seem to increment all their operands.
                if self.increment:
                    context.interpArgIncrement[0] = self.increment
                    context.log(5, "interpretive: opcode increment operand %d" % 0)
                    if self.numOperands > 1:
                        context.interpArgIncrement[1] = self.increment
                        context.log(5, "interpretive: opcode increment operand %d" % 1)
            else:
                # Other opcodes only increment the first operand.
                if self.increment:
                    context.interpArgIncrement[0] = self.increment
                    context.log(5, "interpretive: opcode increment operand %d" % 0)
            context.log(5, "interpArgIncrement: %s" % (context.interpArgIncrement))

        if self.mnemonic == "EXIT":
            exitInterp = True

        if context.complementNext:
            self.complement = True
            context.log(5, "record will be complemented")

        mnemonic2 = None

        if operands != None:
            oplen = len(operands)
        else:
            oplen = 0
        opcodes = [ self.opcode ]

        if oplen == 0:
            # Case 1
            context.log(5, "interpretive: packing type [OPCODE,0]")
            context.currentRecord.packingType = PackingType.OPCODE_ONLY
            context.currentRecord.operandType = RecordType.NONE
            context.log(5, "interpretive: %s (%03o)" % (self.mnemonic, self.opcode))
        elif oplen == 1:
            if operands[0] in context.opcodes[OpcodeType.INTERPRETIVE]:
                # Case 2
                context.log(5, "interpretive: packing type [OPCODE,OPCODE]")
                context.currentRecord.packingType = PackingType.OPCODE_PAIR
                context.currentRecord.operandType = RecordType.NONE
                mnemonic2 = operands[0]
                opobj = context.opcodes[OpcodeType.INTERPRETIVE][operands[0]]
                context.log(5, "interpretive: %s (%03o), %s (%03o)" % (self.mnemonic, self.opcode, opobj.mnemonic, opobj.opcode))
                opcodes.append(opobj.opcode)
                numArgs2 = opobj.numOperands
            else:
                # Case 3
                context.log(5, "interpretive: packing type [OPCODE,OPERAND]")
                context.currentRecord.packingType = PackingType.OPCODE_OPERAND
        elif oplen == 2 or oplen == 3:
            # Case 4, 5
            context.log(5, "interpretive: packing type [OPCODE,OPERAND]")
            context.currentRecord.packingType = PackingType.OPCODE_OPERAND
            pass
        else:
            context.syntax("invalid operand expression")

        if self.methodName.endswith('*'):
            context.indexed = True

        context.currentRecord.code = None

        if numArgs > 0:
            if context.interpArgs < 4:
                if (context.interpArgs + numArgs) <= 4:
                    context.log(5, "interpretive: incrementing interpArgs, %d -> %d" % (context.interpArgs, context.interpArgs + numArgs))
                    context.interpArgs += numArgs
                else:
                    context.log(5, "interpretive: incrementing interpArgs, %d -> %d" % (context.interpArgs, 4))
                    context.interpArgs = 4

        # FIXME: Should this be done after parsing first opcode?
        if context.currentRecord.packingType == PackingType.OPCODE_OPERAND:
            isStore = False
            if self.mnemonic == "STORE":
                isStore = True
            Interpretive._parseOperand(context, operands, embedded=True, store=isStore)

        try:
            method = self.__getattribute__("parse_" + self.methodName)
        except:
            method = None
        if method:
            method(context, operands)

        if mnemonic2 != None:
            if numArgs2 > 0:
                if context.interpArgs < 4:
                    if (context.interpArgs + numArgs2) <= 4:
                        context.log(5, "interpretive: incrementing interpArgs, %d -> %d" % (context.interpArgs, context.interpArgs + numArgs2))
                        context.interpArgs += numArgs2
                    else:
                        context.log(5, "interpretive: incrementing interpArgs, %d -> %d" % (context.interpArgs, 4))
                        context.interpArgs = 4
            try:
                method = opobj.__getattribute__("parse_" + opobj.methodName)
            except:
                method = None
            if method:
                operands = operands[1:]
                method(context, operands)
            if mnemonic2 == "EXIT":
                exitInterp = True

            # Increment flag for first operand of second opcode.
            if opobj.numOperands > 0:
                if opobj.numOperands == 2:
                    acindex = context.interpArgs - 2
                else:
                    acindex = context.interpArgs - 1
                if opobj.increment:
                    context.interpArgIncrement[acindex] = opobj.increment
                    context.log(5, "interpretive: opcode increment first operand set [%d]" % (acindex))
                    context.log(5, "interpArgIncrement: %s" % (context.interpArgIncrement))

        code = opcodes[0] + 1
        if len(opcodes) == 2:
            code += (opcodes[1] + 1) * 0200
            context.log(5, "interpretive: opcodes %03o %03o" % (opcodes[0], opcodes[1]))
        else:
            context.log(5, "interpretive: opcode %03o" % (opcodes[0]))
            if context.currentRecord.code:
                operandcode = context.currentRecord.code[0]
                context.log(5, "interpretive: operand %05o" % (operandcode))
                code = (opcodes[0] + operandcode) & 077777

        context.log(5, "interpretive: generated %05o" % code)

        if self.complement:
            code = ~code & 077777
            context.log(5, "interpretive: complemented to %05o " % (code))

        context.currentRecord.code = [ code ]
        context.currentRecord.complete = True
        context.currentRecord.type = self.type

        if (self.mnemonic == "STORE" or self.mnemonic == "STCALL" or self.methodName == "StoreLoad") and context.complementNext:
            context.complementNext = False

        if context.currentRecord.packingType != PackingType.OPERAND_ONLY:
            # If any operands found, parseOperand will already have done this.
            context.incrLoc(self.numwords)

        if exitInterp == True:
            context.interpMode = False
        else:
            context.interpMode = True

    @classmethod
    def _parseOperand(cls, context, operands, embedded=False, store=False):
        context.log(5, "interpretive: trying to parse operand %d %s" % (context.interpArgCount, operands))
        newoperands = []
        indexreg = 0
        for operand in operands:
            if operand.endswith(',1') or operand.endswith(',2'):
                context.log(5, "interpretive: indexed operand %s" % operand)
                if operand.endswith(',1'):
                    indexreg = 1
                else:
                    indexreg = 2
                newoperands.append(operand[:-2])
            else:
                newoperands.append(operand)
        operand = AddressExpression(context, newoperands)
        if operand.complete:
            context.currentRecord.target = operand.value
            context.currentRecord.operandType = operand.refType
            acindex = context.interpArgCount
            if context.interpArgTypes[acindex] != None:
                context.currentRecord.interpArgType = context.interpArgTypes[acindex]
                # Switch or shift operand.
                if context.currentRecord.interpArgType == InterpretiveType.SWITCH:
                    context.currentRecord.argcode = context.interpArgCodes[acindex]
                    context.log(5, "interpretive: switch operand, value=%05o [%d] argcode=%05o" % (operand.value, acindex, context.interpArgCodes[acindex]))
                    context.currentRecord.interpArgIncrement = context.interpArgIncrement[acindex]
                    # Switch operands use the encoding 0WWWWWWNNNNBBBB, where:
                    #  WWWWWW (6 bits) is the quotient when the constant value is divided by 15.
                    #  BBBB (4 bits) is the remainder when the constant value is divided by 15.
                    #  NNNN is an operation-specific value (all switch operations share the same opcode).
                    flag = (operand.value / 15) & 077
                    bit = (operand.value % 15)
                    code = (flag << 8) | bit | (context.currentRecord.argcode << 4)
                    context.log(5, "interpretive: switch operand, flag=%03o bit=%02o code=%05o" % (flag, bit, code))
                elif context.currentRecord.interpArgType == InterpretiveType.SHIFT:
                    if operand.value < 0:
                        code = (~abs(operand.value) + 1) & 077777
                    else:
                        code = operand.value
                    context.log(5, "interpretive: shift operand, code=%05o [%d] argcode=%05o" % (code, acindex, context.interpArgCodes[acindex]))
                    context.currentRecord.argcode = context.interpArgCodes[acindex]
                    context.currentRecord.interpArgIncrement = context.interpArgIncrement[acindex]
                    code += (context.interpArgCodes[acindex] << 6)
                    code &= 077777
                    context.log(5, "interpretive: shift operand, |=%05o, code=%05o" % (context.interpArgCodes[acindex] << 6, code))
                elif context.currentRecord.interpArgType == InterpretiveType.INDEX:
                    code = context.memmap.pseudoToInterpretiveAddress(operand.value)
                    context.log(5, "interpretive: index operand, value=%05o [%d] code=%05o" % (operand.value, acindex, code))
                elif context.currentRecord.interpArgType == InterpretiveType.BRANCH:
                    if operand.value < 0:
                        code = (operand.value - 1) & 077777
                    else:
                        code = context.memmap.pseudoToInterpretiveAddress(operand.value, size=15)
                    context.log(5, "interpretive: branch operand, value=%05o [%d] code=%05o" % (operand.value, acindex, code))
                else:
                    context.error("invalid interpretive argument type")
            else:
                if operand.value >= 0:
                    code = context.memmap.pseudoToInterpretiveAddress(operand.value)
                    context.log(5, "interpretive: positive normal operand [%d] code=%05o" % (acindex, code))
                else:
                    code = operand.value
                    context.log(5, "interpretive: negative normal operand [%d] value=%05o" % (acindex, code))

            if store and indexreg > 0:
                if indexreg == 1:
                    code |= 004000
                else:
                    code |= 010000

            if context.interpArgIncrement[acindex] == True:
                code += 1
                code &= 077777
                context.log(5, "interpretive: operand increment set [%d] code=%05o" % (acindex, code))

            if context.currentRecord.packingType == PackingType.OPERAND_ONLY and (indexreg == 2 or context.complementNext):
                code = ~code & 077777
                context.log(5, "interpretive: indexed X2 or complementNext, code=%05o" % (code))
                if context.complementNext:
                    context.complementNext = False

            context.currentRecord.code = [ code ]
            context.currentRecord.complete = True
            context.log(5, "interpretive: generated operand %05o" % code)
        else:
            context.log(5, "interpretive: operand undefined")

        if not embedded:
            context.incrLoc(1)

        if context.interpArgCount < 4:
            context.log(5, "interpretive: incrementing interpArgCount, %d -> %d" % (context.interpArgCount, context.interpArgCount + 1))
            context.interpArgCount += 1
        if context.interpArgCount == context.interpArgs:
            context.log(5, "interpretive: all args found, resetting interpArgs, %d -> %d" % (context.interpArgs, 0))
            context.interpArgs = 0
            context.interpArgCount = 0

    @classmethod
    def parseOperand(cls, context, operands, embedded=False):
        context.currentRecord.packingType = PackingType.OPERAND_ONLY
        cls._parseOperand(context, operands, embedded)
        context.currentRecord.type = RecordType.INTERP

    def parse_EXIT(self, context, operands):
        context.interpMode = False

    def parse_STORE(self, context, operands):
        if context.complementNext:
            context.log(5, "store record will be complemented")
        else:
            context.log(5, "store record will not be complemented")
            self.complement = False

    def parse_STCALL(self, context, operands):
        if context.complementNext:
            context.log(5, "store record will be complemented")
        else:
            context.log(5, "store record will not be complemented")
            self.complement = False
        # STCALL's 2nd operand is branch address.
        acindex = context.interpArgs - 1
        context.interpArgTypes[acindex] = InterpretiveType.BRANCH
        context.log(5, "interpretive: STCALL branch detected, [%d]" % (acindex))

    def parse_StoreLoad(self, context, operands):
        if context.complementNext:
            context.log(5, "store/load record will be complemented")
        else:
            context.log(5, "store/load record will not be complemented")
            self.complement = False

    def parse_STADR(self, context, operands):
        context.complementNext = True
        context.log(5, "interpretive: STADR, complementing next record")

    def parse_Switch(self, context, operands):
        # Store argcode in appropriate slot in context.interpArgCodes.
        context.log(5, "interpretive: switch, %d operands" % (self.numOperands))
        if self.numOperands > 0:
            # First operand is the switch flag.
            if self.numOperands == 2:
                acindex = context.interpArgs - 2
            else:
                acindex = context.interpArgs - 1
            context.interpArgCodes[acindex] = self.switchcode
            context.interpArgTypes[acindex] = InterpretiveType.SWITCH
            context.log(5, "interpretive: switch detected, [%d]=%05o" % (acindex, context.interpArgCodes[acindex]))
            if self.numOperands == 2:
                # Second operand (if any) is the branch address.
                context.interpArgTypes[acindex+1] = InterpretiveType.BRANCH
                context.log(5, "interpretive: switch branch detected, [%d]" % (acindex+1))

    def parse_Shift(self, context, operands):
        # Store switch code in appropriate slot in context.interpArgCodes.
        if self.numOperands > 0:
            acindex = context.interpArgs - 1
            context.interpArgCodes[acindex] = self.switchcode
            context.interpArgTypes[acindex] = InterpretiveType.SHIFT
            context.log(5, "interpretive: shift detected, [%d]=%05o" % (acindex, context.interpArgCodes[acindex]))

    def parse_Index(self, context, operands):
        context.log(5, "interpretive: index, %d operands" % (self.numOperands))
        if self.numOperands > 0:
            if self.numOperands == 2:
                acindex = context.interpArgs - 2
            else:
                acindex = context.interpArgs - 1
            context.interpArgCodes[acindex] = 0
            context.interpArgTypes[acindex] = InterpretiveType.INDEX
            context.log(5, "interpretive: index detected, [%d]=%05o" % (acindex, context.interpArgCodes[acindex]))

    def parse_Branch(self, context, operands):
        context.log(5, "interpretive: branch, %d operands" % (self.numOperands))
        if self.numOperands > 0:
            # First operand is the branch address.
            if self.numOperands == 2:
                acindex = context.interpArgs - 2
            else:
                acindex = context.interpArgs - 1
            context.interpArgCodes[acindex] = 0
            context.interpArgTypes[acindex] = InterpretiveType.BRANCH
            context.log(5, "interpretive: branch detected, [%d]=%05o" % (acindex, context.interpArgCodes[acindex]))

    def parse_SSP(self, context, operands):
        # SSP's 2nd operand is branch address.
        acindex = context.interpArgs - 1
        context.interpArgTypes[acindex] = InterpretiveType.BRANCH
        context.log(5, "interpretive: SSP address operand detected, [%d]" % (acindex))

    def parse_AXT(self, context, operands):
        # AXT's operand is branch address.
        acindex = context.interpArgs - 1
        context.interpArgTypes[acindex] = InterpretiveType.BRANCH
        context.log(5, "interpretive: AXT address operand detected, [%d]" % (acindex))

