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

import Solution from './class.js';

/* CONSTANTS
============================================================================= */

const DAY = 'day4';

/* CORE FUNCTIONS
============================================================================= */


/* MAIN EXECUTION
============================================================================= */

// Load the data file and measure the time it takes
const [dataLines] = getRuntime(loadTextFile, `${process.cwd()}/src/days/${DAY}/data.txt`);

// Get the size of the data file and measure the time it takes
const [dataSize] = getRuntime(getFileSize, `${process.cwd()}/src/days/${DAY}/data.txt`);

// Load the part 1 and part 2 example data files
const [exampleData] = getRuntime(loadTextFile, `${process.cwd()}/src/days/${DAY}/example-data.txt`);

// Get the size of the solution file and measure the time it takes
const [solutionSize] = getRuntime(getFileSize, `${process.cwd()}/src/days/${DAY}/solution.js`);

// Calculate the solution for part 1 and measure the time it takes
// const [solution, solutionTime] = getRuntime(getWinningCards, dataLines, false);
// const [solution, solutionTime] = getRuntime(getSolution, exampleData, true);


console.time("Runtime Part-1");
const solution = new Solution(exampleData, false);
solution.part1();
console.timeEnd("Runtime Part-1");
console.time("Runtime Part-2");
solution.part2();
console.timeEnd("Runtime Part-2");

console.log('\n\n', solution);
// console.log(solution.cards);
// console.log('\npart-1:', solution.totalPoints);
// console.log('part-2:', solution.totalScratchcards);

/* OUTPUT LOGS
============================================================================= */

console.log('\n🎄🎄🎄🎄🎄🎄🎄🎄🎄🎄\n');

// Print the day number
log(`${chalk.blue('Day:')} ${chalk.green(DAY[DAY.length - 1])}\n`);

// Print the solutions for part 1 and part 2
// log(`${chalk.blue('Part-1:')} ${chalk.green(solution.part1)}`);
// log(`${chalk.blue('Part-2:')} ${chalk.green(solution.part2.total)}\n`);

// Print the sizes of the script and data files
// console.log(`${chalk.blue('Script:')} ${chalk.green(`${solutionSize}kb`)}`);
// console.log(`${chalk.blue('Data:')} ${chalk.green(`${dataSize}kb\n`)}`);

// Print the total runtime
// console.log(`${chalk.blue('Runtime:')} ${chalk.green(`${solutionTime}`)}\n`);

console.log('🎁🎁🎁🎁🎁🎁🎁🎁🎁🎁\n');

// Print the header for the part 1 example
// console.log('Part 1 & 2\n');
// const [exampleSolution, exampleTime] = getRuntime(getWinningCards, exampleData, true);
// console.log('');
// console.log(`${chalk.blue('Total points:')} ${chalk.green(exampleSolution.part1)}`);
// console.log(`${chalk.blue('Total scratchcards:')} ${chalk.green(exampleSolution.part2.total)}`);
// console.log(`${chalk.blue('Runtime:')} ${chalk.green(`${exampleTime}`)}\n`);

console.log('🎅🎅🎅🎅🎅🎅🎅🎅🎅🎅\n');
