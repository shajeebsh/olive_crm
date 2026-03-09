import openai
from django.conf import settings

class AIService:
    def __init__(self):
        self.api_key = getattr(settings, 'OPENAI_API_KEY', None)
        if self.api_key:
            self.client = openai.OpenAI(api_key=self.api_key)
        else:
            self.client = None
    
    def score_lead(self, contact_data):
        """Analyze contact and assign lead score 0-100"""
        if not self.client:
            return 0
            
        prompt = f"""
        Analyze this lead and score them 0-100 based on their potential as a customer:
        - Job Title: {contact_data.get('title')}
        - Company Size: {contact_data.get('company_size')}
        - Industry: {contact_data.get('industry')}
        - Interactions: {contact_data.get('interaction_count')} emails/calls
        
        Return only a number between 0-100.
        """
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=10
            )
            return int(response.choices[0].message.content.strip())
        except Exception as e:
            print(f"Error scoring lead: {e}")
            return 0
    
    def compose_email(self, context):
        """Generate personalized email based on context"""
        if not self.client:
            return "AI Service not configured."
            
        prompt = f"""
        Write a professional sales follow-up email to {context['contact_name']} 
        from {context['company_name']}. They showed interest in {context['product']}.
        Keep it concise and friendly.
        """
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=300
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error composing email: {e}")
            return "Error generating email."
    
    def sentiment_analysis(self, text):
        """Analyze sentiment of interaction"""
        if not self.client:
            return "NEUTRAL"
            
        prompt = f"Analyze the sentiment of this text: '{text}'. Return POSITIVE, NEUTRAL, or NEGATIVE."
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=20
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error analyzing sentiment: {e}")
            return "NEUTRAL"
