cd ~/plutus
rm -f -R -- */

cd ~/fortuna
rm -f -R -- */

git clone https://github.com/pyfortuna/fortuna
cp ~/fortuna.properties fortuna/config

cd ~/fortuna/fortuna/src
python3 generateShell.py

cd ~/plutus
sh -x wgetYrFin.sh

cd ~/fortuna/fortuna/src
python3 processFinYr.py

exit
