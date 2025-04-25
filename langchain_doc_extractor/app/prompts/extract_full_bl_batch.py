PROMPT = {
    "name": "extract_full_bl_batch",
    "description": "여러 개의 BL 문서 텍스트가 하나로 연결된 경우, 각각의 문서 정보를 분리하여 추출합니다.",
    "template": 
"""The following text contains multiple shipping documents (e.g., House Bill of Lading or Master B/L),
each separated by page breaks or distinct visual boundaries.

Please extract and return a **list of JSON objects**, one per document, using exactly the following keys:

- HouseBL_No: House Bill of Lading Number
- BL_NO: Master BL Number (optional, may be missing in HBL)
- Container_No: Container Number
- Seal_No: Container Seal Number
- Package_Quantity: Number of packages
- Package_Weight: Total weight (kg)
- Package_Volume: Total volume (CBM)
- POL: Port of Loading
- POL_ETD: Expected Departure Date
- POD: Port of Discharge
- POD_ETA: Expected Arrival Date
- Final_Delivery_LOC: Final Delivery Location
- Vessel_Name: Vessel Name
- Voyage_No: Voyage Number
- Shipper: Exporter
- Consignee: Importer
- Notify_Party: Notify Party
- Commodity: Item Description
- Move_Type: FCL/FCL, LCL/FCL or LCL/LCL

✅ Return a **valid JSON array** of objects only. No explanations, markdown, or code blocks.

Input text:
{text}"""
}
