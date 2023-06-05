# VAC-Checker
A discord bot that uses the steam api to check if a user is VAC banned. You can manually add steam accounts to the database and check their status. Once added any you will get a pm every hour for any account banned.

Available commands:

Default prefix - "!"

status <steamID> - Check the status of a specific account
add <steamID> - Add a steam account to the database
remove <steamID> - Remove a steam account from the database
setPrefix <new prefix> - Change the prefix for the server
checkPrefix - Shows current prefix for the server
help - Shows this help menu
  
![image](https://github.com/deChaplin/VAC-Checker/assets/85872356/bdcde8f5-397d-4ee3-88ff-c848328f6d95)

Create a .env file inside the Bot folder. This will contain your discord token and steam api key.  

"TOKEN=12345.123.12345"  
"KEY=12345"


TO DO:

    1. Add a command to check the status of all your accounts in the database
    2. Subscribe option for private message updates
    3. Remove accounts when confirmed banned