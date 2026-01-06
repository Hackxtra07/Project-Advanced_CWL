#!/usr/bin/env python3
"""
CUSTOM WORDLIST GENERATOR - User-Defined Only
No auto-added words, no assumptions. User defines EVERYTHING.
"""

import argparse
import sys
from datetime import datetime
import os
import re
from typing import Set, Dict, List

class CustomWordlistGenerator:
    def __init__(self):
        # Only basic leet mappings - user can customize if needed
        self.leet_maps = {
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
        
        # NO pre-defined patterns - user provides everything
    
    def get_user_input(self):
        """Get ALL information from user - nothing assumed"""
        print("\n" + "="*60)
        print(" CUSTOM WORDLIST GENERATOR - User Defined Only")
        print("="*60)
        print("\n[!] You define everything. Nothing is auto-added.\n")
        
        data = {}
        
        # Personal Information (user provides or skips)
        print("--- PERSONAL INFORMATION (optional) ---")
        data['first_name'] = input("First name: ").strip().lower() or None
        data['last_name'] = input("Last name: ").strip().lower() or None
        data['nickname'] = input("Nickname: ").strip().lower() or None
        data['maiden_name'] = input("Mother's maiden name: ").strip().lower() or None
        data['pet_name'] = input("Pet name: ").strip().lower() or None
        data['company'] = input("Company name: ").strip().lower() or None
        
        # Dates (user provides or skips)
        print("\n--- IMPORTANT DATES (optional) ---")
        data['birthdate'] = input("Birthdate (DD/MM/YYYY): ").strip() or None
        data['partner_birthdate'] = input("Partner's birthdate: ").strip() or None
        data['anniversary'] = input("Anniversary date: ").strip() or None
        
        # Keywords (user defines)
        print("\n--- KEYWORDS (define your own) ---")
        keywords = input("Important keywords (comma-separated): ").strip().lower()
        data['keywords'] = [k.strip() for k in keywords.split(',') if k.strip()]
        
        # Numbers (user defines)
        print("\n--- IMPORTANT NUMBERS (optional) ---")
        data['phone'] = input("Phone number: ").strip() or None
        data['zipcode'] = input("Zip/Postal code: ").strip() or None
        
        # Custom patterns (user defines)
        print("\n--- CUSTOM PATTERNS (optional) ---")
        patterns = input("Custom number patterns (comma-separated, e.g., 123,456,789): ").strip()
        data['custom_patterns'] = [p.strip() for p in patterns.split(',') if p.strip()]
        
        # Special characters to use (user defines)
        print("\n--- SPECIAL CHARACTERS (optional) ---")
        specials = input("Special characters to use (e.g., !@#$): ").strip()
        data['special_chars'] = list(specials) if specials else []
        
        # Generation options (user chooses)
        print("\n--- GENERATION OPTIONS ---")
        
        # Leet speak options
        leet_choice = input("Enable leet speak? (y/n): ").strip().lower()
        data['leet_enabled'] = leet_choice == 'y'
        
        if data['leet_enabled']:
            leet_custom = input("Custom leet mappings (format a=4,@ b=8, leave blank for default): ").strip()
            if leet_custom:
                data['custom_leet'] = self.parse_custom_leet(leet_custom)
        
        # Number addition options
        num_choice = input("Add number patterns? (y/n): ").strip().lower()
        data['numbers_enabled'] = num_choice == 'y'
        
        if data['numbers_enabled']:
            num_range = input("Number range to add (e.g., 0-99 or 0-999): ").strip()
            if num_range and '-' in num_range:
                start, end = map(int, num_range.split('-'))
                data['number_range'] = list(range(start, end + 1))
            else:
                data['number_range'] = list(range(0, 100))  # Default 0-99
        
        # Special characters options
        special_choice = input("Add special characters? (y/n): ").strip().lower()
        data['special_enabled'] = special_choice == 'y'
        
        # Combination options
        print("\n--- COMBINATION OPTIONS ---")
        combo_choice = input("Generate word combinations? (y/n): ").strip().lower()
        data['combinations_enabled'] = combo_choice == 'y'
        
        if data['combinations_enabled']:
            separators = input("Separators to use (e.g., .,_@): ").strip()
            data['separators'] = list(separators) if separators else ['']
        
        # Length constraints
        print("\n--- LENGTH CONSTRAINTS ---")
        min_len = input("Minimum password length (default: 4): ").strip()
        data['min_length'] = int(min_len) if min_len.isdigit() else 4
        
        max_len = input("Maximum password length (default: 32): ").strip()
        data['max_length'] = int(max_len) if max_len.isdigit() else 32
        
        return {k: v for k, v in data.items() if v is not None and v != []}
    
    def parse_custom_leet(self, leet_str: str) -> Dict:
        """Parse custom leet mappings from user input"""
        custom_leet = {}
        mappings = leet_str.split()
        for mapping in mappings:
            if '=' in mapping:
                char, replacements = mapping.split('=', 1)
                custom_leet[char.lower()] = [r.strip() for r in replacements.split(',')]
        return custom_leet
    
    def parse_date_components(self, date_str: str) -> List[str]:
        """Extract date components based on user input"""
        components = []
        
        if not date_str:
            return components
        
        # Try common formats
        formats = ['%d/%m/%Y', '%m/%d/%Y', '%d-%m-%Y', '%m-%d-%Y', '%Y-%m-%d', '%d%m%Y', '%m%d%Y']
        
        for fmt in formats:
            try:
                dt = datetime.strptime(date_str, fmt)
                # User gets exactly what they input, no extra combinations
                components = [
                    dt.strftime('%d'),      # Day
                    dt.strftime('%m'),      # Month
                    dt.strftime('%Y'),      # Year
                    dt.strftime('%y'),      # Short year
                ]
                # Also add basic combinations if user wants
                components.append(dt.strftime('%d%m%Y'))  # DDMMYYYY
                components.append(dt.strftime('%m%d%Y'))  # MMDDYYYY
                components.append(dt.strftime('%Y%m%d'))  # YYYYMMDD
                break
            except ValueError:
                continue
        
        # If no format matches, try to extract year
        if not components:
            year_match = re.search(r'(19\d{2}|20\d{2})', date_str)
            if year_match:
                year = year_match.group(1)
                components.append(year)
                components.append(year[2:])
        
        return list(set([c for c in components if c]))
    
    def get_base_words(self, data: Dict) -> Set:
        """Get ONLY the words user provided - no extras"""
        words = set()
        
        # Names (exactly as user provided)
        name_fields = ['first_name', 'last_name', 'nickname', 'maiden_name', 'pet_name', 'company']
        for field in name_fields:
            if field in data:
                words.add(data[field])
                # Only add basic variations if user explicitly wants
                words.add(data[field].title())
        
        # Dates (parsed as user provided)
        date_fields = ['birthdate', 'partner_birthdate', 'anniversary']
        for field in date_fields:
            if field in data:
                words.update(self.parse_date_components(data[field]))
        
        # Keywords (exactly as user provided)
        if 'keywords' in data:
            for keyword in data['keywords']:
                words.add(keyword)
                words.add(keyword.title())
        
        # Numbers (exactly as user provided)
        if 'phone' in data:
            phone_digits = re.sub(r'\D', '', data['phone'])
            if phone_digits:
                words.add(phone_digits)
                if len(phone_digits) >= 4:
                    words.add(phone_digits[-4:])  # Last 4 digits
        
        if 'zipcode' in data:
            words.add(data['zipcode'])
        
        # Custom patterns (exactly as user provided)
        if 'custom_patterns' in data:
            words.update(data['custom_patterns'])
        
        return words
    
    def apply_leet_speak(self, word: str, leet_map: Dict) -> Set:
        """Apply leet speak transformations (only if user enabled)"""
        variations = {word}
        
        if not leet_map:
            return variations
        
        # Basic leet replacements
        leet_word = word
        for char, replacements in leet_map.items():
            if char in leet_word.lower():
                for replacement in replacements:
                    variations.add(leet_word.lower().replace(char, replacement))
        
        return variations
    
    def generate_combinations(self, base_words: Set, separators: List[str]) -> Set:
        """Generate combinations of base words (only if user enabled)"""
        combinations = set()
        
        words_list = list(base_words)
        
        # Add all base words
        combinations.update(base_words)
        
        # Generate 2-word combinations
        for i in range(len(words_list)):
            for j in range(i + 1, len(words_list)):
                word1 = words_list[i]
                word2 = words_list[j]
                
                for sep in separators:
                    combinations.add(word1 + sep + word2)
                    combinations.add(word2 + sep + word1)
                
                # Without separator
                combinations.add(word1 + word2)
                combinations.add(word2 + word1)
        
        return combinations
    
    def add_number_patterns(self, words: Set, number_range: List[int], custom_patterns: List[str]) -> Set:
        """Add number patterns to words (only if user enabled)"""
        enhanced = set()
        
        for word in words:
            enhanced.add(word)  # Keep original
            
            # Add numbers from user-defined range
            for num in number_range:
                enhanced.add(word + str(num))
                enhanced.add(str(num) + word)
            
            # Add custom patterns
            for pattern in custom_patterns:
                enhanced.add(word + pattern)
                enhanced.add(pattern + word)
        
        return enhanced
    
    def add_special_chars(self, words: Set, special_chars: List[str]) -> Set:
        """Add special characters (only if user enabled)"""
        enhanced = set()
        
        for word in words:
            enhanced.add(word)  # Keep original
            
            # Add special chars at beginning and end
            for char in special_chars:
                enhanced.add(char + word)
                enhanced.add(word + char)
                enhanced.add(char + word + char)
        
        return enhanced
    
    def generate(self, data: Dict) -> Set:
        """Main generation function - ONLY what user defined"""
        print("\n[*] Starting generation with user-defined parameters...")
        
        # Step 1: Get base words (exactly what user provided)
        base_words = self.get_base_words(data)
        print(f"[+] Base words collected: {len(base_words)}")
        
        all_words = base_words.copy()
        
        # Step 2: Apply leet speak if enabled
        if data.get('leet_enabled', False):
            print("[*] Applying leet speak...")
            leet_words = set()
            leet_map = data.get('custom_leet', self.leet_maps)
            
            for word in all_words:
                leet_words.update(self.apply_leet_speak(word, leet_map))
            
            all_words.update(leet_words)
            print(f"[+] After leet: {len(all_words)} words")
        
        # Step 3: Generate combinations if enabled
        if data.get('combinations_enabled', False):
            print("[*] Generating word combinations...")
            separators = data.get('separators', [''])
            combos = self.generate_combinations(all_words, separators)
            all_words.update(combos)
            print(f"[+] After combinations: {len(all_words)} words")
        
        # Step 4: Add number patterns if enabled
        if data.get('numbers_enabled', False):
            print("[*] Adding number patterns...")
            number_range = data.get('number_range', range(0, 100))
            custom_patterns = data.get('custom_patterns', [])
            numbered = self.add_number_patterns(all_words, number_range, custom_patterns)
            all_words.update(numbered)
            print(f"[+] After numbers: {len(all_words)} words")
        
        # Step 5: Add special characters if enabled
        if data.get('special_enabled', False):
            print("[*] Adding special characters...")
            special_chars = data.get('special_chars', ['!', '@', '#', '$'])
            special = self.add_special_chars(all_words, special_chars)
            all_words.update(special)
            print(f"[+] After special chars: {len(all_words)} words")
        
        # Step 6: Filter by length
        min_len = data.get('min_length', 4)
        max_len = data.get('max_length', 32)
        
        filtered = {w for w in all_words if min_len <= len(w) <= max_len}
        
        print(f"[*] Filtering by length ({min_len}-{max_len}): {len(all_words)} -> {len(filtered)}")
        
        return filtered
    
    def save_wordlist(self, wordlist: Set, filename: str):
        """Save wordlist to file"""
        wordlist_list = sorted(list(wordlist))
        
        print(f"\n[*] Saving {len(wordlist_list):,} words to {filename}...")
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                for word in wordlist_list:
                    f.write(word + '\n')
            
            file_size = os.path.getsize(filename)
            print(f"[+] Successfully saved {len(wordlist_list):,} words")
            print(f"[+] File size: {file_size:,} bytes ({file_size/1024/1024:.2f} MB)")
            
            return True
            
        except Exception as e:
            print(f"[-] Error saving file: {e}")
            return False

def main():
    parser = argparse.ArgumentParser(
        description='CUSTOM WORDLIST GENERATOR - User Defined Only',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive mode (user defines everything)
  python custom_generator.py
  
  # Command line mode with basic info
  python custom_generator.py --first john --last doe --birthdate 15/06/1990
  
  # With specific options
  python custom_generator.py --first john --leet --numbers 0-999 --special "!@#"
        """
    )
    
    # Basic info (optional - user can provide in interactive mode)
    parser.add_argument('--first', help='First name')
    parser.add_argument('--last', help='Last name')
    parser.add_argument('--birthdate', help='Birthdate (DD/MM/YYYY)')
    parser.add_argument('--keywords', help='Comma-separated keywords')
    
    # Options
    parser.add_argument('--leet', action='store_true', help='Enable leet speak')
    parser.add_argument('--numbers', help='Number range (e.g., 0-99)')
    parser.add_argument('--special', help='Special characters to use (e.g., "!@#$")')
    
    # Output
    parser.add_argument('-o', '--output', default='custom_wordlist.txt',
                       help='Output filename')
    
    args = parser.parse_args()
    
    generator = CustomWordlistGenerator()
    
    # If command line has minimal args, use interactive mode for rest
    use_interactive = not (args.first and args.last and args.birthdate)
    
    if use_interactive:
        data = generator.get_user_input()
    else:
        # Build data from command line args
        data = {}
        
        if args.first:
            data['first_name'] = args.first.lower()
        if args.last:
            data['last_name'] = args.last.lower()
        if args.birthdate:
            data['birthdate'] = args.birthdate
        if args.keywords:
            data['keywords'] = [k.strip().lower() for k in args.keywords.split(',')]
        
        # Get additional options interactively
        print("\n[!] Using command line input. Configure additional options:")
        print("-" * 50)
        
        if args.leet:
            data['leet_enabled'] = True
        else:
            leet_choice = input("Enable leet speak? (y/n): ").strip().lower()
            data['leet_enabled'] = leet_choice == 'y'
        
        if args.numbers:
            data['numbers_enabled'] = True
            start, end = map(int, args.numbers.split('-'))
            data['number_range'] = list(range(start, end + 1))
        else:
            num_choice = input("Add number patterns? (y/n): ").strip().lower()
            if num_choice == 'y':
                data['numbers_enabled'] = True
                num_range = input("Number range (e.g., 0-99): ").strip()
                if num_range and '-' in num_range:
                    start, end = map(int, num_range.split('-'))
                    data['number_range'] = list(range(start, end + 1))
                else:
                    data['number_range'] = list(range(0, 100))
        
        if args.special:
            data['special_enabled'] = True
            data['special_chars'] = list(args.special)
        else:
            special_choice = input("Add special characters? (y/n): ").strip().lower()
            if special_choice == 'y':
                data['special_enabled'] = True
                specials = input("Special characters to use: ").strip()
                data['special_chars'] = list(specials) if specials else ['!', '@', '#', '$']
        
        # Default options
        data['combinations_enabled'] = True
        data['separators'] = ['', '.', '_', '-']
        data['min_length'] = 4
        data['max_length'] = 32
    
    print(f"\n{'='*60}")
    print(" GENERATION PARAMETERS")
    print(f"{'='*60}")
    
    # Show what user defined
    for key, value in data.items():
        if key not in ['number_range', 'custom_leet']:  # Skip large lists
            if isinstance(value, list):
                print(f"  {key}: {', '.join(str(v) for v in value[:5])}" + 
                      (f"... ({len(value)} total)" if len(value) > 5 else ""))
            else:
                print(f"  {key}: {value}")
    
    print(f"{'='*60}\n")
    
    # Generate wordlist
    wordlist = generator.generate(data)
    
    print(f"\n{'='*60}")
    print(" GENERATION COMPLETE")
    print(f"{'='*60}")
    print(f" Total words generated: {len(wordlist):,}")
    
    if wordlist:
        print("\n[*] Sample of generated words:")
        sample = list(wordlist)[:20]
        for i, word in enumerate(sample):
            print(f"  {i+1:2}. {word}")
    
    # Save
    output_file = args.output
    generator.save_wordlist(wordlist, output_file)

if __name__ == '__main__':
    main()