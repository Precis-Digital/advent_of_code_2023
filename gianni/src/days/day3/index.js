// This file is the main entry point for the application.
import path from 'path';
import chalk from 'chalk';
import { get, log } from '../../utils/utils.js';

// The name of the parent folder is used to determine the day.
const day = path.basename(path.dirname(import.meta.url));
const DayNumber = day.slice(-1);

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

function sumAdjacentToSymbol(lines, isLoggingEnabled) {
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
    if (isLoggingEnabled) {
      console.log(line);
    }
  }

  return {
    totalSum: {
      part1: totalSum,
      part2: 0,
    },
  };
}

/* MAIN EXECUTION
  ============================================================================= */

// The data for the current day is loaded.
const { data: dataLines, size: dataSize } = get.dataAndSize('data.txt', day);
const { data: exampleLines } = get.dataAndSize('example-data.txt', day);
const { size: classSize } = get.dataAndSize('index.js', day);

// Calculate the solution and measure the time it takes
const solution = sumAdjacentToSymbol(exampleLines, false);
solution.time = solution.time || {};
solution.time.part1 = 0;
solution.time.part2 = 0;

/* OUTPUT LOGS
  ============================================================================= */

// The day and results are logged to the console.
log.message(`\n${'🎄'.repeat(DayNumber)} ⭐⭐ ⭐⭐ ❌❌ (Unresolved challenge.)\n`);
log.results(day, classSize, dataSize, solution);

// Present box separator
console.log(`${'🎁'.repeat(20)}\n`);

const example = sumAdjacentToSymbol(exampleLines, true);

console.log('');
