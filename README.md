# OTF Data

Create a CSV file from Orange Theory Fitness workout summary emails using a browser-based UI.

## Installation

The code is available from [GitHub](https://github.com/JimmyVanHout/otf_data). Install the dependencies:

```
pip3 install flask
pip3 install bs4
```

## Gmail Account Configuration

If you chose to use the forwarding feature (see below), you will need to temporarily [disable two-factor authentication](https://support.google.com/accounts/answer/1064203?hl=en&co=GENIE.Platform%3DDesktop) and [allow "less secure app" access](https://support.google.com/accounts/answer/6010255?hl=en) in your [Google account security settings](https://myaccount.google.com/intro/security) for the account you wish to forward from. It is recommended that you [enable two factor authentication](https://www.google.com/landing/2step/) and [disable "less secure app" access](https://support.google.com/accounts/answer/6010255?hl=en) after you have finished running the program, in order to maintain the security of your account.

The new Gmail account that you will likely want to create (also see below) should permanently have its two-factor authentication disabled and permission for "less secure app" access turned on, as these settings are required for the main functionality of the program.

## Usage

Run:

```
python3 otf.py [--browser|--terminal|--help]
```

`--browser` specifies to run the browser user interface (default).

`--terminal` specifies to run the terminal user interface.

`--help` brings up the help screen.

This program should be used to extract data from `otbeatreport@orangetheoryfitness.com` emails to a CSV file. When the program is run, it searches for the configuration file `config.txt`. If it is not present, the user interface will display and the entered data will be saved to the new configuration file. Since the configuration file contains the user's **unencrypted** email password, you will likely want to set up a new Gmail account to use with this program (see below). For the email from which you normally receive `otbeatreport@orangetheoryfitness.com` emails, set up a filter to forward all incoming emails from `otbeatreport@orangetheoryfitness.com` to the new email you just created (again, see below). Using this setup, the security of your primary email account remains the same since only the password of the new account is stored in plain text in the configuration file. While there is no reason that this password should be compromised if proper security precautions are taken, in the event that it were, the only compromised data would be the workout summaries from `otbeatreport@orangetheoryfitness.com`.

Therefore, the following steps should generally be taken when using the program:

1. Create a new [Gmail account](https://support.google.com/mail/answer/56256?hl=en).

1. Set up a [filter](https://support.google.com/mail/answer/6579?hl=en) on the account that typically receives `otbeatreport@orangetheoryfitness.com`. The filter should forward all future mail from `otbeatreport@orangetheoryfitness.com` to the new Gmail account.

1. Perform the configuration steps outlined in the [Gmail Account Configuration](#gmail-account-configuration) section.

1. Run the program (see above). Select the option to forward all past emails from `otbeatreport@orangetheoryfitness.com` to the new account. To make the program run faster in the future, select the option to only search for new `otbeatreport@orangetheoryfitness.com` emails--this searches only for emails received on or after the latest workout record present in the data file, `data.csv`. Since the data file does not exist when first running the program, all emails will be searched for the first time it is run regardless of whether the option is selected.

The program will then forward all the past emails to your new account, and it will generate a `data.csv` file containing the workout data. Errors reading the data are written to standard output. The error rate in testing was typically very small. Erroneous data is not written to the data file.

After creating the new Gmail account, setting up the filter, and running the program for the first time with the forwarding option selected, you will not need to repeat these steps the next time you want to run the program to obtain the latest data, nor will you need to go through the configuration step. Simply run the program whenever you want to get the latest data.
