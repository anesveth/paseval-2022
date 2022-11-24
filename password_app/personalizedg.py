import random 
from .p_testing import special_char,special_char_limited,special_char_rare,numbers_char
from string import ascii_lowercase, ascii_uppercase
letters = ascii_lowercase+ascii_uppercase+' '
all_symbols = special_char+special_char_limited+special_char_rare
# https://appliedinteractive.com/blog/2015/09/15/how-to-choose-a-better-password-using-an-easy-algorithm/

#  Come up with a word you remember. Longer words are best, and phrases are even better. The word may be a dog or cat you had years ago, or even a street you lived on. For this example I will use a street I lived on: Mower Street.
#   Pick a number you can remember, such as the year you graduated high school. For this example, I will use the year I graduated from college: 1980.
#   Add a unique element to each password. For this example, I will use the first letter of the website I am going to use the password on. I will select A for Amazon.
#   Pick a symbol you will remember. Make sure it is readily available on your keyboard so you don’t have to hunt for it. For this example I will use ^.
#   Lastly, decide the order. In this case, we will go in the order I listed the elements of the password: word-number-unique element-symbol.
def evaluation(l:list,type:str):
    """
    checks that numbers are numbers, symbols are symbols
    input: list to eval, type ['number','symbol']
    """
    eval = True
    if type == 'number':
        for element in l:
            print("number")
            try:
                e = int(element)
                print(e)
            except:
                print("False!")
                print(element)
                eval = False

    elif type == 'symbol':
        for element in l:
            if element not in all_symbols:
                print("False!")
                print(element)
                eval = False
    
    elif type == 'words':
        for element in l:
            element = element.replace(' ', '')
            
            for i in element:
                if (i not in letters):
                    print("False!")
                    print(element)
                    eval = False
    
    elif type == 'special_e':
        for element in l:
            if (element not in letters) and (element not in all_symbols):
                try:
                    e = int(element)
                    print(e)
                except:
                    eval =  False
    return eval

def personalized_generator(word_or_phrase:str, numbers:str, special_e:str, symbols:str):
   
    final_password = ''

    if "," in numbers:
        numbers = numbers.split(",")
    if "," in symbols:
        symbols = symbols.split(",")
    if ',' in word_or_phrase:
        word_or_phrase = word_or_phrase.split(',')
    if ',' in special_e:
        special_e = special_e.split(',')

    options = [word_or_phrase, numbers, special_e, symbols]
    print(options)
    valid_n = evaluation(numbers,'number')
    print(valid_n)
    valid_s = evaluation(symbols,'symbol')
    # print(valid_n)
    valid_w = evaluation(word_or_phrase,'words')
    # print(valid_n)
    valid_e = evaluation(special_e,'special_e')
    # print(valid_n)
    # print(options)
    if (valid_n and valid_s and valid_w and valid_e):
        while len(options) > 1:
            op_n = len(options)
            n = random.randrange(op_n)
            if isinstance(options[n], list):
                if len(options[n]) > 1:
                    op_n = len(options[n])
                    ni = random.randrange(op_n)
                    ## to avoid having the prohibited symbols from being placed first in password, since symbols will always go last in the original list
                    if (options[n][ni] in special_char_limited) and len(final_password)<1:
                        final_password += options[n-1].pop(ni)
                    else:
                        final_password += options[n].pop(ni)
                else:
                    ni = 0
                    final_password += options.pop(n)[0]
            else:
                final_password += options.pop(n)

        try:
            final_password += options.pop()
        except:
            print("OPTIONS")
            for i in range(len(options)):
                final_password += options.pop()
        final_password = final_password.replace(' ', '')
    # print(options)
    else:
        final_password = "You filled in the form wrong so the password couldn't be generated"
    return final_password

    


