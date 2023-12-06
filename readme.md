# ![ADD Banner Photo]('change to relational link"./src/images/final/finalreadmeBanner.jpg"')
An eCommerce web application written in Python created by Leah Livingston.

[Click Here to Check out the App Now]('change to app link"https://fitforecast-dc33e66f392f.herokuapp.com/"')

---
### **Project Idea and Description**

My goal for the capstone project is to add a well-rounded fourth piece to my Github portfolio. The idea is to keep it simple, while showing off two new skills: 
[1] an eCommerce functionality via [Stripe's API](https://stripe.com/docs/development/quickstart?lang=python) 
[2] the ability to code in Python. 


Without a clear picture on the details, the idea is to build a responsive website with the ability to take a quiz to learn your Ayurvedic dosha. This quiz ends on a landing URL educating you on your dosha type and provides recommended foods based on quiz answers. There will be a short sales funnel leading to a prompt to buy a traditional Ayurvedic copper tongue scraper.


[Click Here to Check out the App Now]('change to app link"https://fitforecast-dc33e66f392f.herokuapp.com/"')



---
### **Tech Stack**
It's a responsive eCommerce web application hosted on Heroku utilizing Python, HTML, CSS, and Stripe payments API to sell retail.

##### **API Details**
The application utilizes the third-party API from [Stripe](https://stripe.com/docs) (allowing free test development). 
[ADD MORE DESCRIPTION HERE ONCE GETTING SETUP]

![ADD API Details]('change to relational link"./public/images/pitch/apiDetails.png"')


---
## ERDs
![ADD ERD]('change to relational link"./src/images/final/finalERD.png"')


---
### **Restful Routing Chart**

| HTTP METHOD | URL | CRUD | Response | Notes |
| -------------------- | ------------- | ---- | -------- | ----- |
| `full index of items`  |   |   |   |   |
| GET | `/` | Read | View Dosha | retrieves dosha information  |
| GET | `/fetch-stripe-data` | Read | View API connection | retrieves ability to process payments  |



---
### **Screenshots of the Web Application**

###### Home Page
![Wireframes]('change to relational link"./src/images/final/currentWireframes.png"')



---
### **Credit**

A big thank you to Weston Bailey, Rondell Charles, April Gonzalez, Tom Kolsrud, and Ben Manley for your support. 



---
### **MVP Goals**

###### User Stories
- [ ] AAU, I want to learn about Ayurveda and how it will help me be healthy through a balanced lifestyle.
- [ ] AAU, I want to see a landing page with information without having to log-in.
- [ ] AAU, I want the ability to take a quiz to learn my Ayurvedic dosha type.
- [ ] AAU, I want the application to determine my dosha type based upon my provided answers.
- [ ] AAU, I want the application to suggest a food recommendations, sleep schedule, yoga postures, and other preventative health methods to find whole-body balance based upon my dosha type.
- [ ] AAU, I want the ability to purchase a traditional Ayurvedic copper tongue scraper.
- [ ] AAU, I don't want to feel forced to buy the copper tongue scraper. 

###### Style
- [ ] Include basic CSS to successfully utilize the website
- [ ] Include top hamburger navigation including 'Home', 'Take Quiz', and 'Shopping Cart' page links
- [ ] Include 15 individual page views, including:  'Home', 'Quiz', 'Your Dosha', and 'Shopping Cart' screens
- [ ] Include visual optimization for mobile view

###### Functionality
- [ ] Include educational information about Ayurveda and prompt to start quiz on landing page
- [ ] Include a 10-question quiz that will determine dosha type based off provided answers
- [ ] Include ability for application to end quiz on that dosha type's page after determining dosha type
- [ ] Include "suggested lifestyle" based on dosha type
- [ ] Include opportunity to purchase a product
- [ ] Include shopping cart functionality 
- [ ] Include Stripe payments API 



---
### **Stretch Goals**

###### User Stories
- [ ] AAU, I want the ability to create a profile once I'm ready to purchase something.
- [ ] AAU, I want the ability to log-in and reference my dosha type and the recommendations from time to time.
- [ ] AAU, I do not want other users to see my quiz results or purchase history.
- [ ] AAU, I want the ability to log-out.

###### Style
- [ ] Include a 'Brand Kit' for future development use
- [ ] Include CSS styling following a 'Brand Kit'
- [ ] Include visual optimization for desktop and tablet

###### Functionality
- [ ] Include ability to create a new user profile upon purchase of a product
- [ ] Include ability for user to view their profile
- [ ] Include ability to log-in via oAuth in top navigation
- [ ] Include ability for user to view past purchases
- [ ] Include ability for user to log-out
- [ ] Include functionality that allows each user to only see their own purchase data
- [ ] Include more in-depth quiz option for upsell opportunity (i.e. first 10 basic, add 2 options for in-depth nature dosha and in-depth nurture dosha.)
- [ ] Include opportunity to sign up for quarterly self-care package
- [ ] Include ability to save dosha scores in profile
- [ ] Include ability to re-test from time to time in order to track changes in balance
- [ ] Include ability to upload photos of hands, tongue, and eyes to monitor health
- [ ] Include ability to sign up for a one-hour session with a traditional Ayurvedic doctor in India.
- [ ] Includes ability to sign up for monthly newsletter with educational content and more upsell opportunities