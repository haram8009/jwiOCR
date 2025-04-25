class ExtractionPipeline:
    def __init__(self, preprocessor, extractor, output_handler):
        self.preprocessor = preprocessor
        self.extractor = extractor
        self.output_handler = output_handler

    def run(self, input_path: str, output_path: str):
        text = self.preprocessor.extract_text(input_path)
        result = self.extractor.extract(text)
        self.output_handler.save(result, output_path)
