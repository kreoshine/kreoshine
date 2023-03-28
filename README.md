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

6. Run main backend application 
```angular2html
python -m app.backend.services.main.run
```

7. Enjoy with develop