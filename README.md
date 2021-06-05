# Django_TripBuddyApp
A travel social media app with login and registration that can handle all of the CRUD operations to create, read, update, and destroy trips. App checks that user is in session in order to update and delete only the trips the user created. Allows the user to join trips created by other users. 

1. Main route displays login and registration template
2. POST to /register route - creates new user record in database
3. GET to /login route - retrieves user record to put in session while user is logged in. 
4. GET to /logout route - retrieve user id to clear from session
5. GET to /dashboard route- reads all trips created by user in session, get all trips joined by user in session, and all trips not joined by user in session.
6. GET to /new/trips route - displays form template to create new trip.
7. POST to /trips/create - creates new trip in database
8. GET to /trips/id route - retrieves fields from trip record specified in route
9. POST to /join/id route - creates new record for user to join trip
10. GET to /trips/edit/id - retrieves edit form template
11.  PUT to /trips/id/update - updates existing record
12. DELETE to /trips/delete/id - Destroys trip record specified in route
