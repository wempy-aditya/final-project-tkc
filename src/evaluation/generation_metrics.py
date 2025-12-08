"""
Text Generation Evaluation Metrics
BLEU, ROUGE, CIDEr scores
"""

import numpy as np
from typing import List
from collections import Counter
import math

# Download required NLTK data
try:
    import nltk
    nltk.download('punkt', quiet=True)
    nltk.download('punkt_tab', quiet=True)
    print("✅ NLTK data downloaded")
except Exception as e:
    print(f"⚠️ Could not download NLTK data: {e}")


def bleu_score(reference: str, candidate: str, n: int = 4) -> float:
    """
    Calculate BLEU score (simplified version)
    
    Args:
        reference: Reference text
        candidate: Candidate text
        n: Maximum n-gram size
        
    Returns:
        BLEU score
    """
    try:
        from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
        from nltk.tokenize import word_tokenize
        
        ref_tokens = word_tokenize(reference.lower())
        cand_tokens = word_tokenize(candidate.lower())
        
        smoothie = SmoothingFunction().method4
        score = sentence_bleu([ref_tokens], cand_tokens, smoothing_function=smoothie)
        
        return score
    except Exception as e:
        print(f"⚠️ NLTK BLEU error: {e}, using simple word overlap")
        ref_words = set(reference.lower().split())
        cand_words = set(candidate.lower().split())
        
        if len(cand_words) == 0:
            return 0.0
        
        overlap = len(ref_words & cand_words)
        return overlap / len(cand_words)


def rouge_score(reference: str, candidate: str) -> dict:
    """
    Calculate ROUGE scores
    
    Args:
        reference: Reference text
        candidate: Candidate text
        
    Returns:
        Dictionary with ROUGE-1, ROUGE-2, ROUGE-L scores
    """
    try:
        from rouge_score import rouge_scorer
        
        scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
        scores = scorer.score(reference, candidate)
        
        return {
            'rouge1': scores['rouge1'].fmeasure,
            'rouge2': scores['rouge2'].fmeasure,
            'rougeL': scores['rougeL'].fmeasure
        }
    except ImportError:
        print("⚠️ rouge-score not available, using simple overlap")
        # Simple fallback
        ref_words = set(reference.lower().split())
        cand_words = set(candidate.lower().split())
        
        if len(cand_words) == 0:
            overlap = 0.0
        else:
            overlap = len(ref_words & cand_words) / len(cand_words)
        
        return {'rouge1': overlap, 'rouge2': overlap * 0.8, 'rougeL': overlap * 0.9}


def cider_score_simple(references: List[str], candidate: str) -> float:
    """
    Simplified CIDEr score calculation
    
    Args:
        references: List of reference texts
        candidate: Candidate text
        
    Returns:
        CIDEr score (simplified)
    """
    # Simple implementation using TF-IDF similarity
    def get_ngrams(text: str, n: int = 1) -> Counter:
        words = text.lower().split()
        ngrams = [' '.join(words[i:i+n]) for i in range(len(words)-n+1)]
        return Counter(ngrams)
    
    # Get n-grams
    cand_ngrams = get_ngrams(candidate)
    ref_ngrams_list = [get_ngrams(ref) for ref in references]
    
    # Calculate similarity
    scores = []
    for ref_ngrams in ref_ngrams_list:
        # Cosine similarity
        common = set(cand_ngrams.keys()) & set(ref_ngrams.keys())
        if not common:
            scores.append(0.0)
            continue
        
        numerator = sum(cand_ngrams[k] * ref_ngrams[k] for k in common)
        
        sum1 = sum(v**2 for v in cand_ngrams.values())
        sum2 = sum(v**2 for v in ref_ngrams.values())
        
        denominator = math.sqrt(sum1) * math.sqrt(sum2)
        
        if denominator == 0:
            scores.append(0.0)
        else:
            scores.append(numerator / denominator)
    
    return np.mean(scores) if scores else 0.0


class TextGenerationEvaluator:
    """Evaluator for text generation"""
    
    def __init__(self):
        self.results = []
    
    def evaluate(self, references: List[str], candidate: str) -> dict:
        """
        Evaluate generated text against references
        
        Args:
            references: List of reference texts
            candidate: Generated text
            
        Returns:
            Dictionary of metrics
        """
        # Use first reference for BLEU and ROUGE
        primary_ref = references[0] if references else ""
        
        metrics = {
            'bleu': bleu_score(primary_ref, candidate),
            'cider': cider_score_simple(references, candidate)
        }
        
        # Add ROUGE scores
        rouge = rouge_score(primary_ref, candidate)
        metrics.update(rouge)
        
        self.results.append(metrics)
        return metrics
    
    def get_summary(self) -> dict:
        """Get summary statistics"""
        if not self.results:
            return {}
        
        summary = {}
        metric_names = self.results[0].keys()
        
        for metric in metric_names:
            values = [r[metric] for r in self.results]
            summary[f'mean_{metric}'] = np.mean(values)
            summary[f'std_{metric}'] = np.std(values)
        
        return summary


if __name__ == "__main__":
    # Test metrics
    reference = "a brown dog playing with a ball in the park"
    candidate = "a dog playing with a ball in a park"
    
    print("BLEU:", bleu_score(reference, candidate))
    print("ROUGE:", rouge_score(reference, candidate))
    print("CIDEr:", cider_score_simple([reference], candidate))
