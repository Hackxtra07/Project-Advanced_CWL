#!/usr/bin/env python3
"""
MEGA WORDLIST GENERATOR v3.0
Combines ALL features: maximum combinations, minimal input, leet mode, 
special chars, numbers, interactive mode, batch processing, AND CUPP-like features
"""

import argparse
import sys
import itertools
from datetime import datetime
import os
import re
import json
import csv
import random
from typing import List, Set, Dict, Any, Optional
from collections import OrderedDict

class MegaWordlistGenerator:
    def __init__(self):
        self.total_generated = 0
        self.word_cache = set()
        
        # Enhanced leet mappings (from first code + more)
        self.leet_maps = {
            'a': ['4', '@', '/\\', '^', '∂', 'λ', 'ª', 'à', 'á', 'â', 'ã', 'ä', 'å', 'ā', 'ă', 'ą'],
            'b': ['8', '13', '|3', 'ß', ']3', 'þ', 'Þ', 'β'],
            'c': ['(', '[', '<', '©', '¢', 'ç', 'ć', 'č', 'ĉ', 'ċ'],
            'd': ['|)', '|]', 'Ð', 'đ', 'ď', 'ð'],
            'e': ['3', '&', '€', '£', 'ë', 'ē', 'ĕ', 'ė', 'ę', 'ě', 'ȅ', 'ȇ', 'ε'],
            'f': ['|=', 'ph', 'ƒ', 'ф', 'φ'],
            'g': ['6', '9', '&', 'ğ', 'ĝ', 'ğ', 'ġ', 'ģ'],
            'h': ['#', '|-|', '}{', ']-[', ')-('],
            'i': ['1', '!', '|', 'ï', 'ì', 'í', 'î', 'ĩ', 'ī', 'ĭ', 'į', 'ı'],
            'j': ['_|', ']', '¿'],
            'k': ['|<', '|{', 'ɮ', 'ķ', 'ĸ'],
            'l': ['1', '|', '7', '£', '¬', 'ł', 'ĺ', 'ļ', 'ľ', 'ŀ'],
            'm': ['/\\/\\', '|\\/|', '^^', 'ɱ', 'µ'],
            'n': ['|\\|', '/\\/', 'И', 'п', 'ñ', 'ń', 'ņ', 'ň', 'ŉ'],
            'o': ['0', '()', '°', 'Θ', 'Ø', 'õ', 'ó', 'ô', 'ő', 'ø', 'ō', 'ŏ', 'ő'],
            'p': ['|>', '|*', 'þ', '¶', 'ρ', 'Þ', 'π'],
            'q': ['0_', '9', '(,)'],
            'r': ['|2', 'Я', '®', 'ʁ', 'ŕ', 'ŗ', 'ř'],
            's': ['5', '$', 'z', '§', 'š', 'ś', 'ş', 'ŝ', 'ș'],
            't': ['7', '+', '†', 'ţ', 'ť', 'ŧ'],
            'u': ['|_|', 'µ', 'û', 'ü', 'ù', 'ú', 'ű', 'ū', 'ŭ', 'ů'],
            'v': ['\\/', '|/', '√', 'ν'],
            'w': ['\\/\\/', 'vv', 'ш', 'ω', 'ŵ'],
            'x': ['><', '}{', '×', 'ж', 'χ', 'ξ'],
            'y': ['`/', '¥', 'ÿ', 'ý', 'ŷ', 'ȳ'],
            'z': ['2', '7_', 'ž', 'ζ', 'ź', 'ż', 'ž']
        }
        
        # Common number patterns (extensive list)
        self.number_patterns = [
            '', '1', '12', '123', '1234', '12345', '123456', '1234567', '12345678', '123456789',
            '0', '00', '000', '0000', '00000', '000000',
            '01', '02', '03', '04', '05', '06', '07', '08', '09', '10',
            '11', '22', '33', '44', '55', '66', '77', '88', '99',
            '111', '222', '333', '444', '555', '666', '777', '888', '999',
            '1111', '2222', '3333', '4444', '5555', '6666', '7777', '8888', '9999',
            '101', '202', '303', '404', '505', '606', '707', '808', '909',
            '010', '020', '030', '040', '050', '060', '070', '080', '090',
            '1122', '1212', '1221', '2112', '2211', '2121',
            '007', '008', '009',
            '100', '200', '300', '400', '500', '600', '700', '800', '900',
            '1000', '2000', '3000', '5000',
            '69', '6969', '420', '4242', '666', '777', '888', '999',
            '123123', '321321', '456456', '654654',
            '0101', '0202', '0303', '0404', '0505',
            '102030', '304050', '405060',
            '112233', '223344', '334455', '445566',
            '13579', '24680', '10203', '30405',
            '54321', '654321', '7654321', '87654321', '987654321'
        ]
        
        # Special characters
        self.special_chars = ['!', '@', '#', '$', '%', '^', '&', '*', '-', '_', '.', '+', '=', '~', '`']
        self.special_prefixes = ['!', '@', '#', '$', '%', '^', '&', '*']
        self.special_suffixes = ['!', '@', '#', '$', '%', '^', '&', '*', '123', '1', '!!', '!!!']
        
        # Common passwords and words (from CUPP and more)
        self.common_passwords = [
            'password', '123456', '12345678', '1234', 'qwerty', '12345', 'dragon', 'baseball',
            'football', 'letmein', 'monkey', 'mustang', 'michael', 'shadow', 'master', 'jennifer',
            '111111', '2000', 'jordan', 'superman', 'harley', 'fuckme', 'hunter', 'fuckyou',
            'trustno1', 'ranger', 'buster', 'thomas', 'tigger', 'robert', 'soccer', 'batman',
            'test', 'pass', 'killer', 'hockey', 'george', 'charlie', 'andrew', 'michelle',
            'love', 'sunshine', 'jessica', 'pepper', 'daniel', 'access', '1234567', '654321',
            'joshua', 'maggie', 'starwars', 'silver', 'william', 'dallas', 'yankees', '123123',
            'ashley', 'bailey', 'hello', 'matrix', 'buster', '123', '1234', '12345', '123456',
            '1234567', '12345678', 'admin', 'welcome', 'login', 'abc123', 'passw0rd', 'password1',
            'admin123', 'qwerty123', 'welcome123', 'monkey123', 'letmein123', 'dragon123'
        ]
        
        # Separators for combinations
        self.separators = ['', '.', '_', '-', '', ' ', '@', '$', '&']
        
        # Keyboard patterns
        self.keyboard_patterns = [
            'qwerty', 'asdfgh', 'zxcvbn', 'qazwsx', '123qwe', '1qaz', '2wsx', '3edc',
            '4rfv', '5tgb', '6yhn', '7ujm', '8ik,', '9ol.', '0p;/', '!qaz', '@wsx',
            'zaq1xsw2', 'xsw2zaq1', '!qaz@wsx', '1qaz2wsx3edc', 'qwertyuiop',
            'asdfghjkl', 'zxcvbnm', 'qwerty123', 'asdf1234', 'zxcv1234'
        ]
        
        # Months and seasons
        self.months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
        self.seasons = ['spring', 'summer', 'autumn', 'winter', 'fall']
        
        # Common suffixes/prefixes for names
        self.name_suffixes = ['y', 'ie', 'ey', 'i', 'o', 'er', 'man', 'boy', 'girl', 'kid', 'master', 'lord', 'king', 'queen']
        self.name_prefixes = ['big', 'little', 'super', 'mega', 'ultra', 'hyper', 'micro', 'macro', 'mr', 'ms', 'mrs', 'dr', 'prof']
    
    def get_interactive_input(self):
        """Get comprehensive input interactively (from first code)"""
        print("\n" + "="*70)
        print(" MEGA WORDLIST GENERATOR - Interactive Mode")
        print("="*70)
        
        data = {}
        
        print("\n--- PERSONAL INFORMATION ---")
        data['first_name'] = input("First name: ").strip().lower()
        data['last_name'] = input("Last name: ").strip().lower()
        data['nickname'] = input("Nickname (optional): ").strip().lower()
        data['maiden_name'] = input("Mother's maiden name (optional): ").strip().lower()
        data['pet_name'] = input("Pet name (optional): ").strip().lower()
        data['company'] = input("Company name (optional): ").strip().lower()
        
        print("\n--- IMPORTANT DATES ---")
        data['birthdate'] = input("Birthdate (DD/MM/YYYY or MM/DD/YYYY): ").strip()
        data['partner_birthdate'] = input("Partner's birthdate (optional): ").strip()
        data['anniversary'] = input("Anniversary date (optional): ").strip()
        
        print("\n--- KEYWORDS AND NUMBERS ---")
        keywords = input("Important keywords (comma-separated): ").strip().lower()
        data['keywords'] = [k.strip() for k in keywords.split(',') if k.strip()]
        
        data['phone'] = input("Phone number (optional): ").strip()
        data['zipcode'] = input("Zip/Postal code (optional): ").strip()
        
        print("\n--- ADDITIONAL INFORMATION ---")
        data['city'] = input("City/Town (optional): ").strip().lower()
        data['country'] = input("Country (optional): ").strip().lower()
        data['school'] = input("School/University (optional): ").strip().lower()
        data['team'] = input("Favorite sports team (optional): ").strip().lower()
        data['band'] = input("Favorite band/artist (optional): ").strip().lower()
        data['movie'] = input("Favorite movie (optional): ").strip().lower()
        data['book'] = input("Favorite book (optional): ").strip().lower()
        data['color'] = input("Favorite color (optional): ").strip().lower()
        data['food'] = input("Favorite food (optional): ").strip().lower()
        data['car'] = input("Car brand/model (optional): ").strip().lower()
        
        print("\n--- GENERATION OPTIONS ---")
        data['auto_common'] = input("Add common passwords? (y/n, default: y): ").strip().lower() != 'n'
        data['add_months'] = input("Add months and seasons? (y/n, default: y): ").strip().lower() != 'n'
        data['add_keyboard'] = input("Add keyboard patterns? (y/n, default: y): ").strip().lower() != 'n'
        
        # Clean empty values
        return {k: v for k, v in data.items() if v}
    
    def get_minimal_input(self):
        """Get minimal input for maximum generation"""
        print("\n" + "="*70)
        print(" MINIMAL INPUT MODE - Maximum combinations")
        print("="*70)
        
        data = {}
        
        print("\n[!] Provide minimum info for maximum combinations!\n")
        
        # Absolute minimum
        data['first_name'] = input("First name (REQUIRED): ").strip().lower()
        if not data['first_name']:
            print("[!] First name is required!")
            sys.exit(1)
        
        data['last_name'] = input("Last name (optional but recommended): ").strip().lower()
        
        birth_input = input("Birth year (YYYY) or full date (DD/MM/YYYY): ").strip()
        if birth_input:
            if '/' in birth_input:
                data['birthdate'] = birth_input
            else:
                data['birthdate'] = f"01/01/{birth_input}"
        
        # One keyword
        keyword = input("One important word (pet, city, team, etc.): ").strip().lower()
        if keyword:
            data['keywords'] = [keyword]
        
        # Auto options
        print("\n[!] Auto-enabling all generation features for maximum combinations!")
        data['auto_common'] = True
        data['add_months'] = True
        data['add_keyboard'] = True
        data['aggressive_mode'] = True
        data['extreme_mode'] = True
        
        return data
    
    def parse_date_comprehensive(self, date_str):
        """Parse dates in ALL possible formats (from first code + enhanced)"""
        date_parts = []
        
        if not date_str:
            return date_parts
        
        # Try multiple date formats
        formats = [
            '%d/%m/%Y', '%m/%d/%Y', '%d-%m-%Y', '%m-%d-%Y', '%Y-%m-%d',
            '%d/%m/%y', '%m/%d/%y', '%y-%m-%d', '%Y/%m/%d', '%m/%d/%Y',
            '%d%m%Y', '%m%d%Y', '%Y%m%d', '%d%m%y', '%m%d%y',
            '%d %b %Y', '%d %B %Y', '%b %d %Y', '%B %d %Y'
        ]
        
        for fmt in formats:
            try:
                dt = datetime.strptime(date_str, fmt)
                
                # Individual components
                day = dt.strftime('%d').lstrip('0') or '0'  # Remove leading zero but keep '0'
                month = dt.strftime('%m').lstrip('0') or '0'
                year_full = dt.strftime('%Y')
                year_short = dt.strftime('%y')
                month_name = dt.strftime('%b').lower()  # Jan
                month_full = dt.strftime('%B').lower()  # January
                
                # Add all variations
                variations = [
                    # Basic components
                    day, month, year_full, year_short,
                    month_name, month_full,
                    
                    # Combined without separators
                    day + month,
                    month + day,
                    day + month + year_short,
                    month + day + year_short,
                    day + month + year_full,
                    month + day + year_full,
                    year_short + month + day,
                    year_full + month + day,
                    year_short + day + month,
                    year_full + day + month,
                    
                    # With separators
                    f"{day}.{month}.{year_short}",
                    f"{month}.{day}.{year_short}",
                    f"{day}_{month}_{year_short}",
                    f"{month}_{day}_{year_short}",
                    f"{day}-{month}-{year_short}",
                    f"{month}-{day}-{year_short}",
                    
                    # Reversed
                    day[::-1], month[::-1], year_full[::-1],
                    (day + month)[::-1],
                    (month + day)[::-1],
                    
                    # Last 4 digits of year combinations
                    year_full[2:] + year_full[2:],  # 9090
                    year_full[2:] + day,
                    year_full[2:] + month,
                ]
                
                date_parts.extend(variations)
                break  # Stop at first successful format
                
            except ValueError:
                continue
        
        # Also try to extract year from any string
        year_match = re.search(r'(19\d{2}|20\d{2})', date_str)
        if year_match:
            year = year_match.group(1)
            if year not in date_parts:
                date_parts.extend([year, year[2:]])
        
        # Remove duplicates and empty strings
        return list(set([p for p in date_parts if p and p.strip()]))
    
    def extract_all_base_words(self, data: Dict) -> Set:
        """Extract ALL base words from input data"""
        base_words = set()
        
        # Personal names and variants
        personal_fields = ['first_name', 'last_name', 'nickname', 'maiden_name', 'pet_name']
        for field in personal_fields:
            if field in data and data[field]:
                name = data[field]
                base_words.add(name)
                base_words.add(name.title())
                base_words.add(name.upper())
                
                # Generate name variations
                base_words.update(self.generate_name_variations(name))
        
        # Company
        if 'company' in data and data['company']:
            company = data['company']
            base_words.add(company)
            base_words.add(company.title())
            base_words.add(company.replace(' ', ''))
            base_words.add(company.replace(' ', '_'))
        
        # Dates
        date_fields = ['birthdate', 'partner_birthdate', 'anniversary']
        for field in date_fields:
            if field in data and data[field]:
                base_words.update(self.parse_date_comprehensive(data[field]))
        
        # Keywords
        if 'keywords' in data:
            for keyword in data['keywords']:
                base_words.add(keyword)
                base_words.add(keyword.title())
                base_words.add(keyword.upper())
        
        # Location and other info
        extra_fields = ['city', 'country', 'school', 'team', 'band', 'movie', 'book', 'color', 'food', 'car']
        for field in extra_fields:
            if field in data and data[field]:
                value = data[field]
                base_words.add(value)
                base_words.add(value.title())
        
        # Phone and zip
        if 'phone' in data and data['phone']:
            phone = re.sub(r'\D', '', data['phone'])  # Keep only digits
            if phone:
                base_words.add(phone)
                # Last 4 digits
                if len(phone) >= 4:
                    base_words.add(phone[-4:])
        
        if 'zipcode' in data and data['zipcode']:
            base_words.add(data['zipcode'])
        
        # Add common passwords if enabled
        if data.get('auto_common'):
            base_words.update(self.common_passwords)
        
        # Add months and seasons if enabled
        if data.get('add_months'):
            base_words.update(self.months)
            base_words.update(self.seasons)
            base_words.update([m.title() for m in self.months])
            base_words.update([s.title() for s in self.seasons])
        
        # Add keyboard patterns if enabled
        if data.get('add_keyboard'):
            base_words.update(self.keyboard_patterns)
        
        return base_words
    
    def generate_name_variations(self, name: str) -> List[str]:
        """Generate variations of a name"""
        variations = set()
        
        if not name or len(name) < 2:
            return list(variations)
        
        name_lower = name.lower()
        
        # Basic variations
        variations.update([name_lower, name_lower.title(), name_lower.upper()])
        
        # Common modifications
        for suffix in self.name_suffixes:
            variations.add(name_lower + suffix)
            variations.add(name_lower.title() + suffix)
        
        for prefix in self.name_prefixes:
            variations.add(prefix + name_lower)
            variations.add(prefix.title() + name_lower.title())
        
        # Double and triple
        variations.add(name_lower * 2)
        variations.add(name_lower * 3)
        variations.add(name_lower.title() * 2)
        
        # Reverse
        reversed_name = name_lower[::-1]
        variations.add(reversed_name)
        variations.add(reversed_name.title())
        
        # Remove vowels
        no_vowels = ''.join([c for c in name_lower if c not in 'aeiou'])
        if no_vowels and len(no_vowels) >= 2:
            variations.add(no_vowels)
            variations.add(no_vowels.title())
        
        # Every other letter
        if len(name_lower) >= 3:
            every_other = name_lower[::2]
            variations.add(every_other)
            variations.add(every_other.title())
        
        # Initials and combinations
        if len(name_lower) >= 3:
            variations.add(name_lower[0])  # First letter
            variations.add(name_lower[0] + name_lower[-1])  # First and last
        
        return list(variations)
    
    def generate_combinations_level1(self, base_words: Set) -> Set:
        """Level 1: Basic combinations (from first code)"""
        combinations = set()
        
        words_list = list(base_words)
        
        print("[*] Level 1: Generating basic combinations...")
        
        # Single words with case variations
        for word in words_list:
            combinations.add(word)
            combinations.add(word.lower())
            combinations.add(word.upper())
            combinations.add(word.title())
            combinations.add(word.capitalize())
        
        # Two-word combinations with separators
        for i, word1 in enumerate(words_list[:50]):  # Limit to first 50
            for word2 in words_list[:50]:
                if word1 != word2:
                    for sep in self.separators:
                        combinations.add(word1 + sep + word2)
                        combinations.add(word2 + sep + word1)
                    
                    # Without separator
                    combinations.add(word1 + word2)
                    combinations.add(word2 + word1)
        
        return combinations
    
    def generate_combinations_level2(self, base_words: Set) -> Set:
        """Level 2: Number patterns (aggressive)"""
        combinations = set()
        
        words_list = list(base_words)
        
        print("[*] Level 2: Adding number patterns...")
        
        for word in words_list[:200]:  # Limit for performance
            # Add ALL number patterns
            for num in self.number_patterns:
                if num:  # Skip empty
                    combinations.add(word + num)
                    combinations.add(num + word)
                    combinations.add(word + '_' + num)
                    combinations.add(num + '_' + word)
                    combinations.add(word + '.' + num)
                    combinations.add(num + '.' + word)
            
            # Add sequential numbers 0-999
            for i in range(1000):
                combinations.add(word + str(i).zfill(3))
                combinations.add(str(i).zfill(3) + word)
            
            # Add common year patterns
            for year in range(1970, 2026):
                year_str = str(year)
                combinations.add(word + year_str)
                combinations.add(word + year_str[2:])
                combinations.add(year_str + word)
                combinations.add(year_str[2:] + word)
        
        return combinations
    
    def generate_combinations_level3(self, base_words: Set) -> Set:
        """Level 3: Special characters"""
        combinations = set()
        
        words_list = list(base_words)[:100]  # Limit
        
        print("[*] Level 3: Adding special characters...")
        
        for word in words_list:
            # Add to all combinations
            combinations.add(word)
            
            # Every special char at start and end
            for special in self.special_chars:
                combinations.add(special + word)
                combinations.add(word + special)
                combinations.add(special + word + special)
                
                # Double special
                combinations.add(special * 2 + word)
                combinations.add(word + special * 2)
                combinations.add(special * 3 + word)
                combinations.add(word + special * 3)
            
            # Multiple special chars
            for pre in self.special_prefixes:
                for suf in self.special_suffixes:
                    combinations.add(pre + word + suf)
        
        return combinations
    
    def generate_combinations_level4(self, base_words: Set) -> Set:
        """Level 4: Leet speak transformations"""
        combinations = set()
        
        words_list = list(base_words)[:50]  # Limit
        
        print("[*] Level 4: Applying leet speak...")
        
        for word in words_list:
            word_lower = word.lower()
            combinations.add(word)  # Original
            
            # Generate leet variations
            leet_variations = self.apply_leet_transform(word_lower)
            combinations.update(leet_variations)
            
            # Case variations of leet
            for leet_word in list(leet_variations)[:10]:
                combinations.add(leet_word.title())
                combinations.add(leet_word.upper())
        
        return combinations
    
    def apply_leet_transform(self, word: str, max_variations: int = 1000) -> Set:
        """Apply leet speak transformations to a word"""
        variations = set([word])
        
        if len(word) > 10:
            word = word[:10]  # Limit for performance
        
        # Common leet patterns
        common_patterns = [
            word.replace('a', '4').replace('e', '3').replace('i', '1').replace('o', '0'),
            word.replace('s', '5').replace('t', '7').replace('o', '0'),
            word.replace('a', '@').replace('s', '$').replace('i', '!'),
            word.replace('a', '4').replace('e', '3').replace('i', '!').replace('o', '0').replace('s', '$'),
        ]
        
        variations.update(common_patterns)
        
        # Generate random leet variations
        for _ in range(min(max_variations, 500)):
            leet_word = ''
            for char in word:
                if char in self.leet_maps and random.random() > 0.7:
                    leet_word += random.choice(self.leet_maps[char][:2])
                else:
                    leet_word += char
            variations.add(leet_word)
        
        return variations
    
    def generate_combinations_level5(self, base_words: Set) -> Set:
        """Level 5: Advanced hybrid combinations"""
        combinations = set()
        
        words_list = list(base_words)[:30]  # Limit
        
        print("[*] Level 5: Creating hybrid combinations...")
        
        # Three-part combinations
        for i in range(min(20, len(words_list))):
            for j in range(min(20, len(words_list))):
                if i != j:
                    word1 = words_list[i]
                    word2 = words_list[j]
                    
                    # Combine with common words in middle
                    for common in ['love', 'baby', 'girl', 'boy', 'man', 'woman', 'kid', 'boss', 'master', 'king']:
                        combinations.add(word1 + common + word2)
                        combinations.add(word2 + common + word1)
                        combinations.add(common + word1 + word2)
                    
                    # With numbers in middle
                    for num in range(100):
                        num_str = str(num).zfill(2)
                        combinations.add(word1 + num_str + word2)
                        combinations.add(word2 + num_str + word1)
                        combinations.add(num_str + word1 + word2)
        
        # Initial combinations
        initials = []
        for word in words_list[:10]:
            if word and len(word) > 0:
                initials.append(word[0].lower())
        
        if len(initials) >= 2:
            for i in range(len(initials)):
                for j in range(len(initials)):
                    if i != j:
                        combo = initials[i] + initials[j]
                        combinations.add(combo)
                        combinations.add(combo.upper())
                        
                        # With numbers
                        for num in self.number_patterns[:20]:
                            if num:
                                combinations.add(combo + num)
                                combinations.add(num + combo)
        
        return combinations
    
    def generate_combinations_level6(self, base_words: Set) -> Set:
        """Level 6: Keyboard pattern combinations"""
        combinations = set()
        
        words_list = list(base_words)[:20]
        
        print("[*] Level 6: Adding keyboard patterns...")
        
        # Add keyboard patterns themselves
        combinations.update(self.keyboard_patterns)
        
        # Combine words with keyboard patterns
        for word in words_list:
            for pattern in self.keyboard_patterns[:10]:
                combinations.add(word + pattern)
                combinations.add(pattern + word)
                combinations.add(word + '_' + pattern)
                combinations.add(pattern + '_' + word)
        
        return combinations
    
    def mega_generate(self, data: Dict, mode: str = 'aggressive') -> Set:
        """Master generation function - combines ALL levels"""
        all_combinations = set()
        
        print(f"\n{'='*70}")
        print(f" MEGA GENERATION MODE: {mode.upper()}")
        print(f"{'='*70}")
        
        # Extract ALL base words
        print("\n[*] Extracting base words from input...")
        base_words = self.extract_all_base_words(data)
        print(f"[+] Base words extracted: {len(base_words)}")
        
        # Apply generation levels based on mode
        levels_to_run = []
        
        if mode == 'normal':
            levels_to_run = [1, 2, 3]
        elif mode == 'aggressive':
            levels_to_run = [1, 2, 3, 4, 5]
        elif mode == 'extreme':
            levels_to_run = [1, 2, 3, 4, 5, 6]
        elif mode == 'ultimate':
            # Run everything multiple times
            levels_to_run = [1, 2, 3, 4, 5, 6]
        
        # Run selected levels
        for level in levels_to_run:
            if level == 1:
                all_combinations.update(self.generate_combinations_level1(base_words))
            elif level == 2:
                all_combinations.update(self.generate_combinations_level2(base_words))
            elif level == 3:
                all_combinations.update(self.generate_combinations_level3(base_words))
            elif level == 4:
                all_combinations.update(self.generate_combinations_level4(base_words))
            elif level == 5:
                all_combinations.update(self.generate_combinations_level5(base_words))
            elif level == 6:
                all_combinations.update(self.generate_combinations_level6(base_words))
            
            print(f"[+] Level {level} complete: {len(all_combinations):,} total combinations")
        
        # For ultimate mode, do extra passes
        if mode == 'ultimate':
            print("[*] ULTIMATE MODE: Running extra generation passes...")
            
            # Pass 1: Add number patterns to everything
            extra_combinations = set()
            for word in list(all_combinations)[:50000]:  # Limit
                for num in self.number_patterns[:50]:
                    if num:
                        extra_combinations.add(word + num)
                        extra_combinations.add(num + word)
            
            all_combinations.update(extra_combinations)
            print(f"[+] Extra pass 1: {len(all_combinations):,} total")
            
            # Pass 2: Add special chars to everything
            extra_combinations = set()
            for word in list(all_combinations)[:50000]:
                for special in self.special_chars[:5]:
                    extra_combinations.add(special + word)
                    extra_combinations.add(word + special)
            
            all_combinations.update(extra_combinations)
            print(f"[+] Extra pass 2: {len(all_combinations):,} total")
        
        # Filter by length
        min_len = data.get('min_length', 4)
        max_len = data.get('max_length', 32)
        
        filtered = {w for w in all_combinations if min_len <= len(w) <= max_len}
        
        print(f"\n[*] Filtering: {len(all_combinations):,} -> {len(filtered):,} "
              f"(length {min_len}-{max_len})")
        
        return filtered
    
    def save_wordlist(self, wordlist: Set, filename: str, max_words: int = 10000000):
        """Save wordlist with progress and statistics"""
        wordlist_list = list(wordlist)
        
        if len(wordlist_list) > max_words:
            print(f"[!] Wordlist too large ({len(wordlist_list):,}), sampling to {max_words:,}")
            
            # Intelligent sampling
            sampled = set()
            
            # Keep all short passwords (more likely)
            short = [w for w in wordlist_list if len(w) <= 8]
            sampled.update(short[:100000])
            
            # Keep all with special chars
            special = [w for w in wordlist_list if any(c in '!@#$%^&*' for c in w)]
            sampled.update(special[:200000])
            
            # Keep all leet passwords
            leet = [w for w in wordlist_list if any(c.isdigit() for c in w) and any(c.isalpha() for c in w)]
            sampled.update(leet[:300000])
            
            # Random sample the rest
            remaining = [w for w in wordlist_list if w not in sampled]
            if len(remaining) > max_words - len(sampled):
                import random
                sampled.update(random.sample(remaining, max_words - len(sampled)))
            
            wordlist_list = list(sampled)
        
        # Sort
        wordlist_list.sort()
        
        # Save
        print(f"[*] Saving {len(wordlist_list):,} words to {filename}...")
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                for i, word in enumerate(wordlist_list):
                    f.write(word + '\n')
                    if i % 1000000 == 0 and i > 0:
                        print(f"  -> Saved {i:,} words...")
            
            file_size = os.path.getsize(filename)
            print(f"[+] Successfully saved {len(wordlist_list):,} words")
            print(f"[+] File size: {file_size:,} bytes ({file_size/1024/1024:.2f} MB)")
            
            # Show statistics
            self.show_statistics(wordlist_list)
            
            return True
            
        except Exception as e:
            print(f"[-] Error: {e}")
            return False
    
    def show_statistics(self, wordlist):
        """Show statistics about generated wordlist"""
        if not wordlist:
            return
        
        print(f"\n{'='*70}")
        print(" WORDLIST STATISTICS")
        print(f"{'='*70}")
        
        # Length distribution
        length_count = {}
        for word in wordlist[:10000]:  # Sample
            length = len(word)
            length_count[length] = length_count.get(length, 0) + 1
        
        print("\nLength distribution (sample):")
        for length in sorted(length_count.keys()):
            count = length_count[length]
            bar = '█' * int(count / max(length_count.values()) * 30)
            print(f"  {length:2} chars: {bar} ({count})")
        
        # Character type analysis
        has_special = sum(1 for w in wordlist[:10000] if any(c in '!@#$%^&*' for c in w))
        has_digits = sum(1 for w in wordlist[:10000] if any(c.isdigit() for c in w))
        has_upper = sum(1 for w in wordlist[:10000] if any(c.isupper() for c in w))
        has_lower = sum(1 for w in wordlist[:10000] if any(c.islower() for c in w))
        
        print(f"\nCharacter types in sample:")
        print(f"  Contains special chars: {has_special/100:.1f}%")
        print(f"  Contains digits: {has_digits/100:.1f}%")
        print(f"  Contains uppercase: {has_upper/100:.1f}%")
        print(f"  Contains lowercase: {has_lower/100:.1f}%")
        
        # Show strongest passwords
        strong = [w for w in wordlist if len(w) >= 12 and 
                 any(c.isdigit() for c in w) and 
                 any(c in '!@#$%^&*' for c in w) and
                 any(c.isupper() for c in w) and
                 any(c.islower() for c in w)]
        
        if strong:
            print(f"\nExamples of strong passwords generated ({len(strong)} total):")
            for i, pwd in enumerate(strong[:5]):
                print(f"  {i+1}. {pwd}")

