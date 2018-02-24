from sympy import *
from sympy.abc import *

def adjust(xl:eval, wrt:str, ref_calculation:str, mode:str) -> str:
    calculation = ref_calculation
    ref_calculation = str(ref_calculation)
    if 'sign' in str(ref_calculation):
        pos = ref_calculation.find('sign')
        ind = indfind(ref_calculation,pos,4,wrt)

        while ref_calculation[pos+4] != ')':
            ref_calculation = ref_calculation[:pos+4] + ref_calculation[pos+5:]

        ref_calculation = ref_calculation[:pos + 4] + ref_calculation[pos + 5:]

        if ind != 1 and (ind%2 == 0 or 1/ind %2 == 0):
            ref_calculation = str(ref_calculation).replace('sign', str(Piecewise((1, xl > 0), (0, Eq(xl, 0)))
                                                                       if mode == 'itgr' else '0'))
        else: ref_calculation = str(ref_calculation).replace('sign', str(Piecewise((1, xl > 0), (0, Eq(xl, 0)), (-1, xl < 0))
                                                                   if mode == 'itgr' else '0'))

        ref_calculation = ('-' + ref_calculation) if 'sign(-' in calculation else ('' + ref_calculation)

    if 'Abs' in str(calculation):
        pos = ref_calculation.find('Abs')
        ind = indfind(ref_calculation, pos, 3, wrt)
        coeff = ''

        off = 4
        while ref_calculation[pos+off] != wrt.replace('d',''):
            coeff += str(ref_calculation[pos+off])
            off +=1
        coeff = 1 if coeff == '' else int(coeff)

        while ref_calculation[pos + 3] != ')':
            ref_calculation = ref_calculation[:pos+3] + ref_calculation[pos+4:]

        ref_calculation = ref_calculation[:pos + 3] + ref_calculation[pos + 4:]
        if ind != 1 and (ind % 2 == 0 or 1 / ind % 2 == 0): ref_calculation = str(ref_calculation).replace('Abs', str(coeff*xl**ind))
        else: ref_calculation = str(ref_calculation).replace('Abs', str(Piecewise((coeff*xl**ind, xl >= 0), (-coeff*xl**ind, True))))

    return ref_calculation

def indfind(ref_calculation:str, pos:int, off:int, wrt:str) -> int:
    ind = ''
    while ref_calculation[pos + off] != ')':
        if ref_calculation[pos + off] == wrt.replace('d', '') and ref_calculation[pos + off + 1] == '^':
            newoff = off
            while ref_calculation[pos + newoff + 2] not in (')', '', '+', '-'):
                ind += ref_calculation[pos + newoff + 2]
                newoff += 1
        off += 1
    ind = 1 if ind == '' else int(ind)
    return ind
