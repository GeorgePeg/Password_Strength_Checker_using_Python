#Author: Georgios Pegiazis
#Date: 03/03/2026
#Version: 2.0
#License: Copyright © 2026 Georgios Pegiazis. All rights reserved. GNU GENERAL PUBLIC LICENSE
#Description: In this project, I fosued on creating a simple password strength checker using Python 3.1.3, using the SHA-256 algorithm for hashing the password. 
#The following python script checks the strength of a password created by the user based on 4 criteria: length, letters, digits and special characters.
#Lastly, this script also connects to a simple UI created in HTML and CSS, where the user can input its password and get feedback on its strength.

import re # Built-in library for using regular expressions
import hashlib # Built-in library for using encoding and decoding algorithms
from flask  import Flask, render_template, request # Library for creating a simple web application 

app =  Flask(__name__) # Initializing the Flask application

# Password Strength Check function
def passwordStrength(password):
    # Score variable
    score = 0
    # Empty list for saving feedbacks
    feedbacks = []
    # 1st check: Length of password
    if len(password) >= 8:
        score = score + 1
    else:
        feedbacks.append("Your password is to small (at least 8 characters)!")
    # 2nd check: Existence of any [A-Z] and [a-z] letter
    if re.search(r"[A-Z]", password) and re.search(r"[a-z]", password):
        score = score + 1
    else: 
        feedbacks.append("Password must contain lowercase and uppercase letters!")
    # 3rd check: Existense of any digit in password (0-9)
    if re.search(r"\d", password) :
        score = score + 1
    else: 
        feedbacks.append("Password must contain at least one digit!")
    # 4th check: Existense of any special character in password
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password) :
        score = score + 1
    else: 
        feedbacks.append("Password must contain at least one special character!")
    # Transforming the password from a plain text to a hash using the SHA-256 algorithm
    bytes = password.encode() # Encoding the password to bytes (UTF-8 by default)
    hashed_password = hashlib.sha256(bytes) #  Making the hashing value
    # Final step: Transforming the hash value to hexademical format and pringing it
    hex_hashed_password = hashed_password.hexdigest()
    print("The hash value of your password is:", hex_hashed_password)
    return score,feedbacks,hex_hashed_password
# User input for password
# password = input("Password: ")
# Calling the function and saving the results inside two variables
#score, feedbacks, hashed = passwordStrength(password)
# Printing the results
# print("Password strength score: ",score)
#for feedback in feedbacks:
    print(feedback)
# Informing the user about the password strength
# Flask Application
@app.route("/", methods=['GET', 'POST'])
def index() :
    results = None
    if request.method == 'POST':
        pwd = request.form.get("password")
        if pwd:
            score, feedbacks, hashed_password = passwordStrength(pwd)
            # Categorizing the password based on the score
            status = "Weak"
            if score == 4: 
                status = "Strong"
            elif score >=2 and score < 4:
                status = "Good"
            # Saving the results in a dictionary and sending it to the HTML page
            results = {"score" : score, 
                       "feedbacks": feedbacks, 
                       "hashed_value": hashed_password, 
                       "status": status
                    }
    return render_template("index.html", results=results)
if __name__ == "__main__":

    app.run(debug=True)
