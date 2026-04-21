# FinSight – Personal Expense Tracker

FinSight is a full‑stack personal finance application designed to help users track expenses, set financial goals, and gain insights into their spending habits. The project currently includes a secure authentication system, a points‑based gamification layer, and a modern React dashboard. Future iterations will incorporate machine learning for intelligent expense categorization and personalized financial advice.


## ✨ Features

### ✅ Implemented
- **User Authentication** – Secure registration/login with JWT and bcrypt password hashing.
- **Points & Gamification** – Earn points for creating/completing goals and taking quizzes.
- **Transaction Logging** – Record and retrieve point transactions with audit trail.
- **Modern Dashboard** – Responsive React UI with dynamic charts and clean design.
- **RESTful API** – Flask backend with MongoDB for scalable data storage.

### 🚧 Planned (Roadmap)
- **ML‑Based Expense Classification** – Automatically categorize transactions using scikit‑learn.
- **Budget Alerts & Insights** – Notifications and spending trend analysis.
- **Bank Integration** – Plaid API for automatic transaction syncing.
- **Export Reports** – PDF/CSV generation for financial summaries.

## 🛠 Tech Stack

| Frontend               | Backend                | Database      |
|------------------------|------------------------|---------------|
| React 19               | Flask (Python 3.10+)   | MongoDB Atlas |
| Vite                   | PyJWT, bcrypt          | PyMongo       |
| Chart.js / Recharts    | Flask‑CORS             |               |
| Axios                  | python‑dotenv          |               |

## 📁 Project Structure
```text
FinSight/
├── backend/
│ ├── auth.py # Authentication & points API
│ ├── requirements.txt # Python dependencies
│ └── .env.example # Environment variable template
├── frontend/
│ ├── src/
│ │ ├── components/ # Reusable UI components
│ │ ├── pages/ # Dashboard, Login, Register, etc.
│ │ ├── context/ # React context for state management
│ │ └── App.jsx # Main routing
│ ├── index.html # Vite entry point
│ ├── package.json
│ └── vite.config.js
└── README.md
```


## 🚀 Getting Started

Follow these instructions to run FinSight locally on your machine.

### Prerequisites
- Python 3.10+
- Node.js 18+ and npm
- MongoDB Atlas account (or local MongoDB instance)

### 1. Clone the Repository
```bash
git clone https://github.com/ShikharNotFound/FinSight_Personal-Expense-Tracker.git
cd FinSight_Personal-Expense-Tracker
```
2. Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```
Create a .env file in the backend/ directory using the template below:

env
```bash
MONGO_URI=mongodb+srv://<username>:<password>@cluster.mongodb.net/?retryWrites=true&w=majority
JWT_SECRET_KEY=your-strong-secret-key-here-min-32-chars
DB_NAME=FinSightDB
AUTH_PORT=8001
INITIAL_USER_POINTS=100
```

Start the Flask server:

```bash
python auth_server.py
```
The API will be available at http://localhost:8001.


3. Frontend Setup
Open a new terminal:

```bash
npm install
npm run dev
```
The React development server will start at http://localhost:5173.

4. Access the Application
Visit http://localhost:5173 in your browser. Register a new account to start using FinSight.

