from src import github, bar

def main():
  print(github._check_rate_limit())
  print("")
  
  print("Caching files from github")
  github.get_all_unit_files()
  print("Caching completed")

if __name__ == '__main__':
  main()
