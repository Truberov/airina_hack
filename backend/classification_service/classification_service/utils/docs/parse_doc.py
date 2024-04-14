import io

import PyPDF2

from docx import Document
from starlette import status
from fastapi import HTTPException
from pyth.plugins.rtf15.reader import Rtf15Reader
from pyth.plugins.plaintext.writer import PlaintextWriter


async def parse_doc(file) -> str:
    content = await file.read()
    file_content_io = io.BytesIO(content)

    file_type = file.filename.split('.')[-1]

    match file_type:
        case 'docx':
            doc = Document(file_content_io)
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs if paragraph.text])
            return text[:15900]

        case 'pdf':
            reader = PyPDF2.PdfReader(file_content_io)
            text = "\n".join([page.extract_text() for page in reader.pages])
            return text[:15900]

        case 'rtf':
            doc = Rtf15Reader.read(file_content_io)
            text = PlaintextWriter.write(doc).getvalue()
            return text[:15900]

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail='File type not supported',
    )
