# UTRegistrationSuite
A collection of python scripts that make up for faults in UT's registration system.

# Usage
In autoadd.py, there are several variables that you have to change.

semester is the semester for which you want to register

course_sched_num is the course schedule number, found in the url of the course schedule

class_num is the course number of the class you want to add

drop_class_num is the course number of the conditional dropped class

eid is your eid

eid_pass is your eid password

is whether or not you want to conditionally drop a class to add the desired class

repeat is whether or not you want to repeat the operation until the class is added

Additionally, you must register for a Twilio account and input your id and auth token.

Run by typing py autoadd.py into terminal while in the folder's directory.
