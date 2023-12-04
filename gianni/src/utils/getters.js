// Import the 'fs' module for file system operations
import * as fs from 'fs';

/**
 * @namespace Utils
 */

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
const loadTextFile = (filePath) => {
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
const getRuntime = (func, ...args) => {
  // Get the start time
  const startTime = process.hrtime();
  // Call the function and get the result
  const result = func(...args);
  // Get the end time
  const endTime = process.hrtime(startTime);
  // Calculate the execution time in milliseconds
  const executionTime = endTime[0] * 1000 + endTime[1] / 1e6;
  // Round execution time to one decimal place
  const executionTimeRounded = Math.round(executionTime * 10) / 10;
  // Return the result and the execution time
  return [result, executionTimeRounded];
};

// Export the functions for use in other modules
export { getRuntime, getFileSize, loadTextFile };
