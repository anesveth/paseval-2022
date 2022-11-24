from string import ascii_lowercase, ascii_uppercase
import random as ra

lowercase_enabled = True
uppercase_enabled = True
numbers_enabled = True
symbols_enabled = True

ascii_numbers = "0123456789"
ascii_symbols = "!()?[]_~;:#$%^&*+=`-."
ascii_symbols_not_first = ["-","."]

# special_char[:0] = "!()?[]_~;:#$%^&*+=`"
# # allowed if not first char in password
# special_char_limited = ['-','.']
# # often times not allowed
# special_char_rare = ['@', ' ']
def check_options_clicked(lowercase_enabled:bool,uppercase_enabled:bool,numbers_enabled:bool,symbols_enabled:bool):
    """
    prevents user from only picking one or 0 options by making others True at random until there are at least 2 True
    """
    l = [lowercase_enabled,uppercase_enabled,numbers_enabled,symbols_enabled]
    n_true = 0
    for b in l:
        if b:
            n_true += 1
        
    if n_true < 2:
        while n_true < 2:
            n = ra.randrange(len(l)-1)
            l[n] = True
            n_true += 1
    
    return l



def random_generator(length_p:int,lowercase_enabled:bool,uppercase_enabled:bool,numbers_enabled:bool,symbols_enabled:bool):
    """
    input: length_p (length) of password, booleans for char choices...
    Generates a password randomly with given options
    """
    generated_password = ""
    check = check_options_clicked(lowercase_enabled,uppercase_enabled,numbers_enabled,symbols_enabled)
    
    character_set = []
    if lowercase_enabled or check[0]:
        character_set += list(ascii_lowercase)
    if uppercase_enabled or check[1]:
        character_set += list(ascii_uppercase)
    if numbers_enabled or check[2]:
        character_set += list(ascii_numbers)
    if symbols_enabled or check[3]:
        character_set += list(ascii_symbols)

    ra.shuffle(character_set)

    for n in range(length_p):
        if n < 2:
            rchar = ra.choice(character_set)
            while rchar in ascii_symbols_not_first:
                rchar = ra.choice(character_set)
            generated_password += rchar
        else:
            rchar = ra.choice(character_set)
            generated_password += rchar

    return generated_password

# print(generated_password)