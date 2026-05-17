<div align="center">

# 🔎 FindIt - Campus Lost & Found
**An intelligent, centralized platform connecting students and staff to retrieve lost belongings across the campus.**

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg?style=flat-square&logo=python&logoColor=white)](https://www.python.org)
[![Flask](https://img.shields.io/badge/Flask-Framework-black.svg?style=flat-square&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Firebase](https://img.shields.io/badge/Firebase-Database-FFCA28.svg?style=flat-square&logo=firebase&logoColor=black)](https://firebase.google.com/)
[![Deployed on Render](https://img.shields.io/badge/Render-Deployed-46E3B7?style=flat-square&logo=render&logoColor=white)](https://findit-ls1x.onrender.com/)

<br/>

### [🚀 View Live Demo](https://findit-ls1x.onrender.com/) &nbsp;|&nbsp; [💻 Source Code](https://github.com/adityasahani001/FindIt)

<br/>

</div>

---

## 📖 Table of Contents
- [About the Project](#-about-the-project)
- [Key Features](#-key-features)
- [Tech Stack](#-tech-stack)
- [Project Architecture](#-project-architecture)
- [Getting Started](#-getting-started)
- [Environment Variables](#-environment-variables)
- [Matching Algorithm](#-matching-algorithm)
- [Project Structure](#-project-structure)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🚀 About the Project

**FindIt** is a highly specialized web application tailored for university campuses and organizations, designed to drastically reduce the friction of the traditional "lost and found" process. Utilizing a robust Flask backend and an AI-assisted text similarity algorithm, FindIt autonomously cross-references reported lost items with found items, immediately alerting users to potential matches.

---

## ✨ Key Features

- **🛡️ Secure Authentication**: Custom session-based authentication utilizing BCrypt password hashing.
- **🔍 Smart Matching Engine**: Automated similarity scoring (Title, Category, Location, Description) to suggest highly probable matches between lost and found items.
- **📱 Responsive UI/UX**: Clean, modern, and mobile-friendly interface styled with custom CSS.
- **☁️ Cloud Infrastructure**: Fully integrated with Google Firebase (Firestore for NoSQL database, Storage for image hosting).
- **👑 Role-Based Access Control**: Differentiated dashboards for standard Users and Administrators.
- **📊 Admin Dashboard**: Centralized management panel to oversee user activity, feedback, and reported items.

---

## 🛠️ Tech Stack

| Category          | Technology                                                                                                    |
| ----------------- | ------------------------------------------------------------------------------------------------------------- |
| **Backend**       | Python, Flask, Gunicorn                                                                                       |
| **Frontend**      | HTML5, CSS3, Vanilla JavaScript, Jinja2 Templates                                                             |
| **Database**      | Google Firebase (Firestore)                                                                                   |
| **Storage**       | Firebase Storage                                                                                              |
| **Security/Auth** | Flask-Session, BCrypt, Flask-CORS                                                                             |
| **Algorithm**     | `difflib.SequenceMatcher` (Pattern Matching)                                                                  |

---

## ⚙️ Getting Started

Follow these instructions to set up the project locally.

### Prerequisites

Ensure you have the following installed:
- [Python 3.8+](https://www.python.org/downloads/)
- [Git](https://git-scm.com/)
- A [Firebase Project](https://console.firebase.google.com/) with Firestore and Storage enabled.

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/adityasahani001/FindIt.git
   cd FindIt
   ```

2. **Create a Virtual Environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate the Virtual Environment:**
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## 🔐 Environment Variables

You must create a `.env` file in the root directory. This file stores sensitive configuration details.

```env
# Flask Settings
SECRET_KEY=your_super_secret_flask_key

# Firebase Configuration (JSON string from your service account key)
FIREBASE_CONFIG={"type": "service_account", "project_id": "...", ...}
FIREBASE_BUCKET=your-app-id.appspot.com
```
> **Warning**: Never commit your `.env` file or Firebase credentials to public version control.

---

## 🧠 Matching Algorithm

FindIt implements a sophisticated weighting system using Python's `SequenceMatcher` to evaluate the probability of a match between a lost and found item.

The algorithm calculates a composite score based on:
1. **Title Similarity (50% weight):** The primary identifier.
2. **Category Match (20% weight):** Exact categorical alignment.
3. **Location Similarity (20% weight):** Geographic proximity on campus.
4. **Description Similarity (10% weight):** Contextual details.

Matches exceeding a **0.55 threshold** are surfaced to the user.

---

## 📁 Project Structure

```text
FindIt/
│
├── app.py                  # Application entry point & Blueprint registration
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (ignored by git)
│
├── routes/                 # API & View Controllers
│   ├── admin_routes.py
│   ├── auth_routes.py
│   ├── feedback_routes.py
│   ├── item_routes.py
│   └── user_routes.py
│
├── services/               # Core Business Logic & Database interaction
│   ├── firebase_service.py # Firebase initialization & CRUD operations
│   ├── matching_service.py # AI similarity scoring algorithm
│   ├── storage_service.py  # Image upload handling
│   └── user_service.py     # User management
│
├── static/                 # Public Assets
│   └── css/
│       └── styles.css      # Core application styling
│
└── templates/              # Jinja2 HTML Views
    ├── index.html
    ├── dashboard.html
    ├── admin.html
    ├── report-lost.html
    ├── report-found.html
    └── ...
```

---

## 🤝 Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

<div align="center">
  <p>Built with ❤️</p>
</div>
