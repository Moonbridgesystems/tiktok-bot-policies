"""
Comment analyzer for detecting product inquiries
"""
from typing import List
import config


class CommentAnalyzer:
    """Analyze comments to detect product inquiries"""
    
    def __init__(self, inquiry_phrases: List[str] = None):
        """
        Initialize comment analyzer
        
        Args:
            inquiry_phrases: List of phrases to detect (default: from config)
        """
        self.inquiry_phrases = inquiry_phrases or config.INQUIRY_PHRASES
        # Convert all phrases to lowercase for case-insensitive matching
        self.inquiry_phrases = [phrase.lower() for phrase in self.inquiry_phrases]
    
    def is_product_inquiry(self, comment_text: str) -> bool:
        """
        Check if a comment contains a product inquiry phrase
        
        Args:
            comment_text: The comment text to analyze
            
        Returns:
            True if comment contains an inquiry phrase, False otherwise
        """
        if not comment_text:
            return False
        
        # Convert to lowercase for case-insensitive matching
        comment_lower = comment_text.lower()
        
        # Check if any inquiry phrase is present in the comment
        for phrase in self.inquiry_phrases:
            if phrase in comment_lower:
                return True
        
        return False
    
    def count_product_inquiries(self, comments: List[str]) -> int:
        """
        Count how many comments contain product inquiries
        
        Args:
            comments: List of comment texts
            
        Returns:
            Number of comments with product inquiries
        """
        if not comments:
            return 0
        
        count = 0
        for comment in comments:
            if self.is_product_inquiry(comment):
                count += 1
        
        return count
    
    def get_inquiry_comments(self, comments: List[str]) -> List[str]:
        """
        Get all comments that contain product inquiries
        
        Args:
            comments: List of comment texts
            
        Returns:
            List of comments containing product inquiries
        """
        if not comments:
            return []
        
        inquiry_comments = []
        for comment in comments:
            if self.is_product_inquiry(comment):
                inquiry_comments.append(comment)
        
        return inquiry_comments
