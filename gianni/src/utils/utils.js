// Import the 'fs' module for file system operations
import * as fs from 'fs';
import { performance } from 'perf_hooks';
import chalk from 'chalk';
import logMessage from './logMessage.js';

/**
 * @namespace Utils
 */

// GETTERS

/**
 * Loads a text file and returns its contents as an array of lines.
 *
 * @memberof Utils
 *
 * @example
 * const lines = loadTextFile('./path/to/file.txt');
 * console.log(lines);
 *
 * @param {string} filePath - The path to the file.
 * @returns {string[]} An array of lines from the file.
 */
const getTextFile = (filePath) => {
  // Read the file synchronously and return its contents
  const data = fs.readFileSync(filePath, 'utf8');
  // Split the data into lines
  const lines = data.split('\n');
  return lines;
};

/**
 * Gets the size of a file in kilobytes.
 *
 * @memberof Utils
 *
 * @example
 * const size = getFileSize('./path/to/file.txt');
 * console.log(`File size: ${size} KB`);
 *
 * @param {string} filePath - The path to the file.
 * @returns {number} The size of the file in kilobytes.
 */
const getFileSize = (filePath) => {
  // Get the stats of the file and return its size
  const stats = fs.statSync(filePath);
  const kilobytes = Math.round(stats.size / 1024);
  return kilobytes;
};

/**
 * Measures the execution time of a function.
 *
 * @memberof Utils
 *
 * @example
 * const [result, time] = getRuntime(someFunction, arg1, arg2);
 * console.log(`Execution time: ${time} ms`);
 *
 * @param {Function} func - The function to measure.
 * @param {...*} args - The arguments to pass to the function.
 * @returns {Array} An array where the first element is the result of the function (of any type) and the second element is the execution time in milliseconds (a number).
 */
const getRuntime = (func) => {
  const t0 = performance.now();
  const result = func();
  const t1 = performance.now();
  let time = t1 - t0; // time in milliseconds
  let unit = 'ms';
  if (time > 1000) {
    time /= 1000; // convert to seconds
    unit = 's';
    if (time > 60) {
      time /= 60; // convert to minutes
      unit = 'm';
      if (time > 60) {
        time /= 60; // convert to hours
        unit = 'h';
      }
    }
  }
  return `${time.toFixed(2)} ${unit}`;
};

const getDataAndSize = (file, day) => {
  const filePath = `./src/days/${day}/${file}`;
  const data = getTextFile(filePath);
  const size = getFileSize(filePath);
  return { data, size };
};

// REPLACE

/**
   * This function replaces the last occurrence of a substring in a source string with a new string.
   *
   * @param {string} sourceString - The original string. For example, 'Hello, world!'.
   * @param {string} substringToReplace - The substring to be replaced. For example, 'world'.
   * @param {string} replace - The string to replace the substring with. For example, 'GitHub Copilot'.
   * @returns {string} The source string with the last occurrence of the substring replaced. For example, 'Hello, GitHub Copilot!'.
   *
   * @example
   * replaceLastOccurrence('Hello, world!', 'world', 'GitHub Copilot'); // returns 'Hello, GitHub Copilot!'
   */
const replaceLastOccurrence = (sourceString, substringToReplace, replace) => {
  const regex = new RegExp(`${substringToReplace}(?=[^${substringToReplace}]*$)`, 'g');
  return sourceString.replace(regex, replace);
};

// PROCESSES

const processLines = (lines, processor) => {
  // Check if the input is a non-empty array
  if (!Array.isArray(lines) || lines.length === 0) {
    throw new Error('Invalid input: dataLines must be a non-empty array');
  }

  // Iterate over each line in the data lines
  for (const line of lines) {
    // Process the game object using the provided processor function
    processor(line);
  }
};

// LOGGING

const logResults = (day, classSize, dataSize, solution) => {
  // Print the day number
  logMessage(`${chalk.blue('Day:')} ${chalk.green(day.slice(-1))}\n`);

  // Print the sizes of the script and data files
  logMessage(`${chalk.blue('Class:')} ${chalk.green(`${classSize}kb`)}`);
  logMessage(`${chalk.blue('Data:')} ${chalk.green(`${dataSize}kb\n`)}`);

  // Print the solutions for part 1 and part 2
  logMessage(`${chalk.blue('Part-1:')} ${chalk.green(solution.totalSum.part1)} ${chalk.blue('Runtime:')} ${chalk.green(`${solution.time.part1}`)}`);
  logMessage(`${chalk.blue('Part-2:')} ${chalk.green(solution.totalSum.part2)} ${chalk.blue('Runtime:')} ${chalk.green(`${solution.time.part2}`)}\n`);
};

const logExecute = (DayClass, partNumber, lines) => {
  console.log(`Part ${partNumber}\n`);
  const solution = new DayClass(lines, true);
  const runtime = getRuntime(() => solution[`part${partNumber}`]());
  console.log(`\n${chalk.blue('Result:')} ${chalk.green(solution.totalSum[`part${partNumber}`])}`);
  console.log(`${chalk.blue('Runtime:')} ${chalk.green(`${runtime}`)}\n`);
};

// EXPORTS

const get = {
  runtime: getRuntime,
  fileSize: getFileSize,
  textFile: getTextFile,
  dataAndSize: getDataAndSize,
};

const replace = {
  lastOccurrence: replaceLastOccurrence,
};

const log = {
  message: logMessage,
  results: logResults,
  execute: logExecute,
};

const process = {
  lines: processLines,
};

export {
  get, replace, log, process,
};
