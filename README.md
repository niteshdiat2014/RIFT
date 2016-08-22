# RIFT

Raspberry-pI Forensics Toolkit for acquisition and preservation of forensic artifats from Raspbian operating system controlled Raspberry-pi Internet of Things Platform. The toolkit cab be executed directly in python or using shell script.

The syntax of RIFt tool execution is followed below:

Method-1: Python environment

<directory or path of RIFT.py>$ python RIFT.py -h
                    -h Provides the option manual
                    
<directory or path of RIFT.py>$ python RIFT.py -d <Destination Directory>

------------------------------------------------------------------------------------------------

Method-2: Shell script environment

<directory or path of RIFT.py>$ sh rift_sh.sh
                 or
<directory or path of RIFT.py>$ ./rift_sh.sh                 
                    
                    
It above commands either automatically detects the destination or user can provide the prefered destination after which it preserve all the important files within the destination ditectory.
