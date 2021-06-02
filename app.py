#imports modules
from flask import Flask, redirect, render_template, url_for, request
from flaskext.mysql import MySQL
import random

#globalises variables
global loggedIn, cursor, dbconn, questionUsed, randomQ, correct, questionType, chosenQ, actualAns, Ans1, Ans2, Ans3, Ans4, buttons, score, total, choice, username, LogUser
mysql = MySQL() #initialises MySQL for the database
app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = 'root' #username for database
app.config['MYSQL_DATABASE_PASSWORD'] = 'Binary' #password for database
app.config['MYSQL_DATABASE_DB'] = 'web_site' #database name
app.config['MYSQL_DATABASE_HOST'] = 'localhost' #host of database
mysql.init_app(app)

dbconn=mysql.connect() 
cursor=dbconn.cursor()

#defines variables
loggedIn=False
questionUsed=[]
randomQ=[]
correct=""
questionType=""
chosenQ=""
actualAns=""
Ans1=""
Ans2=""
Ans3=""
Ans4=""
buttons="abled"
score=0
total=0
choice=""
username=""
LogUser=""

@app.route('/') #creates a url path
@app.route('/welcome') #creates url path
def welcome():  #creates a function for when the path is entered
    global LogUser #globalises the variable LogUser
    LogUser="" #defines LogUser as empty
    return render_template("welcome.html") #outputs this file when the function is called

@app.route('/about') #creates url path
def about():  #creates a function for when the path is entered
    return render_template("About.html") #outputs this file when the function is called

@app.route('/register') #creates a url path
def register(): #creates a function for when the path is entered
    return render_template("register.html") #outputs this file when the function is called

@app.route('/regResult', methods=["POST"]) #creates a url path that can only be accessed through being posted there
def regResult(): #creates a function for when the path is entered
    global loggedIn, cursor, dbconn, username #globalises loggedIn, cursor, dbconn and username variables
    username=request.form.get("Username") #retrieves the username the user enetered from the registration page
    email=request.form.get("Email") #retrieves the email the user enetered from the registration page
    password=request.form.get("password") #retrieves the password the user enetered from the registration page
    passwordVal=request.form.get("passwordVal") #retrieves the password validation the user enetered from the registration page
    
    cursor.execute('SELECT * FROM users WHERE UserName = %s OR UserEmail = %s', (username, email,)) #finds accounts in user database with either the entered username or email
    data=cursor.fetchone() #gets the data for the user that registered in
    if not username or not email or not password or not passwordVal: #checks that all fields are filled in
        error_statement="All Fields Required!" #defines the error statement with the corresponding issue
        return render_template("register.html", username=username, email=email, password=password, passwordVal=passwordVal, error_statement=error_statement) #outputs this file when the function is called and passes through the values the user inputed along with the error
        
    elif password!=passwordVal: #checks that password and passwordVal are equal
        error_statement="Password are not the same!" #defines the error statement with the corresponding issue
        return render_template("register.html", username=username, email=email, password=password, passwordVal=passwordVal, error_statement=error_statement) #outputs this file when the function is called and passes through the values the user inputed along with the error

    elif len(password)<8: #checks that the password is atleast 8 characters long
        error_statement="Password is not long enough!" #defines the error statement with the corresponding issue
        return render_template("register.html", username=username, email=email, password=password, passwordVal=passwordVal, error_statement=error_statement) #outputs this file when the function is called and passes through the values the user inputed along with the error
        
    elif data is None: #checks that there is no account with that username or email
        cursor.execute("INSERT INTO users (UserName, UserEmail, Password) VALUES (%s, %s, %s)",(username, email, password,)) #enters the username, email and password into the database
        dbconn.commit() #commits the insert to the database
        cursor.execute('UPDATE users SET Login_Counter = Login_Counter + 1 WHERE UserName = %s',(username,)) #updates the login counter of the user
        dbconn.commit() #commits the insert to the database
        loggedIn=True #redefines the loggedIn variable to show that the user is logged in
        return render_template("regResult.html", username=username)  #outputs this file when the function is called and passes through the username
    
    else:
        error_statement="An account with your username or email already exists"  #defines the error statement with the corresponding issue
        return render_template("register.html", username=username, email=email, password=password, passwordVal=passwordVal, error_statement=error_statement) #outputs this file when the function is called and passes through the username


@app.route('/login') #creates a url path
def login(): #creates a function for when the path is entered
    return render_template("login.html") #outputs this file when the function is called

