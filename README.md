# shutarp

A quick and dirty tool for identifying top ARPers from the output of `monitor traffic interface` on a Junos platform.

Allows you to specify the top n talkers to list, defaulting to 10.

##Usage

First capture a bunch of traffic on your Junos platform and save it off to a text file with:

`monitor traffic interface irb no-resolve`

Then let `shutarp` do the grunt work for you:

```
bdale@lojack> ./shutarp.py --file traffic-with-headers.txt --topn 12    

Top 12 ARP request sources:

10.1.0.141      :     26
10.1.0.131      :     16
10.1.0.254      :     15
10.1.0.150      :     14
192.168.5.141   :     12
10.1.0.170      :      8
10.1.0.221      :      8
10.1.0.222      :      8
10.1.0.90       :      4
10.1.0.4        :      4
10.1.0.70       :      3
10.1.0.241      :      2

```