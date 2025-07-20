# File Uploader 🔒

A secure, password-protected file sharing web application built with Flask and PostgreSQL. Upload files and share them via unique, password-protected links.

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-12+-336791.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🌟 Overview

File Uploader is a simple yet secure web application that allows users to upload files to a server and share them via unique URLs. Each file is protected with a password, ensuring only authorized users can download the shared content. Files are stored securely in a PostgreSQL database with password hashing for enhanced security.

### ✨ Key Features

- 🔐 **Password Protection**: Every uploaded file is secured with a password
- 🔗 **Unique Share Links**: Each file gets a unique UUID-based URL
- 📁 **Direct Database Storage**: Files stored as binary data in PostgreSQL
- 🛡️ **Secure Implementation**: Password hashing with PBKDF2-SHA256
- 📏 **File Size Limit**: 16MB maximum file size
- 🎨 **Clean Interface**: Simple, responsive web design
- ⚡ **Fast Access**: Indexed UUID lookups for quick file retrieval

## 🖼️ Screenshots

### Upload Page
```
┌─────────────────────────────────────────┐
│      Choose your File to Upload         │
│          (16MB max)                     │
│                                         │
│  Select File: [Choose File]             │
│                                         │
│  Set Password: [************]           │
│                                         │
│         [Upload]                        │
│                                         │
│      Created by Matej Katic             │
└─────────────────────────────────────────┘
```

### Success Page
```
┌─────────────────────────────────────────┐
│    File Uploaded Successfully!          │
│                                         │
│  Your file is now available at:         │
│  ┌───────────────────────────────────┐  │
│  │ http://localhost:5000/get-file/   │  │
│  │ abc123-def456-ghi789...           │  │
│  └───────────────────────────────────┘  │
│                                         │
│  Anyone with this URL and password      │
│  will be able to download your file.    │
│                                         │
│     [Upload Another File]               │
└─────────────────────────────────────────┘
```

## 🛠️ Tech Stack

### Backend
- **Flask** - Web framework
- **Flask-SQLAlchemy** - ORM for database operations
- **PostgreSQL** - Database for storing files and metadata
- **Passlib** - Password hashing library
- **Python-dotenv** - Environment variable management

### Frontend
- **HTML5** - Semantic markup
- **CSS3** - Styling
- **Jinja2** - Template engine

## 📋 Prerequisites

- Python 3.7 or higher
- PostgreSQL 12 or higher
- pip package manager
- Git

## 🚀 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/MatejKatic/File_Uploader.git
cd File_Uploader
```

### 2. Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up PostgreSQL Database

First, ensure PostgreSQL is installed and running. Then create the database:

```bash
# Login to PostgreSQL
psql -U postgres

# Create the database
psql -U postgres -f create_database.sql

# Set up the schema
psql -U postgres -d file_upload -f setup.sql
```

### 5. Configure Environment Variables

Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://postgres:your-password@localhost/file_upload
```

Replace `your-secret-key-here` with a secure secret key and `your-password` with your PostgreSQL password.

### 6. Run the Application
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## 📖 Usage

### Uploading a File

1. Navigate to `http://localhost:5000`
2. Click "Choose File" and select a file (max 16MB)
3. Enter a password to protect the file
4. Click "Upload"
5. Copy the generated URL to share with others

### Downloading a File

1. Open the shared URL in a browser
2. Enter the password that was set during upload
3. Click "Access File"
4. The file will download automatically

## 🗂️ Project Structure

```
File_Uploader/
│
├── app.py                 # Main Flask application
├── config.py             # Configuration settings
├── models.py             # Database models
├── requirements.txt      # Python dependencies
├── README.md            # Project documentation
│
├── create_database.sql   # Database creation script
├── setup.sql            # Database schema setup
│
├── templates/           # HTML templates
│   ├── index.html      # Upload page
│   ├── success.html    # Success page with share link
│   └── get_file.html   # Password entry page
│
└── static/             # Static files
    └── css/
        └── style.css   # Application styles
```

## 🔧 Configuration

### Application Settings (config.py)

| Setting | Description | Default |
|---------|-------------|---------|
| `SECRET_KEY` | Flask secret key for sessions | 'dev-secret-key' |
| `SQLALCHEMY_DATABASE_URI` | PostgreSQL connection string | 'postgresql://postgres:root@localhost/file_upload' |
| `MAX_CONTENT_LENGTH` | Maximum file size in bytes | 16 MB (16 * 1024 * 1024) |

### Database Schema

```sql
CREATE TABLE uploads (
  id SERIAL PRIMARY KEY,
  uuid UUID NOT NULL UNIQUE,
  filename VARCHAR(255) NOT NULL,
  file_data BYTEA NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 🔒 Security Features

### Password Protection
- Passwords are hashed using PBKDF2-SHA256
- Each file requires password authentication for download
- No plain-text passwords stored in database

### File Security
- Files stored as binary data in PostgreSQL
- Unique UUID for each file prevents URL guessing
- Secure filename handling with Werkzeug

### Application Security
- CSRF protection via Flask's SECRET_KEY
- SQL injection prevention through SQLAlchemy ORM
- File size limits to prevent abuse

## 🔌 API Endpoints

### Upload File
```
POST /
Content-Type: multipart/form-data

Parameters:
- file: The file to upload
- password: Password to protect the file

Response: HTML page with share link
```

### Get File (View Password Form)
```
GET /get-file/<uuid>

Response: HTML page with password form
```

### Download File
```
POST /get-file/<uuid>

Parameters:
- password: File password

Response: File download or error message
```

## 🚦 Development

### Running in Debug Mode
```bash
python app.py
```

### Running in Production

For production deployment, use a WSGI server like Gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

### Environment Variables for Production

```env
SECRET_KEY=strong-random-secret-key
DATABASE_URL=postgresql://user:password@host:port/database
FLASK_ENV=production
```

## 📊 Database Management

### Backup Database
```bash
pg_dump -U postgres file_upload > backup.sql
```

### Restore Database
```bash
psql -U postgres file_upload < backup.sql
```

### Clean Old Files (Optional)
```sql
-- Delete files older than 30 days
DELETE FROM uploads 
WHERE created_at < NOW() - INTERVAL '30 days';
```

## 🐛 Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Ensure PostgreSQL is running
   - Check DATABASE_URL in .env file
   - Verify database exists: `psql -U postgres -l`

2. **File Upload Fails**
   - Check file size (must be under 16MB)
   - Ensure uploads table exists
   - Check PostgreSQL logs for errors

3. **Password Not Working**
   - Passwords are case-sensitive
   - Check for trailing spaces
   - Verify password_hash column in database

### Debug Commands

```bash
# Check if database exists
psql -U postgres -c "\l" | grep file_upload

# Verify table structure
psql -U postgres -d file_upload -c "\d uploads"

# Test database connection
python -c "from app import FileUploadApp; app = FileUploadApp(); print('Connected!')"
```

## 🔄 Future Enhancements

- [ ] File expiration dates
- [ ] Multiple file uploads
- [ ] Admin dashboard
- [ ] File type restrictions
- [ ] Download counters
- [ ] Email notifications
- [ ] S3/cloud storage option
- [ ] File preview for images
- [ ] Virus scanning integration
- [ ] Rate limiting
