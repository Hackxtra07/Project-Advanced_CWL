#!/usr/bin/env python3
"""
SMART HUMAN PASSWORD GENERATOR
Generates realistic password patterns that humans would actually create
"""

import argparse
import sys
from datetime import datetime
import os
import re
import itertools
import random
from typing import Set, Dict, List, Tuple
from collections import defaultdict

class SmartHumanPasswordGenerator:
    def __init__(self):
        # Common human password patterns - these are patterns REAL people use
        self.human_patterns = [
            # Name patterns
            "{first}{last}",
            "{last}{first}",
            "{first}{last}{year}",
            "{last}{first}{year}",
            "{first}{last_initial}{year}",
            "{first_initial}{last}{year}",
            
            # Name with partial dates
            "{first}{last}{day}{month}",
            "{first}{last}{month}{year}",
            "{first}{last}{year_short}",
            "{first}{year}",
            "{last}{year}",
            
            # Nickname patterns
            "{nick}{year}",
            "{nick}{birth_day}",
            "{nick}{birth_month}",
            "{nick}{birth_day}{birth_month}",
            
            # Reversed patterns
            "{last}{first}{year_short}",
            "{year}{first}{last}",
            
            # With special characters
            "{first}.{last}{year_short}",
            "{first}_{last}{year}",
            "{first}{special}{last}{year}",
            "{first}{last}{special}{year}",
            
            # Common number patterns humans use
            "{first}{last}123",
            "{first}{last}1234",
            "{first}{last}12345",
            "{first}{last}!",
            "{first}{last}!!",
            "{first}{last}?",
            
            # Family combinations
            "{first}{spouse_initial}{year}",
            "{child_name}{year}",
            "{pet_name}{year}",
            
            # Simple patterns
            "{first}{birth_day}",
            "{last}{birth_month}",
            "{first_initial}{last_initial}{year}",
            
            # Mixed patterns
            "{first}{year}{last}",
            "{year}{first}{year_short}",
        ]
        
        # Common special characters humans actually use
        self.common_specials = ['!', '@', '#', '$', '%', '&', '*', '_', '.', '-']
        
        # Common number patterns (not random - what people actually use)
        self.common_numbers = [
            '123', '1234', '12345', '123456',
            '321', '4321', '54321',
            '111', '222', '333', '444', '555',
            '666', '777', '888', '999',
            '007', '100', '200', '300',
            '69', '420', '777', '888',
            '01', '02', '03', '04', '05',
            '10', '20', '30', '40', '50',
            '99', '88', '77', '66',
            '1111', '2222', '3333', '4444',
            '0000', '11111', '22222'
        ]
        
        # Common years (people use these more than random years)
        self.common_years = [
            '2024', '2023', '2022', '2021', '2020',
            '2019', '2018', '2017', '2016', '2015',
            '2010', '2005', '2000', '1995', '1990',
            '1985', '1980', '1975', '1970',
            '24', '23', '22', '21', '20',
            '19', '18', '17', '16', '15'
        ]
        
        # Simple leet substitutions that people actually use
        self.leet_map = {
            'a': ['4', '@'],
            'e': ['3'],
            'i': ['1', '!'],
            'o': ['0'],
            's': ['5', '$'],
            't': ['7']
        }
        
    def parse_human_date(self, date_str: str) -> Dict:
        """Parse date in human formats"""
        date_info = {}
        
        if not date_str:
            return date_info
        
        # Remove any separators
        clean_date = re.sub(r'[^\d]', '', date_str)
        
        # Try to parse based on length
        if len(clean_date) == 8:  # DDMMYYYY
            date_info['day'] = clean_date[0:2]
            date_info['month'] = clean_date[2:4]
            date_info['year'] = clean_date[4:8]
            date_info['year_short'] = clean_date[6:8]
        elif len(clean_date) == 6:  # DDMMYY
            date_info['day'] = clean_date[0:2]
            date_info['month'] = clean_date[2:4]
            date_info['year'] = '20' + clean_date[4:6]
            date_info['year_short'] = clean_date[4:6]
        elif len(clean_date) == 4:  # DDMM or MMDD
            date_info['day'] = clean_date[0:2]
            date_info['month'] = clean_date[2:4]
        
        # Also add cleaned date itself
        date_info['full'] = clean_date
        
        return date_info
    
    def generate_smart_combinations(self, data: Dict) -> Set[str]:
        """Generate smart, human-like combinations"""
        passwords = set()
        
        # Extract base information
        first_name = data.get('first_name', '').lower()
        last_name = data.get('last_name', '').lower()
        nickname = data.get('nickname', '').lower()
        birth_date = data.get('birth_date', '')
        
        # Parse date
        date_info = self.parse_human_date(birth_date)
        
        # Prepare variables for pattern generation
        vars_dict = {
            'first': first_name,
            'first_initial': first_name[0] if first_name else '',
            'last': last_name,
            'last_initial': last_name[0] if last_name else '',
            'nick': nickname,
            'year': date_info.get('year', ''),
            'year_short': date_info.get('year_short', ''),
            'birth_day': date_info.get('day', ''),
            'birth_month': date_info.get('month', ''),
            'day': date_info.get('day', ''),
            'month': date_info.get('month', ''),
            'special': random.choice(self.common_specials) if data.get('use_specials') else '',
        }
        
        # Add family info if available
        if 'spouse_name' in data:
            spouse = data['spouse_name'].lower()
            vars_dict['spouse_initial'] = spouse[0] if spouse else ''
        
        if 'child_name' in data:
            vars_dict['child_name'] = data['child_name'].lower()
        
        if 'pet_name' in data:
            vars_dict['pet_name'] = data['pet_name'].lower()
        
        # Generate base patterns
        print("\n[*] Generating smart human patterns...")
        
        # Apply each pattern template
        for pattern in self.human_patterns:
            try:
                password = pattern.format(**vars_dict)
                if 6 <= len(password) <= 20:  # Reasonable length
                    passwords.add(password)
                    
                    # Add capitalized versions
                    passwords.add(password.title())
                    passwords.add(password.capitalize())
                    
                    # Add with common numbers
                    if data.get('add_numbers', True):
                        for num in self.common_numbers[:10]:  # First 10 common numbers
                            # Add number at end
                            passwords.add(password + num)
                            # Add number in middle (for some patterns)
                            if '_' in password or '.' in password:
                                parts = re.split(r'[._]', password)
                                if len(parts) > 1:
                                    passwords.add(parts[0] + num + parts[1])
            except KeyError:
                continue
        
        # Generate specific combinations you mentioned
        self.generate_specific_examples(passwords, first_name, last_name, date_info, data)
        
        # Add number variations
        if data.get('add_numbers', True):
            passwords.update(self.add_number_variations(passwords, date_info))
        
        # Add special character variations
        if data.get('use_specials', False):
            passwords.update(self.add_special_variations(passwords, data.get('specials', self.common_specials)))
        
        # Add leet variations
        if data.get('use_leet', False):
            passwords.update(self.add_leet_variations(passwords))
        
        # Add common password patterns
        passwords.update(self.generate_common_passwords(first_name, last_name, date_info))
        
        return passwords
    
    def generate_specific_examples(self, passwords: Set[str], first_name: str, last_name: str, 
                                  date_info: Dict, data: Dict):
        """Generate the specific examples you mentioned"""
        
        if not first_name or not last_name:
            return
        
        day = date_info.get('day', '')
        month = date_info.get('month', '')
        year = date_info.get('year', '')
        year_short = date_info.get('year_short', '')
        
        # Example 1: firstlast + date parts
        passwords.add(f"{first_name}{last_name}{day}{month}{year_short}")
        passwords.add(f"{first_name}{last_name}{year}")
        passwords.add(f"{first_name}{last_name}{day}")
        passwords.add(f"{first_name}{last_name}{month}")
        passwords.add(f"{first_name}{last_name}{year_short}")
        
        # Example 2: lastfirst + date parts
        passwords.add(f"{last_name}{first_name}{day}{month}{year}")
        passwords.add(f"{last_name}{first_name}{year}")
        passwords.add(f"{last_name}{first_name}{day}{month}")
        
        # Example 3: first + last repeated
        passwords.add(f"{first_name}{last_name}{last_name}{year}")
        passwords.add(f"{first_name}{first_name}{last_name}{year}")
        
        # Example 4: With separators
        passwords.add(f"{first_name}.{last_name}{year_short}")
        passwords.add(f"{first_name}_{last_name}{year}")
        passwords.add(f"{first_name}{last_name}@{year_short}")
        
        # Example 5: Mixed patterns
        passwords.add(f"{first_name}{year}{last_name}")
        passwords.add(f"{year_short}{first_name}{last_name}")
        passwords.add(f"{first_name}{last_name[0]}{year}")
        
        # Example 6: Simple combinations
        passwords.add(f"{first_name}{last_name}")
        passwords.add(f"{last_name}{first_name}")
        passwords.add(f"{first_name[0]}{last_name}")
        passwords.add(f"{first_name}{last_name[0]}")
        
        # Example 7: With common endings
        passwords.add(f"{first_name}{last_name}123")
        passwords.add(f"{first_name}{last_name}!23")
        passwords.add(f"{first_name}{last_name}@123")
        
    def add_number_variations(self, passwords: Set[str], date_info: Dict) -> Set[str]:
        """Add intelligent number variations"""
        new_passwords = set()
        
        day = date_info.get('day', '')
        month = date_info.get('month', '')
        year = date_info.get('year', '')
        year_short = date_info.get('year_short', '')
        
        # Date combinations people commonly use
        date_combinations = []
        if day and month:
            date_combinations.append(f"{day}{month}")
            date_combinations.append(f"{month}{day}")
        
        if day and month and year_short:
            date_combinations.append(f"{day}{month}{year_short}")
            date_combinations.append(f"{month}{day}{year_short}")
        
        if year:
            date_combinations.append(year)
        
        if year_short:
            date_combinations.append(year_short)
        
        # Add date combinations to existing passwords
        for pwd in list(passwords)[:100]:  # Limit to avoid explosion
            for date_combo in date_combinations[:3]:  # First 3 date combos
                # Add date at end
                new_passwords.add(pwd + date_combo)
                # Add date at beginning
                new_passwords.add(date_combo + pwd)
                
                # If password already has some numbers, replace them
                if any(char.isdigit() for char in pwd):
                    # Try to replace the last numbers with date
                    num_match = re.search(r'\d+$', pwd)
                    if num_match:
                        new_pwd = pwd[:num_match.start()] + date_combo
                        new_passwords.add(new_pwd)
        
        # Add common number patterns
        for pwd in list(passwords)[:50]:
            for num in self.common_numbers[:5]:
                new_passwords.add(pwd + num)
                
                # Insert number in the middle for passwords with separators
                if len(pwd) > 5 and ('_' in pwd or '.' in pwd or '-' in pwd):
                    parts = re.split(r'[._-]', pwd)
                    if len(parts) == 2:
                        new_passwords.add(parts[0] + num + parts[1])
        
        return new_passwords
    
    def add_special_variations(self, passwords: Set[str], specials: List[str]) -> Set[str]:
        """Add special characters in human-like ways"""
        new_passwords = set()
        
        for pwd in list(passwords)[:200]:  # Limit
            new_passwords.add(pwd)  # Keep original
            
            for special in specials[:3]:  # Most common specials
                # Add at end
                new_passwords.add(pwd + special)
                
                # Add at beginning
                new_passwords.add(special + pwd)
                
                # Add at both ends
                new_passwords.add(special + pwd + special)
                
                # Replace spaces/separators with specials
                if ' ' in pwd:
                    new_passwords.add(pwd.replace(' ', special))
                
                # Insert in the middle for longer passwords
                if len(pwd) > 8:
                    mid = len(pwd) // 2
                    new_passwords.add(pwd[:mid] + special + pwd[mid:])
        
        return new_passwords
    
    def add_leet_variations(self, passwords: Set[str]) -> Set[str]:
        """Add leet speak variations (only common ones)"""
        new_passwords = set()
        
        for pwd in list(passwords)[:100]:  # Limit
            new_passwords.add(pwd)  # Keep original
            
            # Only apply leet to some passwords (30% chance)
            if random.random() < 0.3:
                leet_pwd = pwd
                
                # Apply common leet substitutions
                for char, subs in self.leet_map.items():
                    if char in leet_pwd.lower():
                        # Replace only one occurrence (not all)
                        if random.random() < 0.5:
                            leet_pwd = leet_pwd.replace(char, random.choice(subs))
                            leet_pwd = leet_pwd.replace(char.upper(), random.choice(subs))
                
                if leet_pwd != pwd:
                    new_passwords.add(leet_pwd)
        
        return new_passwords
    
    def generate_common_passwords(self, first_name: str, last_name: str, date_info: Dict) -> Set[str]:
        """Generate common password patterns"""
        passwords = set()
        
        if not first_name or not last_name:
            return passwords
        
        # Very common patterns
        passwords.add(f"{first_name}123")
        passwords.add(f"{first_name}1234")
        passwords.add(f"{last_name}123")
        passwords.add(f"{first_name}{last_name[0]}123")
        
        # With special characters
        passwords.add(f"{first_name}!23")
        passwords.add(f"{first_name}@123")
        passwords.add(f"{first_name}#123")
        
        # Year patterns
        year = date_info.get('year', '')
        year_short = date_info.get('year_short', '')
        
        if year:
            passwords.add(f"{first_name}{year}")
            passwords.add(f"{last_name}{year}")
            passwords.add(f"{first_name}{last_name[0]}{year_short}")
        
        # Simple combinations
        passwords.add(first_name.lower())
        passwords.add(first_name.title())
        passwords.add(last_name.lower())
        passwords.add(last_name.title())
        
        return passwords
    
    def analyze_and_filter(self, passwords: Set[str], min_len: int = 6, max_len: int = 20) -> Set[str]:
        """Analyze and filter passwords"""
        filtered = set()
        
        print("\n[*] Analyzing and filtering passwords...")
        
        # Count patterns
        pattern_stats = defaultdict(int)
        
        for pwd in passwords:
            # Length check
            if not (min_len <= len(pwd) <= max_len):
                continue
            
            # Remove unrealistic patterns
            # Too many consecutive specials
            if re.search(r'[!@#$%^&*]{3,}', pwd):
                continue
            
            # Too many consecutive numbers
            if re.search(r'\d{6,}', pwd):
                continue
            
            # Must have at least one letter
            if not re.search(r'[a-zA-Z]', pwd):
                continue
            
            # Categorize pattern
            if pwd.islower():
                pattern_stats['all_lowercase'] += 1
            elif pwd.isupper():
                pattern_stats['all_uppercase'] += 1
            elif pwd[0].isupper():
                pattern_stats['first_capital'] += 1
            elif pwd.title() == pwd:
                pattern_stats['title_case'] += 1
            
            if any(c in pwd for c in '!@#$%^&*'):
                pattern_stats['has_special'] += 1
            
            if re.search(r'\d', pwd):
                pattern_stats['has_numbers'] += 1
            
            filtered.add(pwd)
        
        # Print statistics
        print(f"\n[+] Pattern Statistics:")
        print(f"    Total generated: {len(passwords)}")
        print(f"    After filtering: {len(filtered)}")
        
        if filtered:
            print(f"\n    Pattern distribution:")
            for pattern, count in sorted(pattern_stats.items()):
                percentage = (count / len(filtered)) * 100
                print(f"      {pattern:20}: {count:6} ({percentage:5.1f}%)")
        
        return filtered
    
    def show_examples(self, passwords: Set[str], count: int = 20):
        """Show example passwords"""
        if not passwords:
            print("\n[-] No passwords generated!")
            return
        
        print(f"\n[*] Example passwords (showing {min(count, len(passwords))}):")
        print("-" * 50)
        
        sample = list(passwords)
        random.shuffle(sample)
        
        for i, pwd in enumerate(sample[:count], 1):
            # Show password with some analysis
            has_special = '✓' if any(c in pwd for c in '!@#$%^&*') else ' '
            has_number = '✓' if any(c.isdigit() for c in pwd) else ' '
            has_upper = '✓' if any(c.isupper() for c in pwd) else ' '
            
            print(f"  {i:2}. {pwd:25} [S:{has_special} N:{has_number} U:{has_upper}]")

