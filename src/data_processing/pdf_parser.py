"""
PDF Parser for Construct 3 Manual
Extracts text from PDF and splits into semantic chunks
"""
import fitz  # PyMuPDF
from pathlib import Path
from typing import List, Dict, Any
from dataclasses import dataclass
import re


@dataclass
class DocumentChunk:
    """Represents a chunk of document content"""
    text: str
    metadata: Dict[str, Any]


class PDFParser:
    """Parse Construct 3 PDF manuals into semantic chunks"""

    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def extract_text_from_pdf(self, pdf_path: Path) -> List[Dict[str, Any]]:
        """Extract text from PDF with page metadata"""
        doc = fitz.open(pdf_path)
        pages = []

        for page_num, page in enumerate(doc):
            text = page.get_text("text")
            pages.append({
                "page": page_num + 1,
                "text": text,
                "source": pdf_path.name
            })

        doc.close()
        return pages

    def detect_chapter_structure(self, text: str) -> List[str]:
        """Detect chapter/section headers in text"""
        # Common patterns for Construct 3 manual headers
        patterns = [
            r'^#{1,3}\s+(.+)$',  # Markdown headers
            r'^(\d+\.[\d.]*\s+.+)$',  # Numbered sections
            r'^([A-Z][A-Z\s]+)$',  # ALL CAPS headers
        ]

        headers = []
        for pattern in patterns:
            matches = re.findall(pattern, text, re.MULTILINE)
            headers.extend(matches)

        return headers

    def split_into_chunks(self, pages: List[Dict[str, Any]]) -> List[DocumentChunk]:
        """Split pages into overlapping chunks"""
        chunks = []

        for page_data in pages:
            text = page_data["text"]
            page_num = page_data["page"]
            source = page_data["source"]

            # Skip empty pages
            if not text.strip():
                continue

            # Split long pages into chunks
            if len(text) <= self.chunk_size:
                chunks.append(DocumentChunk(
                    text=text.strip(),
                    metadata={
                        "source": source,
                        "page": page_num,
                        "chunk_index": 0
                    }
                ))
            else:
                # Split by paragraphs first, then combine
                paragraphs = text.split('\n\n')
                current_chunk = ""
                chunk_index = 0

                for para in paragraphs:
                    if len(current_chunk) + len(para) < self.chunk_size:
                        current_chunk += para + "\n\n"
                    else:
                        if current_chunk.strip():
                            chunks.append(DocumentChunk(
                                text=current_chunk.strip(),
                                metadata={
                                    "source": source,
                                    "page": page_num,
                                    "chunk_index": chunk_index
                                }
                            ))
                            chunk_index += 1

                        # Keep overlap
                        overlap_text = current_chunk[-self.chunk_overlap:] if len(current_chunk) > self.chunk_overlap else ""
                        current_chunk = overlap_text + para + "\n\n"

                # Don't forget the last chunk
                if current_chunk.strip():
                    chunks.append(DocumentChunk(
                        text=current_chunk.strip(),
                        metadata={
                            "source": source,
                            "page": page_num,
                            "chunk_index": chunk_index
                        }
                    ))

        return chunks

    def parse(self, pdf_path: Path) -> List[DocumentChunk]:
        """Main parsing method"""
        print(f"Parsing PDF: {pdf_path}")

        pages = self.extract_text_from_pdf(pdf_path)
        print(f"  Extracted {len(pages)} pages")

        chunks = self.split_into_chunks(pages)
        print(f"  Created {len(chunks)} chunks")

        return chunks


def process_all_manuals():
    """Process all Construct 3 PDF manuals"""
    from src.config import PDF_MANUAL, PDF_SDK

    parser = PDFParser()
    all_chunks = []

    for pdf_path in [PDF_MANUAL, PDF_SDK]:
        if pdf_path.exists():
            chunks = parser.parse(pdf_path)
            all_chunks.extend(chunks)
        else:
            print(f"Warning: PDF not found: {pdf_path}")

    print(f"\nTotal chunks: {len(all_chunks)}")
    return all_chunks


if __name__ == "__main__":
    chunks = process_all_manuals()

    # Preview first few chunks
    print("\n--- Sample Chunks ---")
    for i, chunk in enumerate(chunks[:3]):
        print(f"\nChunk {i+1}:")
        print(f"  Source: {chunk.metadata['source']}, Page: {chunk.metadata['page']}")
        print(f"  Text preview: {chunk.text[:200]}...")