@app.route('/logResult', methods=["POST"]) #creates a url path that can only be accessed through being posted there
def logResult(): #creates a function for when the path is entered
    global loggedIn, cursor, LogUser #globalises loggedIn and cursor variables
    LogUser=request.form["LogUser"] #retrieves the username the user enetered from the login page
    LogPass=request.form["LogPass"] #retrieves the password the user enetered from the login page
    
    cursor.execute('SELECT * FROM users WHERE UserName = %s AND Password = %s', (LogUser, LogPass,)) #finds accounts with the entered username and password
    data=cursor.fetchone() #gets the data for the users that logged in
    if not LogUser or not LogPass: #checks that all fields are filled in
        error_statement="All Fields Required!" #defines the error statement with the corresponding issue
        return render_template("login.html", LogUser=LogUser, LogPass=LogPass, error_statement=error_statement)  #outputs this file when the function is called and passes through the values the user inputted along with the error
    
    elif data is None: #if the username and password combination is not found
        error_statement="Username and password do not match!" #defines the error statement with the corresponding issue
        return render_template("login.html", LogUser=LogUser, LogPass=LogPass, error_statement=error_statement) #outputs this file when the function is called and passes through the values the user inputted along with the error
        
    else:
        loggedIn=True #defines loggedIn as true
        cursor.execute('UPDATE users SET Login_Counter = Login_Counter + 1 WHERE UserName = %s',(LogUser,)) #increments the login counter of the user
        dbconn.commit() #commits the update to the database
        return render_template("regResult.html", LogUser=LogUser) #outputs this file when the function is called and passes through the username


@app.route('/introduction') #creates a url path
def Intro(): #creates a function for when the path is entered
    global loggedIn #globalises loggedIn variable
    if loggedIn==False: #checks whether the user has logged in
        return render_template("login.html") #outputs this file when the function is called
    else:
        return render_template("Intro.html") #outputs this file when the function is called

@app.route('/binary-and-denary') #creates a url path
def BinDen(): #creates a function for when the path is entered
    global loggedIn #globalises loggedIn variable
    if loggedIn==False: #checks whether the user has logged in
        return render_template("login.html") #outputs this file when the function is called
    else:
        return render_template("BinDen.html") #outputs this file when the function is called

@app.route('/binary-and-hex') #creates a url path
def BinHex(): #creates a function for when the path is entered
    global loggedIn #globalises loggedIn variable
    if loggedIn==False: #checks whether the user has logged in
        return render_template("login.html") #outputs this file when the function is called
    else:
        return render_template("BinHex.html") #outputs this file when the function is called

@app.route('/denary-and-hex') #creates a url path
def HexDen(): #creates a function for when the path is entered
    global loggedIn #globalises loggedIn variable
    if loggedIn==False: #checks whether the user has logged in
        return render_template("login.html") #outputs this file when the function is called
    else:
        return render_template("HexDen.html") #outputs this file when the function is called

@app.route('/binary-addition') #creates a url path
def BinAdd(): #creates a function for when the path is entered
    global loggedIn #globalises loggedIn variable
    if loggedIn==False: #checks whether the user has logged in
        return render_template("login.html") #outputs this file when the function is called
    else:
        return render_template("BinAdd.html") #outputs this file when the function is called

@app.route('/binary-shift') #creates a url path
def BinShft(): #creates a function for when the path is entered
    global loggedIn #globalises loggedIn variable 
    if loggedIn==False: #checks whether the user has logged in
        return render_template("login.html") #outputs this file when the function is called
    else:
        return render_template("BinShft.html") #outputs this file when the function is called

@app.route('/quiz-choice') #creates a url path
def QuizChoice(): #creates a function for when the path is entered
    global loggedIn, score, questionUsed #globalises loggedIn, score and questionUsed variables
    score=0 #sets score back to 0
    questionUsed=[] #empties the questionUsed list
    if loggedIn==False: #checks whether the user has logged in
        return render_template("login.html") #outputs this file when the function is called
    else:
        return render_template("QuizChoice.html") #outputs this file when the function is called

