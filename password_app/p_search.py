##  REST API
import requests 
# Module for looking through api reponse for specific password using the PwnedPasswords API

# https://haveibeenpwned.com/API/v3#PwnedPasswords

class searchPassword:
    def __init__(self, password_hash):
        self.password_hash = password_hash
        # API request only accepts the first 5 chars of the hash for privacy. 
        # However we need to keep the rest of the hash to look through the results
        self.password_hash_search = password_hash[:5]  
        self.password_hash_remaining = password_hash[5:].upper()
        self.found = False
        self.count = 0

    def get_count(self):
        '''
        returns count of times a password has been pwned
        '''
        return self.count

    def is_found(self):
        '''
        returns found state
        '''
        return self.found
        
    def get_results(self):
        '''
        returns results of search in list (found[false or true], count (0 if not found)]
        '''
        # print([self.found, self.count])
        return [self.found, self.count]

    def search_password_in_api(self, api_response):
        '''
        Search for the password in the API REPONSE using the remaining charactes in the hash 
        '''
        # we split the response into separate lines to look through it
        api_response = api_response.text.split("\n")
        # print(self.password_hash_remaining)
        for line in api_response:
            l = line.split(":")
            suffix = l[0]
            if suffix == self.password_hash_remaining:
                self.count = int(l[1].strip("\r"))
                # print(self.count)
                self.found = True
        return self.found
    
    
    def find_password(self):
        '''
        process of finding password. Main function
        '''
        api_request = 'https://api.pwnedpasswords.com/range/{password_hash_search}'.format(password_hash_search=self.password_hash_search)
        try: 
            api_response = requests.get(api_request)
            # When a password hash with the same first 5 characters is found in the Pwned Passwords repository, 
            # the API will always respond with an HTTP 200 and include the suffix of every hash beginning with the specified prefix
            if api_response.status_code == 200:
                self.search_password_in_api(api_response)
                # request.session['pwned'] = [found,count]
            else:
                print("API unavailable")
                # request.session['pwned'] = []
        except requests.exceptions.ConnectionError as errorc:
            print ("Error Connecting:",errorc)
        except requests.exceptions.Timeout as errort:
            print ("Timeout Error:",errort)
        except requests.exceptions.RequestException as error:
            print ("OOps: Something Else",error)


        
