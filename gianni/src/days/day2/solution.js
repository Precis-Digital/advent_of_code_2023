/* DIALY MESSAGE
============================================================================= */

/*
  "Phew! This one really tested my coding skills and my ability to work through a hangover!
  🥴 But hey, nothing a red bull couldn't fix!
  Now that it's done, it's time to dive into the next challenge.! 🚀"
*/

/* IMPORTS
============================================================================= */

import chalk from 'chalk';
import { getRuntime, getFileSize, loadTextFile } from '../../utils/getters.js';
import { log } from '../../utils/log.js';

/* CONSTANTS
============================================================================= */

const DAY = 'day2';
const AVAILABLE_CUBES = { red: 12, green: 13, blue: 14 };

/* CORE FUNCTIONS
============================================================================= */

/**
 * @namespace D2_Helpers
 */

/**
 * Prepares a cube set by ensuring all keys are present and sorted.
 *
 * @memberof D2_Helpers
 *
 * @example
 * const cubeSet = { red: 5, blue: 3 };
 * const preparedCubeSet = Day2.prepareCubeSet(cubeSet);
 * console.log(preparedCubeSet); // { red: 5, green: 0, blue: 3 }
 *
 * @param {Object} cubeSet - The cube set to prepare.
 * @returns {Object} The prepared cube set.
 */
const prepareCubeSet = (cubeSet) => {
  // Define the keys for the cube set
  const keys = ['red', 'green', 'blue'];

  // Use the reduce function to create a sorted cube set
  return keys.reduce((sortedCubeSet, key) => {
    // If the cube set has a value for the current key, use it; otherwise, use 0
    sortedCubeSet[key] = cubeSet[key] || 0;
    // Return the sorted cube set
    return sortedCubeSet;
  }, {}); // Start with an empty object for the sorted cube set
};

/**
 * Checks if there are enough cubes for each set in the game object.
 *
* @memberof D2_Helpers
 * @example
 * const gameObject = {
 *   sets: [
 *     { red: 5, green: 0, blue: 3 },
 *     { red: 2, green: 2, blue: 2 }
 *   ]
 * };
 * Day2.checkIfThereIsEnoughCubes(gameObject);
 * console.log(gameObject.hasEnoughCubes); // true or false
 *
 * @param {Object} gameObject - The game object to check.
 */
const checkIfThereIsEnoughCubes = (gameObject) => {
  // Use the some method to check if there is any set that does not have enough cubes
  // For each set, use the every method to check if there are enough cubes of each color
  // If there is any set that does not have enough cubes of any color, the some method will return true
  // If all sets have enough cubes of each color, the some method will return false
  // The result is negated to get a boolean indicating whether there are enough cubes for all sets
  const hasEnoughCubes = !gameObject.sets.some(set => !Object.keys(set).every(color => set[color] <= AVAILABLE_CUBES[color]));

  // Store the result in the game object
  gameObject.hasEnoughCubes = hasEnoughCubes;
};

/**
 * Calculates the minimum number of cubes needed for each color in the game object.
 *
 * @memberof D2_Helpers
 *
 * @example
 * const gameObject = {
 *   sets: [
 *     { red: 5, green: 0, blue: 3 },
 *     { red: 2, green: 2, blue: 2 }
 *   ]
 * };
 * Day2.minimumCubesNeeded(gameObject);
 * console.log(gameObject.minimumCubesNeeded); // { red: 5, green: 2, blue: 3 }
 *
 * @param {Object} gameObject - The game object to calculate for.
 */
const minimumCubesNeeded = (gameObject) => {
  // Use the reduce method to iterate over each set in the game object
  const minimum = gameObject.sets.reduce((acc, set) => {
    // For each set, iterate over each color
    Object.keys(set).forEach((color) => {
      // If the accumulator does not have a value for the current color, or if the number of cubes of the current color in the set is greater than the current value in the accumulator, update the accumulator
      acc[color] = Math.max(acc[color] || 0, set[color]);
    });
    // Return the accumulator for the next iteration
    return acc;
  }, {}); // Start with an empty object for the accumulator

  // Store the minimum number of cubes needed for each color in the game object
  gameObject.minimumCubesNeeded = minimum;
};

/**
 * Parses a game from a line of text.
 *
 * @memberof D2_Helpers
 *
 * @example
 * const line = 'Game 1: 5 red, 3 blue; 2 green, 2 blue';
 * const gameObject = Day2.parseGameFromLine(line);
 * console.log(gameObject);
 * // {
 * //   line: 'Game 1: 5 red, 3 blue; 2 green, 2 blue',
 * //   index: 1,
 * //   sets: [
 * //     { red: 5, green: 0, blue: 3 },
 * //     { red: 0, green: 2, blue: 2 }
 * //   ],
 * //   hasEnoughCubes: true,
 * //   minimumCubesNeeded: { red: 5, green: 2, blue: 3 }
 * // }
 *
 * @param {string} line - The line of text to parse.
 * @returns {Object} The parsed game object.
 */
