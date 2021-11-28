text="                                                                  
__   ___ __ ___  _ __ ___   __ _ _ __  
\ \ / / '_ ' _ \| '_ ' _ \ / _' | '_ \ 
 \ V /| | | | | | | | | | | (_| | | | |
  \_/ |_| |_| |_|_| |_| |_|\__,_|_| |_|
                                                               
"

echo "$text"
echo "Installing vmman docker image manager"
echo ""

chmod +x vmman.py
chmod +x container_ids.cfg
cp vmman.py /bin/vmman
cp container_ids.cfg /home/container_ids

echo "Installing python requirements"
echo ""
pip3 install -r requirements.txt

