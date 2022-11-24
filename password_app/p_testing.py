import string as stg
# dictionary of words
from english_words import english_words_lower_set as english_words



## GLOBAL
levels = ["very weak","risky","good","strong","very strong","strongest"]
all_ascii = stg.ascii_letters
lower_char = stg.ascii_lowercase
upper_char = stg.ascii_uppercase
numbers_char = stg.digits
## percentage of one char necessary to make it 
minimum_good_variation = 25

min_size = 8
## django checks this already
# max_size = 64

# info about valid characters for passwords from : https://www.ibm.com/docs/en/baw/19.x?topic=security-characters-that-are-valid-user-ids-passwords
# NORMALLY ALLOWED
special_char = []
special_char[:0] = "!()?[]_~;:#$%^&*+`"
# allowed if not first char in password
special_char_limited = ['-','.']
# often times not allowed
special_char_rare = ['@', ' ']


class Password_testing:
    def __init__(self,input_password):
        self.input_password = input_password
        # list of chars
        self.password_chars = []
        self.password_chars[:0] = input_password

        self.flags = [] ## returns evaluation of chars
        self.level = '' ## overall rating
        # [count, percentage out of the lenght of the password]
        self.distribution = {'lowercase':[0,0],'uppercase':[0,0],'numbers':[0,0],'special':[0,0]}
        
        self.has_numbers = False
        self.has_special_chars = False
        self.has_uppercase = False
        self.has_lowercase = False
        self.has_invalid_chars = False
        self.has_words = False
        self.count_words = 0
        

    def get_flags(self):
        return self.flags
    
    def get_level(self):
        return self.level

    def get_distribution_of_variety(self):
        return self.distribution
    
    def get_words(self):
        return [self.has_words,self.count_words]

    
    def get_variation(self):
        """
        checks password mix of numers, uppercase chars, etc.
        """
        variation = 0
        if self.has_numbers:
            variation += 1
        if self.has_lowercase:
            variation += 1
        if self.has_uppercase:
            variation += 1
        if self.has_special_chars:
            variation += 1
        return variation

    def char_evaluation(self):
        special_chars_found = []
        number_count = 0
        lower_count = 0
        upper_count = 0
        special_count = 0

        for char in self.password_chars:
            if char in numbers_char:
                number_count += 1
                self.has_numbers = True
            elif char in lower_char:
                lower_count += 1
                self.has_lowercase = True
                # self.flags.append([char,'lowercase'])
            elif char in upper_char:
                upper_count += 1
                self.has_uppercase = True
            elif char in special_char:
                special_count += 1
                self.has_special_chars = True
                special_chars_found.append(char)
            elif char in special_char_limited:
                special_count += 1
                self.has_special_chars = True
                special_chars_found.append(char)
                if char == self.password_chars[0]:
                    self.flags.append([char,'BAD PLACEMENT OF SPECIAL CHAR. SHOULD NOT START THE PASSWORD'])
            elif char in special_char_rare:
                special_count += 1
                self.has_special_chars = True
                special_chars_found.append(char)
                self.flags.append([char,'THIS CHAR IS SOMETIMES NOT ACCEPTED'])
            else:
                self.has_invalid_chars = True
                self.flags.append([char,'THIS CHAR IS PROHIBITED'])
        
        if self.get_variation() < 3:
            self.flags.append(['NOT ENOUGH VARIETY IN CHARS'])
            
        self.distribution['lowercase'] = [lower_count, lower_count/len(self.password_chars)*100]
        self.distribution['uppercase'] = [upper_count, upper_count/len(self.password_chars)*100]
        self.distribution['numbers'] = [number_count, number_count/len(self.password_chars)*100]
        self.distribution['special'] = [special_count, special_count/len(self.password_chars)*100]

        

    def find_words(self):
        """
        looks for words from english dictionary in password
        """
        full_password = self.input_password
        if self.has_numbers:
            full_password = full_password.translate({ord(i): ' ' for i in ['0','1','2','3','4','5','6','7','8','9']})
            
        if self.has_special_chars:
            full_password = full_password.translate({ord(i): ' ' for i in special_char})
            full_password = full_password.translate({ord(i): ' ' for i in special_char_limited})
            full_password = full_password.translate({ord(i): ' ' for i in special_char_rare})
        if self.has_invalid_chars:
            self.flags.append(['WORDS CANNOT PROPERLY BE IDENTIFIED AS YOU ARE USING INVALID_CHARS'])

        password_only_letters = full_password.split(' ')
        try:
            password_only_letters.remove('')
        except:
            pass
        for w in password_only_letters:
            if len(w) > 1:
                if w.lower() in english_words:
                    self.has_words = True
                    self.count_words += 1
                    # print(w.lower())
        # print(self.has_words, self.count_words)


# weak = less than 8 chars,OR/AND only has lowercase letters, uppercase or numbers
# risky = less than 16, has mix of three types of chars
# good = less than 16, mix of all types of chars (lowercase, uppercase, numbers, SPECIAL CHARS)
# strong = longer than 16 in length with no variation of chars/numbers
# very strong = longer than 16 in length with some variation of chars/numbers
# strongest = longer than 16 in length with variation of chars/numbers
    def rating(self):
        """
        Calculate rating
        """
        if len(self.password_chars) < 16:
            # starts with weak rating and changes rating depending on variation and length
            # weak = less than 8 chars,OR/AND only has lowercase letters, uppercase or numbers
            self.level = levels[0]
            
            if len(self.password_chars) >= min_size:
                if ((self.get_variation() == 4) and self.get_words()[1] < 3):
                    # good = less than 16, mix of all types of chars (lowercase, uppercase, numbers, SPECIAL CHARS)
                    self.level = levels[2]            
                elif ((self.get_variation() >= 2) and self.get_words()[1] < 3):
                    # risky = less than 16, has mix of three types of chars
                    self.flags.append(['RECOMMENDATION: HAVE LOWERCASE, UPPERCASE, NUMBERS AND SPECIAL CHARACTERS (&,#,!,...) IN YOUR PASSWORD'])
                    self.level = levels[1]
            else:
                self.flags.append(['PASSWORD IS TOO SHORT'])
                

        elif len(self.password_chars) >= 16:
            # strong = longer than 16 in length with no variation of chars/numbers
            self.level = levels[3]
            if ((self.get_variation() == 4) and self.get_words()[1] < 3):
                # strongest = longer than 16 in length with variation of chars/numbers, doesn't have many dictionary words
                self.level = levels[5]
            elif ((self.get_variation() > 1) and self.get_words()[1] < 3):
                # very strong = longer than 16 in length with 'some' variation of chars/numbers
                self.level = levels[4]

    def testing(self):
        self.char_evaluation()
        self.find_words()
        self.rating()
        print(self.get_level())

    
        
        