@app.route('/quiz', methods=["POST"]) #creates a url path
def Quiz(): #creates a function for when the path is entered
    #globalises multiple variables to be used in the function
    global loggedIn, questionUsed, randomQ, correct, questionType, chosenQ, actualAns, Ans1, Ans2, Ans3, Ans4, buttons, choice, score
    if loggedIn==False: #checks whether the user has logged in
        return render_template("login.html") #outputs this file when the function is called
    else:
        randomQ=[] #empties the randomQ array
        buttons="abled" #allows the buttons to be functional again
        if len(questionUsed)==0: #checks to see whether a question has been added to the array
            choice=request.form['QuizChoice'] #obtains the value for the topic the user wants to be quizzed on

        if choice=="ALL": #checks to see whether the topic chosen was all topics
            maximum=119 #sets the maximum variable to 119
            cursor.execute('SELECT * FROM quiz WHERE QuestionTopic <> %s', ('TEST',)) #finds all questions in the database
        elif choice=="ADD":  #checks to see whether the topic chosen was binary addition
            maximum=19 #sets the maximum variable to 19
            cursor.execute('SELECT * FROM quiz WHERE QuestionTopic = %s', ('ADD',)) #finds all questions to do with binary addition
        elif choice=="BAH":  #checks to see whether the topic chosen was binary and hex
            maximum=24 #sets the maximum variable to 24
            cursor.execute('SELECT * FROM quiz WHERE QuestionTopic = %s', ('BAH',)) #finds all questions to do with binary and hex
        elif choice=="BAD":  #checks to see whether the topic chosen was binary and denary
            maximum=24 #sets the maximum variable to 24
            cursor.execute('SELECT * FROM quiz WHERE QuestionTopic = %s', ('BAD',)) #finds all questions to do with binary and denary
        elif choice=="HAD":  #checks to see whether the topic chosen was hex and denary
            maximum=24 #sets the maximum variable to 24
            cursor.execute('SELECT * FROM quiz WHERE QuestionTopic = %s', ('HAD',)) #finds all questions to do with hex and denary
        elif choice=="BSH":  #checks to see whether the topic chosen was binary shifts
            maximum=24 #sets the maximum variable to 24
            cursor.execute('SELECT * FROM quiz WHERE QuestionTopic = %s', ('BSH',)) #finds all questions to do with binary shifts

        questiontuple=cursor.fetchall() #fetches all questions that corresponded with the topic chosen
        rndNo=random.randint(0,maximum) #generates a random number
        while rndNo in questionUsed: #checks whether that number has already been chosen
            rndNo=random.randint(0,maximum) #generates another random number
        questionUsed.append(rndNo) #adds the random number to the list
        questionlist=list(questiontuple) #converts the tuple to a list
        questionType=questionlist[rndNo][2] #holds the value for the question type from the list using the random number
        chosenQ=questionlist[rndNo][3] #holds the value for the question 
        actualAns=questionlist[rndNo][4] #holds the value for the correct answer
        randomQ.append(actualAns) #adds te correct answer to the list
        if questionType == 1: #checks to see whether the question is multiple choice
            W1=questionlist[rndNo][5] #gets the first incorrect answer from the list
            W2=questionlist[rndNo][6] #gets the second incorrect answer from the list
            W3=questionlist[rndNo][7] #gets the third incorrect answer from the list
            randomQ.append(W1) #adds an incorrect answer to the list
            randomQ.append(W2) #adds an incorrect answer to the list
            randomQ.append(W3) #adds an incorrect answer to the list
            random.shuffle(randomQ) #shuffles the list in a random order
            Ans1=randomQ[0] #gets the first value from the list
            Ans2=randomQ[1] #gets the second value from the list
            Ans3=randomQ[2] #gets the third value from the list
            Ans4=randomQ[3] #gets the fourth value from the list
            if Ans1==actualAns: #checks to see if Ans1 is the correct answer
                correct=Ans1 #defines correct as Ans1
            elif Ans2==actualAns: #checks to see if Ans2 is the correct answer
                correct=Ans2 #defines correct as Ans2
            elif Ans3==actualAns: #checks to see if Ans3 is the correct answer
                correct=Ans3 #defines correct as Ans3
            elif Ans4==actualAns: #checks to see if Ans4 is the correct answer
                correct=Ans4 #defines correct as Ans4
        elif questionType==2: #checks whether the question is a short answer question
            Ans1=actualAns #sets Ans1 equal to the correct asnwer
            correct=Ans1 #sets correct as Ans1
        
        if len(questionUsed)>10: #checks to see if the 10 questions have
            questionUsed=[] #empties list
            total=score #defines total as score
            if LogUser=="": #checks to see if the user logged in or registered through the website
                user=username #if user registered then defines user as this
            else:
                user=LogUser #if user logged in then defines user as this
            cursor.execute('UPDATE users SET TotalScore = TotalScore + %s WHERE UserName = %s',(score, user,)) #updates the user total score in the database
            cursor.execute('UPDATE users SET TotalQuestions = TotalQuestions + 10 WHERE UserName = %s',(user,)) #updates the users total questions in the database
            dbconn.commit() #commits the update of the database
            score=0 #sets score to 0
            return render_template("result.html", total=total, correct=correct) #outputs this file when the function is called
        else:
            return render_template("quiz.html", questionType=questionType, chosenQ=chosenQ, actualAns=actualAns, Ans1=Ans1, Ans2=Ans2, Ans3=Ans3, Ans4=Ans4, correct=correct, buttons=buttons) #outputs this file when the function is called and passes through those variables

