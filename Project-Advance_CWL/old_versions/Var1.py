#!/usr/bin/env python3
"""
Advanced Custom Wordlist Generator (ACWG)
A tool for generating meaningful wordlists from personal information
with leet mode, number patterns, and special characters support
"""

import argparse
import sys
import itertools
from datetime import datetime
import re
import os

class WordlistGenerator:
    def __init__(self):
        self.wordlist = set()
        self.leet_replacements = {
            'a': ['4', '@', '/\\'],
            'b': ['8', '13', '|3'],
            'c': ['(', '[', '<'],
            'e': ['3', '&'],
            'g': ['6', '9'],
            'h': ['#', '|-|'],
            'i': ['1', '!', '|'],
            'l': ['1', '|', '7'],
            'o': ['0', '()'],
            's': ['5', '$', 'z'],
            't': ['7', '+'],
            'z': ['2', '7_']
        }
        
    def get_user_input(self):
        """Collect personal information from user"""
        print("\n" + "="*60)
        print(" ADVANCED CUSTOM WORDLIST GENERATOR")
        print("="*60)
        
        data = {}
        
        # Basic information
        data['first_name'] = input("First name: ").strip().lower()
        data['last_name'] = input("Last name: ").strip().lower()
        data['nickname'] = input("Nickname (optional): ").strip().lower()
        data['maiden_name'] = input("Mother's maiden name (optional): ").strip().lower()
        data['pet_name'] = input("Pet name (optional): ").strip().lower()
        data['company'] = input("Company name (optional): ").strip().lower()
        
        # Important dates
        data['birthdate'] = input("Birthdate (DD/MM/YYYY or MM/DD/YYYY): ").strip()
        data['partner_birthdate'] = input("Partner's birthdate (optional): ").strip()
        data['anniversary'] = input("Anniversary date (optional): ").strip()
        
        # Keywords
        keywords = input("Important keywords (comma-separated): ").strip().lower()
        data['keywords'] = [k.strip() for k in keywords.split(',') if k.strip()]
        
        # Special numbers
        data['phone'] = input("Phone number (optional): ").strip()
        data['zipcode'] = input("Zip/Postal code (optional): ").strip()
        
        return {k: v for k, v in data.items() if v}
    
    def parse_date(self, date_str):
        """Extract date components from date string"""
        date_parts = []
        
        # Try different date formats
        formats = ['%d/%m/%Y', '%m/%d/%Y', '%d-%m-%Y', '%m-%d-%Y',
                  '%d/%m/%y', '%m/%d/%y', '%Y', '%m/%Y']
        
        for fmt in formats:
            try:
                dt = datetime.strptime(date_str, fmt)
                date_parts.extend([
                    dt.strftime('%d'),      # Day (01-31)
                    dt.strftime('%m'),      # Month (01-12)
                    dt.strftime('%Y'),      # Year (2023)
                    dt.strftime('%y'),      # Year (23)
                    dt.strftime('%Y%m%d'),  # YYYYMMDD
                    dt.strftime('%d%m%Y'),  # DDMMYYYY
                    dt.strftime('%m%d%Y'),  # MMDDYYYY
                ])
                break
            except ValueError:
                continue
        
        return list(set([p for p in date_parts if p]))
    
    def generate_base_words(self, data):
        """Generate meaningful base combinations"""
        words = []
        
        # Extract components
        first = data.get('first_name', '')
        last = data.get('last_name', '')
        nick = data.get('nickname', '')
        maiden = data.get('maiden_name', '')
        pet = data.get('pet_name', '')
        company = data.get('company', '')
        
        # Basic name combinations
        if first:
            words.append(first)
        if last:
            words.append(last)
        if nick:
            words.append(nick)
        if maiden:
            words.append(maiden)
        if pet:
            words.append(pet)
        if company:
            words.append(company)
        
        # Combined names
        if first and last:
            words.extend([
                first + last,
                last + first,
                first + '.' + last,
                last + '.' + first,
                first + '_' + last,
                last + '_' + first,
                first[0] + last,
                last[0] + first,
                first + last[0],
                last + first[0]
            ])
        
        # Extract and process dates
        date_words = []
        for key in ['birthdate', 'partner_birthdate', 'anniversary']:
            if key in data:
                date_words.extend(self.parse_date(data[key]))
        
        words.extend(date_words)
        
        # Add keywords
        words.extend(data.get('keywords', []))
        
        # Add special numbers
        for key in ['phone', 'zipcode']:
            if key in data:
                words.append(data[key])
        
        # Generate initial patterns
        base_words = list(set(words))
        
        # Generate variations with dates appended
        patterns = []
        for word in base_words:
            patterns.append(word)
            # Append date variations
            for date in date_words:
                patterns.append(word + date)
                patterns.append(date + word)
                patterns.append(word + '_' + date)
                patterns.append(date + '_' + word)
        
        return list(set(patterns))
    
    def apply_leet_speak(self, word):
        """Apply leet speak transformations to a word"""
        leet_variations = [word]
        
        # Basic leet replacements
        leet_word = word
        for char, replacements in self.leet_replacements.items():
            if char in leet_word:
                for replacement in replacements:
                    leet_variations.append(leet_word.replace(char, replacement))
        
        # Mixed case variations
        if len(word) <= 8:  # Limit for performance
            leet_variations.append(word.title())
            leet_variations.append(word.upper())
        
        # Partial leet replacements
        if len(word) > 3:
            # Replace first vowel with leet
            for i, char in enumerate(word):
                if char in self.leet_replacements:
                    for replacement in self.leet_replacements[char]:
                        new_word = word[:i] + replacement + word[i+1:]
                        leet_variations.append(new_word)
                    break
        
        return list(set(leet_variations))
    
    def add_number_patterns(self, word, max_numbers=4):
        """Add number patterns to words"""
        patterns = [word]
        
        # Common number patterns
        common_numbers = [
            '', '1', '12', '123', '1234',
            '0', '00', '000', '0000',
            '01', '007', '100', '200', '500',
            '69', '420', '666', '777', '888', '999',
            '2023', '2024', '2025'
        ]
        
        # Add numbers at end
        for num in common_numbers:
            if num:  # Skip empty string as it's already in patterns
                patterns.append(word + num)
                patterns.append(word + '_' + num)
        
        # Add numbers at beginning
        for num in common_numbers:
            if num:
                patterns.append(num + word)
                patterns.append(num + '_' + word)
        
        # Add birth year patterns if available
        if hasattr(self, 'birth_year'):
            year = self.birth_year
            patterns.append(word + year)
            patterns.append(year + word)
            patterns.append(word + year[2:])  # Last 2 digits
        
        return list(set(patterns))
    
    def add_special_chars(self, word):
        """Add special character variations"""
        patterns = [word]
        
        special_chars = ['!', '@', '#', '$', '%', '&', '*', '-', '_', '.']
        
        # Add special chars at end
        for char in special_chars:
            patterns.append(word + char)
        
        # Add special chars at beginning
        for char in special_chars:
            patterns.append(char + word)
        
        # Wrap with special chars
        for char in special_chars:
            patterns.append(char + word + char)
        
        # Replace spaces/underscores with special chars
        for char in special_chars:
            patterns.append(word.replace('_', char))
            patterns.append(word.replace(' ', char))
        
        return list(set(patterns))
    
    def generate_advanced_combinations(self, base_words, 
                                      use_leet=False, 
                                      use_numbers=False, 
                                      use_special_chars=False,
                                      max_length=32,
                                      min_length=4):
        """Generate advanced combinations with optional transformations"""
        all_combinations = set()
        
        for word in base_words:
            # Skip if too short or too long
            if len(word) < min_length or len(word) > max_length:
                continue
            
            current_variations = [word]
            
            # Apply leet speak
            if use_leet:
                leet_vars = []
                for w in current_variations:
                    leet_vars.extend(self.apply_leet_speak(w))
                current_variations = leet_vars
            
            # Apply number patterns
            if use_numbers:
                num_vars = []
                for w in current_variations:
                    num_vars.extend(self.add_number_patterns(w))
                current_variations = num_vars
            
            # Apply special characters
            if use_special_chars:
                special_vars = []
                for w in current_variations:
                    special_vars.extend(self.add_special_chars(w))
                current_variations = special_vars
            
            # Add to final set
            all_combinations.update(current_variations)
        
        return sorted(list(all_combinations))
    
    def save_wordlist(self, wordlist, filename):
        """Save wordlist to file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                for word in wordlist:
                    f.write(word + '\n')
            return True
        except Exception as e:
            print(f"Error saving wordlist: {e}")
            return False

def main():
    parser = argparse.ArgumentParser(
        description='Advanced Custom Wordlist Generator',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --interactive
  %(prog)s --first john --last doe --birthdate 15/06/1990 --leet --numbers
  %(prog)s -f john -l doe -b 15/06/1990 -k password,secret -o my_wordlist.txt
        """
    )
    
    # Input methods
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-i', '--interactive', action='store_true',
                      help='Interactive mode')
    group.add_argument('--auto', action='store_true',
                      help='Automatic mode with command line arguments')
    
    # Personal information
    parser.add_argument('-f', '--first', help='First name')
    parser.add_argument('-l', '--last', help='Last name')
    parser.add_argument('-n', '--nick', help='Nickname')
    parser.add_argument('-m', '--maiden', help="Mother's maiden name")
    parser.add_argument('-p', '--pet', help='Pet name')
    parser.add_argument('-c', '--company', help='Company name')
    parser.add_argument('-b', '--birthdate', help='Birthdate (DD/MM/YYYY)')
    parser.add_argument('-k', '--keywords', help='Comma-separated keywords')
    
    # Generation options
    parser.add_argument('--leet', action='store_true',
                       help='Enable leet speak transformations')
    parser.add_argument('--numbers', action='store_true',
                       help='Add number patterns')
    parser.add_argument('--special', action='store_true',
                       help='Add special characters')
    parser.add_argument('--max-length', type=int, default=32,
                       help='Maximum password length (default: 32)')
    parser.add_argument('--min-length', type=int, default=4,
                       help='Minimum password length (default: 4)')
    
    # Output options
    parser.add_argument('-o', '--output', default='custom_wordlist.txt',
                       help='Output filename (default: custom_wordlist.txt)')
    parser.add_argument('--show', action='store_true',
                       help='Show generated words on screen')
    
    args = parser.parse_args()
    
    # Initialize generator
    generator = WordlistGenerator()
    
    # Collect data
    if args.interactive:
        data = generator.get_user_input()
    else:
        data = {}
        if args.first:
            data['first_name'] = args.first.lower()
        if args.last:
            data['last_name'] = args.last.lower()
        if args.nick:
            data['nickname'] = args.nick.lower()
        if args.maiden:
            data['maiden_name'] = args.maiden.lower()
        if args.pet:
            data['pet_name'] = args.pet.lower()
        if args.company:
            data['company'] = args.company.lower()
        if args.birthdate:
            data['birthdate'] = args.birthdate
        if args.keywords:
            data['keywords'] = [k.strip().lower() for k in args.keywords.split(',')]
    
    if not data:
        print("Error: No data provided!")
        sys.exit(1)
    
    # Generate base words
    print("\n[*] Generating base words...")
    base_words = generator.generate_base_words(data)
    print(f"[+] Generated {len(base_words)} base words")
    
    # Generate advanced combinations
    print("[*] Creating advanced combinations...")
    wordlist = generator.generate_advanced_combinations(
        base_words,
        use_leet=args.leet,
        use_numbers=args.numbers,
        use_special_chars=args.special,
        max_length=args.max_length,
        min_length=args.min_length
    )
    
    # Remove duplicates and sort
    wordlist = sorted(list(set(wordlist)))
    
    # Show statistics
    print(f"\n[+] Generation complete!")
    print(f"[+] Total unique words: {len(wordlist):,}")
    
    # Show sample if requested
    if args.show and wordlist:
        print("\n[*] Sample of generated words:")
        for i, word in enumerate(wordlist[:20]):
            print(f"  {i+1:2}. {word}")
        if len(wordlist) > 20:
            print(f"  ... and {len(wordlist)-20:,} more")
    
    # Save wordlist
    print(f"\n[*] Saving to '{args.output}'...")
    if generator.save_wordlist(wordlist, args.output):
        print(f"[+] Wordlist saved successfully!")
        print(f"[+] File size: {os.path.getsize(args.output):,} bytes")
    else:
        print("[-] Failed to save wordlist!")

if __name__ == '__main__':
    main()