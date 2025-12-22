"""
Enhanced Evaluation Pipeline for Multimodal RAG System
Includes comprehensive metrics and test scenarios
"""

import json
import sys
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any
import random

sys.path.append(str(Path(__file__).parent.parent))

from src.retrieval.retriever import Retriever
from src.models.context_builder import ContextBuilder
from src.models.text_generator import TextGenerator
from src.evaluation.retrieval_metrics import RetrievalEvaluator
from src.evaluation.generation_metrics import TextGenerationEvaluator


# ==================== TEST SCENARIOS ====================

TEST_SCENARIOS = {
    "simple_objects": [
        "a cat sitting on a couch",
        "a dog playing in the park",
        "a car on the street",
        "a person riding a bicycle",
        "a bird flying in the sky"
    ],
    "complex_scenes": [
        "a group of people having dinner at a restaurant",
        "children playing soccer in a field",
        "a busy city street with cars and pedestrians",
        "a beach with people swimming and surfing",
        "a market with vendors selling fruits and vegetables"
    ],
    "specific_attributes": [
        "a red sports car",
        "a black and white cat",
        "a person wearing a blue shirt",
        "a yellow school bus",
        "a green apple on a table"
    ],
    "abstract_concepts": [
        "a happy family moment",
        "a peaceful nature scene",
        "an exciting sports action",
        "a cozy indoor setting",
        "a vibrant outdoor celebration"
    ]
}


# ==================== ENHANCED RETRIEVAL EVALUATION ====================

def calculate_recall_at_k(retrieved_ids: List[int], relevant_ids: set, k: int) -> float:
    """Calculate Recall@K"""
    retrieved_k = set(retrieved_ids[:k])
    if len(relevant_ids) == 0:
        return 0.0
    return len(retrieved_k & relevant_ids) / len(relevant_ids)


def calculate_precision_at_k(retrieved_ids: List[int], relevant_ids: set, k: int) -> float:
    """Calculate Precision@K"""
    retrieved_k = set(retrieved_ids[:k])
    if k == 0:
        return 0.0
    return len(retrieved_k & relevant_ids) / k


