# app/schemas/schema.py 
from app.config import settings
from pydantic import BaseModel, Field, root_validator
import json

# Load categories
with open(settings.cat_cols_name, "r") as f:
    categories = json.load(f)

class CarPriceData(BaseModel):
    brand: str = Field(..., alias='Brand')
    name_model : str = Field(..., alias='Model Name')
    variant_model : str = Field(..., alias='Model Variant')
    car_type : str = Field(..., alias='Car Type')
    transimission : str = Field(..., alias='Transmission')
    fuel_type : str = Field(..., alias='Fuel Type')
    year : int = Field(..., alias='Year')
    kilometer : float = Field(..., alias="Kilometers")
    owner : str = Field(..., alias='Owner')
    state :str = Field(..., alias='State')
    accidental : str = Field(..., alias='Accidental')
    price : str = Field(..., alias='Price')

# Validation 
@root_validator(pre=True)
def validate_categoricals(cls, values):
    for col, allowed in categories.items():
        if col in values and values[col] not in allowed:
            raise ValueError(
                f"❌ Invalid value '{values[col]}' for '{col}'."
                f"Allowed examples : {allowed[:10]}..."
            )
    return values

class Config:
    populate_by_name = True