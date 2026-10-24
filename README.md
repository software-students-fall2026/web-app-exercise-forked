# Web Application Exercise

A little exercise to build a web application following an agile development process. See the [instructions](instructions.md) for more detail.

## Product vision statement

Forked is an application that allows people of all ages to trade their skills by matching interests and allowing them to meet up to teach & learn.

## User stories

[User Stories](https://github.com/software-students-fall2026/web-app-exercise-forked/issues) 

## Steps necessary to run the software

### Create a Python virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment:

**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### Install required dependencies
```
pip install -r requirements.txt
```

### Configure .env file
Add this to your .env file, replace the placeholders with your MongoDB cluster, and create a secret key.
```env
MONGO_URI=mongodb+srv://<username>:<password>@<cluster-url>/
MONGO_DBNAME=your_database_name
SECRET_KEY=your_secret_key
```

### Run the Flask app
```bash
flask --app app run --debug
```

Access the app in your web browser with:
```
http://127.0.0.1:5000
```

## Task boards

[Task Board](https://github.com/orgs/software-students-fall2026/projects/2/views/1)
