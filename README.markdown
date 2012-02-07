Text Automator v0.1
===================

A framework for doing things with texts
---------------------------------------

This is a framework based on the Google Voice API in python that you can find [here](http://code.google.com/p/pygooglevoice/)
Currently only reminders are implemented.

To test out the reminder service, all you have to do is text your request to 201-308-3785.
The proper syntax for reminders is: "Remind me to X in/at Y".

###Current to do list:
-  Move to an actual server
-  Alarm clock feature
-  Make the replies friendlier
-  Confirmation texts so you know if your reminder was processed correctly
-  More powerful syntax analyzing
-  More compatible ways of describing time
-  Various small bugs in current syntax reading
-  Correctly delete incorrectly formatted texts and old texts

###Lineup for v0.2
-  Move to an actual server
-  Make the replies friendlier
-  "12:00" bug
-  Process X hours and Y minutes query

###How to actually use it
1. Go to the website linked above
2. Install the google voice api
3. If you're on linux, you can do this with *sudo easy_install -U pygooglevoice*
4. Setup your google voice info in the ~/.gvoice file.
5. The actual file that checks messages and sends texts is analyzer.py
6. run.sh runs everything sequentially
7. server.sh is a makeshift server that queries google voice every minute for new texts
8. Get crackin'
