
#DRIVE_D
sudo adduser dev vboxsf

#ubuntu desktop
sudo apt install gnome-tweaks
dbeaver https://computingforgeeks.com/install-and-configure-dbeaver-on-ubuntu-debian/

#mysql
sudo apt install mysql-server
sudo mysql
mysql -u dev -p
GRANT ALL PRIVILEGES ON *.* TO 'dev'@'localhost';
mysql -u pymain -p
GRANT ALL PRIVILEGES ON *.* TO 'pymain'@'localhost';

#vue
sudo npm install -g @vue/cli
vue --version
npm i leaflet vue2-leaflet --save
npm i --save vue2-leaflet-markercluster
npm i --save vue2-leaflet-draw-toolbar
npm i @geoman-io/leaflet-geoman-free
npm i --save leaflet-editable
npm i --save @mdi/font
vue create front
cd front
npm run serve

#sublime
sublime-merge
	https://www.sublimemerge.com/download
	из deb-пакета
FileIcons
Terminus
Python Breakpoints
	https://habr.com/ru/post/104086/
	ctrl+shift+b
jQuery
bottom bar -> spaces 4 -> convert identation to spaces
Color Highlighter
    "trim_trailing_white_space_on_save": true,
Vue Syntax Highlight
PyYapf

#venv
sudo apt install python3-dev default-libmysqlclient-dev build-essential

virtualenv --version
virtualenv -p python3.8 env

pip install mysqlclient
pip install psycopg2-binary # pqsql
pip install Django
pip install geojson
pip install requests
pip install rply			# lexer parser

pip install pytest			# tests
pip install flake8

pip freeze > requirements.txt
pip install -r requirements.txt

python3 manage.py runserver 0.0.0.0:8000

#git
sudo apt install git
git init
git config --global user.name "vg"
git config --global user.email "vgena09@gmail.com"
git remote add github github:vgena09/sp.git
git add .
git commit -m "start"
git branch -M main
git push github main
git push -u --force github main

git branch struct		создать ветку
git checkout struct     переключиться на ветку

#ssh
sudo apt install ssh
# https://docs.github.com/en/github/authenticating-to-github/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent
ssh-keygen -t ed25519 -C "vgena09@gmail.com"
chmod 400 ~/.ssh/github
copy github.pub to clipboard
paste settings/Deploy keys/
ssh -T git@github.com
yes
nano /home/dev/.ssh/config
'''
Host github
    HostName ssh.github.com
    Port 443
    User git
    PreferredAuthentications publickey
    IdentityFile ~/.ssh/github
'''
sudo service ssh restart

#PROJECT
django-admin startproject sp .
python3 manage.py startapp admin_dop
python3 manage.py startapp authent
python3 manage.py startapp map
python3 manage.py startapp graph
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py createsuperuser --username=sysadmin
python3 manage.py runserver 0.0.0.0:8000


#dbForge MySQL
для отображения русских символов установить галочку "Использовать Юникод" в редакторе соединения на страничке "Дополнительные"

Убрать предупреждение о медленной сети
chrome://flags/#force-effective-connection-type



#Настройка virtualBox
http://rus-linux.net/MyLDP/vm/VirtualBox-networking.html
включить виртуальный адаптер хоста
192.168.56.1   - хост
192.168.56.101 - гость
ip route show

sudo apt-get install mysql-client
mysql --host=192.168.56.1 --user=pymain -p
sudo apt-get remove libaio1 mysql-client mysql-client-5.7 mysql-client-core-5.7

cd [WORK_DIR]
git init
virtualenv --no-site-packages -p python3.6 env
source env/bin/activate
#pip install pip-tools
#    click, pip-tools
pip install django
pip install mysqlclient
pip install mysql-python не ставит так как медленнее (первый на C)
pip install django_compressor
    django-appconf, django-compressor, rcssmin, rjsmin, six
#pip install django-bootstrap4
#    soupsieve, beautifulsoup4, django-bootstrap4
