# NLP-to-the-rescue
DePaul MSDS Capstone Project

You have been hired by an aspiring navigation app company to determine what features are required to become a leader in the navigation app space. You are provided 6 months of Apple AppStore and Google Play Store reviews from all over the world.  Your goal is to use NLP techniques to build a model that can predict the topics associated with each reviews. 

You'll start with simple bag of words techniques to gain some insight and then proceed to build an advanced classifier to represent the review topics and compare across different navigation apps. Along the way you'll have to run translation and overcome some not so friendly emoji's that interfere (or help?) your topic models. Not all topics are equally represented so you may also face some issues around class imbalance when building your classifier.

## Dataset Description

🤔The NLP process will mainly focused on some key 🔑 features to create two thresholds one for positive 👍 rating and one for negative 👎. And depend on the positive rating what features we can get from users’ review, so as to negative. 

``Rating:`` The indicator that can reflect the users' attitude of their reviews, rated from 1 to 5, low to high respectively.

``Subject:`` The subject of a user's review. Some reviews actually leave review body blank, hence the subject may contain the hidden information that we need.

``Body:`` The body of a user's review, and written in multiple languages.

``Translated Subject:`` The auto-translated english version of respective subject of user's review.

``Translated Body:`` The auto-translated english version of respective body of user's review.

``Emotion:`` Some users did marked their emotion by couple of default status, such as happy, sad, delighted, and angry.


