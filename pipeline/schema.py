# schema which every validation will be based on.
# every value was selected after reviewing the the csv files.

SCHEMA = {
    "id": {
        "type": "int",
        "required": True,
    },
    "Age": {
        "type": "int",
        "required": True,
        "min": 1,
    },
    "Sex": {
        "type": "int",
        "required": True,
        "allowed": [0, 1],
        "decode": {0: "female", 1: "male"},
    },
    "Chest pain type": {
        "type": "int",
        "required": True,
        "allowed": [1, 2, 3, 4],  
        "decode": {
            1: "typical angina",
            2: "atypical angina",
            3: "non-anginal pain",
            4: "asymptomatic",
        },
    },
    "BP": {
        "type": "int",
        "required": True,
        "min": 1,      
    },
    "Cholesterol": {
        "type": "int",
        "required": True,
        "min": 1,       
    },
    "FBS over 120": {
        "type": "int",
        "required": False,
        "allowed": [0, 1],
        "decode": {0: "fbs <= 120 mg/dl", 1: "fbs > 120 mg/dl"},
    },
    "EKG results": {
        "type": "int",
        "required": False,
        "allowed": [0, 1, 2], 
    },
    "Max HR": {
        "type": "int",
        "required": True,
        "min": 1,       
        "max": 300,    
    },
    "Exercise angina": {
        "type": "int",
        "required": False,
        "allowed": [0, 1],
        "decode": {0: "no", 1: "yes"},
    },
    "ST depression": {
        "type": "float",
        "required": False,
        "min": 0.0,    
    },
    "Slope of ST": {
        "type": "int",
        "required": False,
        "allowed": [1, 2, 3],
        "decode": {1: "upsloping", 2: "flat", 3: "downsloping"},
    },
    "Number of vessels fluro": {
        "type": "int",
        "required": False,
        "allowed": [0, 1, 2, 3], 
    },
    "Thallium": {
        "type": "int",
        "required": False,
        "allowed": [3, 6, 7],   
        "decode": {3: "normal", 6: "fixed defect", 7: "reversable defect"},
    },
    "Heart Disease": {
        "type": "str",
        "required": False,
        "allowed": ["Presence", "Absence"],
    },
}

REQUIRED_FIELDS  = [k for k, v in SCHEMA.items() if v.get("required")]