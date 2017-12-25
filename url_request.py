import csv, os
import webkit_server
filename = 'subscribe.csv'

def profile_address(insta_id):
  """returns instagram profile address"""
  insta_url = "https://instagram.com/"+insta_id
  return insta_url

def find_latest(insta_url):
  """find latest post address from instagram profile URL"""
  import dryscrape
  from bs4 import BeautifulSoup
  sess.set_attribute('auto_load_images', False)
  sess.visit(insta_url)
  response = sess.body()
  sess.reset()
  soup = BeautifulSoup(response, "lxml")
  latest_post = soup.select('div._cmdpi a[href]')
  try:
    ying = latest_post[0].get('href')
  except IndexError:
    return 'NULL'
  latest_post_url = "https://instagram.com"+ying
  # server.kill()
  return latest_post_url

def duplicate_check(insta_id):
  import sys
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
        latest_url = find_latest(profile_address(insta_id))
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
