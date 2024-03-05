# INSTRUCTIONS FOR PAST PAPER OPENER

This opens the past paper of a levels subject after given a code in the form of
`subject code/paper no/month beginning/month end/year` so it would look something like this
`9709/13/M/J/22`. This is paper 13 of A Levels Mathematics examination from May June 2022.

## INSTRUCTIONS

1. Install python if you haven't already.
2. Now that you've installed python you're ready to download and run the code.
3. Click on **Code** button above
4. You will find a **Download ZIP** option. Click on that.
5. **Download the zip file as `past_paper` and not `past_paper-main`.**
6. Extract the files in your desired folder.
7. Open the folder and go to `subject_info.json`. If the subjects you have are not there, replace them with the current ones in the same format as they existed.
8. Open terminal and `cd` to the directory in which your folder is in.
9. First we need to create pipenv. To do that, type the following steps sequentially
    ```cmd
    > python -m pip install pipenv
    > pipenv install
    ```
10. The requirements for this program to run has been completed.
11. Type `help` or `h` on how to use this program.
12. You can find all of the downloaded past papers in the `papers` folder created by the program.
