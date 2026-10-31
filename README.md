python script that creates a barker code rf pulse.

user can edit the barker code,  pri ,  iq sample rate,  and the freq offset of the barker code rf pulse train.

enjoy

see thegmr140 youtube channel to see demo of this.






qpsk signal

fs = 48khz
samples per symbol:  48

8 bit char

first char in signal:  H

00 = 45 degrees
01 = 135 degrees
11 = 225 degrees
10  =  315 degrees


signal has freq offset  and some awgn noise




















the lora signal  

sf = 5
bw = 10khz

preamble:  17 upchirps,  then 2 downchirps

iq sample rate:  48khz

text:  8 bit char

chirp time or symbol time:    2^sf / bw






