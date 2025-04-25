from langchain.prompts import ChatPromptTemplate

extract_full_bl = ChatPromptTemplate.from_messages([
    ("system", "You are an expert logistics document extractor. Always return valid JSON."),
    ("user", 
"""The following text contains shipping document information (such as a Bill of Lading).  
Please extract and return a **JSON object** with the following fields (use exactly these keys):

- HouseBL_No: House Bill of Lading Number
- BL_NO: Master BL Number (optional, may be missing in HBL)
- Containers: list of Containers:
    - Container_No: Container Number
    - Seal_No: Container Seal Number
    - Package_Quantity: Number of packages
    - Package_Weight: Total weight 
    - Package_Unit: Weight unit (KGS, LBS, etc.)
    - Package_Volume: Total volume (CBM)
    - Package_Type: Package type (CTNR, PKGS, PALLET, etc.)
- POL: Port of Loading
- POL_ETD: Expected Departure Date
- POD: Port of Discharge
- POD_ETA: Expected Arrival Date
- Final_Delivery_LOC: Final Delivery Location (place of delivery)
- Vessel_Name: Vessel Name ('VESSEL'/VOYAGE)
- Voyage_No: Voyage Number (VESSEL/'VOYAGE')
- Shipper: Exporter
- Consignee: Importer
- Notify_Party: Notify Party
- Commodity: Item Description
- Move_Type: FCL/FCL, LCL/FCL, LCL/LCL, CY/DOOR, DOOR/CY, etc.

✅ Please return **only a valid JSON object** with no explanation, no markdown, no code blocks.

Input text:
{text}"""
    )
])