def run_enhanced_retrieval_evaluation(
    retriever: Retriever,
    test_queries: List[str] = None,
    num_random_queries: int = 30,
    k_values: List[int] = [1, 3, 5, 10]
) -> Dict[str, Any]:
    """
    Enhanced retrieval evaluation with Recall@K, Precision@K, and Latency
    
    Args:
        retriever: Retriever instance
        test_queries: Optional list of test queries
        num_random_queries: Number of random queries from dataset
        k_values: K values for metrics
    
    Returns:
        Dictionary with detailed metrics
    """
    print("\n" + "="*60)
    print("ENHANCED RETRIEVAL EVALUATION")
    print("="*60)
    
    results = {
        'recall_at_k': {k: [] for k in k_values},
        'precision_at_k': {k: [] for k in k_values},
        'latencies': [],
        'avg_similarity_scores': [],
        'query_details': []
    }
    
    # Combine test queries with random samples
    all_queries = []
    
    # Add predefined test queries
    if test_queries:
        all_queries.extend(test_queries)
        print(f"\n📋 Using {len(test_queries)} predefined test queries")
    
    # Add random queries from metadata
    metadata = retriever.metadata
    if num_random_queries > 0:
        sample_indices = random.sample(range(len(metadata)), min(num_random_queries, len(metadata)))
        for idx in sample_indices:
            all_queries.append(metadata[idx]['captions'][0])
        print(f"📋 Added {len(sample_indices)} random queries from dataset")
    
    print(f"\n🔍 Total queries to evaluate: {len(all_queries)}\n")
    
    # Evaluate each query
    for i, query in enumerate(all_queries, 1):
        print(f"[{i}/{len(all_queries)}] Evaluating: '{query[:50]}...'")
        
        # Measure latency
        start_time = time.time()
        results_data = retriever.search_by_text(query, k=max(k_values))
        latency = time.time() - start_time
        
        results['latencies'].append(latency)
        
        # Get retrieved IDs and scores
        retrieved_ids = [r['image_id'] for r in results_data['results']]
        similarity_scores = [r['similarity_score'] for r in results_data['results']]
        
        if similarity_scores:
            results['avg_similarity_scores'].append(sum(similarity_scores) / len(similarity_scores))
        
        # For evaluation, we consider images with same caption as relevant
        # (This is a simplified ground truth - in real scenario, you'd have labeled data)
        relevant_ids = set()
        for meta in metadata:
            if query.lower() in ' '.join(meta['captions']).lower():
                relevant_ids.add(meta['image_id'])
        
        # Calculate metrics for each K
        query_metrics = {'query': query, 'latency': latency}
        for k in k_values:
            recall = calculate_recall_at_k(retrieved_ids, relevant_ids, k)
            precision = calculate_precision_at_k(retrieved_ids, relevant_ids, k)
            
            results['recall_at_k'][k].append(recall)
            results['precision_at_k'][k].append(precision)
            
            query_metrics[f'recall@{k}'] = recall
            query_metrics[f'precision@{k}'] = precision
        
        results['query_details'].append(query_metrics)
        print(f"   ⏱️  Latency: {latency:.3f}s | Avg Similarity: {results['avg_similarity_scores'][-1]:.3f}")
    
    # Calculate summary statistics
    summary = {
        'total_queries': len(all_queries),
        'avg_latency': sum(results['latencies']) / len(results['latencies']),
        'min_latency': min(results['latencies']),
        'max_latency': max(results['latencies']),
        'avg_similarity': sum(results['avg_similarity_scores']) / len(results['avg_similarity_scores']) if results['avg_similarity_scores'] else 0
    }
    
    # Add average metrics for each K
    for k in k_values:
        summary[f'recall@{k}'] = sum(results['recall_at_k'][k]) / len(results['recall_at_k'][k])
        summary[f'precision@{k}'] = sum(results['precision_at_k'][k]) / len(results['precision_at_k'][k])
    
    # Print summary
    print("\n" + "="*60)
    print("RETRIEVAL METRICS SUMMARY")
    print("="*60)
    print(f"📊 Total Queries: {summary['total_queries']}")
    print(f"\n⏱️  LATENCY METRICS:")
    print(f"   Average: {summary['avg_latency']:.4f}s")
    print(f"   Min: {summary['min_latency']:.4f}s")
    print(f"   Max: {summary['max_latency']:.4f}s")
    print(f"\n📈 SIMILARITY METRICS:")
    print(f"   Average Similarity Score: {summary['avg_similarity']:.4f}")
    print(f"\n🎯 RECALL@K:")
    for k in k_values:
        print(f"   Recall@{k}: {summary[f'recall@{k}']:.4f}")
    print(f"\n🎯 PRECISION@K:")
    for k in k_values:
        print(f"   Precision@{k}: {summary[f'precision@{k}']:.4f}")
    
    return {
        'summary': summary,
        'detailed_results': results
    }


# ==================== ENHANCED GENERATION EVALUATION ====================

def calculate_faithfulness(generated_text: str, context_captions: List[str]) -> float:
    """
    Calculate faithfulness score (how much generated text is grounded in context)
    Simple implementation: ratio of context words found in generated text
    """
    # Tokenize and normalize
    context_words = set()
    for caption in context_captions:
        words = caption.lower().split()
        context_words.update(words)
    
    generated_words = set(generated_text.lower().split())
    
    # Calculate overlap
    if len(generated_words) == 0:
        return 0.0
    
    overlap = len(generated_words & context_words)
    return overlap / len(generated_words)