def main():
    parser = argparse.ArgumentParser(
        description='MEGA WORDLIST GENERATOR v3.0 - All features combined',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive mode with all options (like first code)
  python mega_generator.py --interactive --mode aggressive
  
  # Minimal input for maximum combinations
  python mega_generator.py --minimal --mode ultimate
  
  # Command line with specific info
  python mega_generator.py --first john --last doe --birthdate 15/06/1990 --mode extreme
  
  # Quick generation with just name
  python mega_generator.py --first john --quick
  
  # Generate from config file
  python mega_generator.py --config profile.json
        """
    )
    
    # Input methods
    input_group = parser.add_mutually_exclusive_group()
    input_group.add_argument('-i', '--interactive', action='store_true',
                           help='Interactive mode (full CUPP-like input)')
    input_group.add_argument('-m', '--minimal', action='store_true',
                           help='Minimal input mode (max combinations)')
    input_group.add_argument('-q', '--quick', action='store_true',
                           help='Quick mode (just name and year)')
    input_group.add_argument('--config', help='Load from config file')
    
    # Personal info (for command line)
    parser.add_argument('-f', '--first', help='First name')
    parser.add_argument('-l', '--last', help='Last name')
    parser.add_argument('-b', '--birthdate', help='Birthdate (DD/MM/YYYY)')
    parser.add_argument('-y', '--year', help='Birth year (YYYY)')
    parser.add_argument('-k', '--keywords', help='Comma-separated keywords')
    
    # Generation options
    parser.add_argument('--mode', choices=['normal', 'aggressive', 'extreme', 'ultimate'],
                       default='aggressive', help='Generation intensity')
    parser.add_argument('--leet', action='store_true', default=True,
                       help='Enable leet speak (default: true)')
    parser.add_argument('--numbers', action='store_true', default=True,
                       help='Add number patterns (default: true)')
    parser.add_argument('--special', action='store_true', default=True,
                       help='Add special characters (default: true)')
    
    # Control options
    parser.add_argument('--min-length', type=int, default=4,
                       help='Minimum password length (default: 4)')
    parser.add_argument('--max-length', type=int, default=32,
                       help='Maximum password length (default: 32)')
    parser.add_argument('--limit', type=int, default=10000000,
                       help='Maximum words to save (default: 10,000,000)')
    
    # Output options
    parser.add_argument('-o', '--output', default='mega_wordlist.txt',
                       help='Output filename')
    parser.add_argument('--show-sample', type=int, default=20,
                       help='Number of sample passwords to show')
    parser.add_argument('--stats', action='store_true',
                       help='Show detailed statistics')
    
    args = parser.parse_args()
    
    # Initialize generator
    generator = MegaWordlistGenerator()
    
    # Collect data based on input method
    data = {}
    
    if args.interactive:
        print("\n[+] Starting interactive mode...")
        data = generator.get_interactive_input()
        
    elif args.minimal:
        print("\n[+] Starting minimal input mode...")
        data = generator.get_minimal_input()
        
    elif args.quick:
        print("\n[+] Starting quick mode...")
        data['first_name'] = args.first or input("First name: ").strip().lower()
        if not data['first_name']:
            print("[!] First name required!")
            sys.exit(1)
        
        if args.last:
            data['last_name'] = args.last.lower()
        else:
            data['last_name'] = input("Last name (optional): ").strip().lower()
        
        year = args.year or input("Birth year (YYYY, optional): ").strip()
        if year:
            data['birthdate'] = f"01/01/{year}"
        
        data['auto_common'] = True
        data['add_months'] = True
        data['add_keyboard'] = True
        
    elif args.config:
        print(f"\n[+] Loading from config: {args.config}")
        try:
            with open(args.config, 'r') as f:
                data = json.load(f)
        except Exception as e:
            print(f"[!] Error loading config: {e}")
            sys.exit(1)
            
    else:
        # Command line mode
        if not args.first:
            print("[!] At least --first name is required for command line mode")
            sys.exit(1)
        
        data['first_name'] = args.first.lower()
        if args.last:
            data['last_name'] = args.last.lower()
        if args.birthdate:
            data['birthdate'] = args.birthdate
        elif args.year:
            data['birthdate'] = f"01/01/{args.year}"
        if args.keywords:
            data['keywords'] = [k.strip().lower() for k in args.keywords.split(',')]
        
        # Enable all features by default
        data['auto_common'] = True
        data['add_months'] = True
        data['add_keyboard'] = True
    
    # Add generation options to data
    data['leet_enabled'] = args.leet
    data['numbers_enabled'] = args.numbers
    data['special_enabled'] = args.special
    data['min_length'] = args.min_length
    data['max_length'] = args.max_length
    
    # Show input summary
    print(f"\n{'='*70}")
    print(" INPUT SUMMARY")
    print(f"{'='*70}")
    
    important_fields = ['first_name', 'last_name', 'nickname', 'birthdate', 
                       'keywords', 'city', 'country', 'team']
    
    for field in important_fields:
        if field in data and data[field]:
            if field == 'keywords':
                print(f"  {field}: {', '.join(data[field])}")
            else:
                print(f"  {field}: {data[field]}")
    
    print(f"  Generation mode: {args.mode}")
    print(f"  Expected combinations: Millions to tens of millions")
    print(f"{'='*70}\n")
    
    # Generate wordlist
    wordlist = generator.mega_generate(data, mode=args.mode)
    
    # Show final statistics
    print(f"\n{'='*70}")
    print(" GENERATION COMPLETE!")
    print(f"{'='*70}")
    print(f" Total unique passwords generated: {len(wordlist):,}")
    
    if wordlist:
        # Show sample
        print(f"\n[*] Sample of generated passwords:")
        sample_size = min(args.show_sample, len(wordlist))
        step = max(1, len(wordlist) // sample_size)
        
        for i in range(sample_size):
            idx = i * step
            if idx < len(wordlist):
                print(f"  {i+1:2}. {list(wordlist)[idx]}")
    
    # Save to file
    print(f"\n[*] Saving to: {args.output}")
    generator.save_wordlist(wordlist, args.output, max_words=args.limit)

if __name__ == '__main__':
    main()