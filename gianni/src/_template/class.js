// import chalk from 'chalk';
import { process } from '../../utils/utils.js';

/**
 * @class
 *
 * @description Represents a day in a game. It holds the game details and performs operations related to the game.
 *
 * @property {Array} dataLines - The lines of data for the game.
 * @property {boolean} isLoggingEnabled - Whether logging is enabled.
 * @property {number} totalSum - The total sum of the numbers.
 */
export class Day2 {
  /**
   * Creates a new day.
   *
   * @example
   * const day2 = new Day2(dataLines, true);
   *
   * @param {Array} dataLines - The lines of data for the game.
   * @param {boolean} isLoggingEnabled - Whether logging is enabled.
   */
  constructor(dataLines, isLoggingEnabled) {
    this.dataLines = dataLines;
    this.isLoggingEnabled = isLoggingEnabled;
    this.totalSum = {
      part1: 0,
      part2: 0,
    };
  }

  /**
   * This function processes the data lines for part 1 of the game.
   *
   * @example
   * part1(); // processes the data lines for part 1
   */
  part1() {
    process.lines(this.dataLines, (line) => {
      // Parse the game from the line
      console.log(line);
    });
    // If logging is enabled, log the game details
    if (this.isLoggingEnabled) {
      console.log(this.totalSum);
    }
  }

  /**
   * This function processes the data lines for part 2 of the game.
   *
   * @example
   * part2(); // processes the data lines for part 2
   */
  part2() {
    process.lines(this.dataLines, (line) => {
      console.log(line);
    });
    // If logging is enabled, log the game details
    if (this.isLoggingEnabled) {
      console.log(this.totalSum);
    }
  }
}











