/* DIALY MESSAGE
============================================================================= */

/*
  Epic fail tried many ways to solve this but I couldn't find a way to do it.
  Still stuck on part 1 Will need to come back to this one later.

  I also got stuck last year on something similar and I couldn't solve it.

  Im The example data works but real data doenst
  Getting false positives and negatives and even some numbers dont get detected.
*/

/* IMPORTS
============================================================================= */

import chalk from 'chalk';
import { getRuntime, getFileSize, loadTextFile } from '../../utils/getters.js';
import { log } from '../../utils/log.js';

/* CONSTANTS
============================================================================= */

const DAY = 'day3';

/* CORE FUNCTIONS
============================================================================= */
function getSurroundingChars(grid, num) {
  let result = [];

  for (let i = 0; i < grid.length; i++) {
    for (let j = 0; j < grid[i].length; j++) {
      if (
        grid[i].substring(j, j + num.length) === num
      ) {

        const left = isNaN(grid[i][j]) ? grid[i][j] : '';
        const right = isNaN(grid[i][j + (num.length - 1)]) ? grid[i][j + (num.length - 1)] : '';

        const top = grid[i - 1] ? grid[i - 1].substring(j, j + num.length) : '';
        const bottom = grid[i + 1] ? grid[i + 1].substring(j, j + num.length) : '';

        result = {
          left,
          right,
          top,
          bottom,
          hasSpecialCharAdjacent: `${left}${right}${top}${bottom}`.replaceAll(/[a-zA-Z]/g, '').replaceAll('.', '').length > 0,
        };
        // console.log(num, result);
      }
    }
  }
  return result;
}

function sumAdjacentToSymbol(lines) {
  let totalSum = 0;
  for (let i = 0; i < lines.length; i++) {

    let line = lines[i];



    if (/\d/.test(lines[i])) {
      const numbers = lines[i].match(/.[0-9]+./g);

      numbers.forEach((number) => {
        const { left, right, hasSpecialCharAdjacent } = getSurroundingChars(lines, number);
        let parsedNumber;
        if (left) {
          number = number.substring(1);
        }
        if (right) {
          parsedNumber = number.substring(0, number.length - 1);
        }
        if (hasSpecialCharAdjacent) {
          line = line.replace(`${left}${parsedNumber}${right}`, `${left}${chalk.green(parsedNumber)}${right}`);
          totalSum += parseInt(parsedNumber, 10);
        } else {
          line = line.replace(`${left}${parsedNumber}${right}`, `${left}${chalk.red(parsedNumber)}${right}`);
        }
        // console.log(i, number, parsedNumber, hasSpecialCharAdjacent);
      });
    }

    if (/[^a-zA-Z0-9]/.test(lines[i])) {
      const specialCharacters = lines[i].match(/[^a-zA-Z0-9]/g);

      specialCharacters.forEach((character) => {
        if (character !== '.') {
          line = line.replaceAll(character, chalk.cyanBright(character));
        }
      });
    }

    console.log(line);
  }

  return {
    part1: totalSum,
    part2: 0,
  };
}

/* MAIN EXECUTION
============================================================================= */

// Load the data file and measure the time it takes
const [dataLines, readTime] = getRuntime(loadTextFile, `${process.cwd()}/src/days/${DAY}/data.txt`);

// Get the size of the data file and measure the time it takes
const [dataSize, dataSizeTime] = getRuntime(getFileSize, `${process.cwd()}/src/days/${DAY}/data.txt`);

// Load the example data file and measure the time it takes
const [exampleLines, exampleReadTime] = getRuntime(loadTextFile, `${process.cwd()}/src/days/${DAY}/example-data.txt`);

// Get the size of the solution file and measure the time it takes
const [solutionSize, solutionSizeTime] = getRuntime(getFileSize, `${process.cwd()}/src/days/${DAY}/solution.js`);

// Calculate the solution and measure the time it takes
const [solution, solutionTime] = getRuntime(sumAdjacentToSymbol, exampleLines);

// Calculate the total time
const totalTime = Math.round(readTime + dataSizeTime + solutionSizeTime + solutionTime);

/* OUTPUT LOGS
============================================================================= */

console.log('\n🎄🎄🎄🎄🎄🎄🎄🎄🎄🎄\n');

// Print the day number
log(`${chalk.blue('Day:')} ${chalk.green(DAY[DAY.length - 1])}\n`);

// Print the solutions for part 1 and part 2
log(`${chalk.blue('Part-1:')} ${chalk.green(solution.part1)}`);
// log(`${chalk.blue('Part-2:')} ${chalk.green(solution.part2)}\n`);

// Print the sizes of the script and data files
console.log(`${chalk.blue('Script:')} ${chalk.green(`${solutionSize}kb`)}`);
console.log(`${chalk.blue('Data:')} ${chalk.green(`${dataSize}kb\n`)}`);

// Print the total runtime
console.log(`${chalk.blue('Runtime:')} ${chalk.green(`${totalTime}ms`)}\n`);

console.log('🎁🎁🎁🎁🎁🎁🎁🎁🎁🎁\n');

// Print the header for the part 1 & 2 example
// console.log('Part 1 & 2\n');
// const [solutionExample, solutionExampleTime] = getRuntime(sumAdjacentToSymbol, exampleLines);
// console.log('');
// console.log(`${chalk.blue('Total sum of indexes:')} ${chalk.green(solutionExample.part1)}`);
// console.log(`${chalk.blue('Total sum of power:')} ${chalk.green(solutionExample.part2)}`);
// console.log(`${chalk.blue('Runtime:')} ${chalk.green(`${exampleReadTime + solutionExampleTime}ms`)}\n`);
// console.log('🎅🎅🎅🎅🎅🎅🎅🎅🎅🎅\n');
