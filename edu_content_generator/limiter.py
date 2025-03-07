import time

class RateLimiter:
    """Implement API call rate limiting and token management"""
    
    def __init__(self, max_tokens_per_minute=60000):
        self.max_tokens_per_minute = max_tokens_per_minute
        self.current_tokens = 0
        self.last_reset_time = time.time()
    
    def consume_tokens(self, tokens):
        """
        Check and manage token consumption
        
        Args:
            tokens: Number of tokens to consume
            
        Returns:
            Boolean indicating if tokens can be consumed
        """
        current_time = time.time()
        time_since_reset = current_time - self.last_reset_time
        
        if time_since_reset >= 60:
            self.current_tokens = 0
            self.last_reset_time = current_time
            
        if self.current_tokens + tokens > self.max_tokens_per_minute:
            return False
            
        self.current_tokens += tokens
        return True