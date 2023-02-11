### Project
LoveTest50

### Background
LoveTest50 uses the Love Calculator API from https://rapidapi.com/ajith/api/love-calculator. In order to use this API, you must set up an account at https://rapidapi.com/auth/sign-up. Once an account has been made, you will have access to your own API key in the textbox labeled X-RapidAPI-Key.

### Getting Started
You should have a directory named project that contains a Python based website that is run using Flask. Before the website can be run, the API key must exported using the following command in your terminal:   $ export API_KEY=value
where value is your API key that was previously set up.

### Running
After the API key has been set up, you can start Flask’s built-in web server (within project/) with:    $ flask run
Visit the URL outputted by flask to see the distribution code in action. 

### Register/Login
You will reach an inital webpage that you must register an account for, using the register button. You will have to provide a unique username as well as a password. Any incomplete portion will return an apology. DO NOT use a password you use for other sites. Once registered, you can log in with the username and password, and have the option to use LoveTest50.

### Homepage
The homepage introduces you to the the app and includes links to three different dating websites, Tinder, Bumble, and Grindr. There is a navigation bar with abilites to access the Homepage, Compatibility, Love Triangle, Compatibility Search History, Love Triangle Search History, and Logout, that are accessible at every page.

### Compatibility
Compatibility will lead you to a form that takes in the names of the two people whose compatibility is being tested, before displaying the compatibility and a related image. Any incomplete portion will return an apology.

### Love Triangle
LoveTriangle will lead you to a form that takes in the names of the three people whose compatibility is being tested, before displaying the names of the most compatibile couple if possible. Any incomplete portion will return an apology.

### Compatibility Search History
Compatibility Search History will lead you to a table that displays every compatibility search the user requested, with the two people and percentage displayed.

### Love Triangle Search History
Love Triangle Search History will lead you to a table that displays every love triangle search the user requested, with the three people and best couple displayed.
