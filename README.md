# Udacity Project Logs Analysis

In this project I created a reporting tool that prints out reports (in plain text) based on the data in the database. 
This reporting tool is a Python program using the `psycopg2` module to connect to the database.
It will answer three questions with database queries:

1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?

## Setup

- Make sure you have the following installed:
    - python
    - git
    - Vagrant
    - VirtualBox

- Clone the master fork from https://github.com/josejimenezjr0/logsanalysis.git
- Clone the Vagrant machine from Udacity from https://github.com/udacity/fullstack-nanodegree-vm
- Inside the vagrant subdirectory run the command `vagrant up` then `vagrant ssh`
- Next, [download the data here.](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip) You will need to unzip this file after downloading it. The file inside is called newsdata.sql. Put this file into the vagrant directory, which is shared with your virtual machine.

- To build the reporting tool, you'll need to load the site's data into your local database. To load the data, use the command `psql -d news -f newsdata.sql`.

## How to run

- From your computer in a terminal execute the following code within the directory where you cloned the logsanalyisis.git repository

```
python logsanalysis.py

```

The questions and results should display!
