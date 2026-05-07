# 2026-tdp-ctf

## Contributing 

Instructions for contributing a challenge:

Create an issue outlining what challenge you are working on (e.g "Basic SQL injection") and label it appropriately. This well help make sure that multiple people aren't working on the 'same' challenge.
Clone the repo (don't use HTTPS authentication, use SSH) and make sure it is up to date.
Make a branch with your challenge name (e.g web/basic-sql).
Make a directory inside the corresponding challenge category (e.g. web/basic-sql).
Develop your challenge. Your folder structure should look roughly as follows:
.
├─ web/
│  ├─ my-chall/
│  │  └── README.md        # include name and description for ctfd
│  │  └── chall-file         # any files you need to provide
│  │  ├── src/
│  │  │   └── src.py             # files used to create your challenge
│  │  ├── solve/                 # solution scripts
│  │  │   └── flag.txt           # a text file with JUST the flag string
│  │  │   └── solve-writeup.md   # solution writeup
│  │  │   └── solve.py           # solution scripts, if necessary
Commit your files and push to the remote.
Open a pull request to merge your branch into main.
Have your challenge reviewed. The reviewer should verify that the files provided in dist/ are sufficient to solve the challenge, and that the challenge is solvable. The reviewer should ideally attempt to solve the challenge without using the submitter's solution, this can help uncover unintended solutions.
Once your PR is approved, you can merge it.
