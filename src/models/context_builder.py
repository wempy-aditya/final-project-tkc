"""
Context Builder for RAG
Combines user query with retrieved captions to create LLM context
Optimized for longer, more detailed descriptions
"""

from typing import List, Dict


class ContextBuilder:
    def __init__(self):
        """Initialize context builder"""
        # System message for detailed descriptions
        self.system_template = """You are an expert image description assistant. Create rich, detailed, and engaging descriptions based on the captions provided."""
        
        # User template for longer descriptions
        self.user_template = """Query: {query}

Captions:
{captions}

Create a detailed, comprehensive description (5-7 sentences). Include:
- Main subject and primary action
- Setting, environment, and background details
- Colors, lighting, and visual elements
- Atmosphere, mood, and overall impression
- Any notable objects, people, or features
- Spatial relationships and composition

Description:"""
    
    def build_context(self, query: str, captions: List[str], max_captions: int = 5) -> Dict[str, str]:
        """
        Build context for LLM
        
        Args:
            query: User query
            captions: List of retrieved captions
            max_captions: Maximum number of captions to include (default: 5 for richer context)
            
        Returns:
            Dictionary with system and user messages
        """
        # Use more captions for richer context
        captions = captions[:max_captions]
        
        # Format captions - simple format
        captions_text = "\n".join([f"{i+1}. {cap}" for i, cap in enumerate(captions)])
        
        # Build user message
        user_message = self.user_template.format(
            query=query,
            captions=captions_text
        )
        
        return {
            'system': self.system_template,
            'user': user_message
        }
    
    def build_image_generation_prompt(self, query: str, captions: List[str], max_captions: int = 5) -> str:
        """
        Build prompt for image generation
        
        Args:
            query: User query
            captions: Retrieved captions
            max_captions: Maximum captions to use
            
        Returns:
            Image generation prompt
        """
        # Use top captions
        top_captions = captions[:max_captions]
        
        # Combine query with captions
        if query:
            prompt = f"{query}, " + ", ".join(top_captions[:3])
        else:
            prompt = ", ".join(top_captions[:3])
        
        return prompt


if __name__ == "__main__":
    # Test context builder
    builder = ContextBuilder()
    
    query = "a dog playing in the park"
    captions = [
        "a brown dog playing with a ball in the park",
        "a happy dog running in the grass",
        "a dog playing fetch outdoors"
    ]
    
    context = builder.build_context(query, captions)
    print("System:", context['system'])
    print("\nUser:", context['user'])
    
    img_prompt = builder.build_image_generation_prompt(query, captions)
    print("\nImage prompt:", img_prompt)
