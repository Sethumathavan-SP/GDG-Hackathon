from PIL import Image
import streamlit as st
import mysql.connector
import AI_analysis as AI
import base64
import io
import pandas as pd

conn = mysql.connector.connect(
    host="localhost",
    user="root",     
    password="1234",
    database="users"  
)

cursor = conn.cursor()
def image_to_base64(binary_image):
    image = Image.open(io.BytesIO(binary_image))
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

def pil_to_blob(image, format="PNG"):
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format=format)
    return img_byte_arr.getvalue()

def check_signup(username, email):
    cursor.execute("Select * from users")
    for data in  cursor.fetchall():
        if username == data[1]:
            st.error("Username already exists. Please choose a different one.")
            return False
        elif email == data[3]:
            st.error("Email already in use. Please use a different email address.")
            return False
    return True

def check_login(username, password):
    cursor.execute("Select * from users")
    for data in  cursor.fetchall():
        if (username.lower() == data[1].lower() or username.lower() == data[3].lower()) and password.lower() == data[2].lower():
            return [True,data[4],data[3],data[5],data[6]]
    return [False]

def login_page():
    st.markdown("<h1 style='text-align: center;'>Login Page</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([2, 3, 2])
    col4, col5, col6, col7 = st.columns([2.45, 2, 2, 2])
    with col2:
        username = st.text_input(r"Username\Email", placeholder="Enter your username", max_chars=20)
        password = st.text_input("Password", type="password", placeholder="Enter your password", max_chars=20)
        with col5:
            if st.button("Login"):
                check = check_login(username, password)
                if check[0]:
                    st.session_state.logged_in = True
                    st.session_state["email"] = check[2]
                    st.session_state["address"] = check[3]
                    st.session_state["phoneNumber"] = check[4]
                    st.session_state["username"] = username
                    st.session_state.page = "welcome"
                    if(check[1] == 'user'):
                        st.session_state.user = True
                    else:
                        st.session_state.docter = True
                else:
                    st.error("Invalid credentials")
            
        with col6:
            if st.button("Go to Sign Up"):
                st.session_state.page = "signup"
        

def signup_page():
    st.markdown("<h1 style='text-align: center;'>Sign Up</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1.25,3,1.25])
    col4, col5, colSpace, col6, col7 = st.columns([1.15,1,1,1,1])
    with col2:
        username = st.text_input("Username", placeholder="Choose a username")
        email = st.text_input("Email", placeholder="Enter your email")
        password = st.text_input("Password", type="password", placeholder="Choose a password")
        confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password")
        address = st.text_input("address",placeholder="Enter address")
        contact = st.text_input("phone No.",placeholder="Enter phone number")
        with col5:
            if st.button("Sign Up"):
                if password != confirm_password:
                    st.error("Passwords do not match. Please try again.")
                else:
                    with col1:    
                        if check_signup(username, email):
                            cursor.execute("INSERT INTO users (name, password, email,type,address,phoneNumber) VALUES (%s, %s, %s, 'user', %s,%s)", (username, password, email,address,contact))
                            conn.commit()
                            cursor.close()
                            conn.close()
                            st.session_state.signed_up = True
                            st.session_state["username"] = username
                            st.success("You have successfully signed up!")
                            st.session_state.page = "login"
        with col6:
            if st.button("Go to Login"):
                st.session_state.page = "login"

def user_page():
    uploaded_file = st.file_uploader("Choose an image", type=["jpg", "png", "jpeg"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        col1,col2,col3 = st.columns(3)
        with col1:
            st.image(image, caption="Uploaded Image", use_container_width=2)
        AI_report = AI.analyze(image)
        st.write("Our experienced doctors will reach out to you shortly and provide the best care. Rest assured, you're in good hands.")
        st.title("AI Report:")
        st.write(AI_report)
        diseaseNAme = AI.get_keyword(AI_report)
        cursor.execute("select disease,severity from report;")
        severityScore = AI.severity_score(cursor.fetchall(),diseaseNAme)
        cursor.execute("insert into report(disease,name,phoneNumber,email,image,severity) values(%s,%s,%s,%s,%s,%s  )",(diseaseNAme,st.session_state["username"],st.session_state["phoneNumber"],st.session_state["email"],pil_to_blob(image),severityScore))
        conn.commit()

def docter_page():
    st.markdown("<h1 style='text-align: center;'>Reports</h1>", unsafe_allow_html=True)
    st.write(f"Hello doctor {st.session_state['username']}!")
    cursor.execute("SELECT disease, name, phoneNumber, email, image FROM report order by severity desc")
    data = cursor.fetchall()

    processed_data = []
    for row in data:
        image_base64 = image_to_base64(row[4])
        processed_data.append(row[:4] + (image_base64,))

    if "processed_data" not in st.session_state:
        st.session_state.processed_data = [ row[:4] + (image_to_base64(row[4]),) for row in data ]

    html = "<table style='width:100%;border:1px solid black;'>"
    html += "<tr><th>Disease</th><th>Name</th><th>Phone Number</th><th>Email</th><th>Image</th><th>Action</th></tr>"

    col1,col2 = st.columns([1,6])

    for i, row in enumerate(st.session_state.processed_data):
        html += f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td><td>{row[3]}</td>"
        html += f"<td><img src='data:image/png;base64,{row[4]}' width='100' height='100'></td>"
        with col1:
            if st.button(f"complete", key=f"delete_{i}"):
                st.session_state.processed_data.pop(i)
                st.rerun()
    html += "</table>"

    with col2:
        st.markdown(html, unsafe_allow_html=True)

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if 'user' not in st.session_state:
    st.session_state.user = False

if 'docter' not in st.session_state:
    st.session_state.docter = False

if 'page' not in st.session_state:
    st.session_state.page = "login"

if st.session_state.logged_in:
    if st.session_state.user:
        user_page()
    elif st.session_state.docter:
        docter_page()
else:
    if st.session_state.page == "login":
        login_page()
    elif st.session_state.page == "signup":
        signup_page()
