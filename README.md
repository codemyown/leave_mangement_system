# 🧾 Leave Management System

A Python Django-based Leave Management System for handling employee leave requests, approvals, and balance tracking.  
Easily deployable using **Docker** and **PostgreSQL**.

---

## 🚀 Setup Instructions (Docker)

For a fast walkthrough of the Docker setup, watch the video here:  
[Watch Video](https://drive.google.com/file/d/10zGOMXtCFnwT6nztZEtD9AWD_-nAfazx/view?usp=sharing)

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/codemyown/leave_mangement_system.git
cd leave_mangement_system
```

---

### 2️⃣ Prerequisites
Make sure Docker and Docker Compose are properly installed on your system.

---

### 3️⃣ Environment Setup
Create a `.env` file in the project root and add the following:

```bash
POSTGRES_HOST=db
POSTGRES_PORT=5432
POSTGRES_DB=mydb123
POSTGRES_USER=bhanu123
POSTGRES_PASSWORD=bhanu
```

> ⚙️ You can modify the values as per your setup.

---

### 4️⃣ Build and Run the Containers
```bash
docker-compose up --build -d
```

If already built, simply run:
```bash
docker-compose up -d
```

---

### 5️⃣ Access the Application
Once the containers are running, open your browser and go to:

👉 **http://localhost:8000**

---

## 🧩 Default Services
- **Backend:** Django (Python 3.12)
- **Database:** PostgreSQL
- **Server:** Gunicorn
- **Reverse Proxy:** Nginx (optional, if configured)

---

## 🛠️ Useful Docker Commands

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

## 📸 Demo Video
[🎥 Watch Project Demo](https://drive.google.com/file/d/1CzkiKfz21qvxce7AH8Sz9CJmwk46P65Z/view?usp=sharing)

---

**Developed by:** *MR Softwares*
