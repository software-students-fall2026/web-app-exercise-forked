# Web Application Exercise

A little exercise to build a web application following an agile development process. See the [instructions](instructions.md) for more detail.

## Team members
- [Jack Jiang](https://github.com/jack-k-jiang)
- [Ruikun Xu](https://github.com/xuruikun)
- [Shuo Cao](https://github.com/ShuoWu6529)
- [Ronald Szeto](https://github.com/ronaldszeto)
- [Eric Wu](https://github.com/ew2725)

## Product vision statement

Forked is an application that allows people of all ages to trade their skills by matching interests and allowing them to meet up to teach & learn.

## User stories

[User Stories](https://github.com/software-students-fall2026/web-app-exercise-forked/issues) 

## Steps necessary to run the software

### 1. Prerequisites

- Python
- Git
- Access to a MongoDB database

### 2. Clone the repository

Clone a copy of this repository to your local machine from GitHub and open the repository directory.

```bash
git clone https://github.com/software-students-fall2026/web-app-exercise-git-forked.git
cd web-app-exercise-forked
```

### 3. Configure Python virtual environment

First, create a virtual environment with the name ```.venv```. Then, activate the virtual environment and install the required dependencies.

#### Create a virtual environment:
```bash
python -m venv .venv
```

#### Activate the virtual environment:

**On Windows:**
```bash
.venv\Scripts\activate.bat
```

**On macOS/Linux:**
```bash
source .venv/bin/activate
```

#### Install the required dependencies:
```
pip install -r requirements.txt
```

### 4. Configure environment files

Create a ```.env``` file and copy ```.env.example``` into it:
```bash
cp .env.example .env
```

Then, replace the dummy variables with their respective values:
- ```MONGO_URI```: The MongoDB connection string: ```mongodb+srv://<username>:<password>@<cluster-url>/```
- ```MONGO_DBNAME:```: The database name, e.g. ```Forked```
- ```SECRET_KEY```: A random string used for Flask sessions

### 5. Run the Flask app

Run the app with the following command:
```bash
flask run
```

To access the application in your web browser, visit the link [http://127.0.0.1:5000](http://127.0.0.1:5000). To stop the app at any point, press CTRL+C. 

## Task boards

- [Sprint 1](https://github.com/orgs/software-students-fall2026/projects/2/views/1)
- [Sprint 2](https://github.com/orgs/software-students-fall2026/projects/71)