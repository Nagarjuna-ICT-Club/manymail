# manymail
Ever had the need to send mails to multiple people but change only their names? Well, `manymail` is the solution.

## Structure
It has three tabs: `Email Template`, `Recipients`, `Sender Info`

### Email Template
This tab has two fields: `Subject` and `Email template`

#### Subject
The email subject

#### Email template (Not the tab, but the field)
- Write your email template
- Select the part of the text that needs to be changed for every email
- Click on "**Make Selected Text a Variable**"

### Recipients
This tab contains two fields: `Recipient Info` and `Preview`

#### Recipient Info
- Enter recipient info(one per line) in one of the two formats:
    - name \<email\>
    - name email
- Example:
    - user \<user@gmail.com\>
    - user user@gmail.com
- Both of these syntax are valid

#### Preview
This lets you see the email for multiple recipients before sending them.

### Sender Info
Fill in the sender's `email` and `password`.

**Note: If you are using gmail, you need to use gmail app password instead of your actual password.**

## Installation
- Clone the project
```
git clone https://github.com/Nagarjuna-ICT-Club/manymail.git
```

## Run
Nagivate to the project. (**/path/to/manymail**)
```
python3 main.py
```

## Requirements (Optional)
If it is giving dependency errors
```
pip install -r requirements.txt
```