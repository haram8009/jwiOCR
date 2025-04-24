from dotenv import load_dotenv
import os
from pipeline import ExtractionPipeline
from preprocessor import PDFPreprocessor
from extractor import GPTExtractor
from output_handler import JSONSaver

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

if __name__ == "__main__":
    input_path = os.path.join(BASE_DIR, "../sample.pdf")
    output_path = os.path.join(BASE_DIR, "../output/result.json")

    pipeline = ExtractionPipeline(
        preprocessor=PDFPreprocessor(),
        extractor=GPTExtractor(api_key=os.getenv("OPENAI_API_KEY"),
                               prompt_name="extract_logistics"),
        output_handler=JSONSaver()
    )
    pipeline.run(input_path, output_path)
