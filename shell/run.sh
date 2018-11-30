# cd ~/plutus
# rm -f -R -- */

cd ~/fortuna
rm -f -R -- */

git clone https://github.com/pyfortuna/fortuna
cp ~/fortuna.properties fortuna/config
cd fortuna/src
python3 hello.py

# cd ~/plutus
# sh -x wgetYrFin.sh

exit
