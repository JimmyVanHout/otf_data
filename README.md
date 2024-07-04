# OTF Data

> **Notice:** This repository has been archived and will no longer be maintained. The [repository](https://github.com/JimmyVanHout/ot_fitness_data) for the associated site, [OTFitnessData.com](https://www.otfitnessdata.com), will also no longer be maintained, and the site will no longer be hosted.

Create a CSV file from OrangeTheory Fitness workout summary emails using a browser-based UI. Optionally, after running the program, upload the file to [OTFitnessData.com](https://www.otfitnessdata.com).

## Installation

Install the code from [GitHub](https://github.com/JimmyVanHout/otf_data):

```
git clone https://github.com/JimmyVanHout/otf_data.git
```

Install the dependencies:

```
pip3 install flask
pip3 install bs4
```

Note that this program writes the files `config.txt` and `data.csv`, and **it will overwrite any** `config.txt` **or** `data.csv` **files that already exist in the same directory**.

## Usage

Run:

```
python3 otf_data.py [--browser|--terminal|--help] [--store-password]
```

`--browser` specifies to run the browser user interface (default).

`--terminal` specifies to run the terminal user interface.

`--help` brings up the help screen.

`--store-password` specifies whether the password should be stored, unencrypted, in the configuration file

This program should be used to extract data from `otbeatreport@orangetheoryfitness.com` emails to a CSV file. When the program is run, it searches for the configuration file `config.txt`. If the file is not present, the user interface will display and the entered data will be saved to the new configuration file. Note that the browser-based user interface does not retrieve a web page from the internet but rather from a local server that is temporarily run on the host machine.

The program will optionally perform a one-time batch forward of all workout summary emails found in your regular Gmail account during the first run of the program and will send them to the new Gmail account you will create. The main functionality of the program, performed first during setup and then on each subsequent run, is to extract the data from all of the workout summary emails found in your new account and create a CSV file containing the data.

The following steps are recommended the first time you use this program:

1. Create a new [Gmail account](https://support.google.com/mail/answer/56256?hl=en).

1. Set up a [filter](https://support.google.com/mail/answer/6579?hl=en) on the account that typically receives `otbeatreport@orangetheoryfitness.com` emails. The filter should forward all future mail from `otbeatreport@orangetheoryfitness.com` to the new Gmail account.

1. Set up an [application-specific password](https://support.google.com/mail/answer/185833?hl=en-GB) on your new Gmail account. Also set one up on the account that typically receives the workout summary emails if you intend use the forwarding feature.

1. Run the program. In the configuration menu that appears:

    * Select the option to forward all past emails from `otbeatreport@orangetheoryfitness.com` to the new account.
    * Enter the appropriate email addresses and the application-specific passwords you set up previously.
    * For the originating email addresses, enter `otbeatreport@orangetheoryfitness.com` as well as the Gmail address for which you set up the filter.
    * To make the program run faster in the future, select the option to only search for new `otbeatreport@orangetheoryfitness.com` emails--this searches only for emails received on or after the latest workout record present in the data file, `data.csv`. Since the data file does not exist when first running the program, all emails will be searched for the first time it is run, even if the option is selected.

The program will then forward all the past emails to your new account, retrieve the data from the new account, and generate a `data.csv` file containing the workout data. Erroneous data is not written to the data file and is instead written to standard output. The error rate in testing was typically very small.

After the initial setup, you will **not** need to repeat all of these steps the next time you want to run the program to obtain the latest data, nor will you need to go through the user interface. Simply run the program whenever you want to get the latest data.
