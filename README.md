# py-vrmjuice
Python 3 bindings for Victron's JUICE API

You can find out more about the JUICE API here: [https://juice.victronenergy.com/build/apidoc/](https://juice.victronenergy.com/build/apidoc/)

Python 2 is not supported at this time.

## Prerequisites
You must have the following python 3 modules already installed:

* requests
* json
* logging

Please consult your distribution package manager to install the appropriate packages.

You can verify that you have the above modules installed by invoking python3 and importing the modules:

	>>> import requests

	>>> import json

	>>> import logging

If you do not receive any ImportError exceptions, then you have all the required modules installed.

## Usage
You need to initialize the class with your VRM username and password:

juice = VictronJuice("johnsmith@example.com","Sup3rSecr3t!")

The class will handle authentication with the JUICE API after this step

### Methods
We aim to provide as much compatibility with the JUICE API as possible.

#### get_site
You provide the site_id, the method returns JSON data from the API. Functionally equivalent to JUICE API sites/get_site

#### get_sites
The method returns JSON data on all sites the user has been granted access to. Functionally equivalent to the JUICE API sites/get

#### get_site_ids
The method returns a list of site_id integers that the user has been granted access to. No functional equivalent provided by JUICE API

#### get_site_attributes
You provide the site_id, the method returns JSON data on all attributes available from equipment installed on site. Functionally equivalent to the JUICE API sites/get_site_attributes

#### get_site_attributes_by_code
You provide the site_id, and the attribute codes in an array, the method returns JSON data on the provided attribute codes. Functionally equivalent to the JUCIE API sites/attributes_by_code

For a list of valid attribute codes (as of 24.02.2016) see the file: attribute_codes.md

This is a list we have compiled through observation. We could not find any official Victron documentation on the attribute codes, so the list may be incomplete.

#### get_energy_data
You provide the site_id, the method returns JSON data of the energy produced/consumed by the equipment installed. Functionally equivalent to the JUICE API sites/get_energy_data

#### get_lost_contact
You provide a timeout value in seconds, and the method returns a list of sites which have a last update time exceeding the threshold. Useful for determining if sites have communications issues. No functional equivalent provided by JUICE API

