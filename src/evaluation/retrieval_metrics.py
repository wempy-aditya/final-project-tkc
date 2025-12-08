"""
Retrieval Evaluation Metrics
Precision@k, Recall@k, Mean Average Precision (mAP)
"""

import numpy as np
from typing import List, Dict, Set


def precision_at_k(retrieved: List[int], relevant: Set[int], k: int) -> float:
    """
    Calculate Precision@k
    
    Args:
        retrieved: List of retrieved item IDs (in order)
        relevant: Set of relevant item IDs
        k: Number of top results to consider
        
    Returns:
        Precision@k score
    """
    if k == 0:
        return 0.0
    
    retrieved_at_k = retrieved[:k]
    relevant_retrieved = sum(1 for item in retrieved_at_k if item in relevant)
    
    return relevant_retrieved / k


def recall_at_k(retrieved: List[int], relevant: Set[int], k: int) -> float:
    """
    Calculate Recall@k
    
    Args:
        retrieved: List of retrieved item IDs
        relevant: Set of relevant item IDs
        k: Number of top results to consider
        
    Returns:
        Recall@k score
    """
    if len(relevant) == 0:
        return 0.0
    
    retrieved_at_k = retrieved[:k]
    relevant_retrieved = sum(1 for item in retrieved_at_k if item in relevant)
    
    return relevant_retrieved / len(relevant)


def average_precision(retrieved: List[int], relevant: Set[int]) -> float:
    """
    Calculate Average Precision
    
    Args:
        retrieved: List of retrieved item IDs
        relevant: Set of relevant item IDs
        
    Returns:
        Average Precision score
    """
    if len(relevant) == 0:
        return 0.0
    
    precisions = []
    num_relevant = 0
    
    for k, item in enumerate(retrieved, 1):
        if item in relevant:
            num_relevant += 1
            precisions.append(num_relevant / k)
    
    if len(precisions) == 0:
        return 0.0
    
    return sum(precisions) / len(relevant)


def mean_average_precision(all_retrieved: List[List[int]], all_relevant: List[Set[int]]) -> float:
    """
    Calculate Mean Average Precision (mAP)
    
    Args:
        all_retrieved: List of retrieved item lists for each query
        all_relevant: List of relevant item sets for each query
        
    Returns:
        mAP score
    """
    aps = [average_precision(ret, rel) for ret, rel in zip(all_retrieved, all_relevant)]
    return np.mean(aps)


class RetrievalEvaluator:
    """Evaluator for retrieval system"""
    
    def __init__(self):
        self.results = []
    
    def evaluate_query(self, retrieved: List[int], relevant: Set[int], k_values: List[int] = [1, 3, 5, 10]):
        """
        Evaluate a single query
        
        Args:
            retrieved: Retrieved item IDs
            relevant: Relevant item IDs
            k_values: K values to evaluate
            
        Returns:
            Dictionary of metrics
        """
        metrics = {
            'ap': average_precision(retrieved, relevant)
        }
        
        for k in k_values:
            metrics[f'p@{k}'] = precision_at_k(retrieved, relevant, k)
            metrics[f'r@{k}'] = recall_at_k(retrieved, relevant, k)
        
        self.results.append(metrics)
        return metrics
    
    def get_summary(self) -> Dict[str, float]:
        """Get summary statistics across all queries"""
        if not self.results:
            return {}
        
        summary = {}
        
        # Get all metric names
        metric_names = self.results[0].keys()
        
        for metric in metric_names:
            values = [r[metric] for r in self.results]
            summary[f'mean_{metric}'] = np.mean(values)
            summary[f'std_{metric}'] = np.std(values)
        
        # Add mAP
        summary['mAP'] = np.mean([r['ap'] for r in self.results])
        
        return summary


if __name__ == "__main__":
    # Test evaluation metrics
    retrieved = [1, 3, 5, 7, 9, 2, 4, 6, 8, 10]
    relevant = {1, 2, 3, 4, 5}
    
    print("Precision@5:", precision_at_k(retrieved, relevant, 5))
    print("Recall@5:", recall_at_k(retrieved, relevant, 5))
    print("Average Precision:", average_precision(retrieved, relevant))
