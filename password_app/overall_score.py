from .p_testing import levels
score_types = ['Change it as soon as possible!','Unsafe','Safe enough','Very safe','Safest']

def score(password_level:str,search_results:list):
    """
    Input: Password_testing level of strength, list containing API search results
    """
    final_score = ''
    ## if it is true that password has been found, it can't be safe
    if search_results[0]:
        print("true")
        if search_results[1] > 1:
            print("too many results")
            final_score = score_types[0] 
        else:
            if not (password_level == levels[0] or password_level == levels[1]):
                final_score = score_types[1] 
    else:
        final_score = score_types[1] 
        if password_level == levels[2]:
            final_score = score_types[2]
        elif (password_level == levels[3]) or (password_level == levels[4]):
            final_score = score_types[3]
        elif password_level == levels[5]:
            final_score = score_types[4]
    print("final score: "+final_score)
    return final_score

