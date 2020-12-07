# YouTutor
Welcome to YouTutor! YouTutor is a video playlist and tutoring platform.

Right now, YouTube hosts video solutions to programming problems but little opportunity to interact directly with content creators. Tutoring platforms, like Wyzant, do show you reviews for tutors but not how their teaching style or demonstrating their knowledge in a subject.

YouTutor believes there is a significant number of people on YouTube that want to interact directly with content consumers for a negotiated price and Wyzant tutors want to create YouTube tutorials that will drive advertisement to themselves. 

YouTutor is that marketplace. 

With margins on YouTube being $0.001 per view and margins on Wyzant being 25% of a tutor's negotiated hourly rate, there is an opportunity to serve the market that exists between these two platforms and offer missing elements of each platform. 

From a student perspective, I want to be able to post what I'm looking for, be referred to videos that will answer my question or speak to someone that is demonstrably knowledgeable about the sought area.

## Next Steps
YouTutor has five educating streamers interested in posting their videos on the YouTutor platform.

# ToDo: Missing for current project due date

### Inconsistent DRY-ness
- There is so much code, especially in Django and HTML that is repeated. Between Listing, Tutor cards. I probably could have used one javascript function that would insert and replace all the info on one html page.

### Category
- Can not create new categories yet
- Category Filtering: The way categories for layout dropdown is working is not good practice. If I were to do this project in React, context would be used in order to update content at a higher level. Redux may also be good for filtering. 

### profile tagline and other profile components
- On profile page you are able to write more than what is alotted in the models and have it be saved because of the way the form was coded. In retrospect, I should have created a new ModelForm in views to take in specific elements for some forms so that you wouldn't be able to enter more info in to these text areas than alotted in the models. 

# ToDo: Outside of scope of project due date
### Direct Messaging
- DNE yet. 

### Tutor ability to post their own videos
- DNE yet.

### Comments
- planning to turn comments into reviews / opportunities for people to refer. You will see comments still exist but I haven't done anything with them, yet. 

### Create Listing File upload
- students would have the ability to attach files for tutors to look at before commenting.

### Student looking for x level of expertise. 
- As a student, sometimes I just want to talk to someone that has a little bit of knowledge about the subject so that we can both try to understand it together. OTher times I want a real pro. 


### referrals / @tutor notification
- DNE yet.

### Payment methods Strategy:
- Student pays at the before session starts and on setting up date for tutor session, during which, payments are held in escrow until completing the session.
- Student payment method to be connected to a real account. 

### YouTutor background check status
- If tutor, background check optional

### YouTutor Testing
- "What level of specialist are you?"
- Aggregating reviews