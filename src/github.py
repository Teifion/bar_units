from . import cache
import requests
import json

bar_user = "beyond-all-reason"
bar_repo = "Beyond-All-Reason"
bar_units_folder = "units"
headers = {
  'Content-Type': 'application/json; charset=utf-8'
}

def _check_rate_limit():
  url_path = f"https://api.github.com/rate_limit"
  response = requests.get(url_path, headers=headers)
  return response.json()

def _get_unit_folder_contents(user, repo, path):
  def execute():
    url_path = f"https://api.github.com/repos/{user}/{repo}/contents/{path}"
    response = requests.get(url_path, headers=headers)
    result = json.dumps(response.json())
    return result
  return json.loads(cache.get("f_root", execute))

def _get_file(data):
  def execute():
    url_path = data["download_url"]
    response = requests.get(url_path, headers=headers)
    response.encoding = 'utf-8'
    result = response.text
    return result
  return cache.get(data["name"], execute)

def _get_folder(data):
  def execute():
    url_path = data["url"]
    response = requests.get(url_path, headers=headers)
    result = json.dumps(response.json())
    return result
  contents = json.loads(cache.get("f_" + data["name"], execute))
  _get_complete_folder(contents)

def _get_complete_folder(data):
  for f in data:
    if f["type"] == "dir":
      _get_folder(f)
    elif f["type"] == "file":
      _get_file(f)
    else:
      raise Exception(f'No handler for file type {f["type"]}')

def _get_unit(unit):
  url_path = unit['url']
  response = requests.get(url_path, headers=headers)
  return response.json()

  # response = requests.get(url_path, headers=headers)
  # return response.json()

def get_all_unit_files():
  folder_contents = _get_unit_folder_contents(bar_user, bar_repo, bar_units_folder)
  _get_complete_folder(folder_contents)