const parseGameFromLine = (line) => {
  // Split the line into the game and its sets
  const gameAndSets = line.split(':');
  // Split the game into its components
  const game = gameAndSets[0].split(' ');
  // Get the game index from the last component of the game
  const gameIndex = parseInt(game[game.length - 1], 10);
  // Split the sets into an array
  const sets = gameAndSets[1].split(';');
  // Initialize the game object with the line, index, and an empty array for the sets
  const gameObject = { line, index: gameIndex, sets: [] };

  // For each set in the sets array
  sets.forEach((set) => {
    // Split the set into its components
    const setGroup = set.trim().split(',');
    // Initialize an empty object for the cube set
    const cubeSet = {};

    // For each color in the set group
    setGroup.forEach((color) => {
      // Split the color into the cube amount and the cube color
      const [cubeAmount, cubeColor] = color.trim().split(' ');
      // Add the cube color and amount to the cube set
      cubeSet[cubeColor] = parseInt(cubeAmount, 10);
    });

    // Add the prepared cube set to the game object's sets
    gameObject.sets.push(prepareCubeSet(cubeSet));
  });

  // Check if there are enough cubes for the game object's sets
  checkIfThereIsEnoughCubes(gameObject);
  // Calculate the minimum number of cubes needed for the game object's sets
  minimumCubesNeeded(gameObject);

  // Return the game object
  return gameObject;
};

/**
 * @namespace D2_Core
 */

/**
 * Calculates the total sum of indexes and power for a list of games.
 *
 *  @memberof D2_Core
 * 
 * @example
 * const dataLines = [
 *   'Game 1: 5 red, 3 blue; 2 green, 2 blue',
 *   'Game 2: 2 red, 2 green, 2 blue; 5 red, 3 blue'
 * ];
 * const totals = calculateGameTotals(dataLines, true);
 * console.log(totals); // { part1: 1, part2: 60 }
 *
 * @param {string[]} dataLines - The lines of data representing the games.
 * @param {boolean} isLoggingEnabled - Whether to log the game details.
 * @returns {Object} An object containing the total sum of indexes and power.
 * @throws {Error} If dataLines is not a non-empty array.
 */
const calculateGameTotals = (dataLines, isLoggingEnabled) => {
  // Check if the input is a non-empty array
  if (!Array.isArray(dataLines) || dataLines.length === 0) {
    throw new Error('Invalid input: dataLines must be a non-empty array');
  }

  // Initialize the total sum of indexes and power
  let totalSumIndexes = 0;
  let totalSumPower = 0;

  // Iterate over each line in the data lines
  for (const line of dataLines) {
    // Parse the game from the line
    const gameObject = parseGameFromLine(line);
    // Calculate the power of the game
    gameObject.power = gameObject.minimumCubesNeeded.red * gameObject.minimumCubesNeeded.green * gameObject.minimumCubesNeeded.blue;

    // Add the power of the game to the total sum of power
    totalSumPower += gameObject.power;

    // If the game has enough cubes, add its index to the total sum of indexes
    if (gameObject.hasEnoughCubes) {
      totalSumIndexes += gameObject.index;
    }

    // If logging is enabled, log the game details
    if (isLoggingEnabled) {
      console.log(
        `${chalk.dim('Game:')} ${chalk.yellow(gameObject.index)}`,
        `${chalk.dim('Enough Cubes:')} ${(gameObject.hasEnoughCubes ? '✅' : '❌').padEnd(1, ' ')}`,
        `${chalk.dim('Power:')} ${chalk.yellow(gameObject.power)}`,
      );
    }
  }

  // Return the total sum of indexes and power
  return {
    part1: totalSumIndexes,
    part2: totalSumPower,
  };
};

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
const [solution, solutionTime] = getRuntime(calculateGameTotals, dataLines, false);

// Calculate the total time
const totalTime = Math.round(readTime + dataSizeTime + solutionSizeTime + solutionTime);

/* OUTPUT LOGS
============================================================================= */

console.log('\n🎄🎄🎄🎄🎄🎄🎄🎄🎄🎄\n');

// Print the day number
log(`${chalk.blue('Day:')} ${chalk.green(DAY[DAY.length - 1])}\n`);

// Print the solutions for part 1 and part 2
log(`${chalk.blue('Part-1:')} ${chalk.green(solution.part1)}`);
log(`${chalk.blue('Part-2:')} ${chalk.green(solution.part2)}\n`);

// Print the sizes of the script and data files
console.log(`${chalk.blue('Script:')} ${chalk.green(`${solutionSize}kb`)}`);
console.log(`${chalk.blue('Data:')} ${chalk.green(`${dataSize}kb\n`)}`);

// Print the total runtime
console.log(`${chalk.blue('Runtime:')} ${chalk.green(`${totalTime}ms`)}\n`);

console.log('🎁🎁🎁🎁🎁🎁🎁🎁🎁🎁\n');

// Print the header for the part 1 & 2 example
console.log('Part 1 & 2\n');
const [solutionExample, solutionExampleTime] = getRuntime(calculateGameTotals, exampleLines, true);
console.log('');
console.log(`${chalk.blue('Total sum of indexes:')} ${chalk.green(solutionExample.part1)}`);
console.log(`${chalk.blue('Total sum of power:')} ${chalk.green(solutionExample.part2)}`);
console.log(`${chalk.blue('Runtime:')} ${chalk.green(`${exampleReadTime + solutionExampleTime}ms`)}\n`);
console.log('🎅🎅🎅🎅🎅🎅🎅🎅🎅🎅\n');
