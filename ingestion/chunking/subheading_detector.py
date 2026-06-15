import re
from .models.semantic_segment import SemanticSegment

class SubHeadingDetector:
    SUBHEADING_PATTERNS = [
        re.compile(r"^[A-Z][A-Z\s&/\-]{5,}$"),
        re.compile(r"^\d+\.\s+[A-Z].*$"),
        re.compile(r"^[A-Z][a-zA-Z\s]{3,}:$"),
    ]
    
    def detect(self, content:str, page_number: int)-> list[SemanticSegment]:
        lines = [line.strip() for line in content.splitlines() if line.strip()]   

        if not lines:
            return []

        segments = []
        current_title = 'GENERAL'
        current_content = []

        for line in lines:
            if self.is_subheading(line):
                if current_content:
                    segments.append(
                        SemanticSegment(
                            title = current_title,
                            content='\n'.join(current_content),
                            page_number=page_number
                        )
                    )
                
                current_title = line
                current_content = []
            current_content.append(line)
        
        if current_content:
            segments.append(
                SemanticSegment(
                    title=current_title,
                    content='\n'.join(current_content),
                    page_number=page_number
                )
            )
        
        return segments

    
    def is_subheading(self, line: str) -> bool:
        if len(line.split()) > 12:
            return False

        for pattern in self.SUBHEADING_PATTERNS:
            if pattern.match(line):
                return True
        return False