def calculate_answer_relevance(generated_text: str, query: str) -> float:
    """
    Calculate answer relevance (how relevant is answer to query)
    Simple implementation: word overlap between query and generated text
    """
    query_words = set(query.lower().split())
    generated_words = set(generated_text.lower().split())
    
    if len(query_words) == 0:
        return 0.0
    
    overlap = len(query_words & generated_words)
    return overlap / len(query_words)


def calculate_context_precision(context_captions: List[str], query: str) -> float:
    """
    Calculate context precision (how relevant is retrieved context to query)
    Simple implementation: average word overlap of captions with query
    """
    query_words = set(query.lower().split())
    
    if len(context_captions) == 0:
        return 0.0
    
    relevance_scores = []
    for caption in context_captions:
        caption_words = set(caption.lower().split())
        if len(caption_words) > 0:
            overlap = len(query_words & caption_words)
            relevance_scores.append(overlap / len(caption_words))
    
    return sum(relevance_scores) / len(relevance_scores) if relevance_scores else 0.0


def run_enhanced_generation_evaluation(
    retriever: Retriever,
    text_gen: TextGenerator,
    context_builder: ContextBuilder,
    test_queries: List[str] = None,
    num_random_queries: int = 15
) -> Dict[str, Any]:
    """
    Enhanced generation evaluation with Faithfulness, Answer Relevance, and Context Precision
    
    Args:
        retriever: Retriever instance
        text_gen: Text generator instance
        context_builder: Context builder instance
        test_queries: Optional list of test queries
        num_random_queries: Number of random queries
    
    Returns:
        Dictionary with detailed metrics
    """
    print("\n" + "="*60)
    print("ENHANCED GENERATION EVALUATION")
    print("="*60)
    
    results = {
        'faithfulness_scores': [],
        'answer_relevance_scores': [],
        'context_precision_scores': [],
        'generation_times': [],
        'query_details': []
    }
    
    # Prepare queries
    all_queries = []
    if test_queries:
        all_queries.extend(test_queries)
    
    metadata = retriever.metadata
    if num_random_queries > 0:
        sample_indices = random.sample(range(len(metadata)), min(num_random_queries, len(metadata)))
        for idx in sample_indices:
            all_queries.append(metadata[idx]['captions'][0])
    
    print(f"\n📝 Total queries to evaluate: {len(all_queries)}\n")
    
    # Evaluate each query
    for i, query in enumerate(all_queries, 1):
        print(f"[{i}/{len(all_queries)}] Generating for: '{query[:50]}...'")
        
        # Retrieve context
        retrieval_results = retriever.search_by_text(query, k=5)
        captions = retriever.get_captions_from_results(retrieval_results)
        
        # Generate text
        context = context_builder.build_context(query, captions)
        
        start_time = time.time()
        generated_text = text_gen.generate_from_context(context)
        gen_time = time.time() - start_time
        
        results['generation_times'].append(gen_time)
        
        # Calculate RAG-specific metrics
        faithfulness = calculate_faithfulness(generated_text, captions)
        answer_relevance = calculate_answer_relevance(generated_text, query)
        context_precision = calculate_context_precision(captions, query)
        
        results['faithfulness_scores'].append(faithfulness)
        results['answer_relevance_scores'].append(answer_relevance)
        results['context_precision_scores'].append(context_precision)
        
        query_detail = {
            'query': query,
            'generated_text': generated_text,
            'generation_time': gen_time,
            'faithfulness': faithfulness,
            'answer_relevance': answer_relevance,
            'context_precision': context_precision,
            'num_context_captions': len(captions)
        }
        results['query_details'].append(query_detail)
        
        print(f"   ⏱️  Gen Time: {gen_time:.2f}s | Faithfulness: {faithfulness:.3f} | Relevance: {answer_relevance:.3f}")
    
    # Calculate summary
    summary = {
        'total_queries': len(all_queries),
        'avg_generation_time': sum(results['generation_times']) / len(results['generation_times']),
        'avg_faithfulness': sum(results['faithfulness_scores']) / len(results['faithfulness_scores']),
        'avg_answer_relevance': sum(results['answer_relevance_scores']) / len(results['answer_relevance_scores']),
        'avg_context_precision': sum(results['context_precision_scores']) / len(results['context_precision_scores'])
    }
    
    # Print summary
    print("\n" + "="*60)
    print("GENERATION METRICS SUMMARY")
    print("="*60)
    print(f"📊 Total Queries: {summary['total_queries']}")
    print(f"\n⏱️  GENERATION TIME:")
    print(f"   Average: {summary['avg_generation_time']:.4f}s")
    print(f"\n🎯 RAG QUALITY METRICS:")
    print(f"   Faithfulness (Grounding): {summary['avg_faithfulness']:.4f}")
    print(f"   Answer Relevance: {summary['avg_answer_relevance']:.4f}")
    print(f"   Context Precision: {summary['avg_context_precision']:.4f}")
    
    return {
        'summary': summary,
        'detailed_results': results
    }


