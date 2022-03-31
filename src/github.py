import os


def clone():
    """
    in this function we use git sparse checkout. this is a relatively new feature of git that allowes to
    dowloading only a part of the repository

    here its limited to only the units folder and the language files
    """
    # the repo needs to be cloned before we can use any of it
    if(not os.path.isdir('repo')):
        os.system(
            'git clone --filter=blob:none --no-checkout https://github.com/beyond-all-reason/Beyond-All-Reason repo')
        os.system('cd repo && git sparse-checkout set units language')
    # fetch the newest information
    os.system('cd repo && git fetch')
    # checkout the master of github
    os.system('cd repo && git checkout origin/master')
