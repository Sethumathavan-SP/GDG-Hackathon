# AI-Powered Medical Diagnosis System

## Overview
This project is a **Streamlit-based web application** that utilizes **AI-driven medical image analysis** to assist doctors in diagnosing diseases. The system allows users to upload medical images, get AI-generated diagnostic reports, and facilitates **efficient patient-doctor interactions**.

## Features
- **User Authentication** – Secure login & signup with MySQL database  
- **AI-Based Disease Analysis** – Processes medical images and provides diagnostic insights  
- **Doctor Dashboard** – Displays patient reports ranked by severity  
- **Remote Diagnosis Support** – Expands healthcare access in rural areas  

## Technologies Used
- **Python** (Streamlit, PIL, Pandas)  
- **AI Model** (Integrated as `AI_analysis` module)  
- **MySQL** (Stores user & diagnosis data)  
- **Base64 Encoding** (Image storage & retrieval)  

## Setup Instructions

### 1. Install Dependencies
```bash
pip install streamlit mysql-connector-python pillow pandas
```

### 2. Configure MySQL Database
- Create a MySQL database named `users`  
- Use the following schema for `users` and `report` tables:  
```sql
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) UNIQUE,
    password VARCHAR(255),
    email VARCHAR(255) UNIQUE,
    type ENUM('user', 'doctor'),
    address TEXT,
    phoneNumber VARCHAR(20)
);

CREATE TABLE report (
    id INT AUTO_INCREMENT PRIMARY KEY,
    disease VARCHAR(255),
    name VARCHAR(255),
    phoneNumber VARCHAR(20),
    email VARCHAR(255),
    image LONGBLOB,
    severity INT
);
```

### 3. Run the Application
```bash
streamlit run app.py
```

## Usage
1. **Users** upload medical images for AI analysis  
2. **Doctors** review reports sorted by severity  
3. **AI insights** assist in quick and accurate diagnosis  

## Future Enhancements
🚀 **Expand AI model capabilities**  
📡 **Integrate cloud-based remote consultation**  
📊 **Improve reporting and data visualization**  
