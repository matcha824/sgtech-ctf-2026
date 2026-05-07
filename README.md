# 2026-tdp-ctf

## Contributing 

Instructions for contributing a challenge:

1. Create an issue outlining what challenge you are working on (e.g "Basic SQL injection") and label it appropriately. This well help make sure that multiple people aren't working on the 'same' challenge.
2. Clone the repo (don't use HTTPS authentication, use SSH) and make sure it is up to date.
3. Make a branch with your challenge name (e.g `web/basic-sql`).
4. Make a directory inside the corresponding challenge category (e.g. `web/basic-sql`).
5. Develop your challenge. Your folder structure should look roughly as follows:
```
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
```
6. Commit your files and push to the remote.
7. Open a pull request to merge your branch into main.
8. Have your challenge reviewed. The reviewer should verify that the files provided in `dist/` are sufficient to solve the challenge, and that the challenge is solvable. The reviewer should ideally attempt to solve the challenge without using the submitter's solution, this can help uncover unintended solutions.
9. Once your PR is approved, you can merge it.
