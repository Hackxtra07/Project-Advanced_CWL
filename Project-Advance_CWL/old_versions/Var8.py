#!/usr/bin/env python3
"""
BHARATIYA PASSWORD GENERATOR - Indian-Specific Advanced Password Generator
Tailored for Indian names, dates, festivals, and cultural patterns
"""

import argparse
import sys
from datetime import datetime, date
import os
import re
import itertools
import random
import string
import json
from typing import Set, Dict, List, Tuple, Optional
from collections import defaultdict, Counter
import math

class IndianPasswordGenerator:
    def __init__(self):
        # Indian names database (common first names and surnames)
        self.indian_names = {
            'male_first': [
                'aarav', 'vivaan', 'aditya', 'vihaan', 'arjun', 'sai', 'krishna', 'raman',
                'surya', 'raj', 'kumar', 'ram', 'shiva', 'vishnu', 'ganesh', 'karthik',
                'suresh', 'rakesh', 'mahesh', 'narendra', 'amit', 'rahul', 'rohit',
                'vikram', 'deepak', 'manoj', 'prakash', 'sanjay', 'ajay', 'vijay'
            ],
            'female_first': [
                'saanvi', 'ananya', 'diya', 'aadhya', 'tanya', 'riya', 'priya', 'neha',
                'pooja', 'kavita', 'sunita', 'meera', 'radha', 'sita', 'laxmi', 'saraswati',
                'anjali', 'madhavi', 'shreya', 'tanvi', 'ishita', 'divya', 'nandini',
                'kritika', 'sneha', 'shweta', 'pallavi', 'vaishnavi', 'gauri', 'parvati'
            ],
            'surnames': [
                'sharma', 'verma', 'gupta', 'malhotra', 'kapoor', 'singh', 'kumar', 'patel',
                'reddy', 'rao', 'menon', 'iyer', 'chatterjee', 'banerjee', 'mukherjee',
                'das', 'nair', 'pillai', 'mehta', 'shah', 'jain', 'agarwal', 'goswami',
                'trivedi', 'tiwari', 'mishra', 'choudhary', 'thakur', 'yadav', 'naik'
            ],
            'nicknames': [
                'bittu', 'chintu', 'golu', 'monu', 'sonu', 'pappu', 'kallu', 'bablu',
                'rajju', 'kaku', 'mamu', 'chotu', 'motu', 'guddu', 'bunty', 'babu',
                'pinky', 'sweety', 'guddi', 'chinki', 'munni', 'bubbly', 'chumki'
            ]
        }
        
        # Indian festivals and important dates
        self.indian_festivals = {
            'diwali': ['diwali', 'deepavali', 'dipawali'],
            'holi': ['holi', 'holika', 'rang'],
            'eid': ['eid', 'ramzan', 'ramadan'],
            'christmas': ['christmas', 'xmas', 'bada din'],
            'ganesh_chaturthi': ['ganesh', 'ganpati', 'vinayak'],
            'durga_puja': ['durga', 'puja', 'navratri'],
            'rakhi': ['rakhi', 'raksha', 'bandhan'],
            'onam': ['onam', 'thiruvonam'],
            'pongal': ['pongal', 'sankranti'],
            'baisakhi': ['baisakhi', 'vaisakhi'],
            'guru_nanak_jayanti': ['gurunanak', 'guruparab'],
            'maha_shivaratri': ['shivaratri', 'mahashivratri'],
            'janmashtami': ['janmashtami', 'krishna'],
            'ram_navami': ['ramnavami', 'ram'],
            'vijayadashami': ['vijayadashami', 'dussehra']
        }
        
        # Indian cultural keywords
        self.indian_keywords = [
            'bharat', 'india', 'hindustan', 'desh', 'vande', 'mataram',
            'jai', 'shree', 'om', 'namah', 'shivaya', 'hare', 'rama',
            'krishna', 'bholenath', 'hanuman', 'saraswati', 'lakshmi',
            'swami', 'baba', 'devi', 'amma', 'akka', 'didi', 'bhai',
            'dada', 'chacha', 'mausi', 'nana', 'chachi', 'tau'
        ]
        
        # Indian cities and states (common ones)
        self.indian_places = {
            'cities': [
                'mumbai', 'delhi', 'bangalore', 'hyderabad', 'chennai',
                'kolkata', 'pune', 'ahmedabad', 'jaipur', 'surat',
                'lucknow', 'kanpur', 'nagpur', 'indore', 'thane',
                'bhopal', 'visakhapatnam', 'patna', 'vadodara', 'ghaziabad'
            ],
            'states': [
                'maharashtra', 'delhi', 'karnataka', 'tamilnadu', 'kerala',
                'andhra', 'telangana', 'gujarat', 'rajasthan', 'punjab',
                'haryana', 'uttarpradesh', 'madhya pradesh', 'bihar', 'westbengal',
                'odisha', 'assam', 'jharkhand', 'chhattisgarh', 'uttarakhand'
            ]
        }
        
        # Common Indian number patterns
        self.indian_numbers = {
            'lucky_numbers': ['7', '9', '108', '21', '51', '101', '1008'],
            'vehicle_patterns': ['1234', '0001', '1001', '786', '420', '999', '1111'],
            'phone_patterns': ['123456', '987654', '112233', '223344', '334455'],
            'year_patterns': [str(y) for y in range(1947, 2025)] +  # Independence year onwards
                           ['47', '75', '83', '00', '08', '12', '20', '24'],
            'repeating_patterns': ['11', '22', '33', '44', '55', '66', '77', '88', '99',
                                 '111', '222', '333', '444', '555', '666', '777', '888', '999']
        }
        
        # Indian mobile number patterns
        self.mobile_prefixes = ['98', '99', '97', '96', '95', '94', '93', '92', '91', '90',
                               '89', '88', '87', '86', '85', '84', '83', '82', '81', '80',
                               '79', '78', '77', '76', '75', '74', '73', '72', '71', '70']
        
        # Indian-specific leet speak
        self.indian_leet = {
            'a': ['4', '@', 'å'],
            'b': ['8', '|3', 'ß'],
            'e': ['3', '€', '£'],
            'g': ['6', '9', '&'],
            'i': ['1', '!', '|'],
            'l': ['1', '|', '£'],
            'o': ['0', '()', '°'],
            's': ['5', '$', 'z'],
            't': ['7', '+', '†'],
            'z': ['2', '~/_'],
            # Indian language specific
            'aa': ['4', '@'],
            'ee': ['3'],
            'oo': ['00'],
            'sh': ['5h', '$h'],
            'ch': ['6h', 'ch']
        }
        
        # Common Indian password patterns analysis
        self.common_patterns = [
            # Name + Year
            '{name}{year}',
            '{year}{name}',
            '{name.capitalize()}{year}',
            
            # Name + Mobile
            '{name}{mobile_last4}',
            '{mobile_last4}{name}',
            
            # Name + Special + Number
            '{name}{special}{lucky_number}',
            '{name}{special}{year}',
            
            # Nickname patterns
            '{nickname}{birth_day}',
            '{nickname}{special}{birth_month}',
            
            # Family patterns
            '{son_name}{daughter_name}',
            '{father_name}{special}{year}',
            
            # Festival patterns
            '{festival}{year}',
            'happy{festival}{year}',
            
            # Place patterns
            '{city}{year}',
            '{state_abbr}{mobile_pattern}',
            
            # Cultural patterns
            'jai{keyword}',
            '{keyword}{lucky_number}',
            
            # Vehicle patterns
            '{vehicle_number}',
            'dl{vehicle_last4}',
            
            # Mobile only patterns
            '{mobile_full}',
            '{mobile_last6}',
            
            # Simple patterns
            '{name}123',
            '{name}@{year}',
            '{nickname}!@#',
            
            # Complex patterns
            '{name}{special}{city}{year}',
            '{keyword}{special}{lucky_number}',
            
            # Bollywood inspired
            '{actor}{year}',
            '{actress}{special}',
            
            # Cricket inspired
            '{cricketer}{jersey}',
            'team{keyword}{year}'
        ]
        
        # Bollywood actors/actresses
        self.bollywood = {
            'actors': ['srk', 'salman', 'amitabh', 'akshay', 'hrithik', 'ranveer', 'ranbir',
                      'ajay', 'varun', 'tiger', 'kartik', 'vicky', 'ayushmann', 'rajkumar'],
            'actresses': ['kajol', 'aishwarya', 'priyanka', 'deepika', 'katrina', 'kareena',
                         'anushka', 'alia', 'kiara', 'sara', 'janhvi', 'nora', 'shraddha'],
            'movies': ['dilwale', 'hum', 'dabangg', 'singham', 'krish', 'raees', 'tiger',
                      'war', 'pathaan', 'jawan', 'animal', 'golmaal', 'dhamaal']
        }
        
        # Cricket players
        self.cricket = {
            'players': ['sachin', 'dhoni', 'kohli', 'rohit', 'rahul', 'bumrah', 'hardik',
                       'pandya', 'ashwin', 'jadeja', 'yuvraj', 'sehwag', 'ganguly', 'dravid'],
            'teams': ['india', 'mumbai', 'chennai', 'kolkata', 'bangalore', 'delhi', 'punjab'],
            'terms': ['cricket', 'match', 'win', 'six', 'four', 'century', 'wicket']
        }
        
        # Special characters commonly used in India
        self.indian_specials = ['!', '@', '#', '$', '%', '&', '*', '_', '-', '.', '~']
        
        # Indian vehicle number patterns
        self.vehicle_patterns = [
            # Format: StateCode CityCode Number
            'DL01AB1234', 'MH02CD5678', 'KA03EF9012', 'TN04GH3456',
            'AP05IJ7890', 'UP06KL1234', 'GJ07MN5678', 'RJ08OP9012'
        ]
        
        # Initialize counters
        self.password_counter = 0
        self.max_passwords = 1000000
        
    def get_indian_user_input(self) -> Dict:
        """Get Indian-specific user information"""
        print("\n" + "="*70)
        print(" 🇮🇳 BHARATIYA PASSWORD GENERATOR - Advanced Edition")
        print("="*70)
        print("\n[!] Tailored for Indian names, dates, and cultural patterns\n")
        
        data = {}
        
        # === PERSONAL INFORMATION (Indian Context) ===
        print("--- निजी जानकारी / Personal Information ---")
        
        personal = {}
        
        # Name in Indian format
        print("\n[नाम / Name]")
        personal['first_name'] = input("First Name: ").strip().lower() or random.choice(self.indian_names['male_first'] + self.indian_names['female_first'])
        personal['middle_name'] = input("Middle Name (optional): ").strip().lower() or None
        personal['last_name'] = input("Last Name/Surname: ").strip().lower() or random.choice(self.indian_names['surnames'])
        personal['nickname'] = input("Nickname/Petname: ").strip().lower() or random.choice(self.indian_names['nicknames'])
        
        # Family information (common in Indian passwords)
        print("\n[परिवार / Family]")
        personal['father_name'] = input("Father's Name: ").strip().lower() or None
        personal['mother_name'] = input("Mother's Name: ").strip().lower() or None
        personal['spouse_name'] = input("Spouse Name (if married): ").strip().lower() or None
        personal['child_name'] = input("Child Name(s), comma separated: ").strip().lower() or None
        
        data['personal'] = {k: v for k, v in personal.items() if v}
        
        # === IMPORTANT DATES (Indian Format) ===
        print("\n--- महत्वपूर्ण तारीखें / Important Dates ---")
        
        dates = {}
        
        # Birth dates (DD/MM/YYYY format)
        dates['birth_date'] = input("Your Birth Date (DD/MM/YYYY): ").strip() or None
        dates['anniversary'] = input("Anniversary Date (DD/MM/YYYY): ").strip() or None
        dates['child_birth'] = input("Child Birth Date(s), comma separated: ").strip() or None
        
        # Important Indian dates
        print("\n[भारतीय महत्वपूर्ण तारीखें / Indian Important Dates]")
        dates['independence_day'] = '15/08'  # Always important
        dates['republic_day'] = '26/01'     # Always important
        
        festival_pref = input("Favorite Festival (diwali/holi/eid/christmas/ganesh_chaturthi): ").strip().lower()
        if festival_pref in self.indian_festivals:
            dates['festival'] = festival_pref
        
        data['dates'] = {k: v for k, v in dates.items() if v}
        
        # === CONTACT INFORMATION ===
        print("\n--- संपर्क जानकारी / Contact Information ---")
        
        contacts = {}
        
        # Mobile numbers (very common in Indian passwords)
        mobile = input("Mobile Number (10 digits): ").strip()
        if mobile and len(mobile) >= 10:
            contacts['mobile'] = mobile[-10:]  # Last 10 digits
        else:
            # Generate random Indian mobile number
            contacts['mobile'] = random.choice(self.mobile_prefixes) + ''.join(random.choices('0123456789', k=8))
        
        # Vehicle number
        vehicle = input("Vehicle Number (optional): ").strip().upper()
        if vehicle:
            contacts['vehicle'] = vehicle
        
        # Aadhaar/PAN last digits
        aadhaar_last4 = input("Aadhaar/PAN last 4 digits (optional): ").strip()
        if aadhaar_last4 and len(aadhaar_last4) == 4:
            contacts['aadhaar_last4'] = aadhaar_last4
        
        data['contacts'] = contacts
        
        # === INDIAN KEYWORDS AND INTERESTS ===
        print("\n--- रुचियाँ और कीवर्ड / Interests and Keywords ---")
        
        interests = {}
        
        # Favorite things
        fav_keywords = input("Favorite Indian words/terms (comma separated): ").strip().lower()
        if fav_keywords:
            interests['keywords'] = [k.strip() for k in fav_keywords.split(',')]
        else:
            # Add some common Indian keywords
            interests['keywords'] = random.sample(self.indian_keywords, 3)
        
        # Bollywood interests
        print("\n[बॉलीवुड / Bollywood]")
        fav_actor = input("Favorite Actor: ").strip().lower()
        if fav_actor:
            interests['actor'] = fav_actor
        
        fav_actress = input("Favorite Actress: ").strip().lower()
        if fav_actress:
            interests['actress'] = fav_actress
        
        # Cricket interests
        print("\n[क्रिकेट / Cricket]")
        fav_cricketer = input("Favorite Cricketer: ").strip().lower()
        if fav_cricketer:
            interests['cricketer'] = fav_cricketer
        
        fav_team = input("Favorite IPL Team: ").strip().lower()
        if fav_team:
            interests['team'] = fav_team
        
        data['interests'] = interests
        
        # === PASSWORD GENERATION OPTIONS ===
        print("\n--- पासवर्ड जेनरेशन विकल्प / Password Generation Options ---")
        
        # Generation style
        print("\n[पासवर्ड स्टाइल / Password Style]")
        print("1. सरल / Simple (name + year)")
        print("2. मध्यम / Medium (name + special + number)")
        print("3. उन्नत / Advanced (multiple combinations)")
        print("4. व्यापक / Comprehensive (all patterns)")
        print("5. स्मार्ट / Smart (AI-like prediction)")
        
        style = input("Choose style (1-5): ").strip()
        data['style'] = style if style in ['1', '2', '3', '4', '5'] else '3'
        
        # Advanced features
        print("\n[उन्नत सुविधाएँ / Advanced Features]")
        
        # Language variations
        lang_variations = input("Add Hindi/regional language variations? (y/n): ").strip().lower()
        data['lang_variations'] = lang_variations == 'y'
        
        # Leet speak
        leet_choice = input("Use Indian leet speak (e.g., @ for a)? (y/n): ").strip().lower()
        data['leet_enabled'] = leet_choice == 'y'
        
        if data['leet_enabled']:
            leet_level = input("Leet level (1-3, 3=extreme): ").strip()
            data['leet_level'] = min(max(int(leet_level) if leet_level.isdigit() else 2, 1), 3)
        
        # Special characters
        special_choice = input("Add special characters? (y/n): ").strip().lower()
        data['special_enabled'] = special_choice == 'y'
        
        if data['special_enabled']:
            specials = input(f"Special chars to use (default: {''.join(self.indian_specials[:5])}): ").strip()
            data['specials'] = list(specials) if specials else self.indian_specials[:5]
        
        # Number patterns
        num_choice = input("Add Indian number patterns? (y/n): ").strip().lower()
        data['numbers_enabled'] = num_choice == 'y'
        
        if data['numbers_enabled']:
            print("  Number types: 1=Lucky 2=Year 3=Mobile 4=Repeating 5=All")
            num_types = input("  Choose types (comma separated): ").strip()
            data['number_types'] = [t.strip() for t in num_types.split(',')] if num_types else ['5']
        
        # Length constraints
        print("\n[लंबाई सीमाएँ / Length Constraints]")
        min_len = input("Minimum length (6-32): ").strip()
        data['min_length'] = int(min_len) if min_len.isdigit() and 6 <= int(min_len) <= 32 else 8
        
        max_len = input("Maximum length (12-64): ").strip()
        data['max_length'] = int(max_len) if max_len.isdigit() and 12 <= int(max_len) <= 64 else 16
        
        # Quantity
        max_passwords = input("Maximum passwords to generate (1000-1000000): ").strip()
        data['max_passwords'] = min(int(max_passwords), 1000000) if max_passwords.isdigit() else 50000
        
        return data
    
    def extract_indian_date_components(self, date_str: str) -> Dict[str, List[str]]:
        """Extract components from Indian date formats"""
        components = defaultdict(list)
        
        if not date_str:
            return dict(components)
        
        # Indian date formats (DD/MM/YYYY is most common)
        formats = [
            '%d/%m/%Y', '%d-%m-%Y', '%d.%m.%Y', '%d%m%Y',
            '%d/%m/%y', '%d-%m-%y', '%d.%m.%y', '%d%m%y',
            '%Y/%m/%d', '%Y-%m-%d',  # Some people use international format
        ]
        
        parsed_date = None
        for fmt in formats:
            try:
                parsed_date = datetime.strptime(date_str, fmt)
                break
            except ValueError:
                continue
        
        if parsed_date:
            # Basic components
            day = parsed_date.strftime('%d')
            month = parsed_date.strftime('%m')
            year = parsed_date.strftime('%Y')
            short_year = parsed_date.strftime('%y')
            
            # Day variations
            components['day'].extend([day, day.lstrip('0')])
            
            # Month variations
            components['month'].extend([month, month.lstrip('0')])
            
            # Year variations
            components['year'].extend([year])
            components['short_year'].extend([short_year])
            
            # Common Indian date patterns
            patterns = [
                f"{day}{month}{year}",      # DDMMYYYY
                f"{day}{month}{short_year}", # DDMMYY
                f"{month}{day}{year}",      # MMDDYYYY
                f"{year}{month}{day}",      # YYYYMMDD
                f"{day.lstrip('0')}{month.lstrip('0')}{short_year}", # DMMYY
            ]
            
            components['patterns'].extend(patterns)
            
            # Add month names in Hindi/English
            month_names_eng = ['jan', 'feb', 'mar', 'apr', 'may', 'jun',
                             'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
            month_names_hindi = ['जनवरी', 'फरवरी', 'मार्च', 'अप्रैल', 'मई', 'जून',
                               'जुलाई', 'अगस्त', 'सितंबर', 'अक्टूबर', 'नवंबर', 'दिसंबर']
            
            month_num = int(month)
            if 1 <= month_num <= 12:
                components['month_name_eng'].append(month_names_eng[month_num - 1])
                components['month_name_hindi'].append(month_names_hindi[month_num - 1])
        
        return dict(components)
    
    def generate_indian_mobile_patterns(self, mobile: str) -> List[str]:
        """Generate mobile number patterns common in India"""
        patterns = []
        
        if not mobile or len(mobile) != 10:
            # Generate random patterns
            mobile = random.choice(self.mobile_prefixes) + ''.join(random.choices('0123456789', k=8))
        
        # Common patterns
        patterns.append(mobile)                     # Full number
        patterns.append(mobile[-4:])                # Last 4 digits
        patterns.append(mobile[-6:])                # Last 6 digits
        patterns.append(mobile[:5])                 # First 5 digits
        patterns.append(mobile[5:])                 # Last 5 digits
        
        # Repeating patterns from the number
        for i in range(0, 7, 2):
            pattern = mobile[i:i+4]
            if len(pattern) == 4:
                patterns.append(pattern)
        
        # Common Indian mobile patterns
        patterns.extend([
            '1234567890',
            '9876543210',
            '1122334455',
            '2233445566',
            '9988776655',
            '8877665544',
        ])
        
        return list(set(patterns))
    
    def generate_indian_number_patterns(self, types: List[str]) -> List[str]:
        """Generate Indian-specific number patterns"""
        patterns = set()
        
        if '1' in types or '5' in types:
            patterns.update(self.indian_numbers['lucky_numbers'])
        
        if '2' in types or '5' in types:
            patterns.update(self.indian_numbers['year_patterns'][-20:])  # Recent years
        
        if '3' in types or '5' in types:
            patterns.update(self.indian_numbers['phone_patterns'])
            
            # Generate some mobile-like patterns
            for _ in range(10):
                prefix = random.choice(self.mobile_prefixes)
                patterns.add(prefix + ''.join(random.choices('0123456789', k=8)))
        
        if '4' in types or '5' in types:
            patterns.update(self.indian_numbers['repeating_patterns'])
            patterns.update(self.indian_numbers['vehicle_patterns'])
        
        # Add some random Indian lucky numbers
        indian_lucky = ['7', '9', '21', '51', '108', '1008', '786']
        patterns.update(indian_lucky)
        
        # Add birth year of India
        patterns.add('1947')
        patterns.add('47')
        
        return list(patterns)
    
    def apply_indian_leet(self, word: str, level: int = 2) -> List[str]:
        """Apply Indian-style leet speak"""
        variations = {word}
        
        if level == 1:
            # Basic: only common substitutions
            basic_subs = {'a': '@', 'i': '1', 'o': '0', 's': '5', 'e': '3'}
            for char, sub in basic_subs.items():
                if char in word:
                    variations.add(word.replace(char, sub))
        
        elif level == 2:
            # Moderate: Indian common leet
            for char, subs in self.indian_leet.items():
                if len(char) == 1 and char in word:
                    for sub in subs[:2]:
                        variations.add(word.replace(char, sub))
        
        elif level == 3:
            # Advanced: Multiple substitutions
            char_list = list(word)
            for i, char in enumerate(char_list):
                if char in self.indian_leet:
                    for sub in self.indian_leet[char]:
                        new_word = char_list.copy()
                        new_word[i] = sub
                        variations.add(''.join(new_word))
            
            # Try some common Indian leet words
            common_leet_words = {
                'india': '1nd1@',
                'bharat': '8h@r@7',
                'shiva': '5h1v@',
                'krishna': 'kr15hn@',
                'ganesh': '9@n35h',
                'om': '0m',
                'jai': 'j@1',
                'shree': '5hr33'
            }
            
            if word in common_leet_words:
                variations.add(common_leet_words[word])
        
        return list(variations)
    
    def generate_name_variations(self, name: str) -> List[str]:
        """Generate Indian name variations"""
        variations = set()
        
        if not name:
            return []
        
        # Basic variations
        variations.add(name.lower())
        variations.add(name.title())
        variations.add(name.upper())
        
        # Indian-style variations
        variations.add(name[0].upper() + name[1:].lower())  # First letter capital
        
        # Short forms
        if len(name) > 3:
            variations.add(name[:3])  # First 3 letters
            variations.add(name[:2])  # First 2 letters
        
        # Add 'bhai', 'ji', 'babu' suffixes (common in India)
        suffixes = ['bhai', 'ji', 'babu', 'lal', 'kumar', 'singh']
        for suffix in suffixes:
            variations.add(f"{name}{suffix}")
            variations.add(f"{name.title()}{suffix}")
        
        # Reverse (some people use reversed names)
        if len(name) <= 6:
            variations.add(name[::-1])
        
        return list(variations)
    
    def generate_festival_patterns(self, festival: str) -> List[str]:
        """Generate festival-related passwords"""
        patterns = set()
        
        if festival in self.indian_festivals:
            festival_names = self.indian_festivals[festival]
        else:
            festival_names = [festival]
        
        for fest in festival_names:
            # Basic festival patterns
            patterns.add(fest)
            patterns.add(fest.title())
            patterns.add(fest.upper())
            
            # With years
            for year in self.indian_numbers['year_patterns'][-10:]:
                patterns.add(f"{fest}{year}")
                patterns.add(f"{fest.title()}{year}")
            
            # With happy prefix
            patterns.add(f"happy{fest}")
            patterns.add(f"Happy{fest.title()}")
            
            # With special characters
            patterns.add(f"{fest}!")
            patterns.add(f"{fest}!!")
            patterns.add(f"{fest}@123")
        
        return list(patterns)
    
    def generate_bollywood_patterns(self, actor: str = None, actress: str = None) -> List[str]:
        """Generate Bollywood-inspired passwords"""
        patterns = set()
        
        # Use provided names or random ones
        actors = [actor] if actor else random.sample(self.bollywood['actors'], 2)
        actresses = [actress] if actress else random.sample(self.bollywood['actresses'], 2)
        
        for act in actors:
            if act:
                patterns.add(act)
                patterns.add(act.title())
                
                # Actor with year
                for year in self.indian_numbers['year_patterns'][-5:]:
                    patterns.add(f"{act}{year}")
                
                # Actor with numbers
                for num in ['123', '456', '789', '007']:
                    patterns.add(f"{act}{num}")
        
        for actress in actresses:
            if actress:
                patterns.add(actress)
                patterns.add(actress.title())
                
                # Actress with specials
                patterns.add(f"{actress}!")
                patterns.add(f"{actress}@123")
        
        # Movie names
        for movie in random.sample(self.bollywood['movies'], 3):
            patterns.add(movie)
            patterns.add(movie.title())
            patterns.add(f"{movie}123")
        
        return list(patterns)
    
    def generate_cricket_patterns(self, player: str = None, team: str = None) -> List[str]:
        """Generate cricket-inspired passwords"""
        patterns = set()
        
        # Use provided or random
        players = [player] if player else random.sample(self.cricket['players'], 3)
        teams = [team] if team else random.sample(self.cricket['teams'], 2)
        
        for player in players:
            if player:
                patterns.add(player)
                patterns.add(player.title())
                
                # Player with jersey numbers
                jersey_numbers = ['10', '7', '18', '45', '99', '333']
                for jersey in jersey_numbers:
                    patterns.add(f"{player}{jersey}")
        
        for team in teams:
            if team:
                patterns.add(team)
                patterns.add(team.title())
                patterns.add(f"{team}123")
                patterns.add(f"{team}win")
        
        # Cricket terms
        for term in random.sample(self.cricket['terms'], 3):
            patterns.add(term)
            patterns.add(term.title())
        
        return list(patterns)
    
    def generate_smart_combinations(self, data: Dict) -> Set[str]:
        """Generate smart password combinations based on Indian patterns"""
        passwords = set()
        
        # Extract all components
        components = self.extract_all_components(data)
        
        # Generate based on style
        style = data.get('style', '3')
        
        if style in ['1', '2', '3', '4', '5']:
            # Style 1: Simple name + year patterns
            if style in ['1', '2', '3', '4', '5']:
                passwords.update(self.generate_simple_patterns(components))
            
            # Style 2: With special characters
            if style in ['2', '3', '4', '5']:
                passwords.update(self.generate_with_specials(components, data))
            
            # Style 3: Advanced combinations
            if style in ['3', '4', '5']:
                passwords.update(self.generate_advanced_combinations(components, data))
            
            # Style 4: Comprehensive (add everything)
            if style in ['4', '5']:
                passwords.update(self.generate_comprehensive_patterns(components, data))
            
            # Style 5: Smart/AI-like predictions
            if style == '5':
                passwords.update(self.generate_smart_predictions(components, data))
        
        return passwords
    
    def extract_all_components(self, data: Dict) -> Dict:
        """Extract all password components from user data"""
        components = defaultdict(list)
        
        # Personal names
        personal = data.get('personal', {})
        if 'first_name' in personal:
            components['names'].extend(self.generate_name_variations(personal['first_name']))
        if 'last_name' in personal:
            components['names'].extend(self.generate_name_variations(personal['last_name']))
        if 'nickname' in personal:
            components['nicknames'].extend(self.generate_name_variations(personal['nickname']))
        
        # Family names
        family_fields = ['father_name', 'mother_name', 'spouse_name', 'child_name']
        for field in family_fields:
            if field in personal and personal[field]:
                if field == 'child_name' and ',' in personal[field]:
                    for child in personal[field].split(','):
                        components['family'].extend(self.generate_name_variations(child.strip()))
                else:
                    components['family'].extend(self.generate_name_variations(personal[field]))
        
        # Dates
        dates = data.get('dates', {})
        if 'birth_date' in dates:
            date_comps = self.extract_indian_date_components(dates['birth_date'])
            for comp_list in date_comps.values():
                components['dates'].extend(comp_list)
        
        # Mobile patterns
        contacts = data.get('contacts', {})
        if 'mobile' in contacts:
            components['mobile_patterns'].extend(self.generate_indian_mobile_patterns(contacts['mobile']))
        
        # Interests
        interests = data.get('interests', {})
        if 'keywords' in interests:
            components['keywords'].extend(interests['keywords'])
        
        if 'actor' in interests:
            components['bollywood'].append(interests['actor'])
        
        if 'cricketer' in interests:
            components['cricket'].append(interests['cricketer'])
        
        # Add some random Indian elements
        components['festivals'].extend(random.sample(list(self.indian_festivals.keys()), 2))
        components['places'].extend(random.sample(self.indian_places['cities'], 3))
        
        # Number patterns
        if data.get('numbers_enabled', True):
            num_types = data.get('number_types', ['5'])
            components['numbers'].extend(self.generate_indian_number_patterns(num_types))
        
        return dict(components)
    
    def generate_simple_patterns(self, components: Dict) -> Set[str]:
        """Generate simple password patterns"""
        passwords = set()
        
        # Name + Year
        for name in components.get('names', [])[:5]:
            for year in components.get('dates', [])[:3]:
                if year.isdigit() and len(year) in [2, 4]:
                    passwords.add(f"{name}{year}")
                    passwords.add(f"{year}{name}")
            
            # Name + Mobile last 4
            for mobile in components.get('mobile_patterns', []):
                if len(mobile) >= 4:
                    passwords.add(f"{name}{mobile[-4:]}")
        
        # Nickname patterns
        for nickname in components.get('nicknames', [])[:3]:
            for num in ['123', '456', '789', '007']:
                passwords.add(f"{nickname}{num}")
            
            passwords.add(f"{nickname}!")
            passwords.add(f"{nickname}@123")
        
        return passwords
    
    def generate_with_specials(self, components: Dict, data: Dict) -> Set[str]:
        """Generate passwords with special characters"""
        passwords = set()
        
        specials = data.get('specials', self.indian_specials[:3]) if data.get('special_enabled', False) else ['']
        
        for name in components.get('names', [])[:3]:
            for special in specials[:2]:
                if special:
                    # Name + Special + Number
                    for num in components.get('numbers', [])[:5]:
                        passwords.add(f"{name}{special}{num}")
                        passwords.add(f"{special}{name}{num}")
                    
                    # Name + Special + Year
                    for year in components.get('dates', [])[:3]:
                        if year.isdigit():
                            passwords.add(f"{name}{special}{year}")
        
        return passwords
    
    def generate_advanced_combinations(self, components: Dict, data: Dict) -> Set[str]:
        """Generate advanced password combinations"""
        passwords = set()
        
        specials = data.get('specials', self.indian_specials[:3]) if data.get('special_enabled', False) else ['']
        
        # Name + Family member combinations
        names = components.get('names', [])[:2]
        family = components.get('family', [])[:2]
        
        for name in names:
            for fam in family:
                passwords.add(f"{name}{fam}")
                passwords.add(f"{fam}{name}")
                
                for special in specials[:2]:
                    if special:
                        passwords.add(f"{name}{special}{fam}")
        
        # Festival patterns
        for festival in components.get('festivals', [])[:2]:
            festival_names = self.indian_festivals.get(festival, [festival])
            for fest in festival_names[:2]:
                for year in components.get('dates', [])[:2]:
                    if year.isdigit():
                        passwords.add(f"{fest}{year}")
                        passwords.add(f"happy{fest}{year}")
        
        # Place patterns
        for place in components.get('places', [])[:2]:
            for year in self.indian_numbers['year_patterns'][-5:]:
                passwords.add(f"{place}{year}")
            
            for num in ['123', '456']:
                passwords.add(f"{place}{num}")
        
        return passwords
    
    def generate_comprehensive_patterns(self, components: Dict, data: Dict) -> Set[str]:
        """Generate comprehensive password patterns"""
        passwords = set()
        
        # Add Bollywood patterns
        if 'bollywood' in components:
            passwords.update(self.generate_bollywood_patterns(
                components['bollywood'][0] if components['bollywood'] else None,
                None
            ))
        
        # Add Cricket patterns
        if 'cricket' in components:
            passwords.update(self.generate_cricket_patterns(
                components['cricket'][0] if components['cricket'] else None,
                None
            ))
        
        # Complex combinations
        names = components.get('names', [])[:2]
        keywords = components.get('keywords', [])[:2]
        numbers = components.get('numbers', [])[:3]
        
        for name in names:
            for keyword in keywords:
                for num in numbers:
                    passwords.add(f"{name}{keyword}{num}")
                    passwords.add(f"{keyword}{name}{num}")
                
                # With festival
                for festival in components.get('festivals', [])[:1]:
                    fest_names = self.indian_festivals.get(festival, [festival])
                    passwords.add(f"{name}{fest_names[0]}{keyword}")
        
        return passwords
    
    def generate_smart_predictions(self, components: Dict, data: Dict) -> Set[str]:
        """Generate smart/AI-like password predictions"""
        passwords = set()
        
        # Analyze patterns and generate likely passwords
        names = components.get('names', [])
        nicknames = components.get('nicknames', [])
        dates = [d for d in components.get('dates', []) if d.isdigit()]
        mobiles = components.get('mobile_patterns', [])
        
        # Most likely patterns (based on Indian password analysis)
        if names:
            name = names[0]
            
            # Pattern 1: Name + Birth Year
            if dates:
                birth_year = dates[0] if len(dates[0]) == 4 else None
                if birth_year:
                    passwords.add(f"{name}{birth_year}")
                    passwords.add(f"{name.title()}{birth_year}")
                    passwords.add(f"{name}{birth_year[-2:]}")
            
            # Pattern 2: Name + Mobile last 4
            if mobiles:
                last4 = mobiles[0][-4:] if len(mobiles[0]) >= 4 else '1234'
                passwords.add(f"{name}{last4}")
                passwords.add(f"{name.title()}{last4}")
            
            # Pattern 3: Name + Lucky Number
            lucky_numbers = ['7', '9', '11', '13', '21', '51', '108']
            for lucky in lucky_numbers[:3]:
                passwords.add(f"{name}{lucky}")
                passwords.add(f"{name}@{lucky}")
            
            # Pattern 4: Name + Child Birth Year
            if len(dates) > 1:
                child_year = dates[1] if len(dates[1]) == 4 else dates[0]
                passwords.add(f"{name}{child_year}")
        
        # Nickname patterns
        if nicknames:
            nickname = nicknames[0]
            passwords.add(f"{nickname}123")
            passwords.add(f"{nickname}@123")
            passwords.add(f"{nickname}!")
            
            # With birth day
            if dates:
                for date_str in dates:
                    if date_str.isdigit() and len(date_str) == 2:
                        passwords.add(f"{nickname}{date_str}")
        
        # Vehicle number patterns
        contacts = data.get('contacts', {})
        if 'vehicle' in contacts:
            vehicle = contacts['vehicle']
            if len(vehicle) >= 4:
                last4 = vehicle[-4:]
                passwords.add(last4)
                passwords.add(f"dl{last4}")
                passwords.add(f"{last4}@123")
        
        # Aadhaar patterns
        if 'aadhaar_last4' in contacts:
            aadhaar = contacts['aadhaar_last4']
            passwords.add(aadhaar)
            passwords.add(f"aadhaar{aadhaar}")
        
        return passwords
    
    def apply_language_variations(self, passwords: Set[str]) -> Set[str]:
        """Apply Hindi/regional language variations"""
        variations = set()
        
        # Common Hindi transliterations
        hindi_map = {
            'a': ['aa', 'a'],
            'i': ['ee', 'i'],
            'u': ['oo', 'u'],
            'e': ['ai', 'e'],
            'o': ['au', 'o'],
            'sh': ['sh', 's'],
            'ch': ['ch', 'c'],
            'th': ['th', 't'],
            'dh': ['dh', 'd'],
            'bh': ['bh', 'b']
        }
        
        for password in list(passwords)[:1000]:  # Limit to avoid explosion
            variations.add(password)
            
            # Try some common Hindi variations
            if 'sh' in password:
                variations.add(password.replace('sh', '5h'))
            
            if 'om' in password.lower():
                variations.add(password.lower().replace('om', 'ॐ'))
            
            # Add 'ji' suffix (common respectful suffix)
            if len(password) <= 10 and not password.endswith('ji'):
                variations.add(f"{password}ji")
        
        return variations
    
    def filter_and_validate(self, passwords: Set[str], data: Dict) -> Set[str]:
        """Filter and validate generated passwords"""
        filtered = set()
        
        min_len = data.get('min_length', 8)
        max_len = data.get('max_length', 16)
        max_passwords = data.get('max_passwords', 50000)
        
        for pwd in passwords:
            # Length check
            if not (min_len <= len(pwd) <= max_len):
                continue
            
            # Remove unrealistic patterns
            # Too many consecutive specials
            if re.search(r'[!@#$%^&*]{3,}', pwd):
                continue
            
            # Too many consecutive numbers (more than 6)
            if re.search(r'\d{7,}', pwd):
                continue
            
            # Too many consecutive same characters
            if re.search(r'(.)\1{4,}', pwd):
                continue
            
            # Must have at least one letter
            if not re.search(r'[a-zA-Z]', pwd):
                continue
            
            # Must not be just numbers
            if pwd.isdigit():
                continue
            
            filtered.add(pwd)
            
            # Stop if we've reached max
            if len(filtered) >= max_passwords:
                break
        
        return filtered
    
    def analyze_indian_patterns(self, passwords: Set[str]) -> None:
        """Analyze and display Indian password patterns"""
        if not passwords:
            return
        
        print("\n" + "="*70)
        print(" 🇮🇳 INDIAN PASSWORD PATTERN ANALYSIS")
        print("="*70)
        
        sample = random.sample(list(passwords), min(100, len(passwords)))
        
        # Categorize patterns
        categories = {
            'Name + Year': 0,
            'Name + Number': 0,
            'Nickname based': 0,
            'Mobile patterns': 0,
            'Festival based': 0,
            'Place based': 0,
            'Bollywood/Cricket': 0,
            'With Specials': 0,
            'Simple (<=8 chars)': 0,
            'Complex (>12 chars)': 0
        }
        
        for pwd in sample:
            # Check for years
            if any(year in pwd for year in self.indian_numbers['year_patterns'][-20:]):
                categories['Name + Year'] += 1
            
            # Check for mobile patterns
            if any(str(num) in pwd for num in range(1000, 10000)):
                categories['Name + Number'] += 1
            
            # Check for nicknames
            if any(nick in pwd.lower() for nick in self.indian_names['nicknames']):
                categories['Nickname based'] += 1
            
            # Check for mobile number patterns
            if re.search(r'\d{10}', pwd) or re.search(r'\d{4}$', pwd):
                categories['Mobile patterns'] += 1
            
            # Check for festivals
            for festival_names in self.indian_festivals.values():
                if any(fest in pwd.lower() for fest in festival_names):
                    categories['Festival based'] += 1
                    break
            
            # Check for places
            if any(city in pwd.lower() for city in self.indian_places['cities']):
                categories['Place based'] += 1
            
            # Check for Bollywood/Cricket
            for actor in self.bollywood['actors'] + self.bollywood['actresses']:
                if actor in pwd.lower():
                    categories['Bollywood/Cricket'] += 1
                    break
            
            for player in self.cricket['players']:
                if player in pwd.lower():
                    categories['Bollywood/Cricket'] += 1
                    break
            
            # Check for specials
            if any(spec in pwd for spec in self.indian_specials):
                categories['With Specials'] += 1
            
            # Length categories
            if len(pwd) <= 8:
                categories['Simple (<=8 chars)'] += 1
            elif len(pwd) > 12:
                categories['Complex (>12 chars)'] += 1
        
        print("\n📊 Pattern Distribution in Sample:")
        print("-" * 50)
        for category, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / len(sample)) * 100
            bar = '█' * int(percentage / 2)
            print(f"  {category:25} {count:3} {percentage:5.1f}% {bar}")
        
        print(f"\n📈 Total unique passwords generated: {len(passwords):,}")
        
        # Show some examples
        print("\n🔑 Examples of Generated Passwords:")
        print("-" * 50)
        examples = random.sample(list(passwords), min(15, len(passwords)))
        for i, pwd in enumerate(examples, 1):
            strength = self.estimate_strength(pwd)
            strength_bar = '█' * strength + '░' * (10 - strength)
            print(f"  {i:2}. {pwd:20} [Strength: {strength_bar}]")
    
    def estimate_strength(self, password: str) -> int:
        """Estimate password strength (1-10)"""
        score = 0
        
        # Length score
        if len(password) >= 8:
            score += 2
        if len(password) >= 12:
            score += 2
        if len(password) >= 16:
            score += 1
        
        # Character variety
        has_lower = re.search(r'[a-z]', password)
        has_upper = re.search(r'[A-Z]', password)
        has_digit = re.search(r'\d', password)
        has_special = re.search(r'[!@#$%^&*()\-_=+\[\]{}|;:,.<>?/~`]', password)
        
        score += sum([1 for x in [has_lower, has_upper, has_digit, has_special] if x])
        
        # Bonus for non-common patterns
        if not any(year in password for year in self.indian_numbers['year_patterns'][-10:]):
            score += 1
        
        if not any(name in password.lower() for name in self.indian_names['male_first'][:5] + self.indian_names['female_first'][:5]):
            score += 1
        
        return min(score, 10)
    
    def generate(self, data: Dict) -> Set[str]:
        """Main generation function"""
        print("\n[*] Generating Indian-specific passwords...")
        
        # Generate passwords
        passwords = self.generate_smart_combinations(data)
        print(f"[+] Initial generation: {len(passwords):,} passwords")
        
        # Apply leet speak if enabled
        if data.get('leet_enabled', False):
            print("[*] Applying Indian leet speak...")
            leet_passwords = set()
            leet_level = data.get('leet_level', 2)
            
            for pwd in list(passwords)[:5000]:  # Limit to avoid explosion
                leet_passwords.update(self.apply_indian_leet(pwd, leet_level))
            
            passwords.update(leet_passwords)
            print(f"[+] After leet: {len(passwords):,} passwords")
        
        # Apply language variations if enabled
        if data.get('lang_variations', False):
            print("[*] Applying language variations...")
            lang_variations = self.apply_language_variations(passwords)
            passwords.update(lang_variations)
            print(f"[+] After language variations: {len(passwords):,} passwords")
        
        # Filter and validate
        filtered = self.filter_and_validate(passwords, data)
        print(f"[+] After filtering: {len(filtered):,} passwords")
        
        return filtered
    
    def save_wordlist(self, wordlist: Set[str], filename: str, data: Dict):
        """Save wordlist with Indian metadata"""
        wordlist_list = sorted(list(wordlist), key=lambda x: (len(x), x))
        
        print(f"\n[*] Saving {len(wordlist_list):,} passwords to {filename}...")
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                # Add detailed metadata
                f.write("#" * 80 + "\n")
                f.write("# 🇮🇳 BHARATIYA PASSWORD WORDLIST\n")
                f.write("#" * 80 + "\n")
                f.write(f"# Generated: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
                f.write(f"# Total Passwords: {len(wordlist_list):,}\n")
                f.write(f"# Generation Style: {data.get('style', '3')}\n")
                f.write(f"# Length Range: {data.get('min_length', 8)}-{data.get('max_length', 16)}\n")
                f.write("#" * 80 + "\n\n")
                
                # Write passwords in categories
                categories = {
                    'Short (6-8 chars)': [],
                    'Medium (9-12 chars)': [],
                    'Long (13+ chars)': []
                }
                
                for pwd in wordlist_list:
                    if 6 <= len(pwd) <= 8:
                        categories['Short (6-8 chars)'].append(pwd)
                    elif 9 <= len(pwd) <= 12:
                        categories['Medium (9-12 chars)'].append(pwd)
                    else:
                        categories['Long (13+ chars)'].append(pwd)
                
                # Write by category
                for category, pwds in categories.items():
                    if pwds:
                        f.write(f"\n# {category} ({len(pwds)} passwords)\n")
                        f.write("#" * 60 + "\n")
                        for pwd in pwds:
                            f.write(pwd + "\n")
            
            file_size = os.path.getsize(filename)
            print(f"[✅] Successfully saved {len(wordlist_list):,} passwords")
            print(f"[📊] File size: {file_size:,} bytes ({file_size/1024/1024:.2f} MB)")
            
            return True
            
        except Exception as e:
            print(f"[❌] Error saving file: {e}")
            return False

def main():
    parser = argparse.ArgumentParser(
        description='🇮🇳 BHARATIYA PASSWORD GENERATOR - Indian-Specific Advanced Password Generator',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive mode (recommended)
  python indian_password_generator.py
  
  # Quick generation
  python indian_password_generator.py --name "Aarav" --surname "Sharma" --year 1990
  
  # Advanced generation
  python indian_password_generator.py --name "Priya" --mobile "9876543210" 
         --festival "diwali" --style 4 --output "priya_passwords.txt"
        """
    )
    
    # Basic Indian information
    parser.add_argument('--name', help='First name')
    parser.add_argument('--surname', help='Last name/Surname')
    parser.add_argument('--nickname', help='Nickname/Petname')
    parser.add_argument('--year', help='Birth year (YYYY)')
    parser.add_argument('--mobile', help='Mobile number (10 digits)')
    parser.add_argument('--festival', help='Favorite Indian festival')
    
    # Generation options
    parser.add_argument('--style', type=int, choices=[1, 2, 3, 4, 5], default=3,
                       help='Generation style: 1=Simple, 2=Medium, 3=Advanced, 4=Comprehensive, 5=Smart')
    parser.add_argument('--leet', type=int, choices=[1, 2, 3], default=2,
                       help='Leet speak level: 1=Basic, 2=Moderate, 3=Advanced')
    
    # Output options
    parser.add_argument('-o', '--output', default='indian_passwords.txt',
                       help='Output filename')
    parser.add_argument('--max', type=int, default=50000,
                       help='Maximum passwords to generate')
    
    args = parser.parse_args()
    
    generator = IndianPasswordGenerator()
    
    print("\n" + "="*70)
    print(" 🇮🇳 BHARATIYA PASSWORD GENERATOR")
    print("="*70)
    print("\nWelcome! Let's create Indian-specific passwords...\n")
    
    # Check if we have enough command line arguments
    if args.name and args.surname and args.year:
        # Use command line arguments
        print("[*] Using command line parameters...")
        
        data = {
            'personal': {
                'first_name': args.name.lower(),
                'last_name': args.surname.lower(),
            },
            'dates': {
                'birth_date': f"01/01/{args.year}"
            },
            'contacts': {},
            'interests': {},
            'style': str(args.style),
            'leet_enabled': args.leet > 0,
            'leet_level': args.leet,
            'special_enabled': True,
            'specials': generator.indian_specials[:5],
            'numbers_enabled': True,
            'number_types': ['5'],
            'lang_variations': False,
            'min_length': 8,
            'max_length': 16,
            'max_passwords': args.max
        }
        
        if args.nickname:
            data['personal']['nickname'] = args.nickname.lower()
        
        if args.mobile and len(args.mobile) >= 10:
            data['contacts']['mobile'] = args.mobile[-10:]
        
        if args.festival:
            data['interests']['festival'] = args.festival.lower()
        
    else:
        # Interactive mode
        print("[*] Starting interactive mode...")
        data = generator.get_indian_user_input()
    
    print(f"\n{'='*70}")
    print(" GENERATION PARAMETERS")
    print(f"{'='*70}")
    
    # Show key parameters
    print("\n[Personal Information]")
    if 'personal' in data:
        for key, value in data['personal'].items():
            if value:
                print(f"  {key:15}: {value}")
    
    print("\n[Generation Options]")
    print(f"  Style:          {data.get('style', '3')}")
    print(f"  Leet Speak:     {'Yes' if data.get('leet_enabled') else 'No'}")
    print(f"  Special Chars:  {'Yes' if data.get('special_enabled') else 'No'}")
    print(f"  Language Vars:  {'Yes' if data.get('lang_variations') else 'No'}")
    print(f"  Length Range:   {data.get('min_length', 8)}-{data.get('max_length', 16)}")
    print(f"  Max Passwords:  {data.get('max_passwords', 50000):,}")
    
    print(f"\n{'='*70}\n")
    
    # Generate passwords
    passwords = generator.generate(data)
    
    # Analyze patterns
    generator.analyze_indian_patterns(passwords)
    
    # Save to file
    if passwords:
        output_file = args.output
        generator.save_wordlist(passwords, output_file, data)
        
        print(f"\n📁 Wordlist saved to: {os.path.abspath(output_file)}")
        
        # Show some statistics
        print("\n📈 Password Statistics:")
        print("-" * 40)
        
        lengths = [len(p) for p in passwords]
        avg_len = sum(lengths) / len(lengths) if lengths else 0
        
        print(f"  Average length:     {avg_len:.1f} characters")
        print(f"  Shortest password:  {min(lengths) if lengths else 0} chars")
        print(f"  Longest password:   {max(lengths) if lengths else 0} chars")
        
        # Character usage
        all_chars = ''.join(passwords)
        char_counts = Counter(all_chars)
        special_count = sum(1 for c in all_chars if c in generator.indian_specials)
        
        print(f"  Special chars used: {special_count:,} ({special_count/len(all_chars)*100:.1f}%)")
        
        # Most common patterns
        print("\n🔍 Most Common Starting Patterns:")
        first_4_chars = [p[:4] for p in passwords if len(p) >= 4]
        common_starts = Counter(first_4_chars).most_common(5)
        for pattern, count in common_starts:
            print(f"  {pattern}: {count} passwords")
    
    else:
        print("❌ No passwords generated!")

if __name__ == '__main__':
    main()