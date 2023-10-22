# messageMonster

A central messaging service to automatically send and receive network status messages and reports to various groups and users in the corporate.
  
  The application will be based on a python app that accesses various servers and services to send out alerts and notifications.
  It will also allow users to send messages to other users and groups.
  
  The messages will be sent using MQTT as we don't want to use old 21st century methods such as email.

  Other technoligies used will be web API's and servers along with AI to generate humanly readable summary reports for management. 

  IT Admins will be able send command messages to the script such as BACKUP_DB_ONE, RESTART_WEBSERVER_2 etc from their phones while down the pub.

  A typical alert may look like this: NAS_1 going slow, CRM_DB failure, CPU_Temp = 48c 

  Lets create a monster!