@app.route('/answer', methods=["POST","GET"]) #creates a url path
def Answer(): #creates a function for when the path is entered
    global loggedIn, correct, questionType, chosenQ, actualAns, Ans1, Ans2, Ans3, Ans4, buttons, score #globalises multiple variables to then be used in the function
    if loggedIn==False: #checks whether the user has logged in
        return render_template("login.html") #outputs this file when the function is called

    elif questionType==1: #checks whether the question chosen was multiple choice
        if request.form['UserAns'] == "Submit": #checks if the submit button was pressed (only occurs when timer runs out)
            result=False #defines result as false

        elif request.form['UserAns'] == "UserAns1": #checks if the user clicked the first button
            if correct==Ans1: #checks whether the correct asnwer was answer 1
                result=True #shows the user got the correct answer
                score=score+1 #adds 1 to the score
            else:
                result=False #user got answer wrong

        elif request.form['UserAns'] == "UserAns2": #checks if the user clicked the second button
            if correct==Ans2: #checks whether the correct asnwer was answer 2
                result=True #shows the user got the correct answer
                score=score+1 #adds 1 to the score
            else:
                result=False #defines result as false

        elif request.form['UserAns'] == "UserAns3": #checks if the user clicked the third button
            if correct==Ans3: #checks whether the correct asnwer was answer 1
                result=True #defines result as true
                score=score+1 #adds 1 to the score
            else:
                result=False #user got answer wrong

        elif request.form['UserAns'] == "UserAns4": #checks if the user clicked the fourth button
            if correct==Ans4: #checks whether the correct asnwer was answer 1
                result=True #shows the user got the correct answer
                score=score+1 #adds 1 to the score
            else:
                result=False #user got answer wrong
        
    elif questionType==2: #checks to see if it was a short answer question
        EnteredAns=request.form["TypeAns"] #obtains the value inputted by the user
        if EnteredAns==correct: #checks to see if the input was correct
            result=True #user got question correct
            score=score+1 #adds 1 to the score

        else:
            result=False #user got question wrong

    buttons="disabled" #disables buttons
    return render_template("quiz.html", questionType=questionType, chosenQ=chosenQ, actualAns=actualAns,
                            Ans1=Ans1, Ans2=Ans2, Ans3=Ans3, Ans4=Ans4, correct=correct, result=result, 
                            buttons=buttons, score=score) #outputs this file when the function is called
        
