import csv, os
import requests
from bs4 import BeautifulSoup
import json
import re
import sys

filename = 'subscribe.csv'

def profile_address(insta_id):
  """returns instagram profile address"""
  insta_url = "https://instagram.com/"+insta_id
  return insta_url

def find_latest(insta_url):
  """find latest post address from instagram profile URL"""
  try:
    req = requests.get(insta_url)
    html = req.text
    soup = BeautifulSoup(html, 'lxml')
    time.sleep(0.5)
    script_tag = soup.find('script', text=re.compile('window\._sharedData'))
    shared_data = script_tag.string.partition('=')[-1].strip(' ;')
    result = json.loads(shared_data)
    latest_code = result['entry_data']['ProfilePage'][0]['user']['media']['nodes'][0]['code']
  except KeyError:
    return 'NULL'
  latest_url = "https://instagram.com/p/"+latest_code
  return latest_url

def duplicate_check(insta_id):
  with open(filename, newline='') as f:
      reader = csv.reader(f)
      try:
          for idx,row in enumerate(reader):
              if(row[0]==insta_id):
                return idx
          return -1
      except csv.Error as e:
          sys.exit('file {}, line {}: {}'.format(filename, reader.line_num, e))

def add_subscribe(insta_id):
  with open(filename, 'a') as newFile:
    if(duplicate_check(insta_id)==-1):
      newFileWriter = csv.writer(newFile)
      try:
        latest_url = 'NULL'  # should be empty in first addition
        newFileWriter.writerow([insta_id, latest_url])
        return -2
      except IndexError:
        return -4
        # print("page doesn't exist or private account")
    else:
      # print("duplicated subscription request")
      return -3

def unsubscribe(insta_id):
  row_num = duplicate_check(insta_id)
  ROWS_TO_DELETE = {row_num}
  if(row_num == -1):
    # print("there is nothing to unsubscribe")
    return -3
  else:
    with open(filename, 'rt') as infile, open('outfile.csv', 'wt') as outfile:
      outfile.writelines(row for row_num, row in enumerate(infile, 0)
                          if row_num not in ROWS_TO_DELETE)
    os.remove(filename)
    os.rename("outfile.csv", filename)
    return -2

def print_subscribe_list():
  ans = []
  with open(filename, newline='') as f:
      reader = csv.reader(f)
      try:
          for row in reader:
              ans.append(row[0])
          return ans
      except csv.Error as e:
          sys.exit('file {}, line {}: {}'.format(filename, reader.line_num, e))

def initiate_list():
  """remove csv file"""
  os.remove(filename)

# if __name__ == "__main__":
#   import argparse
#   parser = argparse.ArgumentParser()
#   parser.add_argument("--id", help="Instagram ID")
#   args = parser.parse_args()
