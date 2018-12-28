#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv, os
import requests
from bs4 import BeautifulSoup
import json
import re
import sys
from json import JSONDecodeError

def profile_address(insta_id):
  """returns instagram profile address"""
  insta_url = "https://instagram.com/"+insta_id
  return insta_url

def tag_address(insta_id):
  """returns instagram tag address"""
  insta_url = "https://instagram.com/explore/tags/"+insta_id
  return insta_url

def find_latest(insta_url, tag):
  """find latest post address from instagram profile URL"""
  try:
    soup = BeautifulSoup(requests.get(insta_url).text, 'lxml')
    script_tag = soup.find('script', text=re.compile('window\._sharedData'))
    shared_data = script_tag.string.partition('=')[-1].strip(' ;')
    result = json.loads(shared_data)
    if tag == 0:
      tmp = result['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']
    else:
      tmp = result['entry_data']['TagPage'][0]['graphql']['hashtag']['edge_hashtag_to_media']

    if (tmp['count']!=0):
      latest_code=tmp['edges'][0]['node']['shortcode']
    else:
      return 'NULL'
  except (KeyError, JSONDecodeError):
    return 'NULL'

  latest_url = "https://instagram.com/p/"+latest_code
  return latest_url

def duplicate_check(insta_id, filename):
  if (os.path.isfile(filename)!=0):
    return -1
  with open(filename, newline='', encoding='utf-8') as f:
      reader = csv.reader(f)
      try:
          for idx,row in enumerate(reader):
              if(row[0]==insta_id):
                return idx
          return -1
      except csv.Error:
          print('CSV File Error (dup_check)!')

def add_subscribe(insta_id, filename, tag):
  dup=duplicate_check(insta_id, filename)
  if(dup==-1):
    with open(filename, 'a', encoding='utf-8') as newFile:
      newFileWriter = csv.writer(newFile)
      try:
        if tag==0:
          latest_url = find_latest(profile_address(insta_id), tag)
        else:
          latest_url = find_latest(tag_address(insta_id), tag)
        if latest_url=='NULL':
          # print("page doesn't exist or private account")
          return -4
        else:
          newFileWriter.writerow([insta_id, latest_url])
        return -2
      except IndexError:
        return -4
        # print("page doesn't exist or private account")
  else:
    # print("duplicated subscription request")
    return -3

def unsubscribe(insta_id, filename):
  row_num = duplicate_check(insta_id, filename)
  ROWS_TO_DELETE = {row_num}
  if(row_num == -1):
    # print("there is nothing to unsubscribe")
    return -3
  else:
    with open(filename, 'rt', encoding='utf-8') as infile, open('outfile.csv', 'wt', encoding='utf-8') as outfile:
      outfile.writelines(row for row_num, row in enumerate(infile, 0)
                          if row_num not in ROWS_TO_DELETE)
    os.remove(filename)
    os.rename("outfile.csv", filename)
    return -2

def print_subscribe_list(filename):
  ans = []
  with open(filename, newline='', encoding='utf-8') as f:
      reader = csv.reader(f)
      try:
          for row in reader:
              ans.append(row[0])
          return ans
      except csv.Error:
          print('CSV File Error!')

def initiate_list(filename):
  """remove csv file"""
  if os.path.exists(filename):
    os.remove(filename)

# if __name__ == "__main__":
#   import argparse
#   parser = argparse.ArgumentParser()
#   parser.add_argument("--id", help="Instagram ID")
#   args = parser.parse_args()