@app.route('/home') #creates a url path
def Home(): #creates a function for when the path is entered
    global loggedIn, LogUser, username #globalises multiple variables    
    if loggedIn==False: #checks whether the user has logged in
        return render_template("login.html") #outputs this file when the function is called
    else:
        if LogUser=="": #checks to see if the user logged in or registered through the website
            user=username #if user registered then defines user as this
        else:
            user=LogUser #if user logged in then defines user as this
    cursor.execute('SELECT * FROM users WHERE UserName = %s', (user,)) #finds account with this username
    data=cursor.fetchone() #gets the data of the user
    logons=data[5] #holds the amount of times the user has logged in
    QuestionsCorrect=data[6] #holds the amount of questions the user got correct 
    QuestionsAnswered=data[7] #holds the amount of questions a user has answered
    if QuestionsAnswered!=0: #checks to see if the user has answered a question
        CorrectPer=round((QuestionsCorrect/QuestionsAnswered)*100,1) #calculates the percentage of correct answer to 1 decimal place
    else: 
        CorrectPer=0.0 #sets the percentage to 0 if the user hasn't answered a question

    nextstepLog="0"
    if logons>=1: #checks if the user has logged on atleast once
        nextstepLog="5" #defines how many logons are required for the next achievement
        achieve1="logins1.png" #defines the name of the image that corresponds to their achievement
        if logons>=5:  #checks if the user has logged on atleast 5 times
            nextstepLog="10" #defines how many logons are required for the next achievement
            achieve1="logins5.png" #defines the name of the image that corresponds to their achievement
            if logons>=10:  #checks if the user has logged on atleast 10 times
                nextstepLog="25" #defines how many logons are required for the next achievement
                achieve1="logins10.png" #defines the name of the image that corresponds to their achievement
                if logons>=25:  #checks if the user has logged on atleast 25 timea
                    nextstepLog="Complete" #defines that all logon achievements have been completed
                    achieve1="logins25.png" #defines the name of the image that corresponds to their achievement

    nextstepCorrect="10" #defines how many correct answers are required for the next achievement
    achieve2="blanktrophy.png" #defines the name of the image that corresponds to their achievement
    if QuestionsCorrect>=10: #checks the user has got atleast 10 questions correct
        nextstepCorrect="50" #defines how many correct answers are required for the next achievement
        achieve2="correct10.png" #defines the name of the image that corresponds to their achievement
        if QuestionsCorrect>=50: #checks the user has got atleast 50 questions correct
            nextstepCorrect="100" #defines how many correct answers are required for the next achievement
            achieve2="correct50.png" #defines the name of the image that corresponds to their achievement
            if QuestionsCorrect>=100:  #checks the user has got atleast 100 questions correct
                nextstepCorrect="250" #defines how many correct answers are required for the next achievement
                achieve2="correct100.png" #defines the name of the image that corresponds to their achievement
                if QuestionsCorrect>=250:  #checks the user has got atleast 250 questions correct
                    nextstepCorrect="Complete" #defines that there are no more correct answer achievements left
                    achieve2="correct250.png" #defines the name of the image that corresponds to their achievement

    nextstepAnswered="10" #defines how many questions answered are required for the next achievement
    achieve3="blanktrophy.png" #defines the name of the image that corresponds to their achievement
    if QuestionsAnswered>=10: #checks the user has answered atleast 10 questions
        nextstepAnswered="50" #defines how many questions answered are required for the next achievement
        achieve3="answered10.png" #defines the name of the image that corresponds to their achievement
        if QuestionsAnswered>=50: #checks the user has answered atleast 50 questions
            nextstepAnswered="100" #defines how many questions answered are required for the next achievement
            achieve3="answered50.png" #defines the name of the image that corresponds to their achievement
            if QuestionsAnswered>=100: #checks the user has answered atleast 100 questions
                nextstepAnswered="250" #defines how many questions answered are required for the next achievement
                achieve3="answered100.png" #defines the name of the image that corresponds to their achievement  
                if QuestionsAnswered>=250: #checks the user has answered atleast 250 questions
                    nextstepAnswered="Complete" #defines that all questions answered achievements have been completed
                    achieve3="answered250.png" #defines the name of the image that corresponds to their achievement

    cursor.execute('SELECT * FROM users ORDER BY TotalScore DESC;') #gathers all usernames from the database in descending order of score
    data2=cursor.fetchall() #gets all data from database from criteria above
    name1=data2[0][1] #holds the value of the first name  
    score1=data2[0][6] #holds the value of the first score
    name2=data2[1][1] #holds the value of the second name 
    score2=data2[1][6] #holds the value of the second score
    name3=data2[2][1] #holds the value of the third name 
    score3=data2[2][6] #holds the value of the third score
    name4=data2[3][1] #holds the value of the fourth name 
    score4=data2[3][6] #holds the value of the fourth score
    name5=data2[4][1] #holds the value of the fifth name 
    score5=data2[4][6] #holds the value of the fifth score
    #returns the home page and passes through many variables to then be displayed on the screen
    return render_template("Home.html", logons=logons, QuestionsCorrect=QuestionsCorrect, QuestionsAnswered=QuestionsAnswered, 
                            CorrectPer=CorrectPer, name1=name1, score1=score1, name2=name2, score2=score2, name3=name3, score3=score3, 
                            name4=name4, score4=score4, name5=name5, score5=score5, nextstepLog=nextstepLog, 
                            nextstepCorrect=nextstepCorrect, nextstepAnswered=nextstepAnswered, achieve1=achieve1, 
                            achieve2=achieve2, achieve3=achieve3)

if __name__ =="__main__":
    app.run(debug=True) #allows the website to run