# ==================== SCENARIO-BASED EVALUATION ====================

def run_scenario_evaluation(
    retriever: Retriever,
    text_gen: TextGenerator = None,
    context_builder: ContextBuilder = None
) -> Dict[str, Any]:
    """
    Run evaluation across different test scenarios
    """
    print("\n" + "="*60)
    print("SCENARIO-BASED EVALUATION")
    print("="*60)
    
    scenario_results = {}
    
    for scenario_name, queries in TEST_SCENARIOS.items():
        print(f"\n🎬 Scenario: {scenario_name.upper().replace('_', ' ')}")
        print(f"   Queries: {len(queries)}")
        
        # Retrieval evaluation for this scenario
        retrieval_result = run_enhanced_retrieval_evaluation(
            retriever,
            test_queries=queries,
            num_random_queries=0,
            k_values=[1, 3, 5]
        )
        
        scenario_results[scenario_name] = {
            'retrieval': retrieval_result['summary']
        }
        
        # Generation evaluation if available
        if text_gen and context_builder:
            generation_result = run_enhanced_generation_evaluation(
                retriever,
                text_gen,
                context_builder,
                test_queries=queries,
                num_random_queries=0
            )
            scenario_results[scenario_name]['generation'] = generation_result['summary']
    
    return scenario_results


# ==================== MAIN EVALUATION PIPELINE ====================

def main():
    """Run complete enhanced evaluation pipeline"""
    print("="*60)
    print("MULTIMODAL RAG SYSTEM - COMPREHENSIVE EVALUATION")
    print("="*60)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Initialize components
    print("\n🔧 Initializing components...")
    retriever = Retriever()
    context_builder = ContextBuilder()
    
    try:
        text_gen = TextGenerator()
        print("✅ Text Generator: Available")
    except Exception as e:
        print(f"⚠️  Text Generator: Not available ({e})")
        text_gen = None
    
    # Prepare all test queries
    all_test_queries = []
    for queries in TEST_SCENARIOS.values():
        all_test_queries.extend(queries)
    
    # Run comprehensive retrieval evaluation
    print("\n" + "="*60)
    print("PHASE 1: RETRIEVAL EVALUATION")
    print("="*60)
    retrieval_results = run_enhanced_retrieval_evaluation(
        retriever,
        test_queries=all_test_queries,
        num_random_queries=20,
        k_values=[1, 3, 5, 10]
    )
    
    # Run generation evaluation if available
    generation_results = {}
    if text_gen:
        print("\n" + "="*60)
        print("PHASE 2: GENERATION EVALUATION")
        print("="*60)
        generation_results = run_enhanced_generation_evaluation(
            retriever,
            text_gen,
            context_builder,
            test_queries=all_test_queries[:10],  # Subset for faster evaluation
            num_random_queries=10
        )
    
    # Run scenario-based evaluation
    print("\n" + "="*60)
    print("PHASE 3: SCENARIO-BASED EVALUATION")
    print("="*60)
    scenario_results = run_scenario_evaluation(retriever, text_gen, context_builder)
    
    # Compile final results
    final_results = {
        'timestamp': datetime.now().isoformat(),
        'overall_retrieval': retrieval_results['summary'],
        'overall_generation': generation_results.get('summary', {}),
        'scenario_results': scenario_results,
        'detailed_retrieval': retrieval_results.get('detailed_results', {}),
        'detailed_generation': generation_results.get('detailed_results', {})
    }
    
    # Save results
    output_file = "experiments/results/evaluation_results.json"
    Path(output_file).parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(final_results, f, indent=2, ensure_ascii=False)
    
    print("\n" + "="*60)
    print("✅ EVALUATION COMPLETE")
    print("="*60)
    print(f"📁 Results saved to: {output_file}")
    
    # Generate summary report
    generate_summary_report(final_results)


