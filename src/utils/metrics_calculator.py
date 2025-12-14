"""
Metrics Calculator for RAG System
Calculates retrieval quality, generation quality, and performance metrics
"""

import numpy as np
from typing import Dict, List
import re


class MetricsCalculator:
    """Calculate various metrics for retrieval and generation"""
    
    @staticmethod
    def calculate_retrieval_metrics(results: Dict) -> Dict:
        """
        Calculate retrieval quality metrics
        
        Args:
            results: Search results dictionary
            
        Returns:
            Dictionary with retrieval metrics
        """
        if not results.get('results'):
            return {
                'avg_similarity': 0.0,
                'min_similarity': 0.0,
                'max_similarity': 0.0,
                'std_similarity': 0.0,
                'diversity': 0.0,
                'total_results': 0
            }
        
        # Extract similarity scores
        scores = [r['similarity_score'] for r in results['results']]
        
        # Extract all captions
        all_captions = []
        for r in results['results']:
            all_captions.extend(r['captions'])
        
        # Calculate diversity (unique captions ratio)
        diversity = len(set(all_captions)) / len(all_captions) if all_captions else 0.0
        
        return {
            'avg_similarity': float(np.mean(scores)),
            'min_similarity': float(np.min(scores)),
            'max_similarity': float(np.max(scores)),
            'std_similarity': float(np.std(scores)),
            'diversity': float(diversity),
            'total_results': len(results['results'])
        }
    
    @staticmethod
    def calculate_text_metrics(text: str) -> Dict:
        """
        Calculate text generation quality metrics
        
        Args:
            text: Generated text
            
        Returns:
            Dictionary with text metrics
        """
        if not text or not text.strip():
            return {
                'word_count': 0,
                'char_count': 0,
                'sentence_count': 0,
                'avg_word_length': 0.0,
                'unique_words': 0,
                'vocabulary_richness': 0.0
            }
        
        # Clean text
        text = text.strip()
        
        # Word analysis
        words = re.findall(r'\b\w+\b', text.lower())
        word_count = len(words)
        unique_words = len(set(words))
        
        # Sentence analysis
        sentences = [s.strip() for s in re.split(r'[.!?]+', text) if s.strip()]
        sentence_count = len(sentences)
        
        # Character count
        char_count = len(text)
        
        # Average word length
        avg_word_length = np.mean([len(w) for w in words]) if words else 0.0
        
        # Vocabulary richness (unique words / total words)
        vocabulary_richness = unique_words / word_count if word_count > 0 else 0.0
        
        return {
            'word_count': word_count,
            'char_count': char_count,
            'sentence_count': sentence_count,
            'avg_word_length': float(avg_word_length),
            'unique_words': unique_words,
            'vocabulary_richness': float(vocabulary_richness)
        }
    
    @staticmethod
    def format_time(seconds: float) -> str:
        """
        Format time in human-readable format
        
        Args:
            seconds: Time in seconds
            
        Returns:
            Formatted time string
        """
        if seconds < 0.001:
            return f"{seconds*1000:.2f}ms"
        elif seconds < 1:
            return f"{seconds*1000:.0f}ms"
        elif seconds < 60:
            return f"{seconds:.2f}s"
        else:
            minutes = int(seconds // 60)
            secs = seconds % 60
            return f"{minutes}m {secs:.1f}s"
    
    @staticmethod
    def get_metric_interpretation(metric_name: str, value: float) -> str:
        """
        Get interpretation/quality indicator for a metric
        
        Args:
            metric_name: Name of the metric
            value: Metric value
            
        Returns:
            Interpretation string (Good/Fair/Poor)
        """
        interpretations = {
            'avg_similarity': {
                'good': (0.7, float('inf')),
                'fair': (0.5, 0.7),
                'poor': (0, 0.5)
            },
            'diversity': {
                'good': (0.6, float('inf')),
                'fair': (0.4, 0.6),
                'poor': (0, 0.4)
            },
            'vocabulary_richness': {
                'good': (0.7, float('inf')),
                'fair': (0.5, 0.7),
                'poor': (0, 0.5)
            }
        }
        
        if metric_name not in interpretations:
            return ""
        
        ranges = interpretations[metric_name]
        
        for quality, (min_val, max_val) in ranges.items():
            if min_val <= value < max_val:
                return quality.capitalize()
        
        return ""


if __name__ == "__main__":
    # Test metrics calculator
    calc = MetricsCalculator()
    
    # Test retrieval metrics
    test_results = {
        'results': [
            {'similarity_score': 0.85, 'captions': ['a dog', 'a brown dog']},
            {'similarity_score': 0.78, 'captions': ['a dog playing', 'a dog']},
            {'similarity_score': 0.72, 'captions': ['a park', 'green grass']}
        ]
    }
    
    ret_metrics = calc.calculate_retrieval_metrics(test_results)
    print("Retrieval Metrics:")
    for k, v in ret_metrics.items():
        print(f"  {k}: {v}")
    
    # Test text metrics
    test_text = "A brown dog is playing with a ball in the park. The dog looks very happy. It's a beautiful sunny day."
    
    text_metrics = calc.calculate_text_metrics(test_text)
    print("\nText Metrics:")
    for k, v in text_metrics.items():
        print(f"  {k}: {v}")
    
    # Test time formatting
    print("\nTime Formatting:")
    print(f"  0.0005s -> {calc.format_time(0.0005)}")
    print(f"  0.123s -> {calc.format_time(0.123)}")
    print(f"  2.5s -> {calc.format_time(2.5)}")
    print(f"  65s -> {calc.format_time(65)}")
