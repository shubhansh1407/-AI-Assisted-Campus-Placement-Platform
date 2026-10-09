from database.database import initialize_database, insert_student, insert_company_role, insert_placement, insert_user

def populate():
    print("Initializing database...")
    initialize_database()

    print("Creating Student Auth Accounts...")
    for i in range(1, 24):
        insert_user(f"student{i}", f"pass{i}", "student")

    print("Inserting sample students...")
    students_data = [
        ("student1", "Rahul Sharma", "Computer Science", 8.5, "Python, SQL, HTML, CSS, Git, JavaScript, React", "Portfolio Website", "AWS Cloud Practitioner"),
        ("student2", "Priya Patel", "Information Technology", 9.1, "Python, Pandas, Machine Learning, SQL, NumPy, Statistics", "House Price Prediction", "Coursera ML Specialization"),
        ("student3", "Amit Kumar", "Electronics", 7.8, "C++, Java, OOP, Communication", "Smart Attendance System", ""),
        ("student4", "Sneha Gupta", "Computer Science", 8.2, "Java, Spring Boot, SQL, Git", "E-commerce Backend", "Oracle Certified Associate"),
        ("student5", "Rohan Verma", "Mechanical", 7.5, "AutoCAD, SolidWorks, Excel, Communication", "Drone Design", ""),
        ("student6", "Anjali Singh", "Electrical", 8.8, "MATLAB, C, IoT, Python", "Smart Grid Model", "IoT fundamentals"),
        ("student7", "Vikram Rathore", "Computer Science", 7.9, "Python, Django, React, JavaScript, HTML, CSS", "Social Media Clone", ""),
        ("student8", "Neha Reddy", "Information Technology", 8.4, "HTML, CSS, JavaScript, React, Git, Communication", "Weather App", "FreeCodeCamp Frontend"),
        ("student9", "Aditya Joshi", "Civil", 7.2, "AutoCAD, STAAD Pro, Excel", "Bridge Design", ""),
        ("student10", "Kiran Desai", "Computer Science", 9.3, "Python, TensorFlow, Deep Learning, Machine Learning, NumPy, Pandas", "Image Recognition App", "Deep Learning Specialization"),
        ("student11", "Manoj Tiwari", "Electronics", 7.6, "C, Microcontrollers, C++, Communication", "Automated Irrigation", ""),
        ("student12", "Pooja Mehta", "Computer Science", 8.1, "Java, Android Studio, Git, SQL", "Expense Tracker App", ""),
        ("student13", "Siddharth Nair", "Mechanical", 8.0, "Ansys, CATIA, Excel, Power BI", "Formula Student Car", ""),
        ("student14", "Deepika Pillai", "Information Technology", 8.6, "Python, AWS, Docker, Git, SQL", "Serverless API", "AWS Solutions Architect"),
        ("student15", "Karan Singh", "Civil", 7.4, "Surveying, AutoCAD, Excel", "Township Layout", ""),
        ("student16", "Ishita Bose", "Electrical", 8.5, "PLC, SCADA, Python, Data Analysis", "Substation Automation", ""),
        ("student17", "Gaurav Malhotra", "Computer Science", 7.7, "C++, Data Structures, Algorithms, Git, Communication", "Competitive Programming tracker", ""),
        ("student18", "Tanya Agarwal", "Information Technology", 9.0, "Node.js, Express, MongoDB, JavaScript, React, HTML, CSS", "Chat Application", "MongoDB Certified"),
        ("student19", "Arjun Das", "Mechanical", 7.9, "Robotics, Python, Excel, Communication", "Line Follower Robot", ""),
        ("student20", "Meera Krishnan", "Computer Science", 8.9, "Python, NLP, Pandas, Machine Learning, Statistics, NumPy", "Sentiment Analyzer", ""),
        ("student21", "Nikhil Rao", "Electronics", 8.2, "VHDL, Verilog, C, Python", "Processor Design", ""),
        ("student22", "Swati Mishra", "Information Technology", 7.8, "SQL, Power BI, Tableau, Excel, Pandas, Communication", "Sales Dashboard", "Google Data Analytics"),
        ("student23", "Vivek Jain", "Computer Science", 8.4, "Go, Kubernetes, Docker, Python, Git", "Microservices Platform", "CKAD")
    ]
    
    for s in students_data:
        insert_student(*s)

    print("Inserting sample company roles...")
    insert_company_role("TCS", "Software Developer", 7.0, "Java, SQL, OOP", "7 LPA")
    insert_company_role("Deloitte", "Data Analyst", 7.5, "Python, SQL, Excel", "8.5 LPA")
    insert_company_role("Accenture", "Business Analyst", 6.5, "Communication, SQL, Excel", "6.5 LPA")
    insert_company_role("Infosys", "ML Engineer", 8.0, "Python, Machine Learning, Pandas, SQL", "10 LPA")
    insert_company_role("Microsoft", "SDE", 8.5, "Data Structures, Algorithms, C++, Java", "40 LPA")
    insert_company_role("Amazon", "Cloud Support Engineer", 7.5, "AWS, Linux, Networking", "15 LPA")
    insert_company_role("L&T", "Design Engineer", 7.0, "AutoCAD, SolidWorks", "6 LPA")

    print("Inserting sample placements...")
    placements = [
        ("student1", "TCS", "Software Developer", "7 LPA", 2025),
        ("student2", "Infosys", "ML Engineer", "10 LPA", 2025),
        ("student4", "TCS", "Software Developer", "7 LPA", 2024),
        ("student6", "TCS", "Software Developer", "7 LPA", 2023),
        ("student8", "Accenture", "Business Analyst", "6.5 LPA", 2025),
        ("student10", "Microsoft", "SDE", "40 LPA", 2025),
        ("student14", "Amazon", "Cloud Support Engineer", "15 LPA", 2024),
        ("student17", "Accenture", "Business Analyst", "6.5 LPA", 2023),
        ("student18", "Deloitte", "Data Analyst", "8.5 LPA", 2024),
        ("student20", "Infosys", "ML Engineer", "10 LPA", 2025),
        ("student22", "Deloitte", "Data Analyst", "8.5 LPA", 2025),
        ("student23", "Amazon", "Cloud Support Engineer", "15 LPA", 2025)
    ]
    
    for p in placements:
        insert_placement(*p)

    print("Sample data populated successfully!")

if __name__ == "__main__":
    populate()
