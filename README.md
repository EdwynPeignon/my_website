# About
This Repository aim to build my web site

# Configuration
To work on the project:


Build the virtual environement:

```
virtualenv -p python3 venv
```

Activate your virtual environement:

```
source venv/bin/activate
```

Install the dependencies:

```
pip install -r requirements.txt
```

# Working on the project

Make sure your project is up-to-date:
```
git pull
```

Create your branch:
```
git checkout -b your_meaningful_branch_name
```

Do the modification you want on the project.
Add the modification you have made on your branch.
```
git add --all
git commit -m "Summarize the modification you have made"
git push
```

Merge your branch with the master branch:
```
git checkout master
git merge your_meaningful_branch_name
```

Delete your old branch:
```
git branch -d your_meaningful_branch_name
```

Push to github:
```
git push origin master
```

If you want a better understanding, check this article out: https://confluence.atlassian.com/bitbucket/use-a-git-branch-to-merge-a-file-681902555.html# my_website
