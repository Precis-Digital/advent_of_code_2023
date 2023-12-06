/* eslint-disable class-methods-use-this */

import chalk from 'chalk';
import { process, replace } from '../../utils/utils.js';

/**
 * @class
 *
 * @property {Array} dataLines - The data lines to process.
 * @property {boolean} numbersOnly - Whether to only consider numbers.
 * @property {boolean} isLoggingEnabled - Whether logging is enabled.
 * @property {Array} numericWords - The numeric words to consider.
 * @property {number} totalSum - The total sum of the numbers.
 */
export class Day1 {
  /**
    * Creates an instance of Day1.
    *
    * @example
    * // Example 1: With logging enabled
    * const dataLines = ['This is line 1', 'This is line 2', 'This is line 3'];
    * const isLoggingEnabled = true;
    * const solution = new Day1(dataLines, isLoggingEnabled);
    *
    * // Example 2: With logging disabled
    * const dataLines = ['This is another line 1', 'This is another line 2'];
    * const isLoggingEnabled = false;
    * const solution = new Day1(dataLines, isLoggingEnabled);
    *
    * @param {Array.<string>} dataLines - The data lines to process. Each element should be a string.
    * @param {boolean} isLoggingEnabled - Whether logging is enabled. If true, the class will log information about its operations.
    */
  constructor(dataLines, isLoggingEnabled) {
    this.dataLines = dataLines;
    this.isLoggingEnabled = isLoggingEnabled;
    this.numericWords = [
      { word: 'one', number: 1 },
      { word: 'two', number: 2 },
      { word: 'three', number: 3 },
      { word: 'four', number: 4 },
      { word: 'five', number: 5 },
      { word: 'six', number: 6 },
      { word: 'seven', number: 7 },
      { word: 'eight', number: 8 },
      { word: 'nine', number: 9 },
    ];
    this.totalSum = {
      part1: 0,
      part2: 0,
    };
  }

  /**
   * Finds a numeric value in a string.
   *
   * @param {string} sourceString - The string to search in.
   * @param {string} numbersOnly - Determines if only numbers should be searched for.
   * @param {string} [direction='forward'] - The direction to search in.
   * @returns {Object} The found word and its type.
   *
   * @example
   * // Assuming an instance of the class is stored in a variable called `instance`
   * const result1 = instance.findNumeric('hello123', 'numberOnly', 'forward');
   * console.log(result1); // Outputs: { number: 123, type: 'number' }
   *
   * const result2 = instance.findNumeric('hello123', 'all', 'backward');
   * console.log(result2); // Outputs: { number: 123, type: 'number' } if 'hello' is not in the numericWords array
   *
   * const result3 = instance.findNumeric('onetwothree', 'all', 'forward');
   * console.log(result3); // Outputs: { word: 'one', number: 1, type: 'word' } if 'one' is in the numericWords array
   */
  findNumeric(sourceString, numbersOnly, direction = 'forward') {
    let newString = '';
    let foundWord = null;

    const loopCondition = direction === 'forward'
      ? i => i < sourceString.length
      : i => i >= 0;

    const loopIncrement = direction === 'forward'
      ? i => i + 1
      : i => i - 1;

    for (let i = direction === 'forward' ? 0 : sourceString.length - 1; loopCondition(i); i = loopIncrement(i)) {
      if (!Number.isNaN(Number(sourceString[i]))) {
        foundWord = { ...this.numericWords[parseInt(sourceString[i], 10) - 1], type: 'number' };
        break;
      }

      if (numbersOnly !== 'numberOnly') {
        newString = direction === 'forward' ? newString + sourceString[i] : sourceString[i] + newString;
        const numberWord = this.numericWords.find(nw => newString.includes(nw.word));
        if (numberWord) {
          foundWord = { ...numberWord, type: 'word' };
          break;
        }
      }
    }

    return foundWord;
  }

  /**
   * Processes a line to find a numeric value at the front and back. And combines them to a single number
   *
   * @param {string} line - The line to process.
   * @param {string} numbersOnly - Determines if only numbers should be searched for.
   * @returns {number} The found number.
   *
   * @example
   * // Assuming an instance of the class is stored in a variable called `instance`
   * const number = instance.processLine('hello123world456', 'numberOnly');
   * console.log(number); // Outputs: 123456
   *
   * const number2 = instance.processLine('hello123world456', 'all');
   * console.log(number2); // Outputs: 123456 if 'hello' and 'world' are not in the numericWords array
   */
  processLine(line, numbersOnly) {
    const initialWord = this.findNumeric(line, numbersOnly, 'forward');
    const finalWord = this.findNumeric(line, numbersOnly, 'backward');
    const number = parseInt(`${initialWord.number}${finalWord.number}`, 10);

    if (this.isLoggingEnabled) {
      const initialWordValue = initialWord.type === 'word' ? initialWord.word : initialWord.number;
      const finalWordValue = finalWord.type === 'word' ? finalWord.word : finalWord.number;
      line = line.replace(initialWordValue, `${chalk.redBright(initialWordValue)}`);
      line = chalk.grey(replace.lastOccurrence(line, finalWordValue, `${chalk.cyanBright(finalWordValue)}`));
      console.log(line, number);
    }

    return number;
  }

  /**
   * Processes all lines for part 1 and updates the total sum.
   * It only considers numbers in the line.
   *
   * @example
   * // Assuming an instance of the class is stored in a variable called `instance`
   * instance.part1();
   * // The total sum for part 1 can now be accessed via `instance.totalSum.part1`
   */
  part1() {
    process.lines(this.dataLines, (line) => {
      this.totalSum.part1 += this.processLine(line, 'numberOnly');
    });
    if (this.isLoggingEnabled) {
      console.log('');
    }
  }

  /**
   * Processes all lines for part 2 and updates the total sum.
   * It considers both numbers and words in the line.
   *
   * @example
   * // Assuming an instance of the class is stored in a variable called `instance`
   * instance.part2();
   * // The total sum for part 2 can now be accessed via `instance.totalSum.part2`
   */
  part2() {
    process.lines(this.dataLines, (line) => {
      this.totalSum.part2 += this.processLine(line, 'all');
    });
    if (this.isLoggingEnabled) {
      console.log('');
    }
  }
}
