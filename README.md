# Web Timing Attack
This project is an ongoing experiment that is testing the theoretical aspects of side channel attacks on cryptographic operations. 
Right now this tool can execute a timing attack against a local or remote server that is using a constant time equality check to verify a signature.

## Installation
 1. Clone repo
 2. Install dependencies: 
 '''
 pip install -r requirements.txt
 '''
 3. Start server: 
 '''
 ./server.py
 '''
 4. Launch attack:
 '''
  ./web_timing_attack.py (look at usages below)
 '''

## Usage
```
usage: web_timing_attack.py [-h] [-u URL] [-i ITERATIONS] [-b BYTES]                                                                                                                                          
                            [-e EVENTID] [-f] [-v] [--version]                                                                                                                                                
                                                                                                                                                                                                              
Timing attack against event id url signatures.                                                                                                                                                                
                                                                                                                                                                                                              
optional arguments:                                                                                                                                                                                           
  -h, --help     show this help message and exit                                                                                                                                                              
  -u URL         The target url.                                                                                                                                                                              
  -i ITERATIONS  The # of iterations to perform per byte. Default is 2.                                                                                                                                       
  -b BYTES       The # of bytes to guess. Default is 8.                                                                                                                                                       
  -e EVENTID     The EventID. Default is 19295929.                                                                                                                                                            
  -f             Save data to CSVs.                                                                                                                                                                           
  -v             Log to console in debug.                                                                                                                                                                     
  --version      show program's version number and exit   

```
## Contributing
1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D

## License
TODO: Write license