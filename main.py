
from fastapi import FastAPI,Path,Query,HTTPException
from pydantic import BaseModel
from typing import Optional
import uvicorn
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore



cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

pet_db=firestore.client()

app=FastAPI()

class Pet(BaseModel):
    name:str
    owner:str
    age:int
    pet_type:str
    gender:str
    

    
class UpdatePet(BaseModel):
    name:Optional[str]=None
    owner:Optional[str]=None
    age:Optional[int]=None
    pet_type:Optional[str]=None
    gender:Optional[str]=None
    
    
# create
@app.post("/new-pet/{pet_id}")
def add_new_pet(pet_id:str,pet:Pet):
    pet_dict={
        "name":"",
        "owner":"",
        "age":0,
        "pet_type":"",
        "gender":""
    }
    pet_dict["name"]=pet.name
    pet_dict["owner"]=pet.owner
    pet_dict["age"]=pet.age
    pet_dict["pet_type"]=pet.pet_type
    pet_dict["gender"]=pet.gender
    
    pet_db.collection("petstore").document(pet_id).set(pet_dict)

# read
@app.get("/pet-info/{pet_id}")
def get_pet_by_id(pet_id:str=Path(None,description="Store Id of your pet")):
    res=pet_db.collection("petstore").document(pet_id).get()
    return res.to_dict()

# update
@app.put("/update-pet-info/{item_id}")
def update_pet_info(pet_id:str,pet:UpdatePet):
    update_dict=dict()
    if pet.name:
        update_dict["name"]=pet.name
    
    if pet.owner:
        update_dict["owner"]=pet.owner
    
    if pet.age:
        update_dict["age"]=pet.age
    
    if pet.pet_type:
        update_dict["pet_type"]=pet.pet_type
    
    if pet.gender:
        update_dict["gender"]=pet.gender
        
    pet_db.collection("petstore").document(pet_id).update(update_dict)
    res= res=pet_db.collection("petstore").document(pet_id).get()
    return res.to_dict()

# delete
@app.delete("/delete-pet-info/{pet_id}")
def del_pet_info(pet_id:str=Query(None,description="Store Id of your pet")):
    pet_db.collection("petstore").document(pet_id).delete()
    return None
