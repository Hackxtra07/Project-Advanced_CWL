#!/usr/bin/env python3
"""
ENHANCED CUSTOM WORDLIST GENERATOR - Advanced Algorithms
User-Defined with Intelligent Pattern Generation
"""

import argparse
import sys
from datetime import datetime, timedelta
import os
import re
import itertools
import math
from typing import Set, Dict, List, Tuple, Optional
from collections import defaultdict, deque
import random

class EnhancedWordlistGenerator:
    def __init__(self):
        # Extended leet mappings
        self.leet_maps = {
            'a': ['4', '@', '/\\', '^', 'λ'],
            'b': ['8', '|3', 'ß', '13', '|o'],
            'c': ['[', '<', '(', '{'],
            'd': ['|)', '|]', '|>'],
            'e': ['3', '€', 'є', '£'],
            'f': ['|=', 'ph', 'ƒ'],
            'g': ['6', '9', '&', '(_+'],
            'h': ['#', '|-|', ']-[', '}{'],
            'i': ['1', '!', '|', 'ι'],
            'j': [']', '_|', '_/'],
            'k': ['|<', '|{', 'ɮ'],
            'l': ['|_', '£', '1', 'ℓ'],
            'm': ['|v|', '/\\/\\', '^^', '[V]'],
            'n': ['|\\|', '/\\/', 'И', 'ท'],
            'o': ['0', '()', '[]', '°'],
            'p': ['|*', '|>', '9', '|7'],
            'q': ['0_', '9', '(,)'],
            'r': ['|2', '|?', '/2', 'Я'],
            's': ['5', '$', 'z', '§'],
            't': ['7', '+', '†', '‡'],
            'u': ['|_|', 'µ', 'บ'],
            'v': ['\\/', '|/', 'ڤ'],
            'w': ['\\/\\/', 'vv', '\\X/', 'พ'],
            'x': ['><', '}{', '×', 'Ж'],
            'y': ['`/', '¥', 'φ'],
            'z': ['2', '~/_', '%']
        }
        
        # Common keyboard patterns
        self.keyboard_patterns = {
            'qwerty': ['qwerty', 'asdfgh', 'zxcvbn', 'qazwsx', '123456'],
            'keypad': ['789', '456', '123', '147', '258', '369'],
            'adjacent': ['qwe', 'asd', 'zxc', 'rty', 'fgh', 'vbn']
        }
        
        # Common substitutions
        self.common_subs = {
            'and': '&',
            'to': '2',
            'for': '4',
            'you': 'u',
            'are': 'r',
            'ate': '8',
            'see': 'c',
            'why': 'y',
            'one': '1'
        }
        
        # Phonetic substitutions
        self.phonetic_subs = {
            'ph': 'f',
            'gh': 'g',
            'ck': 'k',
            'qu': 'kw',
            'x': 'cks',
            'tion': 'shun'
        }
        
        # Year ranges for generation
        self.year_ranges = {
            'birth_years': list(range(1950, 2025)),
            'recent_years': list(range(2000, 2025)),
            'all_years': list(range(1900, 2025))
        }
        
        # Common separators
        self.common_separators = ['', '.', '_', '-', '@', '#', '$', '&', '*']
        
        # Special character sets
        self.special_char_sets = {
            'basic': ['!', '@', '#', '$', '%', '^', '&', '*'],
            'extended': ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '_', '=', '+'],
            'all': ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '_', '=', '+', 
                   '[', ']', '{', '}', '|', '\\', ';', ':', "'", '"', ',', '.', '<', '>', '/', '?', '~', '`']
        }
        
    def get_user_input(self) -> Dict:
        """Get ALL information from user with advanced options"""
        print("\n" + "="*70)
        print(" ENHANCED CUSTOM WORDLIST GENERATOR")
        print("="*70)
        print("\n[!] Advanced pattern generation available\n")
        
        data = {}
        
        # === PERSONAL INFORMATION ===
        print("--- PERSONAL INFORMATION (optional) ---")
        personal_info = {}
        
        personal_info['first_name'] = input("First name: ").strip().lower() or None
        personal_info['middle_name'] = input("Middle name: ").strip().lower() or None
        personal_info['last_name'] = input("Last name: ").strip().lower() or None
        personal_info['nickname'] = input("Nickname(s), comma-separated: ").strip().lower() or None
        personal_info['maiden_name'] = input("Mother's maiden name: ").strip().lower() or None
        personal_info['spouse_name'] = input("Spouse/Partner name: ").strip().lower() or None
        personal_info['child_name'] = input("Child(ren) names, comma-separated: ").strip().lower() or None
        personal_info['pet_name'] = input("Pet name(s): ").strip().lower() or None
        personal_info['company'] = input("Company/School name: ").strip().lower() or None
        personal_info['city'] = input("City/Town: ").strip().lower() or None
        personal_info['country'] = input("Country: ").strip().lower() or None
        
        # Filter out None values
        personal_info = {k: v for k, v in personal_info.items() if v}
        
        # Process comma-separated values
        for key in ['nickname', 'child_name']:
            if key in personal_info:
                personal_info[key] = [name.strip() for name in personal_info[key].split(',')]
        
        data['personal_info'] = personal_info
        
        # === IMPORTANT DATES ===
        print("\n--- IMPORTANT DATES (optional) ---")
        dates = {}
        
        date_fields = [
            ('birthdate', "Your birthdate (DD/MM/YYYY): "),
            ('spouse_birthdate', "Spouse/Partner birthdate: "),
            ('child_birthdate', "Child birthdate(s), comma-separated: "),
            ('anniversary', "Anniversary date: "),
            ('other_dates', "Other important dates, comma-separated: ")
        ]
        
        for field, prompt in date_fields:
            value = input(prompt).strip()
            if value:
                dates[field] = value
        
        data['dates'] = dates
        
        # === KEYWORDS AND PHRASES ===
        print("\n--- KEYWORDS AND PHRASES ---")
        keywords = input("Important keywords/phrases (comma-separated): ").strip().lower()
        data['keywords'] = [k.strip() for k in keywords.split(',') if k.strip()]
        
        # === NUMERICAL INFORMATION ===
        print("\n--- NUMERICAL INFORMATION (optional) ---")
        numbers = {}
        
        number_fields = [
            ('phone', "Phone number(s), comma-separated: "),
            ('zipcode', "Zip/Postal code(s): "),
            ('street_number', "Street number: "),
            ('license_plate', "License plate: "),
            ('id_numbers', "ID/Passport numbers, comma-separated: ")
        ]
        
        for field, prompt in number_fields:
            value = input(prompt).strip()
            if value:
                numbers[field] = value
        
        data['numbers'] = numbers
        
        # === ADVANCED PATTERNS ===
        print("\n--- ADVANCED PATTERN GENERATION ---")
        
        # Leet speak options
        print("\n[Leet Speak Options]")
        leet_choice = input("Enable leet speak? (y/n): ").strip().lower()
        data['leet_enabled'] = leet_choice == 'y'
        
        if data['leet_enabled']:
            print("  Levels: 1=Basic, 2=Moderate, 3=Advanced, 4=Extreme")
            leet_level = input("  Leet level (1-4): ").strip()
            data['leet_level'] = min(max(int(leet_level) if leet_level.isdigit() else 2, 1), 4)
            
            leet_custom = input("  Custom leet mappings (format a=4,@ b=8, leave blank for default): ").strip()
            if leet_custom:
                data['custom_leet'] = self.parse_custom_leet(leet_custom)
        
        # Number generation options
        print("\n[Number Pattern Options]")
        num_choice = input("Add number patterns? (y/n): ").strip().lower()
        data['numbers_enabled'] = num_choice == 'y'
        
        if data['numbers_enabled']:
            print("  Number generation types:")
            print("  1. Simple ranges (e.g., 0-99)")
            print("  2. Common patterns (123, 456, 789)")
            print("  3. Birth year ranges")
            print("  4. Keyboard patterns")
            print("  5. Sequential/repeating")
            num_types = input("  Select types (comma-separated, 1-5): ").strip()
            data['number_types'] = [t.strip() for t in num_types.split(',')]
            
            if '1' in data['number_types']:
                ranges = input("  Number ranges (e.g., 0-99,100-199): ").strip()
                if ranges:
                    data['number_ranges'] = self.parse_number_ranges(ranges)
        
        # Special character options
        print("\n[Special Character Options]")
        special_choice = input("Add special characters? (y/n): ").strip().lower()
        data['special_enabled'] = special_choice == 'y'
        
        if data['special_enabled']:
            print("  Special character sets:")
            print("  1. Basic (!@#$%^&*)")
            print("  2. Extended (includes ()-_=+)")
            print("  3. All (full keyboard)")
            print("  4. Custom set")
            special_set = input("  Select set (1-4): ").strip()
            
            if special_set == '4':
                custom_chars = input("  Custom characters: ").strip()
                data['special_chars'] = list(custom_chars)
            else:
                set_map = {'1': 'basic', '2': 'extended', '3': 'all'}
                data['special_chars'] = self.special_char_sets[set_map.get(special_set, 'basic')]
        
        # Combination strategies
        print("\n[Combination Strategies]")
        print("  Combination types:")
        print("  1. Simple concatenation")
        print("  2. With separators")
        print("  3. Prefix/Suffix variations")
        print("  4. CamelCase/PascalCase")
        print("  5. Word mangling")
        print("  6. Phonetic substitutions")
        
        combo_types = input("  Select combination types (comma-separated, 1-6): ").strip()
        data['combo_types'] = [t.strip() for t in combo_types.split(',')]
        
        if '2' in data['combo_types']:
            separators = input("  Separators to use (or 'default'): ").strip()
            if separators.lower() == 'default':
                data['separators'] = self.common_separators
            else:
                data['separators'] = list(separators) if separators else ['']
        
        # Pattern depth
        depth = input("\nPattern generation depth (1-5, higher=more combinations): ").strip()
        data['depth'] = min(max(int(depth) if depth.isdigit() else 3, 1), 5)
        
        # Length constraints
        print("\n--- LENGTH AND SIZE CONSTRAINTS ---")
        min_len = input("Minimum password length (default: 6): ").strip()
        data['min_length'] = int(min_len) if min_len.isdigit() else 6
        
        max_len = input("Maximum password length (default: 64): ").strip()
        data['max_length'] = int(max_len) if max_len.isdigit() else 64
        
        # Output size limit
        limit = input("Maximum wordlist size (0 for unlimited, default: 1000000): ").strip()
        data['max_size'] = int(limit) if limit.isdigit() else 1000000
        
        return data
    
    def parse_custom_leet(self, leet_str: str) -> Dict:
        """Parse custom leet mappings from user input"""
        custom_leet = {}
        mappings = leet_str.split()
        for mapping in mappings:
            if '=' in mapping:
                char, replacements = mapping.split('=', 1)
                custom_leet[char.lower()] = [r.strip() for r in replacements.split(',')]
        return custom_leet
    
    def parse_number_ranges(self, ranges_str: str) -> List[Tuple[int, int]]:
        """Parse number ranges from user input"""
        ranges = []
        for range_str in ranges_str.split(','):
            if '-' in range_str:
                try:
                    start, end = map(int, range_str.split('-'))
                    ranges.append((start, end))
                except ValueError:
                    continue
        return ranges
    
    def extract_date_components(self, date_str: str) -> Dict[str, List[str]]:
        """Extract all possible date components with variations"""
        components = defaultdict(list)
        
        if not date_str:
            return components
        
        # Clean the date string
        date_str = date_str.strip()
        
        # Try multiple date formats
        date_formats = [
            '%d/%m/%Y', '%m/%d/%Y', '%Y/%m/%d',
            '%d-%m-%Y', '%m-%d-%Y', '%Y-%m-%d',
            '%d.%m.%Y', '%m.%d.%Y', '%Y.%m.%d',
            '%d%m%Y', '%m%d%Y', '%Y%m%d',
            '%d/%m/%y', '%m/%d/%y', '%y/%m/%d',
            '%d%m%y', '%m%d%y', '%y%m%d'
        ]
        
        parsed_date = None
        for fmt in date_formats:
            try:
                parsed_date = datetime.strptime(date_str, fmt)
                break
            except ValueError:
                continue
        
        if not parsed_date:
            # Try to extract components with regex
            day_match = re.search(r'\b(0[1-9]|[12][0-9]|3[01])\b', date_str)
            month_match = re.search(r'\b(0[1-9]|1[0-2])\b', date_str)
            year_match = re.search(r'\b(19\d{2}|20\d{2})\b', date_str)
            
            if day_match:
                components['day'].append(day_match.group())
            if month_match:
                components['month'].append(month_match.group())
            if year_match:
                year = year_match.group()
                components['year'].append(year)
                components['year_short'].append(year[2:])
            
            return dict(components)
        
        # Extract all date components
        day = parsed_date.strftime('%d')
        month = parsed_date.strftime('%m')
        year = parsed_date.strftime('%Y')
        year_short = parsed_date.strftime('%y')
        
        # Basic components
        components['day'].extend([day, day.lstrip('0')])
        components['month'].extend([month, month.lstrip('0')])
        components['year'].extend([year])
        components['year_short'].extend([year_short])
        
        # Common date patterns
        patterns = [
            ('ddmmyyyy', f"{day}{month}{year}"),
            ('mmddyyyy', f"{month}{day}{year}"),
            ('yyyymmdd', f"{year}{month}{day}"),
            ('ddmmyy', f"{day}{month}{year_short}"),
            ('mmddyy', f"{month}{day}{year_short}"),
            ('yymmdd', f"{year_short}{month}{day}"),
            ('dmy', f"{day.lstrip('0')}{month.lstrip('0')}{year_short}"),
            ('mdy', f"{month.lstrip('0')}{day.lstrip('0')}{year_short}")
        ]
        
        for pattern_name, pattern_value in patterns:
            components['patterns'].append(pattern_value)
        
        # Add month names if applicable
        month_names = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 
                      'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
        month_num = int(month)
        if 1 <= month_num <= 12:
            month_name = month_names[month_num - 1]
            components['month_name'].extend([month_name, month_name.title()])
        
        return dict(components)
    
    def generate_keyboard_patterns(self, length: int = 3) -> List[str]:
        """Generate keyboard walk patterns"""
        patterns = []
        
        # Common keyboard layouts
        qwerty_rows = [
            ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p'],
            ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l'],
            ['z', 'x', 'c', 'v', 'b', 'n', 'm']
        ]
        
        keypad = [
            ['7', '8', '9'],
            ['4', '5', '6'],
            ['1', '2', '3'],
            ['0', '.']
        ]
        
        # Generate horizontal walks
        for row in qwerty_rows:
            for i in range(len(row) - length + 1):
                patterns.append(''.join(row[i:i+length]))
        
        # Generate diagonal walks (simplified)
        diagonals = ['qaz', 'wsx', 'edc', 'rfv', 'tgb', 'yhn', 'ujm', 'ik,', 'ol.', 'p;/']
        patterns.extend(diagonals)
        
        # Generate keypad patterns
        for row in keypad:
            for i in range(len(row) - length + 1):
                patterns.append(''.join(row[i:i+length]))
        
        # Add number sequences
        for i in range(10 - length + 1):
            patterns.append(''.join(str(j) for j in range(i, i+length)))
        
        return list(set(patterns))
    
    def generate_common_patterns(self) -> List[str]:
        """Generate common password patterns"""
        patterns = []
        
        # Repeating patterns
        for char in ['a', '1', '0', '!', '@']:
            for length in [2, 3, 4]:
                patterns.append(char * length)
        
        # Common sequences
        sequences = ['123', '321', '456', '654', '789', '987',
                    'abc', 'cba', 'qwe', 'ewq', 'asd', 'dsa']
        patterns.extend(sequences)
        
        # Pattern templates
        templates = [
            'pass{word}', 'admin{year}', 'welcome{num}',
            'letmein', 'password{year}', 'iloveyou{num}'
        ]
        
        return patterns
    
    def apply_leet_level(self, word: str, level: int, custom_map: Dict = None) -> List[str]:
        """Apply leet speak transformations based on level"""
        variations = [word]
        
        leet_map = custom_map or self.leet_maps
        
        if level == 1:
            # Basic: only common substitutions
            basic_leet = {'a': '4', 'e': '3', 'i': '1', 'o': '0', 's': '5'}
            for char, sub in basic_leet.items():
                if char in word:
                    variations.append(word.replace(char, sub))
        
        elif level == 2:
            # Moderate: more substitutions
            for char, subs in leet_map.items():
                if char in word:
                    for sub in subs[:2]:  # First two substitutions
                        variations.append(word.replace(char, sub))
        
        elif level == 3:
            # Advanced: multiple substitutions per word
            chars_to_replace = [c for c in word if c in leet_map]
            
            if len(chars_to_replace) <= 3:
                # Try all combinations for few replaceable chars
                for combo in itertools.product(*[leet_map.get(c, [c]) for c in word]):
                    variations.append(''.join(combo))
        
        elif level == 4:
            # Extreme: all possible combinations
            char_options = []
            for char in word:
                if char in leet_map:
                    options = [char] + leet_map[char]
                    char_options.append(options)
                else:
                    char_options.append([char])
            
            # Limit to reasonable combinations (avoid explosion)
            max_combinations = 1000
            combo_count = math.prod(len(opts) for opts in char_options)
            
            if combo_count <= max_combinations:
                for combo in itertools.product(*char_options):
                    variations.append(''.join(combo))
            else:
                # Sample random combinations
                for _ in range(max_combinations):
                    new_word = []
                    for opts in char_options:
                        new_word.append(random.choice(opts))
                    variations.append(''.join(new_word))
        
        return list(set(variations))
    
    def apply_case_variations(self, word: str) -> List[str]:
        """Generate case variations of a word"""
        variations = set()
        
        # Basic variations
        variations.add(word.lower())
        variations.add(word.upper())
        variations.add(word.title())
        variations.add(word.capitalize())
        
        # Random case (toggle style)
        if len(word) <= 8:
            # Generate all binary case variations for short words
            for mask in range(2 ** len(word)):
                chars = []
                for i, char in enumerate(word):
                    if (mask >> i) & 1:
                        chars.append(char.upper())
                    else:
                        chars.append(char.lower())
                variations.add(''.join(chars))
        else:
            # For longer words, use common patterns
            patterns = [
                word[0].upper() + word[1:].lower(),  # First letter capital
                word.lower(),
                word.upper(),
                word.title(),
                word[0].lower() + word[1:].upper(),  # camelCase style
            ]
            variations.update(patterns)
        
        return list(variations)
    
    def apply_phonetic_substitutions(self, word: str) -> List[str]:
        """Apply phonetic substitutions"""
        variations = [word]
        
        for phonetic, sub in self.phonetic_subs.items():
            if phonetic in word:
                variations.append(word.replace(phonetic, sub))
        
        # Reverse substitutions
        for sub, phonetic in self.phonetic_subs.items():
            if sub in word:
                variations.append(word.replace(sub, phonetic))
        
        return list(set(variations))
    
    def apply_word_mangling(self, word: str) -> List[str]:
        """Mangle words by adding/removing characters"""
        variations = set()
        
        variations.add(word)
        
        # Double letters
        for i in range(len(word)):
            mangled = word[:i] + word[i] + word[i:]
            variations.add(mangled)
        
        # Remove vowels
        no_vowels = re.sub(r'[aeiou]', '', word, flags=re.IGNORECASE)
        if no_vowels:
            variations.add(no_vowels)
        
        # Remove duplicates
        deduped = ''
        for char in word:
            if not deduped or char != deduped[-1]:
                deduped += char
        if deduped != word:
            variations.add(deduped)
        
        # Reverse word
        variations.add(word[::-1])
        
        # Add common prefixes/suffixes
        prefixes = ['super', 'mega', 'ultra', 'hyper', 'neo']
        suffixes = ['123', '!', '2024', 'admin', 'user']
        
        for prefix in prefixes:
            variations.add(prefix + word)
        
        for suffix in suffixes:
            variations.add(word + suffix)
        
        return list(variations)
    
    def generate_combinations(self, words: List[str], strategy: str, 
                            separators: List[str] = None) -> List[str]:
        """Generate combinations based on strategy"""
        combinations = set()
        
        if not words:
            return []
        
        if strategy == 'simple':
            # All pairwise combinations
            for i in range(len(words)):
                for j in range(len(words)):
                    if i != j:
                        combinations.add(words[i] + words[j])
        
        elif strategy == 'separators':
            # Combinations with separators
            separators = separators or ['']
            for word1 in words:
                for word2 in words:
                    for sep in separators:
                        combinations.add(word1 + sep + word2)
        
        elif strategy == 'camelcase':
            # CamelCase and PascalCase combinations
            for word1 in words:
                for word2 in words:
                    combinations.add(word1.title() + word2.title())
                    combinations.add(word1.lower() + word2.title())
        
        elif strategy == 'three_word':
            # Three word combinations
            if len(words) >= 3:
                for combo in itertools.permutations(words, 3):
                    combinations.add(''.join(combo))
                    for sep in (separators or ['']):
                        combinations.add(sep.join(combo))
        
        return list(combinations)
    
    def generate_number_patterns(self, types: List[str], ranges: List[Tuple[int, int]] = None) -> List[str]:
        """Generate number patterns based on types"""
        patterns = set()
        
        if '1' in types and ranges:
            # Simple ranges
            for start, end in ranges:
                for num in range(start, end + 1):
                    patterns.add(str(num))
                    if len(str(num)) == 1:
                        patterns.add(f"0{num}")  # Zero-padded
        
        if '2' in types:
            # Common patterns
            common_patterns = ['123', '456', '789', '321', '654', '987',
                             '111', '222', '333', '444', '555', '666',
                             '777', '888', '999', '000', '007', '1234',
                             '4321', '1111', '2222', '3333', '4444']
            patterns.update(common_patterns)
        
        if '3' in types:
            # Year patterns
            for year in self.year_ranges['recent_years']:
                patterns.add(str(year))
                patterns.add(str(year)[2:])  # Short year
        
        if '4' in types:
            # Keyboard patterns
            keyboard_pats = self.generate_keyboard_patterns(3)
            patterns.update(keyboard_pats)
        
        if '5' in types:
            # Sequential and repeating
            for length in [2, 3, 4]:
                for start in range(10 - length):
                    seq = ''.join(str(i) for i in range(start, start + length))
                    patterns.add(seq)
                
                for digit in range(10):
                    patterns.add(str(digit) * length)
        
        return list(patterns)
    
    def smart_combine(self, base_words: List[str], numbers: List[str], 
                     special_chars: List[str], depth: int) -> Set[str]:
        """Intelligently combine elements based on depth"""
        all_passwords = set()
        
        # Base words
        all_passwords.update(base_words)
        
        if depth >= 2:
            # Add number suffixes/prefixes
            for word in base_words:
                for num in numbers[:min(100, len(numbers))]:  # Limit to 100 numbers
                    all_passwords.add(word + num)
                    all_passwords.add(num + word)
                    
                    # Add special characters
                    for special in special_chars[:min(10, len(special_chars))]:
                        all_passwords.add(special + word + num)
                        all_passwords.add(word + num + special)
                        all_passwords.add(special + word + special + num)
        
        if depth >= 3:
            # Word combinations
            word_combinations = self.generate_combinations(base_words[:10], 'simple')
            all_passwords.update(word_combinations)
            
            # Add numbers to combinations
            for combo in word_combinations[:min(100, len(word_combinations))]:
                for num in numbers[:min(20, len(numbers))]:
                    all_passwords.add(combo + num)
        
        if depth >= 4:
            # Advanced patterns with separators
            separators = self.common_separators
            for word1 in base_words[:5]:
                for word2 in base_words[:5]:
                    for sep in separators:
                        combo = word1 + sep + word2
                        all_passwords.add(combo)
                        
                        # Add numbers and specials
                        for num in numbers[:min(10, len(numbers))]:
                            all_passwords.add(combo + num)
                            for special in special_chars[:3]:
                                all_passwords.add(special + combo + num + special)
        
        if depth >= 5:
            # Extreme combinations (limited to avoid explosion)
            extreme_combos = set()
            sample_words = base_words[:3]
            sample_nums = numbers[:5]
            sample_specials = special_chars[:3]
            
            # Generate template-based passwords
            templates = [
                '{word}{num}{special}',
                '{special}{word}{num}',
                '{word}{special}{num}{special}',
                '{num}{word}{num}'
            ]
            
            for template in templates:
                for word in sample_words:
                    for num in sample_nums:
                        for special in sample_specials:
                            extreme_combos.add(template.format(
                                word=word, num=num, special=special
                            ))
            
            all_passwords.update(extreme_combos)
        
        return all_passwords
    
    def generate(self, data: Dict) -> Set[str]:
        """Main generation function with advanced algorithms"""
        print("\n[*] Starting advanced generation...")
        
        all_passwords = set()
        
        # === EXTRACT BASE WORDS ===
        base_words = set()
        
        # Personal information
        if 'personal_info' in data:
            for info in data['personal_info'].values():
                if isinstance(info, list):
                    base_words.update(info)
                else:
                    base_words.add(info)
        
        # Date components
        if 'dates' in data:
            for date_str in data['dates'].values():
                if ',' in date_str:  # Multiple dates
                    for single_date in date_str.split(','):
                        components = self.extract_date_components(single_date.strip())
                        for comp_list in components.values():
                            base_words.update(comp_list)
                else:
                    components = self.extract_date_components(date_str)
                    for comp_list in components.values():
                        base_words.update(comp_list)
        
        # Keywords
        if 'keywords' in data:
            base_words.update(data['keywords'])
        
        # Numbers
        number_patterns = set()
        if 'numbers' in data:
            for num_str in data['numbers'].values():
                if num_str:
                    # Extract pure digits
                    digits = re.sub(r'\D', '', num_str)
                    if digits:
                        base_words.add(digits)
                        if len(digits) >= 4:
                            base_words.add(digits[-4:])  # Last 4 digits
        
        print(f"[+] Base words extracted: {len(base_words)}")
        
        # === APPLY TRANSFORMATIONS ===
        transformed_words = set()
        
        for word in base_words:
            transformed_words.add(word)
            
            # Case variations
            if len(word) <= 10:  # Limit for performance
                transformed_words.update(self.apply_case_variations(word))
            
            # Leet speak
            if data.get('leet_enabled', False):
                leet_level = data.get('leet_level', 2)
                custom_map = data.get('custom_leet')
                transformed_words.update(
                    self.apply_leet_level(word, leet_level, custom_map)
                )
            
            # Phonetic substitutions
            transformed_words.update(self.apply_phonetic_substitutions(word))
            
            # Word mangling (for depth >= 3)
            if data.get('depth', 3) >= 3:
                transformed_words.update(self.apply_word_mangling(word))
        
        print(f"[+] After transformations: {len(transformed_words)} words")
        
        # === GENERATE NUMBER PATTERNS ===
        number_patterns = set()
        if data.get('numbers_enabled', False):
            number_types = data.get('number_types', ['1', '2'])
            ranges = data.get('number_ranges', [(0, 99)])
            number_patterns.update(self.generate_number_patterns(number_types, ranges))
            print(f"[+] Number patterns generated: {len(number_patterns)}")
        
        # === GENERATE SPECIAL CHARACTER PATTERNS ===
        special_chars = []
        if data.get('special_enabled', False):
            special_chars = data.get('special_chars', self.special_char_sets['basic'])
        
        # === INTELLIGENT COMBINATION ===
        depth = data.get('depth', 3)
        base_word_list = list(transformed_words)
        number_list = list(number_patterns)
        
        print(f"[*] Generating combinations (depth: {depth})...")
        
        combined = self.smart_combine(
            base_word_list, 
            number_list, 
            special_chars, 
            depth
        )
        
        all_passwords.update(combined)
        print(f"[+] After combination: {len(all_passwords)} passwords")
        
        # === ADD COMMON PATTERNS ===
        if depth >= 2:
            common_patterns = self.generate_common_patterns()
            keyboard_patterns = self.generate_keyboard_patterns()
            
            all_passwords.update(common_patterns)
            all_passwords.update(keyboard_patterns)
            
            print(f"[+] Added {len(common_patterns)} common patterns")
            print(f"[+] Added {len(keyboard_patterns)} keyboard patterns")
        
        # === FILTER AND LIMIT ===
        min_len = data.get('min_length', 6)
        max_len = data.get('max_length', 64)
        max_size = data.get('max_size', 1000000)
        
        filtered = {p for p in all_passwords if min_len <= len(p) <= max_len}
        
        print(f"[*] Filtering by length ({min_len}-{max_len}): "
              f"{len(all_passwords)} -> {len(filtered)}")
        
        # Limit output size if specified
        if 0 < max_size < len(filtered):
            filtered = set(list(filtered)[:max_size])
            print(f"[*] Limited to {max_size} passwords")
        
        return filtered
    
    def save_wordlist(self, wordlist: Set[str], filename: str):
        """Save wordlist to file with metadata"""
        wordlist_list = sorted(list(wordlist))
        
        print(f"\n[*] Saving {len(wordlist_list):,} passwords to {filename}...")
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                # Add metadata header
                f.write(f"# Wordlist generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"# Total passwords: {len(wordlist_list):,}\n")
                f.write("#" * 80 + "\n\n")
                
                # Write passwords
                for word in wordlist_list:
                    f.write(word + '\n')
            
            file_size = os.path.getsize(filename)
            print(f"[+] Successfully saved {len(wordlist_list):,} passwords")
            print(f"[+] File size: {file_size:,} bytes ({file_size/1024/1024:.2f} MB)")
            
            return True
            
        except Exception as e:
            print(f"[-] Error saving file: {e}")
            return False

def main():
    parser = argparse.ArgumentParser(
        description='ENHANCED CUSTOM WORDLIST GENERATOR - Advanced Algorithms',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive mode with all options
  python enhanced_generator.py
  
  # Quick generation with common patterns
  python enhanced_generator.py --quick --depth 4 --output mylist.txt
  
  # Targeted generation
  python enhanced_generator.py --first john --last doe --birthdate 15/06/1990 
                               --keywords "hacker,cyber,security" --leet 3
        """
    )
    
    # Quick mode
    parser.add_argument('--quick', action='store_true', 
                       help='Quick mode with sensible defaults')
    
    # Basic info
    parser.add_argument('--first', help='First name')
    parser.add_argument('--last', help='Last name')
    parser.add_argument('--birthdate', help='Birthdate (DD/MM/YYYY)')
    parser.add_argument('--keywords', help='Comma-separated keywords')
    
    # Advanced options
    parser.add_argument('--depth', type=int, choices=range(1, 6), default=3,
                       help='Generation depth (1-5)')
    parser.add_argument('--leet', type=int, choices=range(1, 5), default=2,
                       help='Leet speak level (1-4)')
    
    # Output
    parser.add_argument('-o', '--output', default='enhanced_wordlist.txt',
                       help='Output filename')
    parser.add_argument('--max-size', type=int, default=1000000,
                       help='Maximum number of passwords to generate')
    
    args = parser.parse_args()
    
    generator = EnhancedWordlistGenerator()
    
    if args.quick:
        # Quick mode with sensible defaults
        print("[*] Quick mode enabled with sensible defaults")
        
        data = {
            'personal_info': {},
            'dates': {},
            'numbers': {},
            'keywords': [],
            'leet_enabled': args.leet > 1,
            'leet_level': args.leet,
            'numbers_enabled': True,
            'number_types': ['1', '2', '3'],
            'number_ranges': [(0, 99), (1950, 2024)],
            'special_enabled': True,
            'special_chars': generator.special_char_sets['basic'],
            'combo_types': ['1', '2', '4'],
            'separators': generator.common_separators,
            'depth': args.depth,
            'min_length': 6,
            'max_length': 32,
            'max_size': args.max_size
        }
        
        # Add any provided command line info
        if args.first:
            data['personal_info']['first_name'] = args.first.lower()
        if args.last:
            data['personal_info']['last_name'] = args.last.lower()
        if args.birthdate:
            data['dates']['birthdate'] = args.birthdate
        if args.keywords:
            data['keywords'] = [k.strip().lower() for k in args.keywords.split(',')]
        
    else:
        # Interactive mode
        data = generator.get_user_input()
    
    print(f"\n{'='*70}")
    print(" GENERATION PARAMETERS")
    print(f"{'='*70}")
    
    # Show key parameters
    for key, value in data.items():
        if key not in ['personal_info', 'dates', 'numbers', 'number_ranges']:
            if isinstance(value, list):
                display = ', '.join(str(v) for v in value[:3])
                if len(value) > 3:
                    display += f'... ({len(value)} items)'
                print(f"  {key:20}: {display}")
            else:
                print(f"  {key:20}: {value}")
    
    print(f"{'='*70}\n")
    
    # Generate wordlist
    wordlist = generator.generate(data)
    
    print(f"\n{'='*70}")
    print(" GENERATION COMPLETE")
    print(f"{'='*70}")
    print(f" Total passwords generated: {len(wordlist):,}")
    
    if wordlist:
        print("\n[*] Sample of generated passwords:")
        sample = random.sample(list(wordlist), min(15, len(wordlist)))
        for i, word in enumerate(sample):
            print(f"  {i+1:2}. {word}")
    
    # Save
    output_file = args.output
    generator.save_wordlist(wordlist, output_file)
    
    print(f"\n[*] Wordlist saved to: {os.path.abspath(output_file)}")

if __name__ == '__main__':
    main()