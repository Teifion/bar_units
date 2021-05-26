from . import cache, parse, db
from datetime import datetime
import requests
import json

bar_user = "beyond-all-reason"
bar_repo = "Beyond-All-Reason"
bar_units_folder = "units"
headers = {
  'Content-Type': 'application/json; charset=utf-8'
}

def filename(data):
  return data["name"].replace(".lua", "") + "_" + data["sha"] + ".lua"

def exclude(name):
    if "chicken" in name: return True
    if "scav" in name: return True
    return False

def _check_rate_limit():
  url_path = f"https://api.github.com/rate_limit"
  response = requests.get(url_path, headers=headers)
  result = response.json()
  remaining = result["resources"]["core"]["remaining"]

  if remaining == 0:
    reset_unix_time = result["resources"]["core"]["reset"]
    reset_timestamp = datetime.fromtimestamp(reset_unix_time)
    raise Exception(f"No loads left, resets at {reset_timestamp}")

def _get_unit_folder_contents(user, repo, path):
  def execute():
    url_path = f"https://api.github.com/repos/{user}/{repo}/contents/{path}"
    response = requests.get(url_path, headers=headers)
    result = json.dumps(response.json())
    return result
  return json.loads(cache.get("f_root", execute))

def _get_file(data):
  name = filename(data)
  def execute():
    url_path = data["download_url"]
    response = requests.get(url_path, headers=headers)
    response.encoding = 'utf-8'
    result = response.text
    return result
  contents = cache.get(name, execute)
  return parse.eval_string(contents)

def _get_folder(data):
  def execute():
    url_path = data["url"]
    response = requests.get(url_path, headers=headers)
    result = json.dumps(response.json())
    return result
  contents = json.loads(cache.get("f_" + data["name"] + "_" + data["sha"], execute))
  _get_complete_folder(contents)

def _get_complete_folder(data):
  for f in data:
    if isinstance(f, str): continue
    if f["type"] == "dir":
      _get_folder(f)
    elif f["type"] == "file":
      if not exclude(f["name"]):
        unit = _get_file(f)
        if unit != None:
          (key, data) = unit
          db.put(key, data)

    else:
      raise Exception(f'No handler for file type {f["type"]}')

def _get_unit(unit):
  url_path = unit['url']
  response = requests.get(url_path, headers=headers)
  return response.json()

def get_all_unit_files():
  folder_contents = _get_unit_folder_contents(bar_user, bar_repo, bar_units_folder)
  _get_complete_folder(folder_contents)