def main():
    parser = argparse.ArgumentParser(
        description='SMART HUMAN PASSWORD GENERATOR - Creates realistic password patterns',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive mode
  python smart_generator.py
  
  # Command line with your example
  python smart_generator.py --first manan --last kamboj --birth 07092010
  
  # With options
  python smart_generator.py --first john --last doe --birth 15061990 
         --special --leet --output john_passwords.txt
        """
    )
    
    parser.add_argument('--first', help='First name')
    parser.add_argument('--last', help='Last name')
    parser.add_argument('--birth', help='Birth date (DDMMYYYY or DD/MM/YYYY)')
    parser.add_argument('--nick', help='Nickname')
    
    parser.add_argument('--special', action='store_true', help='Add special characters')
    parser.add_argument('--leet', action='store_true', help='Add leet speak variations')
    parser.add_argument('--numbers', action='store_true', default=True, 
                       help='Add common number patterns')
    
    parser.add_argument('-o', '--output', default='smart_passwords.txt',
                       help='Output filename')
    parser.add_argument('--max', type=int, default=5000,
                       help='Maximum passwords to generate')
    
    args = parser.parse_args()
    
    generator = SmartHumanPasswordGenerator()
    
    print("\n" + "="*60)
    print(" SMART HUMAN PASSWORD GENERATOR")
    print("="*60)
    
    # Get user input
    data = {}
    
    if args.first and args.last and args.birth:
        # Use command line args
        print("\n[*] Using command line parameters...")
        data['first_name'] = args.first.lower()
        data['last_name'] = args.last.lower()
        data['birth_date'] = args.birth
        
        if args.nick:
            data['nickname'] = args.nick.lower()
        
        data['use_specials'] = args.special
        data['use_leet'] = args.leet
        data['add_numbers'] = args.numbers
        data['specials'] = generator.common_specials
        
    else:
        # Interactive mode
        print("\n[*] Please provide your information:")
        
        data['first_name'] = input("First name: ").strip().lower()
        while not data['first_name']:
            print("First name is required!")
            data['first_name'] = input("First name: ").strip().lower()
        
        data['last_name'] = input("Last name: ").strip().lower()
        while not data['last_name']:
            print("Last name is required!")
            data['last_name'] = input("Last name: ").strip().lower()
        
        data['birth_date'] = input("Birth date (DDMMYYYY or DD/MM/YYYY): ").strip()
        
        data['nickname'] = input("Nickname (optional): ").strip().lower()
        
        # Optional family info
        spouse = input("Spouse name (optional): ").strip().lower()
        if spouse:
            data['spouse_name'] = spouse
        
        child = input("Child name (optional): ").strip().lower()
        if child:
            data['child_name'] = child
        
        pet = input("Pet name (optional): ").strip().lower()
        if pet:
            data['pet_name'] = pet
        
        # Options
        special_choice = input("\nAdd special characters? (y/n): ").strip().lower()
        data['use_specials'] = special_choice == 'y'
        
        if data['use_specials']:
            custom = input(f"Use these specials [{''.join(generator.common_specials[:5])}] or custom? (enter for default): ").strip()
            if custom:
                data['specials'] = list(custom)
            else:
                data['specials'] = generator.common_specials[:5]
        
        leet_choice = input("Add leet speak variations? (y/n): ").strip().lower()
        data['use_leet'] = leet_choice == 'y'
        
        num_choice = input("Add common number patterns? (y/n): ").strip().lower()
        data['add_numbers'] = num_choice == 'y'
    
    print(f"\n[*] Generating passwords for: {data['first_name'].title()} {data['last_name'].title()}")
    if data.get('birth_date'):
        print(f"[*] Birth date: {data['birth_date']}")
    
    # Generate passwords
    passwords = generator.generate_smart_combinations(data)
    
    # Filter
    filtered = generator.analyze_and_filter(passwords, min_len=6, max_len=20)
    
    # Limit if specified
    if args.max > 0 and len(filtered) > args.max:
        filtered = set(list(filtered)[:args.max])
        print(f"[*] Limited to {args.max} passwords")
    
    # Show examples
    generator.show_examples(filtered)
    
    # Save to file
    if filtered:
        print(f"\n[*] Saving {len(filtered)} passwords to {args.output}...")
        
        # Sort by length and alphabetically
        sorted_passwords = sorted(filtered, key=lambda x: (len(x), x))
        
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(f"# Smart human passwords generated on {datetime.now().strftime('%Y-%m-%d')}\n")
            f.write(f"# Name: {data['first_name'].title()} {data['last_name'].title()}\n")
            if data.get('birth_date'):
                f.write(f"# Birth date: {data['birth_date']}\n")
            f.write(f"# Total passwords: {len(sorted_passwords)}\n")
            f.write("#" * 50 + "\n\n")
            
            for pwd in sorted_passwords:
                f.write(pwd + '\n')
        
        file_size = os.path.getsize(args.output)
        print(f"[+] Saved successfully!")
        print(f"[+] File size: {file_size:,} bytes")
        
        # Show some interesting stats
        print(f"\n[*] Interesting facts:")
        print(f"    Most common length: {max(set(len(p) for p in filtered), key=list(len(p) for p in filtered).count)} chars")
        
        # Count patterns
        special_count = sum(1 for p in filtered if any(c in p for c in '!@#$%^&*'))
        number_count = sum(1 for p in filtered if any(c.isdigit() for c in p))
        
        print(f"    Passwords with special chars: {special_count} ({special_count/len(filtered)*100:.1f}%)")
        print(f"    Passwords with numbers: {number_count} ({number_count/len(filtered)*100:.1f}%)")
        
    else:
        print("\n[-] No passwords to save!")

if __name__ == '__main__':
    main()