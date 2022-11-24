# RENDERING FUNCTIONS
from ast import Pass
from operator import is_
import re
from django.shortcuts import render,redirect
## for the redirects of posts/gets
from django.http import HttpResponseRedirect,HttpResponsePermanentRedirect
from django.urls import reverse
## importing forms functions
from . import forms


## importing our own modules
from . import p_testing as pt
from . import p_encoding as pe
from . import p_search as ps
from . import overall_score as sc

from . import randomg as randomizedgen
from . import personalizedg as personalizedgen


def Home(request):
    #placeholders for the forms
    strength_tester = forms.passwordInput()
    
    ## forms for strength tester and generator, grabbed from forms.py
    empty_forms = {
        'strength_tester': strength_tester,
    }
    
    try: 
        request.session['generatedPassword'] = ''
        # get rid of session variables when going back to home 
        del request.session['password_input']
        del request.session['flags']
        del request.session['pwned']
        for key in request.session.keys():
            print("keysss")
            print(key)
            del request.session[key]
    except:
        request.session['generatedPassword'] = ''
    return render(request, "index.html", empty_forms)

def viewStrength(request):
    context = {
        'password_input' : request.session['password_input'],
        # Overall score of strength - takes into account API search results + composition of password
        'score' : request.session['score'],
        # level of strength
        'level' : request.session['level'],
        # dictionary of % of types of chars in password (lowercase, uppercase, number, special)
        'distribution' : request.session['distribution'],
        # list [True if has english words, n of words found]
        'words' : request.session['words'],
        # list [comments/feedback on password composition]
        'flags': request.session['flags'],
        'flags_count': len(request.session['flags']),
        # list (found[false or true], count (0 if not found)]
        'pwned': request.session['pwned']
    }
    
    # print("view")
    # print(request.session['score'])
    return render(request, 'strength.html', context)

def viewRandom(request):
    context = {
        'random_form' : forms.RandomGeneratorInput(),
        'generated' : request.session['generatedPassword']
    }
    return render(request, 'randomg.html',context)

def viewPersonalizedg(request):
    context = {
        'personalized_form' : forms.PersonalizedGeneratorInput(),
        'generated' : request.session['generatedPassword']
    }
    return render(request, 'personalized.html',context)


def Strength(request):
    if request.method == 'POST':
        password_form = forms.passwordInput(request.POST)
        if password_form.is_valid():
            request.session['password_input'] = password_form.cleaned_data['password_input']
            pssword = request.session['password_input']
            ### API --------------------
            ## encoding del password para pasarlo al API 
            # encode_pssword = pe.encodedPassword(pssword)
            password_hash = pe.encode_password(pssword)
            ## search for password in API
            search_password = ps.searchPassword(password_hash)
            search_password.find_password()
            search_results = search_password.get_results()
            request.session['pwned'] = search_results
            ### composition of password ----------
            ## internal testing de nuestro modulo 
            basic_internal_test = pt.Password_testing(pssword)
            basic_internal_test.testing()
            password_level = basic_internal_test.get_level()
            request.session['level'] = password_level
            request.session['distribution'] = basic_internal_test.get_distribution_of_variety()
            request.session['words'] = basic_internal_test.get_words()
            request.session['flags'] = basic_internal_test.get_flags()
            # overall score
            score = sc.score(password_level,search_results)
            request.session['score'] = score
            # print(request.session['score'])
            # print(request.session['level'])
            # print(request.session['pwned'])
            # print(request.session['distribution'])
            # print(request.session['words'])
            request.session['flags'] = basic_internal_test.get_flags()
            print(basic_internal_test.get_flags())
            return redirect('view_strength')
        else:
            print(password_form.errors.as_data())
        
    else:
        return redirect('index')


def randomGeneration(request):
    if request.method == 'POST':
        # print("was here")  
        random_form = forms.RandomGeneratorInput(request.POST)
        if random_form.is_valid():
            request.session['generatedPassword'] = ''
            size = int(random_form.cleaned_data['size'])
            b_lowercase = random_form.cleaned_data['use_lowercase']
            b_uppercase = random_form.cleaned_data['use_uppercase']
            b_numbers = random_form.cleaned_data['use_numbers']
            b_symbols = random_form.cleaned_data['use_special']
            rp = randomizedgen.random_generator(size,b_lowercase,b_uppercase,b_numbers,b_symbols)
            request.session['generatedPassword'] = rp
            print(rp)
        else:
            print(random_form.errors.as_data())
        return redirect('view_random')

    
        
    else:
        return redirect('index')


def personalizedGeneration(request):
    if request.method == 'POST': 
        # print("was here")  
        p_form = forms.PersonalizedGeneratorInput(request.POST)
        if p_form.is_valid():
            request.session['generatedPassword'] = ''
            word_or_phrase = p_form.cleaned_data['word_or_phrase']
            numbers = p_form.cleaned_data['numbers']
            special_e = p_form.cleaned_data['special_e']
            symbols = p_form.cleaned_data['symbols']
            new_password = personalizedgen.personalized_generator(word_or_phrase,numbers,special_e,symbols)
            request.session['generatedPassword'] = new_password
            print(new_password)
        else:
            print(p_form.errors.as_data())
        return redirect('view_personalized')
        
    else:
        return redirect('index')


