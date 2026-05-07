import time
import hashlib

class LLMCache:
    def __init__(self,ttl=300):
        self.cache={}
        self.ttl=ttl
    
    def _make_key(self, prompt, context= None):
        
        raw=str(prompt) + str(context)
        return hashlib.md5(raw.encode()).hexdigest()
    
    def get(self, prompt, context= None):
        key = self._make_key(prompt, context)

        if key in self.cache:
            result, timestamp=self.cache[key]

            if time.time() - timestamp < self.ttl:
                return result
            else:
                del self.cache[key]
        return None
    
    def set(self, prompt, result, context= None):
        key = self._make_key(prompt, context)
        self.cache[key]=(result, time.time())