# Dissonance - Rogue Synergy server

For more information on this tool read the blog post at: https://www.n00py.io/2017/03/compromising-synergy-clients-with-a-rogue-synergy-server/
```
 ,-~~-.___.
  / |  x     \\
 (  )        0            _____  _         Rouge Synergy Server
  \_/-, ,----'  ____     |  __ \(_)               ~n00py~
     ====      ||   \_   | |  | |_ ___ ___  ___  _ __   __ _ _ __   ___ ___
    /  \-'~;   ||     |  | |  | | / __/ __|/ _ \| '_ \ / _` | '_ \ / __/ _ \\
   /  __/~| ...||__/|-"  | |__| | \__ \__ \ (_) | | | | (_| | | | | (_|  __/
 =(  _____||________|    |_____/|_|___/___/\___/|_| |_|\__,_|_| |_|\___\___|
```
## ABOUT:
This script was designed to spoof a Synergy server and to entice users to connect to it.

## INSTALL:
apt install git

git clone https://github.com/n00py/Dissonance.git

pip install zeroconf 
## USAGE:

### Sniffing with Dissonance
```
python dissonance.py --sniff
```
### Starting a server and advertising via Bonjour
```
python dissonance.py -p [PAYLOAD FILE] --bonjour
```

For more information view the blog post located here: TBA

###Future Ideas:
- OS detection
- Dynamic payload selection
- Add functionality for SSL
- Cipboard nabbing
