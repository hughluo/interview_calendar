# interview_calendar

## Description

A Flask + Mongodb based interview calendar that has following features:
* set slots for both candidates & interviewers via API
* query for interview slots matching via API

Please refer to api documents under the directory api_doc/ for more details.




## File lists

 ### |- interview_calender/
    |- venv/                   virtual environments
    |- api_doc/
      |- add_slot.md           api document about adding slot for both candidate and interviewer
      |- matching.md	   api document about get matching result
	|- app/
	  |- api/      
        |- __init__.py         run the server to test by running this, it should be run at localhost:5000
        |- error.py            route for api error handlers
        |- candidates.py       route for candidates relative APIs: add slot and get matching result
        |- interviewers.py     route for interviewers relative APIs: add slot
    |- main/
      |- __init__.py
      |- admin.py              an route to create new Candidates and Interviewers (just for convenience)
    |- models/
      |- __init__.py           base Class Models, parent class of Candidate and Interviewer
      |- candidate.py          class Candidate
      |- interviewer.py        class Interviewer
    |- templates/
      |- admin.html            a simple admin interface
    |- config.py                 
    |- utils.py                storage utilities functions
    |- test.py 	           a unit test, it can help you to understand the usage of APIs. 
                                  (Please run the app/__init__.py first!)                              
 

