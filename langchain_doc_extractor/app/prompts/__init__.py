from .extract_basic import extract_basic
from .extract_full_bl import extract_full_bl
from .extract_full_bl_batch import extract_full_bl_batch
from .extract_full_bl_batch_with_ocr import extract_full_bl_batch_with_ocr

prompts = {
    "extract_basic": extract_basic,
    "extract_full_bl": extract_full_bl,
    "extract_full_bl_batch": extract_full_bl_batch,
    "extract_full_bl_batch_with_ocr": extract_full_bl_batch_with_ocr,
}
