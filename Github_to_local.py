import os
from github import Github, Repository, ContentFile
import requests

class From_GitHub:
    def __init__(self):
        self.g = Github()
        self.repos, self.folder, self.file = '','',''
        self.savein = 'Downloads'

    def download(self,c: ContentFile):
        r = requests.get(c.download_url)
        out = f'{self.savein}/{c.path}'
        os.makedirs(os.path.dirname(out), exist_ok=True)
        with open(out, 'wb') as f:
            f.write(r.content)


    def download_folder(self,repo: Repository, recursive: bool):
        contents = repo.get_contents(self.folder)
        for c in contents:
            if c.download_url is None:
                if recursive:
                    self.download_folder(repo, recursive)
                continue
            self.download(c)


    def download_file(self,repo: Repository):
        c = repo.get_contents(self.file)
        self.download(c)

    def github_download(self):
        f = int(input("Do you want to download a file or folder \nIf folder then enter 1 \nIf file then enter 2 \n"))
        self.repos = input('Enter "username/repositoryname" \n')
        if f == 1:
            try:
                self.folder = input('Enter the folder name \n')
                try:               
                    repo = self.g.get_repo(self.repos)
                    self.download_folder(repo, 1)
                    print('Download completed')
                except:
                    print('Enter a valid folder name')
            except Exception as e:
                print('Repository not found please give a valid URL')

        elif f == 2:
            try:
                repo = self.g.get_repo(self.repos)
                try:
                    self.file = input('Enter the file name or foldername/filename \n')
                    self.download_file(repo)
                    print('Download completed')
                except:
                    print('Enter a Valid file name')
            except Exception as e:
                print('Repository not found please give a valid URL')
        else:
            print('Enter 1 or 2')

if __name__ == '__main__':
    git = From_GitHub()
    git.github_download()