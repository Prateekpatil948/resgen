
# Resume Generator (ResGen)

A **Django-based Resume Generator** web application that allows users to create, preview, and download professional resumes in PDF format.

This project provides a user-friendly interface to generate resumes based on user input. Users can enter their personal, education, work experience, skills, and other relevant details to dynamically generate a formatted resume.

Live Demo : https://resgen-0uya.onrender.com/
---

## 🛠️ Features

✔️ User Authentication (Sign Up / Login)  
✔️ Add & Edit Personal Information  
✔️ Add Multiple Education & Experience Entries  
✔️ Skills, Projects & Achievements Sections  
✔️ Preview Resume in Browser  
✔️ Export Resume as PDF  
✔️ Fully Responsive UI  

---

## 📁 Project Structure

```
resgen/
├── manage.py
├── db.sqlite3
├── requirements.txt
├── users.json
├── datadump.json
├── <Django apps and templates…>
```

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Prateekpatil948/resgen.git
cd resgen
```

### 2. Create & activate virtual environment

```bash
# Linux / Mac
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply migrations

```bash
python manage.py migrate
```

### 5. Seed initial data (optional)

```bash
python manage.py loaddata users.json
python manage.py loaddata datadump.json
```

### 6. Run the development server

```bash
python manage.py runserver
```

Open your browser and go to:  
➡️ http://127.0.0.1:8000/

---

## 🧑‍💻 Usage

1. Sign up / Login  
2. Complete your profile  
3. Fill in education, experience, and skills  
4. Generate resume  
5. Download resume as PDF  

---

## 📦 Dependencies

All required libraries are listed in `requirements.txt`.

---

## 🙌 Contributions

Contributions are welcome!  
Feel free to fork the repository and submit a pull request.

---

## 📄 License

This project is open-source and free to use.

---

## 📞 Contact

**Prateek Patil**  
GitHub: https://github.com/Prateekpatil948
Email: prateekpatil948@gmail.com
