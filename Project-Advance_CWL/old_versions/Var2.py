#!/usr/bin/env python3
"""
ULTIMATE WORDLIST GENERATOR - Maximum combinations with minimal input
Generates exhaustive password combinations from personal information
"""

import argparse
import sys
import itertools
from datetime import datetime
import os
import re
from typing import List, Set, Dict, Any
import math

class UltimateWordlistGenerator:
    def __init__(self):
        self.wordlist = set()
        self.total_generated = 0
        
        # Enhanced leet speak mappings
        self.leet_maps = {
            'a': ['4', '@', '/\\', '^', '∂', 'λ'],
            'b': ['8', '13', '|3', 'ß', ']3'],
            'c': ['(', '[', '<', '©', '¢'],
            'd': ['|)', '|]', 'Ð', 'đ'],
            'e': ['3', '&', '€', '£', 'ë'],
            'f': ['|=', 'ph', 'ƒ'],
            'g': ['6', '9', '&', 'ğ'],
            'h': ['#', '|-|', '}{', ']-[', ')-('],
            'i': ['1', '!', '|', 'ï', 'ì'],
            'j': ['_|', ']', '¿'],
            'k': ['|<', '|{', 'ɮ'],
            'l': ['1', '|', '7', '£', '¬'],
            'm': ['/\\/\\', '|\\/|', '^^', 'ɱ'],
            'n': ['|\\|', '/\\/', 'И', 'п'],
            'o': ['0', '()', '°', 'Θ', 'Ø'],
            'p': ['|>', '|*', 'þ', '¶'],
            'q': ['0_', '9', '(,)'],
            'r': ['|2', 'Я', '®', 'ʁ'],
            's': ['5', '$', 'z', '§', 'š'],
            't': ['7', '+', '†', 'ţ'],
            'u': ['|_|', 'µ', 'û'],
            'v': ['\\/', '|/', '√'],
            'w': ['\\/\\/', 'vv', 'ш', 'ω'],
            'x': ['><', '}{', '×', 'ж'],
            'y': ['`/', '¥', 'ÿ'],
            'z': ['2', '7_', 'ž', 'ζ']
        }
        
        # Common number patterns and years
        self.number_patterns = [
            '', '1', '12', '123', '1234', '12345', '123456',
            '0', '00', '000', '0000', '00000',
            '01', '02', '03', '04', '05', '06', '07', '08', '09',
            '10', '11', '22', '33', '44', '55', '66', '77', '88', '99',
            '007', '100', '200', '500', '1000',
            '69', '420', '666', '777', '888', '999',
            '111', '222', '333', '444', '555',
            '1111', '2222', '3333', '4444', '5555',
            '101', '202', '303', '404', '505',
            '010', '020', '030', '040', '050',
            '1122', '1212', '1221', '2112',
            '1990', '1991', '1992', '1993', '1994', '1995',
            '1996', '1997', '1998', '1999',
            '2000', '2001', '2002', '2003', '2004', '2005',
            '2006', '2007', '2008', '2009',
            '2010', '2011', '2012', '2013', '2014', '2015',
            '2016', '2017', '2018', '2019', '2020', '2021',
            '2022', '2023', '2024', '2025',
            '1980', '1985', '1990', '1995', '2000', '2005',
            '1970', '1975', '1980', '1985'
        ]
        
        # Special characters in different positions
        self.special_chars = ['!', '@', '#', '$', '%', '^', '&', '*', '-', '_', '.', '+', '=']
        self.special_prefixes = ['!', '@', '#', '$', '%', '&', '*']
        self.special_suffixes = ['!', '@', '#', '$', '%', '^', '&', '*', '123', '1']
        
        # Common password patterns and words
        self.common_passwords = [
            'pass', 'password', 'admin', 'user', 'login', 'secret', 'key',
            'welcome', 'letmein', 'master', 'hello', 'access', 'security',
            'qwerty', 'asdf', 'zxcv', 'abc', 'test', 'demo', 'temp',
            'love', 'like', 'cool', 'hot', 'super', 'mega', 'ultra',
            '123', '321', '1234', '4321', '12345', '54321'
        ]
        
        # Separators for combinations
        self.separators = ['', '.', '_', '-', '']
        
    def get_minimal_input(self):
        """Get minimal input from user - just the essentials"""
        print("\n" + "="*60)
        print(" ULTIMATE WORDLIST GENERATOR - Minimal Input Mode")
        print("="*60)
        print("\n[!] Provide just the basics - we'll generate the rest!\n")
        
        data = {}
        
        # Absolute minimum input
        data['first_name'] = input("First name (REQUIRED): ").strip().lower()
        if not data['first_name']:
            print("[!] First name is required!")
            sys.exit(1)
            
        data['last_name'] = input("Last name (optional): ").strip().lower()
        birth_year = input("Birth year YYYY (optional): ").strip()
        
        if birth_year:
            data['birthdate'] = f"01/01/{birth_year}"
        
        # Ask for just one extra keyword
        extra = input("One important word (pet, city, team, etc.): ").strip().lower()
        if extra:
            data['keywords'] = [extra]
        
        # Auto-add common words
        auto_common = input("Auto-add common password words? (y/n, default: y): ").strip().lower()
        if auto_common != 'n':
            data['auto_common'] = True
        
        return data
    
    def parse_date_extensively(self, date_str):
        """Extract ALL possible date combinations"""
        date_parts = []
        
        if not date_str:
            return date_parts
            
        # Try to extract year from any format
        year_match = re.search(r'(19\d{2}|20\d{2})', date_str)
        if year_match:
            year = year_match.group(1)
            date_parts.extend([
                year,                    # 1990
                year[2:],                # 90
                year + year[2:],         # 199090
                year[2:] + year,         # 901990
            ])
        
        # Try common date formats
        formats = [
            '%d/%m/%Y', '%m/%d/%Y', '%d-%m-%Y', '%m-%d-%Y',
            '%d/%m/%y', '%m/%d/%y', '%Y/%m/%d', '%Y-%m-%d',
            '%d%m%Y', '%m%d%Y', '%Y%m%d', '%d%m%y', '%m%d%y'
        ]
        
        for fmt in formats:
            try:
                dt = datetime.strptime(date_str, fmt)
                
                # Generate ALL possible combinations
                day = dt.strftime('%d')      # 01-31
                month = dt.strftime('%m')    # 01-12  
                year_full = dt.strftime('%Y') # 1990
                year_short = dt.strftime('%y') # 90
                
                # Add all individual components
                date_parts.extend([day, month, year_full, year_short])
                
                # Add combinations
                date_parts.extend([
                    day + month,                    # 1506
                    month + day,                    # 0615
                    day + month + year_short,       # 150690
                    month + day + year_short,       # 061590
                    day + month + year_full,        # 15061990
                    month + day + year_full,        # 06151990
                    year_short + month + day,       # 900615
                    year_full + month + day,        # 19900615
                    year_short + day + month,       # 901506
                    year_full + day + month,        # 19901506
                ])
                
                # Reverse combinations
                date_parts.extend([
                    day[::-1], month[::-1], 
                    (day + month)[::-1],
                    (month + day)[::-1],
                ])
                
            except ValueError:
                continue
        
        # Remove empty strings and duplicates
        return list(set([p for p in date_parts if p]))
    
    def generate_name_variations(self, name):
        """Generate ALL possible variations of a name"""
        variations = set()
        
        if not name:
            return variations
        
        # Basic variations
        variations.update([
            name,
            name.title(),
            name.upper(),
            name.capitalize(),
        ])
        
        # Common modifications
        if len(name) > 2:
            variations.update([
                name + 'y',
                name + 'ie',
                name + 'ey',
                name + 'i',
                name + 'o',
                'big' + name,
                'little' + name,
                'super' + name,
                'mr' + name,
                'ms' + name,
                name + '123',
                name + '1',
                name + '2',
            ])
        
        # Double/triple the name
        variations.update([
            name * 2,
            name * 3,
            name + name.title(),
            name.title() + name,
        ])
        
        # Add numbers 0-9 at end
        for i in range(10):
            variations.add(name + str(i))
            variations.add(name + str(i) * 2)
            variations.add(name + str(i) * 3)
        
        return variations
    
    def generate_leet_variations(self, word, max_variations=1000):
        """Generate leet speak variations aggressively"""
        variations = set([word])
        
        if len(word) > 10:  # Limit for performance on long words
            word = word[:10]
        
        # Generate basic leet variations
        for i, char in enumerate(word.lower()):
            if char in self.leet_maps:
                for leet_char in self.leet_maps[char][:3]:  # Limit to 3 variations per char
                    new_word = word[:i] + leet_char + word[i+1:]
                    variations.add(new_word)
                    
                    # Also create capitalized version
                    if new_word:
                        variations.add(new_word.title())
                        variations.add(new_word.upper())
        
        # Generate ALL combinations of leet replacements (limited)
        char_list = list(word.lower())
        leet_possibilities = []
        
        for char in char_list:
            if char in self.leet_maps:
                leet_possibilities.append([char] + self.leet_maps[char][:2])
            else:
                leet_possibilities.append([char])
        
        # Generate some combinations (not all to avoid explosion)
        import random
        for _ in range(min(500, 3**len(word))):  # Limit combinations
            leet_word = ''
            for possibilities in leet_possibilities:
                leet_word += random.choice(possibilities)
            variations.add(leet_word)
            variations.add(leet_word.title())
            variations.add(leet_word.upper())
        
        return list(variations)[:max_variations]
    
    def generate_all_combinations(self, data):
        """Generate ALL possible combinations from the data"""
        all_words = set()
        
        # Extract all base words
        base_words = []
        
        # Names and their variations
        for key in ['first_name', 'last_name', 'nickname', 'maiden_name', 'pet_name', 'company']:
            if key in data and data[key]:
                name = data[key]
                base_words.append(name)
                base_words.extend(self.generate_name_variations(name))
        
        # Dates
        for key in ['birthdate', 'partner_birthdate', 'anniversary']:
            if key in data and data[key]:
                base_words.extend(self.parse_date_extensively(data[key]))
        
        # Keywords
        if 'keywords' in data:
            base_words.extend(data['keywords'])
        
        # Common passwords if enabled
        if data.get('auto_common'):
            base_words.extend(self.common_passwords)
        
        # Generate ALL 2-word combinations
        print("[*] Generating word combinations...")
        for word1 in base_words[:20]:  # Limit to first 20 to avoid explosion
            for word2 in base_words[:20]:
                if word1 != word2:
                    # Add with all separators
                    for sep in self.separators:
                        all_words.add(word1 + sep + word2)
                        all_words.add(word2 + sep + word1)
                        
                    # Add reversed
                    all_words.add(word1[::-1] + word2)
                    all_words.add(word1 + word2[::-1])
        
        # Add all individual words
        all_words.update(base_words)
        
        # Add number-appended versions
        print("[*] Adding number patterns...")
        number_enhanced = set()
        for word in all_words:
            number_enhanced.add(word)
            # Add with common number patterns
            for num in self.number_patterns[:50]:  # Limit to 50 number patterns
                if num:  # Skip empty
                    number_enhanced.add(word + num)
                    number_enhanced.add(num + word)
                    number_enhanced.add(word + '_' + num)
                    number_enhanced.add(num + '_' + word)
        
        all_words.update(number_enhanced)
        
        # Add special character variations
        print("[*] Adding special characters...")
        special_enhanced = set()
        for word in list(all_words)[:10000]:  # Limit to avoid explosion
            special_enhanced.add(word)
            
            # Add prefixes
            for prefix in self.special_prefixes:
                special_enhanced.add(prefix + word)
            
            # Add suffixes
            for suffix in self.special_suffixes:
                special_enhanced.add(word + suffix)
            
            # Wrap with special chars
            for char in self.special_chars[:5]:
                special_enhanced.add(char + word + char)
            
            # Add at both ends with different chars
            for pre in self.special_prefixes[:3]:
                for suf in self.special_suffixes[:3]:
                    special_enhanced.add(pre + word + suf)
        
        all_words.update(special_enhanced)
        
        # Generate leet variations for top words
        print("[*] Generating leet speak variations...")
        leet_enhanced = set()
        for word in list(all_words)[:2000]:  # Process first 2000 words
            leet_enhanced.add(word)
            leet_vars = self.generate_leet_variations(word, max_variations=50)
            leet_enhanced.update(leet_vars)
        
        all_words.update(leet_enhanced)
        
        # Add case variations for all words
        print("[*] Adding case variations...")
        case_variations = set()
        for word in list(all_words)[:5000]:
            case_variations.add(word)
            case_variations.add(word.title())
            case_variations.add(word.upper())
            case_variations.add(word.lower())
            
            # Mixed case patterns
            if len(word) > 3:
                case_variations.add(word[0].upper() + word[1:].lower())
                case_variations.add(word[0].lower() + word[1:].upper())
        
        all_words.update(case_variations)
        
        return all_words
    
    def mega_combine(self, base_words):
        """Generate MEGA combinations - extremely aggressive"""
        mega_set = set()
        
        # Take first 10 base words for combination generation
        core_words = list(base_words)[:10]
        
        # Generate all 2 and 3 word permutations
        print("[*] Generating MEGA combinations (this may take a moment)...")
        
        # 2-word combinations
        for i, word1 in enumerate(core_words):
            for word2 in core_words[i+1:]:
                # Direct concatenation
                mega_set.add(word1 + word2)
                mega_set.add(word2 + word1)
                
                # With separators
                for sep in ['', '.', '_', '-', '']:
                    mega_set.add(word1 + sep + word2)
                    mega_set.add(word2 + sep + word1)
        
        # Add number suffixes to everything
        print("[*] Applying number suffixes...")
        numbered = set()
        for word in mega_set:
            numbered.add(word)
            # Add years 1970-2025
            for year in range(1970, 2026):
                numbered.add(word + str(year))
                numbered.add(word + str(year)[2:])
            
            # Add common patterns
            for i in range(10):
                numbered.add(word + str(i))
                numbered.add(word + str(i) * 2)
                numbered.add(word + str(i) * 3)
        
        mega_set.update(numbered)
        
        return mega_set
    
    def save_wordlist(self, wordlist, filename, max_words=10000000):
        """Save wordlist to file with progress indicator"""
        # Limit wordlist size if too large
        wordlist_limited = list(wordlist)
        if len(wordlist_limited) > max_words:
            print(f"[!] Wordlist too large ({len(wordlist_limited):,} words), limiting to {max_words:,}")
            wordlist_limited = wordlist_limited[:max_words]
        
        print(f"[*] Saving {len(wordlist_limited):,} words to {filename}...")
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                for i, word in enumerate(wordlist_limited):
                    f.write(word + '\n')
                    if i % 100000 == 0 and i > 0:
                        print(f"  -> Saved {i:,} words...")
            
            file_size = os.path.getsize(filename)
            print(f"[+] Successfully saved {len(wordlist_limited):,} words")
            print(f"[+] File size: {file_size:,} bytes ({file_size/1024/1024:.2f} MB)")
            return True
            
        except Exception as e:
            print(f"[-] Error saving file: {e}")
            return False

