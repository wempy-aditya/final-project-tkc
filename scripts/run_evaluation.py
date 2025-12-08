"""
Run Evaluation Pipeline
"""

import json
import sys
from pathlib import Path
import random

sys.path.append(str(Path(__file__).parent.parent))

from src.retrieval.retriever import Retriever
from src.models.context_builder import ContextBuilder
from src.models.text_generator import TextGenerator
from src.evaluation.retrieval_metrics import RetrievalEvaluator
from src.evaluation.generation_metrics import TextGenerationEvaluator


def run_retrieval_evaluation(
    retriever: Retriever,
    num_queries: int = 50,
    k_values: list = [1, 3, 5, 10]
):
    """
    Run retrieval evaluation
    
    Args:
        retriever: Retriever instance
        num_queries: Number of queries to evaluate
        k_values: K values for metrics
    """
    print("\n=== RETRIEVAL EVALUATION ===")
    
    evaluator = RetrievalEvaluator()
    
    # Sample random queries from metadata
    metadata = retriever.metadata
    sample_indices = random.sample(range(len(metadata)), min(num_queries, len(metadata)))
    
    for idx in sample_indices:
        query_meta = metadata[idx]
        query_caption = query_meta['captions'][0]
        
        # Perform retrieval
        results = retriever.search_by_text(query_caption, k=max(k_values))
        
        # Get retrieved IDs
        retrieved_ids = [r['image_id'] for r in results['results']]
        
        # Relevant is the query image itself (and potentially similar ones)
        # For simplicity, we consider only the query image as relevant
        relevant_ids = {query_meta['image_id']}
        
        # Evaluate
        evaluator.evaluate_query(retrieved_ids, relevant_ids, k_values)
    
    # Get summary
    summary = evaluator.get_summary()
    
    print("\nRetrieval Metrics Summary:")
    for metric, value in summary.items():
        print(f"  {metric}: {value:.4f}")
    
    return summary


def run_generation_evaluation(
    retriever: Retriever,
    text_gen: TextGenerator,
    context_builder: ContextBuilder,
    num_queries: int = 20
):
    """
    Run text generation evaluation
    
    Args:
        retriever: Retriever instance
        text_gen: Text generator instance
        context_builder: Context builder instance
        num_queries: Number of queries to evaluate
    """
    print("\n=== TEXT GENERATION EVALUATION ===")
    
    evaluator = TextGenerationEvaluator()
    
    # Sample random queries
    metadata = retriever.metadata
    sample_indices = random.sample(range(len(metadata)), min(num_queries, len(metadata)))
    
    for idx in sample_indices:
        query_meta = metadata[idx]
        query_caption = query_meta['captions'][0]
        
        # Perform retrieval
        results = retriever.search_by_text(query_caption, k=5)
        captions = retriever.get_captions_from_results(results)
        
        # Generate text
        context = context_builder.build_context(query_caption, captions)
        generated = text_gen.generate_from_context(context)
        
        # Evaluate against all captions of the query image
        references = query_meta['captions']
        metrics = evaluator.evaluate(references, generated)
        
        print(f"Query {idx}: BLEU={metrics['bleu']:.3f}, ROUGE-L={metrics['rougeL']:.3f}")
    
    # Get summary
    summary = evaluator.get_summary()
    
    print("\nText Generation Metrics Summary:")
    for metric, value in summary.items():
        print(f"  {metric}: {value:.4f}")
    
    return summary


def main():
    """Run complete evaluation pipeline"""
    print("=" * 60)
    print("MULTIMODAL RAG SYSTEM - EVALUATION")
    print("=" * 60)
    
    # Initialize components
    print("\nInitializing components...")
    retriever = Retriever()
    context_builder = ContextBuilder()
    
    try:
        text_gen = TextGenerator()
    except Exception as e:
        print(f"Warning: Text generator not available: {e}")
        text_gen = None
    
    # Run retrieval evaluation
    retrieval_results = run_retrieval_evaluation(retriever, num_queries=50)
    
    # Run generation evaluation (if text generator available)
    if text_gen:
        generation_results = run_generation_evaluation(
            retriever, text_gen, context_builder, num_queries=20
        )
    else:
        generation_results = {}
    
    # Save results
    results = {
        'retrieval': retrieval_results,
        'generation': generation_results
    }
    
    output_file = "experiments/results/evaluation_results.json"
    Path(output_file).parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n✅ Results saved to {output_file}")


if __name__ == "__main__":
    main()
