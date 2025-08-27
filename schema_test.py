from app.schemas.schema import CarPriceData

example = {
    "Brand": "Hyundai",
    "Model Name": "Creta",
    "Model Variant": "SX",
    "Car Type": "SUV",
    "Transmission": "Manual",
    "Fuel Type": "Petrol",
    "Year": 2019,
    "Kilometers": 32000.5,
    "Owner": "1st",
    "State": "Maharashtra",
    "Accidental": "No",
    "Price": "1100000"
}

try:
    data = CarPriceData(**example)
    print(f"✅ Validated:\n {data}")
except Exception as e:
    print(f"❌ Error: {str(e)}")
