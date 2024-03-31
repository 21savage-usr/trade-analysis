# trade-analysis

trade-analysis
Getting Started
Before using the trade-analysis project, you need to obtain an API key from Alpha Vantage. This key will allow you to fetch financial data through the Alpha Vantage API.

Step 1: Claim Your Alpha Vantage API Key
Visit the Alpha Vantage website.
Follow the instructions to claim your free API key. You will be prompted to enter your email address and agree to the terms of service.
Step 2: Set Your API Key as an Environment Variable
For the trade-analysis project to access the Alpha Vantage API, you must set your API key as an environment variable named ALPHA_VANTAGE_API_KEY. Here's how you can do that on Windows, macOS, and Linux:

Windows
Open the Start search, type cmd, right-click on the Command Prompt, and choose "Run as administrator".

In the Command Prompt, set your API key as an environment variable by running the following command (replace YOUR_API_KEY with the key you obtained from Alpha Vantage):

cmd
Copy code
setx ALPHA_VANTAGE_API_KEY "YOUR_API_KEY" /M
Note: The /M option sets the variable system-wide. Omit /M if you prefer to set the variable for the current user only.

macOS and Linux
Open the Terminal.

To set your API key as an environment variable, add the following line to your .bash_profile, .bashrc, or .zshrc file (depending on which shell you use and whether you're on macOS or Linux). Replace YOUR_API_KEY with the key you obtained from Alpha Vantage:

sh
Copy code
export ALPHA_VANTAGE_API_KEY="YOUR_API_KEY"
Save the file and then run the following command in the Terminal to apply the changes:

sh
Copy code
source ~/.bash_profile  # or the appropriate file you edited
Next Steps
After setting up the ALPHA_VANTAGE_API_KEY environment variable, you can proceed with the installation and usage instructions of the trade-analysis project as detailed below.