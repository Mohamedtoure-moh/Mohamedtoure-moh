# ENETP - Management and Interaction Platform  

## Introduction  
ENETP (École Nationale d’Enseignement Technique et Professionnel) is a web platform designed to facilitate communication and administrative management between students and the school administration. Located in Mali, ENETP trains teachers and professionals in various technical and professional fields.  

This platform aims to:  
- Improve communication between students and the administration.  
- Enable centralized management of complaints, messages, and announcements.  
- Provide a simple and intuitive user experience using modern tools.  

---

## Distinctiveness and Complexity  

### Distinctiveness  
This platform stands out for:  
1. **Combined Features**: Manage messages, complaints, and announcements in a single space.  
2. **Dynamic Integration**: Automated email sending (confirmation, welcome), complaint status management, and interactive data display.  
3. **Accessibility**: Clear and user-friendly interface tailored to the needs of students and the administration.  

### Complexity  
The complex elements of this project include:  
- **Secure Authentication**:  
  - Session management and token handling for password reset.  
- **Multi-level Interactions**:  
  - Users can send messages or complaints.  
  - The administration can directly respond and publish announcements.  
- **Robust Backend**:  
  - Data model management using Django.  
  - Email integration and dynamic form validation.  

---

## Main Features  

1. **Registration and Login**  
   - Account creation with email validation.  
   - Secure login to access features.  

2. **Messaging**  
   - Send direct messages to the administration.  
   - View responses from the administration.  

3. **Complaints**  
   - Submit complaints with status tracking.  
   - View responses from the administration.  

4. **Announcements**  
   - Dedicated section where the administration publishes important information, with the option to include files.  

---

## File Contents  

### Frontend (HTML)  
- **layout.html**: Main template structuring all pages.  
- **login.html**: Login interface.  
- **register.html**: Registration form with validation rules.  
- **accueil.html**: Homepage with announcements and navigation options.  
- **messagerie.html**: Manage messages and complaints.  
- **message.html**: Form for sending messages.  
- **reclamation.html**: Interface for submitting complaints.  

### Backend (Python/Django)  
- **views.py**: Manages user operations, complaints, messages, and announcements.  
- **models.py**: Defines models for users, messages, complaints, and announcements.  
- **urls.py**: Declares routes for each functionality.  
- **forms.py**: Handles and validates forms.  

### Static Files  
- **styles.css**: Customized styles using Bootstrap.  
- **scripts.js**: Adds interactivity (client-side validation, notifications).  

---

## Installation Instructions  

### Prerequisites  
- Python 3.9 or higher.  
- pip to install dependencies.  
- Git to clone the project.  

### Installation Steps  
1. **Clone the repository**:  
   ```bash
   git clone the project
   cd ENETP
2. **Install dependencies:**:
    pip install -r requirements.txt
3. **Configure the database**:
    python manage.py makemigrations
    python manage.py migrate
4. **Create a superuse**:
    python manage.py createsuperuser
5. **Run the server**:
    python manage.py runserver
6. **Access the application**:
    Open a browser and go to http://127.0.0.1:8000.

## Mahamadou TOURE
