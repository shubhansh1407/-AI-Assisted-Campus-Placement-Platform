from database.database import initialize_database, insert_student, insert_company_role, insert_placement

def populate():
    print("Initializing database...")
    initialize_database()

    print("Inserting sample students...")
    insert_student("Rahul Sharma", "Computer Science", 8.5, "Python, SQL, HTML, CSS", "Portfolio Website", "AWS Cloud Practitioner")
    insert_student("Priya Patel", "Information Technology", 9.1, "Python, Pandas, ML, SQL", "House Price Prediction", "Coursera ML Specialization")
    insert_student("Amit Kumar", "Electronics", 7.8, "C++, Java, OOP", "Smart Attendance System", "")

    print("Inserting sample company roles...")
    insert_company_role("TCS", "Software Developer", 7.0, "Java, SQL, OOP", "7 LPA")
    insert_company_role("Deloitte", "Data Analyst", 7.5, "Python, SQL, Excel", "8.5 LPA")
    insert_company_role("Accenture", "Business Analyst", 6.5, "Communication, SQL, Excel", "6.5 LPA")
    insert_company_role("Infosys", "ML Engineer", 8.0, "Python, ML, Pandas, SQL", "10 LPA")

    print("Inserting sample placements...")
    insert_placement("Rahul Sharma", "TCS", "Software Developer", "7 LPA", 2025)
    insert_placement("Priya Patel", "Infosys", "ML Engineer", "10 LPA", 2025)

    print("Sample data populated successfully!")

if __name__ == "__main__":
    populate()
