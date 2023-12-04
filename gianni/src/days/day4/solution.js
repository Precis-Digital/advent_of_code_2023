/* DIALY MESSAGE
============================================================================= */

/*
  part-1 done 
  nice logs and documentation are WIP
*/

/* IMPORTS
============================================================================= */

import chalk from 'chalk';
import { getRuntime, getFileSize, loadTextFile } from '../../utils/getters.js';
import { log } from '../../utils/log.js';

/* CONSTANTS
============================================================================= */

const DAY = 'day4';

/* CORE FUNCTIONS
============================================================================= */

const getWinningCards = (dataLines) => {
  // Check if the input is a non-empty array
  if (!Array.isArray(dataLines) || dataLines.length === 0) {
    // If not, throw an error
    throw new Error('Invalid input: dataLines must be a non-empty array');
  }

  // Initialize the total sum to 0
  let totalSum = 0;

  const cards = dataLines.map((card) => {
    const parts = card.split(': ');
    const index = parts[0].split(' ')[1];
    const numbers = parts[1].split(' | ');
    const winnerNumber = numbers[0].split(' ').filter(str => str.length).map(Number);
    const myNumber = numbers[1].split(' ').filter(str => str.length).map(Number);
    const matchingNumbers = myNumber.filter(num => winnerNumber.includes(num));
    const points = matchingNumbers.length > 0 ? Math.pow(2, matchingNumbers.length - 1) : 0;

    return {
      index,
      points,
    };
  });

  // console.log(cards);
  cards.forEach((card) => {
    totalSum += card.points;
  })
  return totalSum;
};

/* MAIN EXECUTION
============================================================================= */

// Load the data file and measure the time it takes
const [dataLines, readTime] = getRuntime(loadTextFile, `${process.cwd()}/src/days/${DAY}/data.txt`);

// Get the size of the data file and measure the time it takes
const [dataSize, dataSizeTime] = getRuntime(getFileSize, `${process.cwd()}/src/days/${DAY}/data.txt`);

// Load the part 1 and part 2 example data files
const [linesPart1] = getRuntime(loadTextFile, `${process.cwd()}/src/days/${DAY}/part1-data.txt`);
const [linesPart2] = getRuntime(loadTextFile, `${process.cwd()}/src/days/${DAY}/part2-data.txt`);

// Get the size of the solution file and measure the time it takes
const [solutionSize, solutionSizeTime] = getRuntime(getFileSize, `${process.cwd()}/src/days/${DAY}/solution.js`);

// Calculate the solution for part 1 and measure the time it takes
const [part1Solution, part1Time] = getRuntime(getWinningCards, dataLines);

// Calculate the solution for part 2 and measure the time it takes
// const [part2Solution, part2Time] = getRuntime(calculateSumOfMergedNumerics, dataLines, false, false);

// Calculate the total time
// const totalTime = Math.round(readTime + solutionSizeTime + dataSizeTime + part1Time + part2Time);

/* OUTPUT LOGS
============================================================================= */

console.log('\n🎄🎄🎄🎄🎄🎄🎄🎄🎄🎄\n');

// Print the day number
log(`${chalk.blue('Day:')} ${chalk.green(DAY[DAY.length - 1])}\n`);

// Print the solutions for part 1 and part 2
log(`${chalk.blue('Part-1:')} ${chalk.green(part1Solution)}`);
// log(`${chalk.blue('Part-2:')} ${chalk.green(part2Solution)}\n`);

// Print the sizes of the script and data files
console.log(`${chalk.blue('Script:')} ${chalk.green(`${solutionSize}kb`)}`);
console.log(`${chalk.blue('Data:')} ${chalk.green(`${dataSize}kb\n`)}`);

// Print the total runtime
// console.log(`${chalk.blue('Runtime:')} ${chalk.green(`${totalTime}ms`)}\n`);

console.log('🎁🎁🎁🎁🎁🎁🎁🎁🎁🎁\n');

// Print the header for the part 1 example
// console.log('Part 1\n');
// const [part1SolutionExample, part1ExampleTime] = getRuntime(calculateSumOfMergedNumerics, linesPart1, true, true);
// console.log('');
// console.log(`${chalk.blue('Result:')} ${chalk.green(part1SolutionExample)}`);
// console.log(`${chalk.blue('Runtime:')} ${chalk.green(`${part1ExampleTime}ms`)}\n`);

// Print the header for the part 2 example
// console.log('Part 2\n');
// const [part2SolutionExample, part2ExampleTime] = getRuntime(calculateSumOfMergedNumerics, linesPart2, false, true);
// console.log('');
// console.log(`${chalk.blue('Result:')} ${chalk.green(part2SolutionExample)}`);
// console.log(`${chalk.blue('Runtime:')} ${chalk.green(`${part2ExampleTime}ms`)}\n`);
console.log('🎅🎅🎅🎅🎅🎅🎅🎅🎅🎅\n');
