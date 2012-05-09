#!/usr/bin/env python

import os, sys, commands
import numpy
from numpy import log as ln
from numpy import abs

def model_eps(q,rs,ThomasFermi=True):

  kF = 3.63/(rs) # in A^-1, for a free electron gas
  k0 = 0.815*kF*(rs)**0.5 # this is from AM
  q  = q*kF # parser script is giving things in terms of q/kF

  if ( ThomasFermi == True):

    Fq = 1.0

  else:

    beta = q/(2*kF)
    Fq = (1.0/(8.0*beta))*(4*beta + 2*(1 - beta**2)*ln(abs((1 + beta)/(1 - beta))))

  eps = (1 + (k0**2.0)/(q**2.0)*Fq)
  return eps

def main():

  try:
    prog = sys.argv[0]
    rs = float(sys.argv[1])
  except IndexError:
    # Tell the user what they need to give
    print '\nusage: '+prog+' rs (where rs is the density)\n'
    # Exit the program cleanly
    sys.exit(0)

  outputFile = open('epsinv.dat','w')
  outputFile.write('# q/kF, 1/epsilon(ThomasFermi), 1/epsilon(Lindhard)\n')

  epsinv = []

  iq_array = numpy.arange(0.01,100.0, 0.05)
 
  for iq in iq_array:
    epsinv.append(1/model_eps(iq,rs,True)) # store the lindhard value in an array
    outputFile.write(str(iq)+ ' ' + str(1/model_eps(iq,rs,True)) + ' ' + str(1/model_eps(iq,rs,False)) + '\n')

  outputFile.close()

### now let's look at this in real space
### (this part is still in development...

  epsinv = numpy.array(epsinv)

  from numpy.fft import fft, fftfreq
  sp = fft(epsinv)
  freq = fftfreq(iq_array.shape[-1])

  outputFile = open('sp.dat','w')
  outputFile.write('# ALERT, this file isn't ready yet ir, 1/epsilon(Lindhard)\n')


  for ir in range(len(sp)):
    outputFile.write(str(freq[ir])+ ' ' + str(sp[ir].imag) + '\n')

  outputFile.close()

# This executes main() only if executed from shell
if __name__ == '__main__':
    main()
