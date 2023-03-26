***GUIDE to local deployment:***

1. Choose a location for the repository on your local machine and clone the repository:
```angular2html
git clone git@github.com:kreoshine/backend.git
```
2. Change working directory:
```angular2html
cd backend/
```
3. Choose necessary branch by ```git checkout 'target_branch'```
4. Make sure the Python version is as required (==3.11) on your local machine 
5. Create the virtual environment of Python of your choice
(PIP is preferred as a package manager for Python packages: conda or just venv are the best choice)

If you choose venv here you go:
```angular2html
python -m venv deploy/venv
```
```angular2html
source deploy/venv/bin/activate
```
6. Install deploy requirements (if you choose PIP, bellow command will help you)
```angular2html
pip install -r deploy/pip-freeze.txt
```
7. Initiate deployment (don't worry, it's gonna be in 'development' mode)
```angular2html
python deploy/
```

***Steps below will be probably removed in the future for easily deployment!***

Keep a little calm for some more action:

8. Deactivate previous environment
```angular2html
deactivate
```
9. Create and activate env for application
```angular2html
python -m venv venv
```
```angular2html
source venv/bin/activate
```
10. Install app requirements (if you choose PIP, bellow command will help you)
```angular2html
pip install -r pip-freeze.txt
```
11. Run backend application 
```angular2html
python run.py
```

12. Enjoy with develop:
- Verify that the service.log file has been created in the 'tmp' directory located in the project dir. 
(Probably it will appear in IDE after you stop service) 


***NOTE: do not commit the dev-settings.yaml file!!!***