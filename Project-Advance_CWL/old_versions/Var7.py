#!/usr/bin/env python3
"""
HUMAN-LIKE PASSWORD GENERATOR - Realistic Password Patterns
Generates passwords humans would actually create, not just word combos
"""

import argparse
import sys
from datetime import datetime
import os
import re
import itertools
import random
import string
from typing import Set, Dict, List, Tuple
from collections import defaultdict

class HumanPasswordGenerator:
    def __init__(self):
        # Common human password patterns
        self.pattern_templates = [
            # Pattern: Word + Year
            "{word}{year}",
            "{year}{word}",
            "{word.capitalize()}{year}",
            "{word}{special}{year}",
            
            # Pattern: Word + Number sequence
            "{word}{number}",
            "{number}{word}",
            "{word}{special}{number}",
            
            # Pattern: Multiple words
            "{word1}{word2}",
            "{word1.capitalize()}{word2}",
            "{word1}{special}{word2}",
            "{word1.capitalize()}{special}{word2}",
            
            # Pattern: Word + Special + Number
            "{word}{special}{number}",
            "{special}{word}{number}",
            "{word}{number}{special}",
            
            # Pattern: Common phrases
            "ilove{word}",
            "my{word}",
            "{word}123",
            "{word}!!",
            "admin{word}",
            
            # Pattern: Variations with leet
            "{word_leet}{year}",
            "{word_leet}{number}",
        ]
        
        # Special characters humans actually use
        self.common_specials = ['!', '@', '#', '$', '%', '&', '*']
        
        # Common number patterns humans use (not random)
        self.common_numbers = [
            '123', '321', '456', '654', '789', '987',
            '111', '222', '333', '444', '555', '666',
            '777', '888', '999', '000', '007',
            '1234', '4321', '1111', '2222',
            '69', '420', '99', '88', '77'
        ]
        
        # Common years (not all years)
        self.common_years = [
            str(y) for y in range(1970, 2025)
        ] + ['99', '00', '01', '02', '03', '04', '05', 
             '06', '07', '08', '09', '10', '11', '12',
             '13', '14', '15', '16', '17', '18', '19',
             '20', '21', '22', '23', '24']
        
        # Leet substitutions humans actually use
        self.leet_map = {
            'a': ['4', '@'],
            'b': ['8', '|3'],
            'e': ['3'],
            'g': ['6', '9'],
            'i': ['1', '!'],
            'l': ['1', '|'],
            'o': ['0'],
            's': ['5', '$'],
            't': ['7'],
            'z': ['2']
        }
        
        # Common word pairs humans use together
        self.common_pairs = {
            'love': ['you', 'me', 'life', 'god'],
            'my': ['name', 'dog', 'cat', 'baby', 'love'],
            'super': ['man', 'woman', 'hero', 'star'],
            'blue': ['sky', 'sea', 'eyes'],
            'red': ['car', 'rose', 'devil'],
            'gold': ['fish', 'star', 'medal'],
            'black': ['cat', 'dog', 'hole'],
            'white': ['house', 'cat', 'rose'],
        }
    
    def get_human_input(self) -> Dict:
        """Get information for realistic password generation"""
        print("\n" + "="*60)
        print(" HUMAN-LIKE PASSWORD GENERATOR")
        print("="*60)
        print("\n[!] Focus on what a human would actually use as password\n")
        
        data = {}
        
        # Core personal information (what people actually use)
        print("--- CORE PERSONAL INFO (what people remember) ---")
        data['first_name'] = input("First name: ").strip().lower() or None
        data['last_name'] = input("Last name: ").strip().lower() or None
        data['nickname'] = input("Nickname: ").strip().lower() or None
        
        # Important numbers people remember
        print("\n--- IMPORTANT NUMBERS ---")
        data['birth_year'] = input("Birth year (YYYY): ").strip() or None
        data['lucky_number'] = input("Lucky/favorite number: ").strip() or None
        data['anniversary_year'] = input("Anniversary year: ").strip() or None
        
        # Keywords people would use
        print("\n--- KEYWORDS PEOPLE USE ---")
        keywords = input("Words you like (pets, hobbies, teams): ").strip().lower()
        data['keywords'] = [k.strip() for k in keywords.split(',') if k.strip()]
        
        # Generation style
        print("\n--- PASSWORD STYLE ---")
        print("How would you create a password?")
        print("1. Simple: name + year (john1985)")
        print("2. Common: name + common numbers (john123)")
        print("3. Creative: mix of words with specials (John!cat2023)")
        print("4. All styles")
        
        style = input("Choose style (1-4): ").strip()
        data['style'] = style if style in ['1', '2', '3', '4'] else '4'
        
        # Special characters
        spec_choice = input("Use special characters? (y/n): ").strip().lower()
        data['use_specials'] = spec_choice == 'y'
        
        if data['use_specials']:
            common_specs = input("Use common ones only (!@#$%&*)? (y/n): ").strip().lower()
            if common_specs == 'n':
                custom_specs = input("Which ones? (e.g., !@#): ").strip()
                data['specials'] = list(custom_specs) if custom_specs else ['!']
            else:
                data['specials'] = self.common_specials
        
        # Leet speak
        leet_choice = input("Use leet speak (e.g., p@ssw0rd)? (y/n): ").strip().lower()
        data['use_leet'] = leet_choice == 'y'
        
        return {k: v for k, v in data.items() if v is not None and v != []}
    
    def create_natural_passwords(self, data: Dict) -> Set[str]:
        """Create passwords a human would actually make"""
        passwords = set()
        
        # Collect base words
        words = []
        if data.get('first_name'):
            words.append(data['first_name'])
        if data.get('last_name'):
            words.append(data['last_name'])
        if data.get('nickname'):
            words.append(data['nickname'])
        if data.get('keywords'):
            words.extend(data['keywords'])
        
        if not words:
            return passwords
        
        # Get years
        years = []
        if data.get('birth_year'):
            years.append(data['birth_year'])
            years.append(data['birth_year'][2:])  # Short year
        if data.get('anniversary_year'):
            years.append(data['anniversary_year'])
            years.append(data['anniversary_year'][2:])
        
        # Add common years if needed
        if not years or random.choice([True, False]):
            years.extend(random.sample(self.common_years, 5))
        
        # Get numbers
        numbers = []
        if data.get('lucky_number'):
            numbers.append(data['lucky_number'])
        
        # Add common numbers humans use
        numbers.extend(random.sample(self.common_numbers, 10))
        
        # Get specials
        specials = data.get('specials', ['!', '@', '#']) if data.get('use_specials', False) else ['']
        
        style = data.get('style', '4')
        
        # Generate passwords based on style
        for word in words:
            # Basic word variations
            word_variations = [word]
            word_variations.append(word.title())
            word_variations.append(word.upper())
            
            # Add leet variations if enabled
            if data.get('use_leet'):
                leet_word = self.apply_simple_leet(word)
                if leet_word != word:
                    word_variations.append(leet_word)
                    word_variations.append(leet_word.title())
            
            # Style 1: Simple patterns (most common)
            if style in ['1', '4']:
                for w in word_variations:
                    # Word + Year
                    for year in years[:5]:  # Limit to 5 years
                        passwords.add(f"{w}{year}")
                        passwords.add(f"{year}{w}")
                    
                    # Word + Common number
                    for num in numbers[:5]:
                        passwords.add(f"{w}{num}")
                        if len(num) <= 3:  # Short numbers more common
                            passwords.add(f"{num}{w}")
            
            # Style 2: With separators
            if style in ['2', '4']:
                for w in word_variations:
                    for special in specials[:3]:  # Most common specials
                        # Word + Special + Number
                        for num in numbers[:3]:
                            if special:  # Don't add empty separator twice
                                passwords.add(f"{w}{special}{num}")
                                passwords.add(f"{special}{w}{num}")
                        
                        # Word + Special + Year
                        for year in years[:3]:
                            if special:
                                passwords.add(f"{w}{special}{year}")
            
            # Style 3: Creative combinations
            if style in ['3', '4']:
                # Combine with other words
                for w1 in word_variations:
                    for w2 in words:
                        if w2 != word:  # Don't combine with self
                            # Simple combinations
                            passwords.add(f"{w1}{w2}")
                            passwords.add(f"{w1.title()}{w2}")
                            
                            # With specials
                            for special in specials[:2]:
                                if special:
                                    passwords.add(f"{w1}{special}{w2}")
                            
                            # Common phrases
                            if w2 in ['love', 'god', 'life', 'you']:
                                passwords.add(f"ilove{w1}")
                                passwords.add(f"{w1}{w2}")
            
            # Add some common password patterns
            passwords.update(self.get_common_patterns(word))
        
        # Add completely random common passwords
        passwords.update(self.generate_common_passwords(words, years, numbers, specials))
        
        return passwords
    
    def apply_simple_leet(self, word: str) -> str:
        """Apply leet substitutions humans actually use"""
        leet_word = word
        
        # Only do common substitutions
        substitutions = [
            ('a', '4'), ('e', '3'), ('i', '1'), ('o', '0'),
            ('s', '5'), ('t', '7'), ('l', '1')
        ]
        
        # 30% chance to apply leet
        if random.random() < 0.3:
            for char, sub in substitutions:
                if char in leet_word.lower():
                    # Only substitute some occurrences, not all
                    if random.random() < 0.5:
                        leet_word = leet_word.replace(char, sub)
                        leet_word = leet_word.replace(char.upper(), sub)
        
        return leet_word
    
    def get_common_patterns(self, word: str) -> Set[str]:
        """Get common password patterns for a word"""
        patterns = set()
        
        # Very common patterns
        patterns.add(f"{word}123")
        patterns.add(f"{word}1234")
        patterns.add(f"{word}!")
        patterns.add(f"{word}!!")
        patterns.add(f"{word}?")
        
        patterns.add(f"{word.title()}123")
        patterns.add(f"{word.title()}!")
        
        # Common sports patterns
        if len(word) <= 5:
            patterns.add(f"{word}88")
            patterns.add(f"{word}99")
        
        return patterns
    
    def generate_common_passwords(self, words: List[str], years: List[str], 
                                 numbers: List[str], specials: List[str]) -> Set[str]:
        """Generate completely common passwords"""
        common = set()
        
        # Top common passwords (always include)
        top_passwords = [
            'password', '123456', '12345678', '123456789',
            'qwerty', 'abc123', 'password1', '12345',
            '1234567', '1234567890', 'admin', 'welcome',
            'monkey', 'letmein', 'dragon', 'football',
            'baseball', 'superman', 'mustang', 'michael'
        ]
        
        common.update(top_passwords)
        
        # Add year variations to common words
        for pwd in list(common):
            for year in years[:3]:
                common.add(f"{pwd}{year}")
                common.add(f"{year}{pwd}")
        
        # Add some number patterns
        for pwd in list(common)[:10]:
            for num in ['123', '1234', '1', '2', '99', '88']:
                common.add(f"{pwd}{num}")
        
        # Add special character variations
        for pwd in list(common)[:5]:
            for special in specials[:2]:
                if special:
                    common.add(f"{pwd}{special}")
                    common.add(f"{special}{pwd}")
        
        return common
    
    def filter_passwords(self, passwords: Set[str], min_len: int = 6, 
                        max_len: int = 20) -> Set[str]:
        """Filter passwords by length and remove unrealistic ones"""
        filtered = set()
        
        for pwd in passwords:
            # Length check
            if min_len <= len(pwd) <= max_len:
                # Remove passwords with too many specials in a row
                if re.search(r'[!@#$%^&*]{3,}', pwd):
                    continue
                
                # Remove passwords with too many numbers in a row (more than 6)
                if re.search(r'\d{7,}', pwd):
                    continue
                
                # Remove passwords that are just numbers
                if pwd.isdigit():
                    continue
                
                # Remove passwords that are just specials
                if all(c in '!@#$%^&*' for c in pwd):
                    continue
                
                filtered.add(pwd)
        
        return filtered
    
    def analyze_patterns(self, passwords: Set[str]) -> None:
        """Analyze and show password patterns"""
        if not passwords:
            return
        
        print("\n" + "="*60)
        print(" PASSWORD PATTERN ANALYSIS")
        print("="*60)
        
        sample = random.sample(list(passwords), min(50, len(passwords)))
        
        # Categorize patterns
        categories = {
            'name_year': 0,
            'name_number': 0,
            'name_special_number': 0,
            'common_words': 0,
            'simple': 0,
            'creative': 0
        }
        
        for pwd in sample:
            # Check patterns
            if any(year in pwd for year in self.common_years if year):
                categories['name_year'] += 1
            
            if any(num in pwd for num in self.common_numbers):
                categories['name_number'] += 1
            
            if any(spec in pwd for spec in self.common_specials):
                if any(num in pwd for num in self.common_numbers):
                    categories['name_special_number'] += 1
            
            if pwd.lower() in ['password', 'qwerty', 'admin', 'welcome']:
                categories['common_words'] += 1
            
            if len(pwd) <= 8:
                categories['simple'] += 1
            else:
                categories['creative'] += 1
        
        print("\nPattern Distribution in Sample:")
        for category, count in categories.items():
            percentage = (count / len(sample)) * 100
            print(f"  {category:20}: {count:3} ({percentage:5.1f}%)")
        
        print(f"\nSample Passwords Generated:")
        for i, pwd in enumerate(sample[:20], 1):
            print(f"  {i:2}. {pwd}")
        
        print(f"\nTotal unique passwords: {len(passwords):,}")
    
    def generate(self, data: Dict) -> Set[str]:
        """Main generation function"""
        print("\n[*] Generating human-like passwords...")
        
        # Generate natural passwords
        passwords = self.create_natural_passwords(data)
        
        print(f"[+] Initial generation: {len(passwords):,} passwords")
        
        # Filter unrealistic ones
        min_len = 6
        max_len = 20
        filtered = self.filter_passwords(passwords, min_len, max_len)
        
        print(f"[+] After filtering: {len(filtered):,} passwords")
        
        return filtered

