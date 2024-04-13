import copy
import re
from langchain_core.documents import Document
from typing import List, Optional

from langchain_text_splitters import MarkdownHeaderTextSplitter


headers_to_split_on = [
    ("Глава", 'header'),
    ("Статья", "article")
]
markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
from langchain_text_splitters import CharacterTextSplitter


class CharacterTextSplitterWithNoMerge(CharacterTextSplitter):
    def _merge_splits(self, splits, _separator):
        return splits

    def create_documents(
            self, texts: List[str], metadatas: Optional[List[dict]] = None
    ) -> List[Document]:
        _metadatas = metadatas or [{}] * len(texts)
        documents = []
        for i, text in enumerate(texts):
            index = 0
            previous_chunk_len = 0
            for chunk in self.split_text(text):
                metadata = copy.deepcopy(_metadatas[i])
                if self._add_start_index:
                    offset = index + previous_chunk_len - self._chunk_overlap
                    index = text.find(chunk, max(0, offset))
                    metadata["start_index"] = index
                    previous_chunk_len = len(chunk)
                metadata["point"] = re.findall(r'\d{1,2}\. ', chunk)[0].replace('. ', '') if re.findall(r'\d{1,2}\. ',
                                                                                                        chunk) else ''
                metadata["source"] = '223-fz-law'
                new_doc = Document(page_content=chunk, metadata=metadata)
                documents.append(new_doc)
        return documents


text_splitter = CharacterTextSplitterWithNoMerge(
    separator=r'\d{1,2}\. ',
    is_separator_regex=True,
    keep_separator=True,
    chunk_size=1500,
    chunk_overlap=100,
)
