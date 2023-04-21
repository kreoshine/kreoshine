***GUIDE to local deployment:***

1. Choose a location for the repository on your local machine and clone the repository:
```angular2html
git clone git@github.com:kreoshine/kreoshine.git
```
2. Change working directory:
```angular2html
cd kreoshine/
```
3. Choose necessary branch by (currently develop)
```angular2html
git checkout develop
```
4. Make sure the Python version is as required (==3.11) on your local machine

5. Create the virtual environment of Python of your choice
(PIP is preferred as a package manager for Python packages: conda or just venv are the best choice)
```angular2html
python -m venv venv
```

6. Install requirements (if you choose venv, bellow commands will help you)
```angular2html
source venv/bin/activate
```
```angular2html
pip install -r deploy/pip-freeze.txt -r backend/app/services/index/pip-freeze.txt -r ansible/requirements.txt
```

7. Install collections for ansible
```angular2html
ansible-galaxy collection install -r ansible/requirements.yml
```

8. Create ssh keys for "root@localhost" to allow privilege escalation for Ansible:
```angular2html
mkdir .ssh/
```
```angular2html
ssh-keygen -t rsa -b 4096 -C "root@localhost" -f .ssh/id_rsa
```
Keep passphrase empty!
```angular2html
ssh-copy-id -i .ssh/id_rsa root@localhost
```
If your root password is correct but fails,
make sure to set `PermitRootLogin` to `yes` in sshd_config (/etc/ssh/sshd_config) 
and try again after ```service ssh restart```

On success way you'll see a message:
```angular2html
Number of key(s) added: 1

Now try logging into the machine, with:   "ssh 'root@localhost'"
and check to make sure that only the key(s) you wanted were added.
```

9. Initiate deployment
```angular2html
python -m deploy
```
