# 🏢 Leave Management System (LMS)

---

## 👨‍💻 Introduction

Hello, I am Rohith.

This project is an API-based **Leave Management System** designed to automate and streamline employee leave handling.

It provides a centralized platform for employees and administrators to manage leave efficiently.

---

## ❗ Problem Statement

In many organizations, leave management is handled manually using emails or Excel sheets.

### ⚠️ Issues

| Problem                | Description                                   |
|----------------------|-----------------------------------------------|
| No Centralization    | Data scattered across emails or sheets        |
| Slow Approval        | Manual verification delays decisions          |
| Lack of Transparency | Employees cannot track leave status           |
| Data Errors          | High chance of mistakes in manual entries     |
| No Validation        | Invalid data like past dates allowed          |

---

### 🎯 Solution

- Automated system  
- Centralized database  
- Real-time tracking  
- Proper validation  

---

## 🔍 Project Overview

### 👥 User Roles

| Role      | Actions                                      |
|-----------|----------------------------------------------|
| Employee  | Apply, View, Update, Delete Leave            |
| Admin     | View, Approve, Reject Leave                  |

---

### 🔄 Workflow
# 🏢 Leave Management System (LMS)

---

## 👨‍💻 Introduction

Hello, I am Rohith.

This project is an API-based **Leave Management System** designed to automate and streamline employee leave handling.

It provides a centralized platform for employees and administrators to manage leave efficiently.

---

## ❗ Problem Statement

In many organizations, leave management is handled manually using emails or Excel sheets.

### ⚠️ Issues

| Problem                | Description                                   |
|----------------------|-----------------------------------------------|
| No Centralization    | Data scattered across emails or sheets        |
| Slow Approval        | Manual verification delays decisions          |
| Lack of Transparency | Employees cannot track leave status           |
| Data Errors          | High chance of mistakes in manual entries     |
| No Validation        | Invalid data like past dates allowed          |

---

### 🎯 Solution

- Automated system  
- Centralized database  
- Real-time tracking  
- Proper validation  

---

## 🔍 Project Overview

### 👥 User Roles

| Role      | Actions                                      |
|-----------|----------------------------------------------|
| Employee  | Apply, View, Update, Delete Leave            |
| Admin     | View, Approve, Reject Leave                  |

---

### 🔄 Workflow
Employee Login
↓
Apply Leave
↓
Store in Database
↓
Admin Reviews
↓
Approve / Reject
↓
Status Updated
↓
Employee Views Result


---

## ⚙️ Technology Stack

| Technology   | Purpose                             |
|-------------|-------------------------------------|
| FastAPI     | Backend API development             |
| Pydantic    | Data validation                     |
| SQLAlchemy  | ORM for database interaction        |
| PostgreSQL  | Database storage                    |
| Streamlit   | Frontend UI                         |
| Uvicorn     | Backend server                      |
| Requests    | API communication                   |

---

---

## 🗄️ Database Design

### 📋 Users Table

| Field         | Description        |
|--------------|--------------------|
| id           | Primary key        |
| name         | Employee name      |
| email        | Email address      |
| employee_id  | Unique ID          |
| password     | Login password     |
| role         | Admin / Employee   |

---

### 📋 Leave Table

| Field       | Description                     |
|------------|---------------------------------|
| id         | Leave ID                        |
| user_id    | Foreign key                     |
| leave_type | Type of leave                   |
| start_date | Start date                      |
| end_date   | End date                        |
| reason     | Leave reason                    |
| status     | Pending / Approved / Rejected   |

---

---

## 🔌 Backend APIs

| API               | Method | Description            |
|------------------|--------|------------------------|
| /login           | POST   | Authenticate user      |
| /leave           | POST   | Apply leave            |
| /leave/{id}      | GET    | View leave             |
| /leave/{id}      | PUT    | Update leave           |
| /leave/{id}      | DELETE | Delete leave           |
| /approve/{id}    | PUT    | Approve leave          |
| /reject/{id}     | PUT    | Reject leave           |

---

## 🧠 Business Logic

### ✅ Rules Implemented

- Leave cannot be applied for past dates  
- End date must be greater than start date  
- Only pending leaves can be updated or deleted  
- Only admin can approve or reject  
- Completed leaves are hidden  

---

---

### 📊 Logic Summary

| Condition             | Action             |
|----------------------|-------------------|
| Past date            | Rejected          |
| Invalid date range   | Error             |
| Non-pending update   | Not allowed       |
| Admin action         | Status updated    |

---

## 💻 Frontend Features

| Feature        | Description                         |
|---------------|-------------------------------------|
| Login         | Employee/Admin authentication       |
| Apply Leave   | Submit leave request                |
| View Leaves   | Display leave history               |
| Update Leave  | Modify existing leave               |
| Delete Leave  | Remove leave request                |
| Admin Panel   | Approve/Reject leaves               |

---

## 🎯 Conclusion

The Leave Management System provides a structured and automated approach to managing employee leaves.

---

### 📚 Learnings

- Full-stack development  
- API design  
- Database management  

---

### ⚠️ Challenges

- Backend integration  
- UI limitations  

---

### 🚀 Future Enhancements

- JWT Authentication  
- Email notifications  
- Advanced UI (React)  
- Leave balance tracking  

---

## 🙏 Thank You
