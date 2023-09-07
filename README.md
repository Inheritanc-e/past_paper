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
9. Type `python -m past_paper`
<<<<<<< HEAD
10. You will be presented with three different modes: `get paper`, `ms`, `qp`.
    Here, `get paper` mode is for downloading papers of any given subject using the format specified `subject code/paper number/year start-year finish`. `ms` and `qp` are if you want the program to open the question paper or the mark scheme.
=======
10. You will be presented with three different modes:
    a. `ms`: This allows you to open the markscheme by entering the subject code.
        Ex:`9709/13/M/J/22` will open the mark scheme of the given paper.
    b. `qp`: This emulates the same concept as 10a but it will instead open the question  paper.
    c. `get paper`: The format of get paper is: subject-code/paper number/year range.
        Ex: `9702/4/20-22` This will download all the questions papers of Physics (9702)
        paper 4 from 2020 to 2022.
    d. `compile paper`:
        i. The format of compile paper is the same as get paper, but you will be presented with another prompt: page difference between the front page and your first question. Ex: The page difference in a physics paper 4 question is 4. You can verify it on any physics question paper.
        ii. Compile paper compiles is similar to get paper but it compiles all of the question paper into one file making it easier to print.
        Ex: `9702/4/20-22` will make you a pdf of physics with all the questions from 2020 to 2022.
>>>>>>> 84b14be (Elaborative explanation added.)
11. Your program is now up and running, if you want to exit type `q`.
12. Now, everytime you want to open a past paper, you just have execute step 7.
13. You can find all of the downloaded past papers in the `papers` folder created by the program.