def generate_summary_report(results: Dict[str, Any]):
    """Generate a human-readable summary report"""
    report_file = "experiments/results/evaluation_report.txt"
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("="*80 + "\n")
        f.write("MULTIMODAL RAG SYSTEM - EVALUATION REPORT\n")
        f.write("="*80 + "\n")
        f.write(f"Generated: {results['timestamp']}\n\n")
        
        # Overall Retrieval Metrics
        f.write("OVERALL RETRIEVAL PERFORMANCE\n")
        f.write("-"*80 + "\n")
        retrieval = results['overall_retrieval']
        f.write(f"Total Queries Evaluated: {retrieval['total_queries']}\n")
        f.write(f"Average Latency: {retrieval['avg_latency']:.4f}s\n")
        f.write(f"Average Similarity Score: {retrieval['avg_similarity']:.4f}\n\n")
        f.write("Recall@K:\n")
        for k in [1, 3, 5, 10]:
            if f'recall@{k}' in retrieval:
                f.write(f"  - Recall@{k}: {retrieval[f'recall@{k}']:.4f}\n")
        f.write("\nPrecision@K:\n")
        for k in [1, 3, 5, 10]:
            if f'precision@{k}' in retrieval:
                f.write(f"  - Precision@{k}: {retrieval[f'precision@{k}']:.4f}\n")
        
        # Overall Generation Metrics
        if results['overall_generation']:
            f.write("\n" + "="*80 + "\n")
            f.write("OVERALL GENERATION PERFORMANCE\n")
            f.write("-"*80 + "\n")
            generation = results['overall_generation']
            f.write(f"Total Queries Evaluated: {generation['total_queries']}\n")
            f.write(f"Average Generation Time: {generation['avg_generation_time']:.4f}s\n")
            f.write(f"Average Faithfulness: {generation['avg_faithfulness']:.4f}\n")
            f.write(f"Average Answer Relevance: {generation['avg_answer_relevance']:.4f}\n")
            f.write(f"Average Context Precision: {generation['avg_context_precision']:.4f}\n")
        
        # Scenario Results
        f.write("\n" + "="*80 + "\n")
        f.write("SCENARIO-BASED RESULTS\n")
        f.write("-"*80 + "\n")
        for scenario_name, scenario_data in results['scenario_results'].items():
            f.write(f"\n{scenario_name.upper().replace('_', ' ')}:\n")
            f.write(f"  Retrieval Recall@5: {scenario_data['retrieval'].get('recall@5', 0):.4f}\n")
            f.write(f"  Retrieval Precision@5: {scenario_data['retrieval'].get('precision@5', 0):.4f}\n")
            if 'generation' in scenario_data:
                f.write(f"  Generation Faithfulness: {scenario_data['generation']['avg_faithfulness']:.4f}\n")
        
        f.write("\n" + "="*80 + "\n")
        f.write("END OF REPORT\n")
        f.write("="*80 + "\n")
    
    print(f"📄 Summary report saved to: {report_file}")


if __name__ == "__main__":
    main()
