# Name
Chronically Pathological

# Description
The corporate utility server is constantly running out of disk space, and the senior IT admin couldn't be bothered to build a proper log rotation on the machine. Instead, they slapped together a rushed automated cleanup job and pawned the maintenance off to the new hire.

To keep their fragile automation running, they gave the junior admin a single, highly restricted "band-aid" script. Unfortuantely for the company, the junior admin fell for your E-Girl impression and gave you the password they reuse everywhere. 

Can you figure out how their messy solution is glued together, hijack the system automation, and escalate your privileges to uncover the flag?

Access Information:
Connect to your dedicated instance using the credentials below:

ssh -p {{ port }} junior_admin@{{ host }}

Password: dont_get_paid_enough