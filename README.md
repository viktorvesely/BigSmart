# BigBrain

Brain part and training part of Durko

Project is divided into two sections

## Frontend

is located in the `./bigbrain` directory.
It uses vue v2 framework.

**How to install**
Make sure you have **npm** and **vue** (v2) installed
```
cd projectdirectory/bigbrain
npm install
```

**Developing**
If you want to develop something new or fix something run 
```
npm run serve
```
It launches a development server with hot reloading enabled (local code changes are automatically applied). After the server launches you can connect to it via "http://localhost:8080/".


**Building**
If you want to build the enitre project for production run
```
npm run build
```
The enitre app will be build into the `./dist` folder

## Backend

is located in the `./server` directory.
It uses flask python sever.

**Developing**
Windows:
```
cd projectdirectory/server
set FLASK_APP=main
set FLASK_ENV=development
python -m flask run
```
It launches a development server with hot reloading enabled (local code changes are automatically applied).

**Production**
Windows:
```
cd projectdirectory/server
set FLASK_APP=main
set FLASK_ENV=production
python -m flask run
```

## More info about the bigrain can be found on the wiki-page

[Wiki page](https://github.com/viktorvesely/BigSmart/wiki)
