### Project
LoveTest50

### Python/Flask
For the project, I implemented it in Python and used Flask to run it.

### static
In the static directory, the images that I used are located there as well as the css stylesheet.

### templates
The templates directory contains all the html templates that are displayed to the user through their use of the app. In percent.html, five different images can be displayed based on the compatibility of a couple (splitpct). This is done with javascript, and one hidden value is used only for the javascript object listener in order to access the percentage. Apology.html and layout.html are similar to Finance's own, but apology instead is an image of a corgi (much cuter compared to the previous cat), and layout has been modified for the app's own functions and appearances, including an icon change.

### project.db
project.db is a database that contains three tables: 1) users, which contains registered users' id, username, and hashed password, 2) searches, which contains users' compatibility searches (user's id, both inputted names, the percentage given), and 3) triangle, which contains users' love triangle searches (user's id, all three inputted names, and the best couple. This is used to implement the register, login, logout, and history features of the app.

### helpers.py
helpers.py is implemented with some code as Finance from Week 9, but the API used is the Love Calculator API by Ajith Joseph. The api key is not hardcoded into helpers.py because of the potential security issues with having the value exposed inside of the codespace, so instead it has to be exported each time (export API_KEY=value) the codespace restarts for the extra layer of security.

### app.py
app.py is also implemented with some code as Finance, such as login, logout, register, etc. The / route simply leads to the homepage file. 

The /compatibility route can be accessed through GET and POST, GET being the way to access the form, and POST being the way that the form is submitted and leads to percent.html. The percentage is calculated by ensuring that two names are indeed submitted to the form. Then, the two values are passed into the love_calculator function located in helpers that returns answer, which is a text similar to this:

    "fname":"John""sname":"Alice""percentage":"46""result":"Can choose someone better."

In order to only attain the numerical percentage and the quote at the end, answer is split (and cast as an int for splitpct). These values are inserted into the searches table for compatibilty history, and given to percent.html to display the results.

The /lovetriangle route can be accessed through GET and POST, GET being the way to access the form, and POST being the way that the form is submitted and leads to either solvedtriangle.html or unsolvable.html. The best couple is calculated by doing the same process that compatibility did, but three times for each possible couple. Then, the three percentages are compared and the highest percentage determines the most compatible couple, if any, which is inserted into the triangle table to be used for love triangle history, and given to solvedtriangle.html, or unsolvable.html in the case of two or three equally compatible couples.

/history and /triangle can be accessed only with GET (clicking on the button in the navigation pane), and are very similar in which they both lead to html files that display the user's searches in their respective fields (compatibility and love triangle) by using db.execute to only retrieve that specific user's information from the tables searches and triangle in project.db