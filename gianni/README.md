# Advent of Code 2023

This project is a collaborative effort between the developer and GitHub Copilot

- **Language:** *Javascript*  
- **Engine:** *Node.js*
- Open `index.html` in `docs` for project documentation. Note: It's in progress and examples lack context.
- GitHub Copilot comments are guides, not definitive truths.

## Goals
- **Logging:** Enhance application visibility with detailed logs.
- **Unified Function:** Create a single function for tasks of parts 1 and 2.
- **Learning:** Use GitHub Copilot for learning JavaScript techniques and best practices.
- **Optimization:** Write initial functions and optimize with GitHub Copilot's suggestions.
- **Documentation:** Document functions using JSDoc.
- **Progress:** Aim to surpass previous year's AOC progress.

## Commands
- `npm install` Install dependencies.
- `npm run start` Run all days. 
- `npm run start -- day=1` Run a specific day.
- `npm run start -- minify=true` Run minified.
- `npm run start -- day=1 minify=true` Combine the arguments like this.
- `npm run docs` Create documentation of functions that have JSdoc comments.

## Updates

#### Day 1
- Collaborated with CoPilot on this challenge.
- Faced some difficulties in devising a solution for part 2.
- Eventually, we successfully solved the problem.
- CoPilot suggested an almost optimized solution when I wrote a repeatable solution for part 2.
- After some adjustments, we achieved the final result.

#### Day 2
- This challenge significantly tested my coding skills.
- Also had to work through a hangover.
- Managed to overcome the difficulties with the help of a Red Bull.
- Successfully completed the challenge.
- Ready to tackle the next challenge.

#### Day 3
- Encountered significant difficulties in finding a solution.
- Still working on part 1; plan to revisit this later.
- Experienced similar challenges last year without finding a solution.
- The example data works, but the real data does not.
- Encountering issues with false positives and negatives.
- Some numbers are not being detected.

#### Day 4
- Completed part-1 rather quickly.
- Struggled with part-2, especially due to the initially long runtime of 30 seconds.
- After rewriting, the runtime unexpectedly increased to 30 minutes.
- Despite the increased runtime, the refactored code has a cleaner appearance.
- Began refactoring tasks for previous days.

#### Day 5
- Unable to make progress on this day.

#### Day 6
- Implemented minification for classes and `index.js`, ensuring correct functionality.
- System now determines the day based on the folder name.
- Developed classes for Day 1 and Day 2.
- Reintroduced logging in Day 2 class if `isLoggingEnabled` is true.
- Refactored `index.js` for Day 2 and added JSDoc comments to the Day 2 class.
- Considered integrating `processDataLines` into Day 4 or making it a helper function.
- Standardized all logs for consistency.
- Refactored all `index.js` files to align with Day 1's `index.js`.
- Resolved a bug in Day 1 example part-1 logging where characters were being removed.
- UPDATE DAY 4: Used a javascript version of https://github.com/Lyqst/aoc2023/ and converted it to my needs its way way faster now i didnt know you can split data like that. Went from 30min to 2ms HUGE CHANGE

#### Day 7 

- Rewrote Day 2
- Made solution for day 3 with help from https://github.com/Lyqst/aoc2023/ but had to refactor code to work for my logs.

#### Day 8 

- Turned Day 3 into a class
- added extra logging to day 3
- WINTER PARTY!!!

#### Day 9

- Day 3 clean up and added comments
- Added story and the problem/solution in comments (not sure if i should color it)
- turned index.js now launcher.js into a class

#### Day 10

- Made the launcher.js class work for the exceptions
- Made an index.js for the cli commands instead of having it all in the package.json that became unreadable and to call the launcher class
- Added colors to descriptions
- Challenge manager and launcher are ready finally! I wanted to have this so i can use it next year and not waste time creating it
- added new logic for minification of day classes

###### Tasks

- Attempt to find online solutions for missing days 5,6,7,8. and refactor it into a class
- Improve JSDocs in future: Ensure all examples in the documentation are accurate and up-to-date.
