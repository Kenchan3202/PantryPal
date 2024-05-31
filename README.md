# PantryPal

PantryPal is a grocery web app tracker designed to help users manage their pantry inventory, create shopping lists, and organize recipes efficiently. This README file provides instructions on how to run the system, install dependencies, and initialize the database.

## Repository URL
GitHub Repository: [https://github.com/newcastleuniversity-computing/CSC2033_Team44_23-24/tree/master](https://github.com/newcastleuniversity-computing/CSC2033_Team44_23-24/tree/master)

## Getting Started

### Prerequisites
Make sure you have the following installed on your machine:
- Python 3.7 or higher
- Git
- Docker

### Installation

1. **Clone the Repository:**
    On GitHub:
   ```sh
   git clone https://github.com/newcastleuniversity-computing/CSC2033_Team44_23-24.git
   cd CSC2033_Team44_23-24
   ```
    On Docker:
   ```sh
    docker pull kenchan3202/csc2033-team44_web:latest
    ```

2. **Check Current Branch**
- Ensure you are on the `master` branch by running the following command in the terminal:
   ```sh
   git branch

3. **Install Dependencies**
- Run this command in the terminal
   ```sh
   pip install -r requirements.txt

### Database Initialization

1. **Initialize the Database**
- Open a python console and run the following commands:
   ```sh
  from app import db
  from models import init_db
  init_db()

2. Populate the Database
- To populate the database with sample data, run the following command in the terminal:
   ```sh
  python populate_db.py

### Running Application
There are two ways to run the application:

#### Method 1: Run Locally

To run the application locally execute the following command:
```sh
python app.py
```

#### Method 2: Run with Docker

1. Update Your System (Linux):
```sh
sudo apt-get update
```
2. Install Docker
```sh
curl -fsSL https://test.docker.com -o test-docker.sh
sudo sh test-docker.sh
```
3. Navigate to Your Project Directory:
```sh
cd /path/to/your/project/
```
4. Run the Docker Container:
```sh
docker run -d -p 5000:5000 theimagenamewithlowercase
```
5. Run App with Docker Compose:
```sh
docker-compose up
```


### Additional Information
1. Sample User Login Details (after running populate_db.py):

Email: gathelstan0@npr.org  
Password: pO6>#*9hV

2. Admin Access:
- To access the admin page, use the following credentials:

Email: admin@email.com  
Password: Admin1!
 
3. Documentation:
- To view the documentation for GUI, team coding, and testing, refer to the documentation folder in the repository.

