"""
TRACK 1: Content Generator
Generates high-quality articles optimized for AdSense
"""

import json
from datetime import datetime, timedelta
from shared.ai_client import get_ai_client
from shared.utils import log_event, generate_id, sanitize_filename, estimate_reading_time

class ContentGenerator:
    def __init__(self, config_path: str = "track1_content/config.json"):
        self.config = self._load_config(config_path)
        self.ai_client = get_ai_client(self.config.get("openai_api_key"))
        self.niches = self.config.get("niches", [
            "AI & Technology",
            "Passive Income Ideas",
            "Productivity Tips",
            "Remote Work",
            "Side Hustles"
        ])
        self.generated_content = []
    
    def _load_config(self, path: str) -> dict:
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except:
            return {}
    
    def generate_article_topic(self, niche: str) -> str:
        """Generate trending article topic in niche"""
        prompt = f"""
        Generate a trending, high-demand article topic for the '{niche}' niche 
        that would get good AdSense clicks. 
        
        Requirements:
        - SEO-friendly
        - Solves a common problem
        - Length: 5-10 words max
        - Include keyword hints
        
        Return only the topic title.
        """
        return self.ai_client.generate_text(prompt, max_tokens=50)
    
    def generate_article(self, topic: str, niche: str) -> dict:
        """Generate full article (1000-1500 words)"""
        prompt = f"""
        Write a comprehensive, SEO-optimized blog article about: "{topic}"
        Niche: {niche}
        
        Requirements:
        - 1000-1500 words
        - Include H2 headers (2-3)
        - Professional but conversational tone
        - Include practical examples
        - End with call-to-action
        - Optimize for AdSense (natural keyword placement)
        - Add meta description (160 chars max)
        
        Format JSON:
        {{
            "title": "Article title",
            "meta_description": "Meta description",
            "content": "Full article content",
            "keywords": ["keyword1", "keyword2", "keyword3"]
        }}
        """
        
        response = self.ai_client.generate_text(prompt, max_tokens=2000)
        
        try:
            article = json.loads(response)
        except:
            article = {
                "title": topic,
                "meta_description": f"Learn about {topic}",
                "content": response,
                "keywords": [topic]
            }
        
        # Add metadata
        article["id"] = generate_id("article")
        article["niche"] = niche
        article["generated_at"] = datetime.now().isoformat()
        article["reading_time"] = estimate_reading_time(article.get("content", ""))
        article["slug"] = sanitize_filename(topic.lower().replace(" ", "-"))
        
        return article
    
    def batch_generate_articles(self, count_per_niche: int = 2) -> list:
        """Generate multiple articles across niches"""
        articles = []
        
        for niche in self.niches:
            for i in range(count_per_niche):
                log_event(f"Generating article {i+1}/{count_per_niche} for {niche}...")
                
                # Generate topic
                topic = self.generate_article_topic(niche)
                if not topic:
                    continue
                
                # Generate full article
                article = self.generate_article(topic, niche)
                articles.append(article)
                
                log_event(f"✓ Generated: {article.get('title')}")
        
        self.generated_content = articles
        return articles
    
    def export_articles(self, output_dir: str = "track1_content/output"):
        """Export articles as JSON and Markdown"""
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        for article in self.generated_content:
            # Save JSON
            json_path = os.path.join(output_dir, f"{article['slug']}.json")
            with open(json_path, 'w') as f:
                json.dump(article, f, indent=2)
            
            # Save Markdown
            md_path = os.path.join(output_dir, f"{article['slug']}.md")
            md_content = f"""# {article['title']}

{article.get('meta_description', '')}

**Reading time:** {article.get('reading_time', 5)} minutes
**Category:** {article.get('niche', '')}

---

{article.get('content', '')}

---

**Keywords:** {', '.join(article.get('keywords', []))}
**Generated:** {article.get('generated_at', '')}
"""
            with open(md_path, 'w') as f:
                f.write(md_content)
        
        log_event(f"✓ Exported {len(self.generated_content)} articles")


if __name__ == "__main__":
    generator = ContentGenerator()
    articles = generator.batch_generate_articles(count_per_niche=1)  # Test: 1 per niche
    generator.export_articles()
    
    print(f"\n✓ Generated {len(articles)} articles")
    for article in articles:
        print(f"  - {article['title']}")
