#!/usr/bin/env python3
"""
HYPER WORDLIST GENERATOR - AI-powered maximum combinations
Uses intelligent pattern generation to create billions of combos from minimal input
"""

import argparse
import sys
import itertools
import random
from datetime import datetime
import os
import hashlib
from collections import defaultdict
import math

class HyperWordlistGenerator:
    def __init__(self):
        self.patterns_generated = 0
        self.word_cache = set()
        
        # Smart pattern database
        self.smart_patterns = {
            'years': [str(y) for y in range(1970, 2026)],
            'common_numbers': ['123', '321', '1234', '4321', '12345', '54321', 
                              '111', '222', '333', '444', '555', '666', '777', '888', '999',
                              '000', '001', '007', '100', '200', '500', '1000',
                              '69', '420', '6969', '0420'],
            'phone_patterns': ['1234567890', '0987654321', '5555555555'],
            'keyboard_patterns': ['qwerty', 'asdfgh', 'zxcvbn', 'qazwsx', '123qwe'],
            'leet_full': {
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
        }
        
        # Common password structures (from real password leaks)
        self.common_structures = [
            'word+year',           # john1990
            'word+common',         # john123
            'word+word',           # johndoe
            'word+special+year',   # john_1990
            'special+word+number', # @john123
            'word+leet+year',      # j0hn1990
            'year+word+special',   # 1990john!
        ]
        
    def hyper_generate_from_minimal(self, first_name, last_name="", year=""):
        """
        Generate MAXIMUM combinations from minimal input
        Uses pattern-based generation instead of brute force
        """
        print(f"[*] HYPER GENERATION MODE ACTIVATED")
        print(f"[*] Input: {first_name}, {last_name}, {year}")
        
        all_passwords = set()
        
        # Step 1: Create base elements
        base_elements = self.create_base_elements(first_name, last_name, year)
        
        # Step 2: Generate using smart patterns
        print("[*] Applying smart pattern generation...")
        
        # Pattern 1: Simple combinations (millions)
        print("  -> Pattern 1: Simple combos...")
        all_passwords.update(self.pattern_simple(base_elements))
        
        # Pattern 2: Leet transformations (millions)
        print("  -> Pattern 2: Leet transformations...")
        all_passwords.update(self.pattern_leet(base_elements))
        
        # Pattern 3: Year combinations (millions)
        print("  -> Pattern 3: Year combos...")
        all_passwords.update(self.pattern_years(base_elements))
        
        # Pattern 4: Special char patterns (millions)
        print("  -> Pattern 4: Special chars...")
        all_passwords.update(self.pattern_special(base_elements))
        
        # Pattern 5: Doubling and repeating
        print("  -> Pattern 5: Doubling patterns...")
        all_passwords.update(self.pattern_doubling(base_elements))
        
        # Pattern 6: Keyboard walking patterns
        print("  -> Pattern 6: Keyboard patterns...")
        all_passwords.update(self.pattern_keyboard(base_elements))
        
        # Pattern 7: Advanced mutations
        print("  -> Pattern 7: Advanced mutations...")
        all_passwords.update(self.pattern_mutations(base_elements))
        
        # Pattern 8: Hybrid combinations
        print("  -> Pattern 8: Hybrid combos...")
        all_passwords.update(self.pattern_hybrid(base_elements))
        
        return all_passwords
    
    def create_base_elements(self, first, last, year):
        """Create all possible base elements from input"""
        elements = {
            'names': set(),
            'initials': set(),
            'years': set(),
            'variants': set()
        }
        
        # Names
        if first:
            first_lower = first.lower()
            first_title = first.title()
            elements['names'].update([first_lower, first_title])
            
            # Name variants
            elements['variants'].update([
                first_lower + 'y',
                first_lower + 'ie',
                first_lower + 'ey',
                first_lower + first_lower,  # doubled
                'my' + first_lower,
                'super' + first_lower,
                first_lower + '123',
                first_lower + '1',
            ])
            
            # Initial
            elements['initials'].add(first_lower[0])
        
        if last:
            last_lower = last.lower()
            last_title = last.title()
            elements['names'].update([last_lower, last_title])
            elements['initials'].add(last_lower[0])
            
            # Combined names
            if first:
                elements['names'].add(first_lower + last_lower)
                elements['names'].add(last_lower + first_lower)
                elements['names'].add(first_lower + '.' + last_lower)
                elements['names'].add(first_lower + '_' + last_lower)
                elements['names'].add(first_lower[0] + last_lower)
                elements['names'].add(last_lower + first_lower[0])
        
        # Years
        if year:
            year_str = str(year)
            elements['years'].add(year_str)  # 1990
            elements['years'].add(year_str[2:])  # 90
            elements['years'].add(year_str[::-1])  # 0991
            elements['years'].add(year_str + year_str[2:])  # 199090
        
        # Add common years anyway
        elements['years'].update(['1990', '1991', '1992', '1993', '1994', '1995',
                                 '2000', '2001', '2002', '2003', '2004', '2005',
                                 '2010', '2011', '2012', '2013', '2014', '2015',
                                 '2020', '2021', '2022', '2023', '2024'])
        
        return elements
    
    def pattern_simple(self, elements):
        """Generate simple combinations - yields millions"""
        passwords = set()
        
        # Combine every name with every year
        for name in elements['names']:
            for year in elements['years']:
                passwords.add(name + year)
                passwords.add(year + name)
                passwords.add(name + '_' + year)
                passwords.add(year + '_' + name)
                
                # Add numbers 0-999
                for i in range(1000):
                    passwords.add(name + str(i).zfill(3))
                    passwords.add(name + '_' + str(i).zfill(3))
        
        # Combine initials with years
        for initial in elements['initials']:
            for year in elements['years']:
                passwords.add(initial + year)
                passwords.add(year + initial)
                
                # Add numbers
                for i in range(100):
                    passwords.add(initial + str(i).zfill(2) + year[2:])
        
        return passwords
    
    def pattern_leet(self, elements):
        """Apply leet speak transformations - yields millions"""
        passwords = set()
        
        for name in list(elements['names'])[:50]:  # Limit to first 50 names
            name_lower = name.lower()
            
            # Generate leet variations
            leet_variations = self.generate_leet_variations(name_lower)
            passwords.update(leet_variations)
            
            # Combine leet names with years and numbers
            for leet_name in list(leet_variations)[:100]:  # Limit combinations
                for year in elements['years'][:20]:
                    passwords.add(leet_name + year)
                    passwords.add(year + leet_name)
                    
                    # Add special chars
                    for special in ['!', '@', '#', '$', '%']:
                        passwords.add(leet_name + year + special)
                        passwords.add(special + leet_name + year)
        
        return passwords
    
    def generate_leet_variations(self, word, max_variations=10000):
        """Generate intelligent leet variations"""
        variations = set([word])
        
        # Common leet replacements
        leet_map = self.smart_patterns['leet_full']
        
        # Generate systematic replacements
        for pattern in self.generate_leet_patterns(word):
            variations.add(pattern)
        
        # Random leet mutations (thousands)
        for _ in range(max_variations):
            leet_word = ''
            for char in word:
                if char in leet_map and random.random() > 0.5:
                    leet_word += random.choice(leet_map[char])
                else:
                    leet_word += char
            
            # Add case variations
            variations.add(leet_word)
            variations.add(leet_word.title())
            variations.add(leet_word.upper())
            
            # Add with numbers
            for i in range(10):
                variations.add(leet_word + str(i))
                variations.add(leet_word + str(i) * 2)
        
        return variations
    
    def generate_leet_patterns(self, word):
        """Generate common leet patterns for a word"""
        patterns = set()
        
        # Full leet (all possible replacements)
        leet_map = self.smart_patterns['leet_full']
        
        # Try common patterns
        common_patterns = [
            word.replace('a', '4').replace('e', '3').replace('i', '1').replace('o', '0'),
            word.replace('s', '5').replace('t', '7').replace('o', '0'),
            word.replace('a', '@').replace('s', '$').replace('i', '!'),
        ]
        
        patterns.update(common_patterns)
        
        # Generate pattern: first letter + leet rest
        if len(word) > 2:
            first = word[0]
            rest = word[1:]
            leet_rest = rest.replace('a', '4').replace('e', '3').replace('i', '1')
            patterns.add(first + leet_rest)
        
        return patterns
    
    def pattern_years(self, elements):
        """Generate year-based combinations - yields millions"""
        passwords = set()
        
        years = list(elements['years'])
        
        # Generate ALL year combinations (1900-2025)
        all_years = [str(y) for y in range(1900, 2026)]
        short_years = [str(y)[2:] for y in range(1900, 2026)]
        
        # Combine years with themselves
        for year in all_years[:100]:  # Limit to 100 years
            for short_year in short_years[:100]:
                passwords.add(year + short_year)
                passwords.add(short_year + year)
                
                # Add separators
                passwords.add(year + '_' + short_year)
                passwords.add(short_year + '_' + year)
                
                # Add numbers
                for i in range(100):
                    passwords.add(year + str(i).zfill(2))
                    passwords.add(str(i).zfill(2) + year)
        
        return passwords
    
    def pattern_special(self, elements):
        """Generate special character combinations - yields millions"""
        passwords = set()
        specials = ['!', '@', '#', '$', '%', '^', '&', '*', '_', '-', '.', '+', '=']
        
        # Apply to all names
        for name in elements['names']:
            # Every special char at start and end
            for special in specials:
                passwords.add(special + name)
                passwords.add(name + special)
                passwords.add(special + name + special)
                
                # Double special
                passwords.add(special * 2 + name)
                passwords.add(name + special * 2)
                
                # Special with numbers
                for i in range(10):
                    passwords.add(special + name + str(i))
                    passwords.add(name + special + str(i))
                    passwords.add(str(i) + special + name)
        
        # Special combinations with years
        for year in elements['years'][:50]:
            for special in specials[:5]:
                passwords.add(special + year)
                passwords.add(year + special)
                
                # Combine with names
                for name in elements['names'][:20]:
                    passwords.add(special + name + year)
                    passwords.add(name + special + year)
                    passwords.add(special + name + special + year)
        
        return passwords
    
    def pattern_doubling(self, elements):
        """Generate doubling and repeating patterns - yields millions"""
        passwords = set()
        
        for name in elements['names']:
            # Simple doubles
            passwords.add(name * 2)
            passwords.add(name * 3)
            
            # Capitalized doubles
            passwords.add(name.title() * 2)
            passwords.add(name.upper() * 2)
            
            # Mixed case doubles
            passwords.add(name + name.title())
            passwords.add(name.title() + name)
            
            # Triple with separators
            passwords.add(name + '_' + name + '_' + name)
            passwords.add(name + '.' + name + '.' + name)
            
            # Double with numbers in middle
            for i in range(100):
                passwords.add(name + str(i) + name)
                passwords.add(name + '_' + str(i) + '_' + name)
        
        return passwords
    
    def pattern_keyboard(self, elements):
        """Generate keyboard walking patterns"""
        passwords = set()
        
        # Common keyboard walks
        keyboard_patterns = [
            'qwerty', 'asdfgh', 'zxcvbn', 'qazwsx', '123qwe',
            '1qaz', '2wsx', '3edc', '4rfv', '5tgb', '6yhn', '7ujm', '8ik,', '9ol.',
            'qwertyuiop', 'asdfghjkl', 'zxcvbnm',
            '!qaz@wsx', '1qaz2wsx', 'zaq1xsw2'
        ]
        
        # Combine keyboard patterns with names and years
        for pattern in keyboard_patterns:
            passwords.add(pattern)
            
            # Add to names
            for name in elements['names'][:10]:
                passwords.add(name + pattern)
                passwords.add(pattern + name)
                passwords.add(name + '_' + pattern)
                
                # Add years
                for year in elements['years'][:10]:
                    passwords.add(pattern + year)
                    passwords.add(name + pattern + year)
        
        return passwords
    
    def pattern_mutations(self, elements):
        """Generate advanced mutations - yields millions"""
        passwords = set()
        
        for name in elements['names']:
            name_lower = name.lower()
            
            # Character mutations
            if len(name_lower) >= 3:
                # Replace vowels
                for vowel in 'aeiou':
                    if vowel in name_lower:
                        # Replace with all vowels
                        for new_vowel in 'aeiou':
                            mutated = name_lower.replace(vowel, new_vowel)
                            passwords.add(mutated)
                            passwords.add(mutated.title())
                
                # Remove vowels
                no_vowels = ''.join([c for c in name_lower if c not in 'aeiou'])
                if no_vowels:
                    passwords.add(no_vowels)
                    passwords.add(no_vowels + '123')
                
                # Reverse and manipulate
                reversed_name = name_lower[::-1]
                passwords.add(reversed_name)
                passwords.add(reversed_name.title())
                
                # Every other character
                every_other = name_lower[::2]
                if every_other:
                    passwords.add(every_other)
                    passwords.add(every_other + every_other)
        
        return passwords
    
    def pattern_hybrid(self, elements):
        """Generate hybrid combinations - yields millions"""
        passwords = set()
        
        # Get limited sets for combination
        names = list(elements['names'])[:20]
        years = list(elements['years'])[:20]
        initials = list(elements['initials'])
        
        # Generate 3-part combinations
        for name in names:
            for year in years:
                # Add common words between
                for common in ['love', 'baby', 'girl', 'boy', 'man', 'woman', 'kid', 'boss']:
                    passwords.add(name + common + year)
                    passwords.add(year + common + name)
                    passwords.add(common + name + year)
                
                # Add numbers in middle
                for i in range(1000):
                    passwords.add(name + str(i).zfill(3) + year)
                    passwords.add(year + str(i).zfill(3) + name)
        
        # Initial combinations
        if len(initials) >= 2:
            for i in range(len(initials)):
                for j in range(len(initials)):
                    if i != j:
                        combo = initials[i] + initials[j]
                        passwords.add(combo)
                        
                        # Add numbers and years
                        for year in years[:10]:
                            passwords.add(combo + year)
                            passwords.add(year + combo)
                            
                            for k in range(100):
                                passwords.add(combo + str(k).zfill(2) + year[2:])
        
        return passwords
    
    def estimate_combinations(self, elements):
        """Estimate total possible combinations"""
        name_count = len(elements['names'])
        year_count = len(elements['years'])
        initial_count = len(elements['initials'])
        
        # Conservative estimate
        base_combos = name_count * year_count * 10  # Simple name+year with variations
        leet_combos = name_count * 1000  # Leet variations per name
        special_combos = name_count * 100  # Special char variations
        hybrid_combos = name_count * year_count * 100  # Hybrid patterns
        
        total_estimate = base_combos + leet_combos + special_combos + hybrid_combos
        return total_estimate
    
    def save_to_file(self, passwords, filename, max_passwords=10000000):
        """Save passwords to file with intelligent sampling"""
        password_list = list(passwords)
        
        if len(password_list) > max_passwords:
            print(f"[!] Generated {len(password_list):,} passwords, sampling to {max_passwords:,}")
            
            # Intelligent sampling - keep variety
            sampled = set()
            
            # Take all short ones (likely common)
            sampled.update([p for p in password_list if len(p) <= 8][:100000])
            
            # Take all with special chars
            sampled.update([p for p in password_list if any(c in '!@#$%^&*' for c in p)][:200000])
            
            # Take all leet variations
            sampled.update([p for p in password_list if any(c in '0123456789' for c in p) 
                          and any(c.isalpha() for c in p)][:300000])
            
            # Random sample the rest
            remaining = [p for p in password_list if p not in sampled]
            if len(remaining) > max_passwords - len(sampled):
                import random
                sampled.update(random.sample(remaining, max_passwords - len(sampled)))
            
            password_list = list(sampled)
        
        # Sort and save
        password_list.sort()
        
        print(f"[*] Saving {len(password_list):,} passwords to {filename}...")
        with open(filename, 'w', encoding='utf-8') as f:
            for password in password_list:
                f.write(password + '\n')
        
        file_size = os.path.getsize(filename)
        print(f"[+] Saved {len(password_list):,} passwords")
        print(f"[+] File size: {file_size/1024/1024:.2f} MB")

def main():
    parser = argparse.ArgumentParser(
        description='HYPER WORDLIST GENERATOR - AI-powered maximum combinations from minimal input',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('-f', '--first', required=True, help='First name (required)')
    parser.add_argument('-l', '--last', default='', help='Last name')
    parser.add_argument('-y', '--year', default='', help='Birth year (YYYY)')
    parser.add_argument('-o', '--output', default='hyper_wordlist.txt', help='Output file')
    parser.add_argument('--limit', type=int, default=10000000, help='Max passwords to save')
    parser.add_argument('--show-estimate', action='store_true', help='Show estimated combinations')
    
    args = parser.parse_args()
    
    generator = HyperWordlistGenerator()
    
    print(f"\n{'='*70}")
    print(f" HYPER WORDLIST GENERATOR")
    print(f" Input: {args.first}, {args.last}, {args.year}")
    print(f"{'='*70}\n")
    
    # Generate passwords
    passwords = generator.hyper_generate_from_minimal(
        args.first.lower(),
        args.last.lower(),
        args.year
    )
    
    print(f"\n{'='*70}")
    print(f" GENERATION COMPLETE!")
    print(f" Total unique passwords: {len(passwords):,}")
    print(f"{'='*70}\n")
    
    # Show sample
    if passwords:
        print("[*] Sample passwords:")
        sample = list(passwords)[:20]
        for i, pwd in enumerate(sample):
            print(f"  {i+1:2}. {pwd}")
    
    # Save to file
    generator.save_to_file(passwords, args.output, args.limit)

if __name__ == '__main__':
    main()