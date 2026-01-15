from models.medicine import Medicine
from models.sale import Sale
from datetime import datetime, timedelta

def insert_sample_data():
    # Sample medicines data
    medicines = [
        Medicine("Paracetamol", "BATCH001", 100, 5.50, 
                (datetime.now() + timedelta(days=180)).date(), "ABC Pharma"),
        Medicine("Ibuprofen", "BATCH002", 50, 7.25, 
                (datetime.now() + timedelta(days=120)).date(), "XYZ Pharma"),
        Medicine("Amoxicillin", "BATCH003", 75, 12.99, 
                (datetime.now() + timedelta(days=90)).date(), "MediCorp"),
        Medicine("Vitamin C", "BATCH004", 200, 3.75, 
                (datetime.now() + timedelta(days=365)).date(), "HealthPlus"),
        Medicine("Aspirin", "BATCH005", 150, 4.50, 
                (datetime.now() + timedelta(days=60)).date(), "PharmaOne")
    ]

    # Insert medicines
    for med in medicines:
        try:
            med.save()
            print(f"Added medicine: {med.name}")
        except Exception as e:
            print(f"Error adding {med.name}: {str(e)}")

    # Sample sales data (medicine_id will be set after medicines are inserted)
    sales = [
        Sale(1, 5, "Customer: John Doe"),
        Sale(2, 3, "Customer: Jane Smith"),
        Sale(3, 2, "Customer: Clinic A"),
        Sale(1, 10, "Customer: Hospital B"),
        Sale(4, 15, None)
    ]

    # Insert sales
    for sale in sales:
        try:
            sale.save()
            print(f"Recorded sale for medicine ID: {sale.medicine_id}")
        except Exception as e:
            print(f"Error recording sale: {str(e)}")

if __name__ == "__main__":
    insert_sample_data()
    print("Sample data insertion complete!")
