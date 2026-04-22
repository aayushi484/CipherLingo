import string
import random
import base64

class LinguisticEngine:
    """
    Applies custom polyglot transformations to plaintext.
    This acts as Layer 1 in the encryption pipeline, obfuscating text via
    nonce-seeded pseudorandom mapping across 10 international languages and emojis.
    """
    
    def __init__(self):
        # Generate our Polyglot Pool
        self.polyglot_pool = []
        bases = [
            (0x0905, 50),   # Hindi (Devanagari)
            (0x0391, 50),   # Greek
            (0x0410, 50),   # Cyrillic
            (0x0621, 50),   # Arabic
            (0x05D0, 27),   # Hebrew
            (0x30A1, 50),   # Katakana (Japanese)
            (0xAC00, 50),   # Hangul (Korean)
            (0x0531, 38),   # Armenian
            (0x0E01, 40),   # Thai
            (0x1F600, 50),  # Emojis
        ]
        for base, count in bases:
            for i in range(count):
                self.polyglot_pool.append(chr(base + i))
                
        # Supported characters to map
        self.supported_chars = string.ascii_letters + string.digits + " !@#$%^&*()_+-=[]{}|;:',.<>?/`~" + '"'
        
    def _get_seeded_map(self, nonce: bytes) -> dict:
        """Uses the AES Nonce to generate a deterministic random shuffle of the polyglot pool."""
        rng = random.Random()
        rng.seed(nonce)
        
        shuffled_pool = self.polyglot_pool.copy()
        rng.shuffle(shuffled_pool)
        
        mapping = {}
        for i, c in enumerate(self.supported_chars):
            # Maps an ASCII character to a pseudo-random international character
            # ensuring every encryption session uses a novel mapping!
            mapping[c] = shuffled_pool[i % len(shuffled_pool)]
        return mapping

    def transform(self, text: str, nonce: bytes) -> str:
        """
        Transforms input text via:
        1. Nonce-seeded multi-language character mapping.
        2. Grammar shift (reverse words alternatively).
        """
        mapping = self._get_seeded_map(nonce)
        
        # 1. Grammar shift
        words = text.split(" ")
        shifted_words = []
        for i, word in enumerate(words):
            if i % 2 != 0:
                shifted_words.append(word[::-1])
            else:
                shifted_words.append(word)
                
        shifted_text = " ".join(shifted_words)
        
        # 2. Map characters
        transformed_chars = []
        for char in shifted_text:
            if char in mapping:
                transformed_chars.append(mapping[char])
            else:
                b64_c = base64.b64encode(char.encode('utf-8')).decode('utf-8')
                transformed_chars.append(f"[{b64_c}]")
                
        return "".join(transformed_chars)

    def inverse_transform(self, transformed_text: str, nonce: bytes) -> str:
        """
        Reverses the multi-lingual transformation back to plaintext using the same nonce seed.
        """
        mapping = self._get_seeded_map(nonce)
        inverse_mapping = {v: k for k, v in mapping.items()}
        
        # 1. Unmap characters
        unmapped_chars = []
        i = 0
        while i < len(transformed_text):
            if transformed_text[i] == "[":
                # Look for end bracket
                end_idx = transformed_text.find("]", i)
                if end_idx != -1:
                    b64_c = transformed_text[i+1:end_idx]
                    unmapped_chars.append(base64.b64decode(b64_c).decode('utf-8'))
                    i = end_idx + 1
                    continue
            
            c = transformed_text[i]
            if c in inverse_mapping:
                unmapped_chars.append(inverse_mapping[c])
            else:
                unmapped_chars.append(c) 
            i += 1
            
        unmapped_text = "".join(unmapped_chars)
        
        # 2. Reverse Grammar shift
        words = unmapped_text.split(" ")
        unshifted_words = []
        for i, word in enumerate(words):
            if i % 2 != 0:
                unshifted_words.append(word[::-1])
            else:
                unshifted_words.append(word)
                
        return " ".join(unshifted_words)