def main():
    parser = argparse.ArgumentParser(
        description='HUMAN-LIKE PASSWORD GENERATOR - Realistic Password Patterns',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive mode (recommended)
  python human_passwords.py
  
  # Quick mode with basic info
  python human_passwords.py --name john --year 1985 --keywords cat,football
  
  # Generate common passwords only
  python human_passwords.py --common-only
        """
    )
    
    # Basic options
    parser.add_argument('--name', help='First name or nickname')
    parser.add_argument('--year', help='Birth year or important year')
    parser.add_argument('--keywords', help='Comma-separated keywords')
    
    # Generation options
    parser.add_argument('--style', type=int, choices=[1, 2, 3, 4], default=4,
                       help='Password style: 1=Simple, 2=Common, 3=Creative, 4=All')
    parser.add_argument('--common-only', action='store_true',
                       help='Generate only common passwords')
    
    # Output
    parser.add_argument('-o', '--output', default='human_passwords.txt',
                       help='Output filename')
    parser.add_argument('--max-passwords', type=int, default=5000,
                       help='Maximum number of passwords to generate')
    
    args = parser.parse_args()
    
    generator = HumanPasswordGenerator()
    
    if args.common_only:
        print("[*] Generating common passwords only...")
        data = {
            'style': '4',
            'use_specials': True,
            'use_leet': True,
            'specials': generator.common_specials
        }
    else:
        # Get user input
        print("\n" + "="*60)
        print(" HUMAN PASSWORD GENERATOR")
        print("="*60)
        
        data = {}
        
        # Use command line args or ask
        if args.name:
            data['first_name'] = args.name.lower()
        else:
            data['first_name'] = input("\nFirst name/nickname: ").strip().lower() or 'user'
        
        if args.year:
            data['birth_year'] = args.year
        else:
            year_input = input("Important year (birth/anniversary): ").strip()
            if year_input:
                data['birth_year'] = year_input
        
        if args.keywords:
            data['keywords'] = [k.strip().lower() for k in args.keywords.split(',')]
        else:
            keywords = input("Keywords (pets, hobbies, etc.): ").strip().lower()
            if keywords:
                data['keywords'] = [k.strip() for k in keywords.split(',')]
        
        # Generation options
        data['style'] = str(args.style)
        
        use_specials = input("Add special characters? (y/n): ").strip().lower()
        data['use_specials'] = use_specials == 'y'
        
        if data['use_specials']:
            data['specials'] = generator.common_specials
        
        use_leet = input("Use leet speak? (y/n): ").strip().lower()
        data['use_leet'] = use_leet == 'y'
    
    # Generate passwords
    passwords = generator.generate(data)
    
    # Limit if specified
    if args.max_passwords > 0 and len(passwords) > args.max_passwords:
        passwords = set(list(passwords)[:args.max_passwords])
        print(f"[*] Limited to {args.max_passwords} passwords")
    
    # Analyze patterns
    generator.analyze_patterns(passwords)
    
    # Save to file
    if passwords:
        print(f"\n[*] Saving to {args.output}...")
        
        # Sort passwords by length and similarity
        sorted_passwords = sorted(passwords, key=lambda x: (len(x), x))
        
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(f"# Human-like passwords generated on {datetime.now().strftime('%Y-%m-%d')}\n")
            f.write(f"# Total: {len(sorted_passwords)}\n")
            f.write("#" * 50 + "\n\n")
            
            for pwd in sorted_passwords:
                f.write(pwd + '\n')
        
        file_size = os.path.getsize(args.output)
        print(f"[+] Saved {len(sorted_passwords):,} passwords")
        print(f"[+] File size: {file_size:,} bytes")
        
        # Show some examples
        print("\nExamples of generated passwords:")
        examples = random.sample(sorted_passwords, min(10, len(sorted_passwords)))
        for i, pwd in enumerate(examples, 1):
            print(f"  {i:2}. {pwd}")
    else:
        print("[-] No passwords generated!")

if __name__ == '__main__':
    main()