from langchain.prompts import ChatPromptTemplate

extract_full_bl_batch_with_ocr = ChatPromptTemplate.from_messages([
    ("system", 
     "You are an expert logistics document extractor. Always return valid JSON. "
     "If multiple BL documents are included in the input images, split and extract each one separately. "
     "Return a list of JSON objects, one for each BL document."),
    ("user", 
"""The following image contains shipping document information (such as a Bill of Lading).  
Please extract and return a **JSON object** with the following fields (use exactly these keys):

- HouseBL_No: House Bill of Lading Number
- BL_NO: Master BL Number 
- Containers: list of Containers:
    - Container_No: Container Number (!Format: 4 letters + 7 digits, e.g., TGHU9462938.! Avoid mixing with Seal Numbers. 'container'/seal)
    - Container_Type: Container Type (20GP, 40HQ, etc.)
    - Seal_No: Container Seal Number (container/'seal'. If multiple seal numbers are present, return the Carrier Seal. If unclear, set to null.)
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
- Commodity: Item Description ( Exclude brand names, company names, or customer references such as 'RYTAN INC.')
- Move_Type: FCL/FCL, LCL/FCL, LCL/LCL, CY/DOOR, DOOR/CY, CFS/CFS, DOOR/DOOR etc.


✅ Return a **list** of JSON objects, one for each BL document.
✅ The House BL Number or Master BL Number may appear on a standalone line without any label, often near the beginning or end of the text. Please extract it even if it is not explicitly marked.
✅ The HouseBL_No usually follows an alphanumeric format like "KSSEL2501388", "SELM76682700", or "PRKS25040043". It may be 10–14 characters long, and does not follow the 4-letter + 7-digit format used for Container Numbers.
✅ Please return only a valid JSON object, and do not use markdown, do not wrap in code blocks (like ```json), and do not explain anything. Just output pure JSON.""")
])
