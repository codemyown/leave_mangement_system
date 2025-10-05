# 🧾 Leave Management System

A Python Django-based Leave Management System for handling employee leave requests, approvals, and balance tracking.  
Easily deployable using **Docker** and **PostgreSQL**.

---

## 🎥 Demo Video
Watch this video to see the full functionality of the app:  
[Watch Demo](https://drive.google.com/file/d/1X4J3DLt6hN_vs2CtUVjb1_vPZNf_z-q7/view?usp=sharing)

---

## 🚀 Setup Instructions

### 1️⃣ Docker Setup

For a fast walkthrough of the Docker setup, watch the video here:  
[Watch Video](https://drive.google.com/file/d/10zGOMXtCFnwT6nztZEtD9AWD_-nAfazx/view?usp=sharing)

#### Steps:

1. **Clone the Repository**
```bash
git clone https://github.com/codemyown/leave_mangement_system.git
cd leave_mangement_system
```

2. **Prerequisites**
- Docker and Docker Compose installed

3. **Environment Setup**
Create a `.env` file in the project root:
```bash
POSTGRES_HOST=db
POSTGRES_PORT=5432
POSTGRES_DB=mydb123
POSTGRES_USER=bhanu123
POSTGRES_PASSWORD=bhanu
```
> ⚙️ You can modify these values as needed.

4. **Build and Run Containers**
```bash
docker-compose up --build -d
```
If already built:
```bash
docker-compose up -d
```

5. **Seed Initial Data**
```bash
# Enter container
docker exec -it leave-web-1 bash

# Run seed command
python manage.py seed_db
```

6. **Default Login Credentials (After Seeding Data)**
- **Employee:** username: `ajay`, password: `ajay`
- **Manager:** username: `vijay`, password: `vijay`
- **Admin Panel:** username: `admin`, password: `admin`

7. **Run Tests (Docker)**
```bash
# Enter container
docker exec -it leave-web-1 bash

# Run tests
python manage.py test
```

8. **Access the Application**
Open your browser:  
👉 **http://localhost:8000**

9. **Useful Docker Commands**
```bash
# Stop containers
docker-compose down

# View running containers
docker ps

# View logs
docker-compose logs -f

# Rebuild containers
docker-compose up --build
```

---

### 2️⃣ Local Setup (Without Docker)

Follow these steps if you want to run the project directly on your system:

1. **Clone the project**
```bash
git clone https://github.com/codemyown/leave_mangement_system.git
cd leave_mangement_system
```

2. **Create Python Virtual Environment**
- **Linux/Mac**
```bash
python3 -m venv venv
source venv/bin/activate
```
- **Windows**
```bash
python -m venv venv
venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Setup PostgreSQL**
- Install PostgreSQL on your system
- Create a database and user matching `.env` file
Create a `.env` file in the project root:
```bash
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=mydb123
POSTGRES_USER=bhanu123
POSTGRES_PASSWORD=bhanu
```

5. **Run Migrations**
```bash
python manage.py migrate
```

6. **Start the Server**
```bash
python manage.py runserver
```
- Open your browser at: **http://localhost:8000**

7. **Seed Initial Data**
```bash
# After running the server
python manage.py seed_db
```

8. **Default Login Credentials (After Seeding Data)**
- **Employee:** username: `ajay`, password: `ajay`
- **Manager:** username: `vijay`, password: `vijay`
- **Admin Panel:** username: `admin`, password: `admin`

9. **Run Tests (Local)**
```bash
python manage.py test
```

---

## 🧩 Default Services
- **Backend:** Django (Python 3.12)  
- **Database:** PostgreSQL  
- **Server:** Gunicorn  
- **Reverse Proxy:** Nginx (optional)

---

## 📸 Demo Video
[🎥 Watch Project Demo](https://drive.google.com/file/d/1CzkiKfz21qvxce7AH8Sz9CJmwk46P65Z/view?usp=sharing)

---

**Developed by:** *Ajay Pawar*
