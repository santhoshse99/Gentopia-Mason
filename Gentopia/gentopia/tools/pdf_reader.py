import requests
from typing import Optional, Type, AnyStr
from PyPDF2 import PdfReader
from io import BytesIO
from gentopia.tools.basetool import *

class PDFReaderArgs(BaseModel):
    file_path: str = Field(..., description="The URL of the PDF.")

class PDFReader(BaseTool):
    """Tool that adds the capability to read and summarize PDF files from URLs."""

    name = "pdf_reader"
    description = "This reads a pdf from the url  and summarizes it. It retrieves the first 500 characters and also specifically searches for abstract part as these contents passed to the llm would provide a better summary. Input should be a URL."

    args_schema: Optional[Type[BaseModel]] = PDFReaderArgs

    def _run(self, file_path: AnyStr) -> str:
        input_pdf_file = self.save_pdf(file_path)
        return self.pdf_file_read(input_pdf_file)

    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError

    def pdf_file_read(self, input_pdf_file: bytes) -> str:
        try:
            pdf = BytesIO(input_pdf_file)
            pdf_reader_input = PdfReader(pdf)
            pdf_content = ""
            for page in pdf_reader_input.pages:
                pdf_content += page.extract_text()
            
            initial_characters = pdf_content[:500]
            abstract1 = pdf_content.lower().find("abstract")
            abstract2 = pdf_content.lower().find("introduction")
            
            if abstract1 != -1 and abstract2 != -1:
                abstract_content = pdf_content[abstract1:abstract2]
            else:
                abstract_content = pdf_content[:1500]

            summary_input = initial_characters + "\n\n" + abstract_content
            return summary_input
        except Exception as error:
            return f"Error reading PDF: {str(error)}"


    def save_pdf(self, url: str) -> bytes:
        try:
            url_response = requests.get(url)
            url_response.raise_for_status() 
            return url_response.content
        except Exception as error:
            return f"Error downloading PDF: {str(error)}"

if __name__ == "__main__":
    ans = PDFReader()._run("https://arxiv.org/pdf/2406.12288")
    print(ans)
