# Flight Departure Delay API

The Flight Departure Delay API is a web server application that fetches the flight departure and delay data from usecosmos.com, processes this data and serves it via API endpoints. This application is built with Python and Flask framework.

## Main Features

* Fetches the flight schedules and delay information from external APIs.
* Merges and processes the data to include delay information for each flight. 
* Provides API endpoints to query flight information with filters.
* Includes a user-friendly web interface to browse the flight data.
* Peridically updates the data so it remains current.

## Installation

```git clone https://github.com/vproiss/Flight-Departure-Delay-API.git```

## Create and environment

## Install the packages

```sh
pip install -r requirements.txt
```

## Directory structure
```
.
├── templates/
│   └── index.html
├── app.py
├── fetch_data.py
├── test_app.py
├── test_fetch_data.py
├── requirements.txt
└── README.md
```
