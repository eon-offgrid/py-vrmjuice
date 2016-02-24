#!/usr/bin/env python3
# Copyright (c) 2016 E.ON Off Grid Solutions GmbH
# Original Author: Hal Martin (hal.martin@eon-offgrid.com)

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

import requests
import json
import logging

class VictronJuice:

  def __init__(self,username,password):
    # use logging instead of print for debugging/info messages
    logging.basicConfig(level=logging.DEBUG)
    self.log = logging.getLogger(__name__)
    # initialize the class session object
    self.session = requests.Session()
    # default timeouts
    self.TIMEOUT = 12
    # JUICE API version
    self.api_version = 220
    # verification token
    self.vtoken = 1
    # JUICE URL
    self.juice_domain = "https://juice.victronenergy.com/"
    # login
    self.__login(username,password)


  ###################################################
  #                Internal Functions               #
  ###################################################

  """
  Input:
    VRM username (string, email address), VRM password (string)
  Function:
    Login to VRM, on success sets the class variable self.sessionid used in future requests.
    On failure the self.sessionid variable will be NoneType
  Output:
    sets self.sessionid to a valid sessionid, or NoneType on failure
  """
  def __login(self,username,password):
    url = self.juice_domain + "user/login"
    data = {'username': username, 'password': password, 'version': self.api_version, 'verification_token': self.vtoken}
    try:
      response = self.session.request('POST',url,data=data,timeout=self.TIMEOUT)
      if self.__verify_response(response.status_code):
        response_json = json.loads(response.text)
        self.log.debug("Login successful as %s" % response_json["data"]["user"]["user_info"]["email"])
        self.sessionid = response_json["data"]["user"]["sessionid"]
      else:
        self.sessionid = None
    except requests.exceptions.ConnectionError as e:
      # do you have working DNS?
      return None


  """
  Input:
    response status code
  Output:
    True/False based on status code + log messages if failure
  """
  def __verify_response(self,rstatus):
    if rstatus == 200:
      return True
    elif rstatus == 400:
      self.log.error("Invalid data was supplied as input")
    elif rstatus == 403:
      self.log.error("Specified session is expired")
    elif rstatus == 412:
      self.log.error("API version specified (%s) is too old" % self.api_version)
    elif rstats == 500:
      self.log.error("Internal server error")
    return False


  ###################################################
  #                  Site Functions                 #
  ###################################################

  """
  Input:
    site_id (integer, or integer as string)
  Output:
    Returns JSON data on the specified site
  """
  def get_site(self,site_id):
    url = self.juice_domain + "sites/get_site"
    data = {'sessionid': self.sessionid, 'version': self.api_version, 'verification_token': self.vtoken, 'siteid': site_id}
    try:
      response = self.session.request('POST',url,data=data,timeout=self.TIMEOUT)
      if self.__verify_response(response.status_code):
        response_json = json.loads(response.text)
        return response_json
      else:
        return None
    except requests.exceptions.ConnectionError as e:
      # do you have working DNS?
      return None


  """
  Input:
    None
  Output:
    Returns JSON summary data on each site the user has access to in VRM
  """
  def get_sites(self):
    url = self.juice_domain + "sites/get"
    data = {'sessionid': self.sessionid, 'version': self.api_version, 'verification_token': self.vtoken}
    try:
      response = self.session.request('POST',url,data=data,timeout=self.TIMEOUT)
      if self.__verify_response(response.status_code):
        response_json = json.loads(response.text)
        self.log.debug("Got data on %s sites" % len(response_json["data"]["sites"]))
        return response_json
      else:
        return None
    except requests.exceptions.ConnectionError as e:
      # do you have working DNS?
      return None


  """
  Input:
    None
  Output:
    Returns a list of all idSite that the user has access to (can also be accessed by looping through get_sites data)
  """
  def get_site_ids(self):
    sites = self.get_sites()
    site_ids = []
    for site in range(0,len(sites["data"]["sites"])):
      site_ids.append(sites["data"]["sites"][site]["idSite"])
    self.log.debug("%s sites available" % len(sites["data"]["sites"]))
    return site_ids


  """
  Input:
    VRM site id, instance id (optional)
  Output:
    Returns a list of all attributes available from the site
  """
  def get_site_attributes(self,site_id,instance_id = 0):
    url = self.juice_domain + "sites/get_site_attributes"
    data = {'sessionid':self.sessionid, 'version': self.api_version, 'verification_token': self.vtoken, 'siteid': site_id, 'instance': instance_id}

    try:
      response = self.session.request('POST',url,data=data,timeout=self.TIMEOUT)
    except requests.exceptions.ConnectionError as e:
      # do you have working DNS?
      return None

    if self.__verify_response(response.status_code):
      return json.loads(response.text)["data"]["attributes"]
    else:
      return None


  """
  Input:
    VRM site id, attribute codes, instance id (optional)
  Output:
    Returns a list of all attributes available from the site
  """
  def get_site_attributes_by_code(self,site_id,attribute_codes,instance_id = 0):
    url = self.juice_domain + "sites/attributes_by_code"
    data = {'sessionid':self.sessionid, 'version': self.api_version, 'verification_token': self.vtoken, 'siteid': site_id, 'codes': json.dumps(attribute_codes), 'instance': instance_id}

    try:
      response = self.session.request('POST',url,data=data,timeout=self.TIMEOUT)
    except requests.exceptions.ConnectionError as e:
      return None

    if self.__verify_response(response.status_code):
      return json.loads(response.text)["data"]["attributes"]
    else:
      return None


  """
  Input:
    VRM site id, instance id (optional)
  Output:
    Returns a list of all attributes available from the site
  """
  def get_energy_data(self,site_id,instance_id = 0):
    url = self.juice_domain + "sites/get_energy_data"
    data = {'sessionid':self.sessionid, 'version': self.api_version, 'verification_token': self.vtoken, 'siteid': site_id, 'instance': instance_id}

    try:
      response = self.session.request('POST',url,data=data,timeout=self.TIMEOUT)
    except requests.exceptions.ConnectionError as e:
      # do you have working DNS?
      return None

    if self.__verify_response(response.status_code):
      rdata = json.loads(response.text)
      return rdata["data"]["energyAttributes"]
    else:
      return None


  ###################################################
  #                 Alarm Functions                 #
  ###################################################

  """
  Input:
    Alarm threshold in seconds (e.g. 1 hour = 3600)
  Output:
    Returns a list of sites where the last contact exceeded the provided threshold
  """
  def get_lost_contact(self, threshold):
    import datetime
    import time
    sites = self.get_sites()
    lost_contact = []
    for site in range(0,len(sites["data"]["sites"])):
      if time.mktime(datetime.datetime.utcnow().timetuple()) - sites["data"]["sites"][site]["lastTimestamp"] > threshold:
        lost_contact.append(sites["data"]["sites"][site]["idSite"])
        self.log.info("Site exceeded threshold: %s" % sites["data"]["sites"][site]["name"])
    return lost_contact