def main():
    parser = argparse.ArgumentParser(
        description='ULTIMATE WORDLIST GENERATOR - Maximum combinations from minimal input',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --mega                       # Interactive mega mode
  %(prog)s -f john -l doe -y 1990       # Quick command line
  %(prog)s --first john --extreme       # Extreme mode with just first name
  %(prog)s -f john -l doe -o 10M.txt --limit 10000000  # Generate 10M passwords
        """
    )
    
    # Input options
    parser.add_argument('-f', '--first', help='First name (minimum required)')
    parser.add_argument('-l', '--last', help='Last name')
    parser.add_argument('-y', '--year', help='Birth year (YYYY)')
    parser.add_argument('-k', '--keyword', help='One important keyword')
    parser.add_argument('--common', action='store_true', default=True,
                       help='Add common password words (default: true)')
    
    # Mode options
    parser.add_argument('--mega', action='store_true',
                       help='MEGA mode - generate maximum combinations')
    parser.add_argument('--extreme', action='store_true',
                       help='EXTREME mode - even more combinations than mega')
    parser.add_argument('--aggressive', action='store_true',
                       help='AGGRESSIVE mode - balance of size and speed')
    
    # Control options
    parser.add_argument('--limit', type=int, default=5000000,
                       help='Maximum words to generate (default: 5,000,000)')
    parser.add_argument('--min-length', type=int, default=4,
                       help='Minimum password length (default: 4)')
    parser.add_argument('--max-length', type=int, default=32,
                       help='Maximum password length (default: 32)')
    
    # Output options
    parser.add_argument('-o', '--output', default='mega_wordlist.txt',
                       help='Output filename (default: mega_wordlist.txt)')
    parser.add_argument('--show-count', type=int, default=20,
                       help='Show N sample passwords (default: 20)')
    
    args = parser.parse_args()
    
    # Initialize generator
    generator = UltimateWordlistGenerator()
    
    # Collect data
    if args.first or args.mega or args.extreme:
        # Command line mode
        data = {}
        if args.first:
            data['first_name'] = args.first.lower()
        if args.last:
            data['last_name'] = args.last.lower()
        if args.year:
            data['birthdate'] = f"01/01/{args.year}"
        if args.keyword:
            data['keywords'] = [args.keyword.lower()]
        
        data['auto_common'] = args.common
        
        if not data:
            print("[!] At least provide --first name!")
            sys.exit(1)
            
    else:
        # Interactive minimal mode
        data = generator.get_minimal_input()
    
    print(f"\n{'='*60}")
    print(f" GENERATING WORDLIST WITH:")
    for key, value in data.items():
        if value and key != 'auto_common':
            print(f"  • {key}: {value}")
    print(f"{'='*60}\n")
    
    # Generate base combinations
    print("[*] PHASE 1: Generating base combinations...")
    all_words = generator.generate_all_combinations(data)
    print(f"[+] Phase 1 complete: {len(all_words):,} base combinations")
    
    # Apply selected mode
    if args.extreme:
        print("[*] EXTREME MODE: Generating MEGA combinations...")
        mega_words = generator.mega_combine(all_words)
        all_words.update(mega_words)
        print(f"[+] Added {len(mega_words):,} MEGA combinations")
        
        # Double up everything with numbers
        print("[*] EXTREME MODE: Doubling with numbers...")
        doubled = set()
        for word in list(all_words)[:100000]:  # Limit for performance
            for i in range(100):  # Add numbers 0-99
                doubled.add(word + str(i).zfill(2))
                doubled.add(str(i).zfill(2) + word)
        
        all_words.update(doubled)
        
    elif args.mega:
        print("[*] MEGA MODE: Generating enhanced combinations...")
        mega_words = generator.mega_combine(all_words)
        all_words.update(mega_words)
    
    # Filter by length
    print("[*] Filtering by length...")
    filtered_words = set()
    for word in all_words:
        if args.min_length <= len(word) <= args.max_length:
            filtered_words.add(word)
    
    all_words = filtered_words
    
    # Convert to list and sort
    print("[*] Finalizing wordlist...")
    final_wordlist = sorted(list(all_words))
    
    # Show statistics
    print(f"\n{'='*60}")
    print(f" GENERATION COMPLETE!")
    print(f"{'='*60}")
    print(f" Total unique words generated: {len(final_wordlist):,}")
    
    if final_wordlist:
        # Show sample
        print(f"\n[*] Sample of generated passwords:")
        sample_size = min(args.show_count, len(final_wordlist))
        for i in range(sample_size):
            step = len(final_wordlist) // sample_size
            idx = i * step
            print(f"  {i+1:2}. {final_wordlist[idx]}")
        
        # Show strongest passwords
        print(f"\n[*] Examples of strong passwords generated:")
        strong_samples = [w for w in final_wordlist if len(w) >= 12 and any(c in generator.special_chars for c in w)]
        if strong_samples:
            for i, word in enumerate(strong_samples[:5]):
                print(f"  {i+1:2}. {word}")
    
    # Save to file
    print(f"\n[*] Saving to file: {args.output}")
    generator.save_wordlist(final_wordlist, args.output, max_words=args.limit)

if __name__ == '__main__':
    main()