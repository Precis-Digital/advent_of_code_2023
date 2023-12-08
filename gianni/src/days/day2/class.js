/* eslint-disable class-methods-use-this */
// import chalk from 'chalk';
import chalk from 'chalk';
import { process, split } from '../../utils/utils.js';

/**
 * The Day2 class represents a game with a series of sets of colored cubes.
 *
 * @property {Array<string>} dataLines - An array of strings, each representing a game. Each game is represented as a series of sets of cubes, separated by semicolons. Each set of cubes is represented as a series of cube counts, separated by commas. Each cube count is represented as a number followed by a color (red, green, or blue).
 * @property {boolean} isLoggingEnabled - A boolean indicating whether logging is enabled.
 * @property {number} maxLineLength - The maximum length of a line in the dataLines array.
 * @property {Object} availableCubes - An object representing the available cubes, with properties for red, green, and blue cubes.
 * @property {Object} totalSum - An object representing the total sum of cubes, with properties for part1 and part2.
 *
 * @example
 * const dataLines = [
 *   "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green"
 * ];
 * const day2 = new Day2(dataLines);
 * console.log(day2);
 */
export class Day2 {
  /**
   * Creates an instance of the Day2 class.
   *
   * @param {Array<string>} dataLines - An array of strings, each representing a game. Each game is represented as a series of sets of cubes, separated by semicolons. Each set of cubes is represented as a series of cube counts, separated by commas. Each cube count is represented as a number followed by a color (red, green, or blue).
   * @param {boolean} isLoggingEnabled - A boolean indicating whether logging is enabled.
   *
   */
  constructor(dataLines, isLoggingEnabled) {
    this.dataLines = dataLines;
    this.isLoggingEnabled = isLoggingEnabled;
    this.maxLineLength = Math.max(...this.dataLines.map(line => line.length));
    this.availableCubes = { red: 12, green: 13, blue: 14 };
    this.totalSum = {
      part1: 0,
      part2: 0,
    };
  }

  /**
   * Returns a string representation of the available cubes.
   * @returns {string} A string representation of the available cubes.
   * @example
   * const game = new Game();
   * const availableCubesString = game.getAvailableCubesString();
   * console.log(availableCubesString);
   */
  getAvailableCubesString() {
    return Object.entries(this.availableCubes)
      .map(([color, quantity]) => `${chalk[color](color)} ${chalk.yellow(`${quantity}`.padEnd(3, ' '))}`)
      .join(' ');
  }

  /**
   * Returns an array of game sets from a given side string.
   * @param {string} side - The side string to process.
   * @returns {Array} An array of game sets.
   * @example
   * const game = new Game();
   * const gameSets = game.getGameSets("3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green");
   * console.log(gameSets);
   */
  getGameSets(side) {
    return side.split(/\s*;\s*/).map(group => group.split(/\s*,\s*/).reduce((acc, pair) => {
      const [quantity, color] = pair.split(/\s+/);
      acc[color] = parseInt(quantity, 10);
      return acc;
    }, { red: 0, green: 0, blue: 0 }));
  }

  /**
   * Returns an object representing the minimum cubes needed for the game sets.
   * @param {Array} gameSets - The game sets to process.
   * @returns {Object} An object representing the minimum cubes needed.
   * @example
   * const game = new Game();
   * const minimumCubesNeeded = game.getMinimumCubesNeeded([{red: 3, green: 2, blue: 1}, {red: 1, green: 2, blue: 3}]);
   * console.log(minimumCubesNeeded);
   */
  getMinimumCubesNeeded(gameSets) {
    return gameSets.reduce((acc, set) => {
      ['red', 'green', 'blue'].forEach((color) => {
        acc[color] = Math.max(acc[color] || 0, set[color] || 0);
      });
      return acc;
    }, {});
  }

  /**
   * Checks if there are enough cubes for the game sets.
   * @param {Array} gameSets - The game sets to check.
   * @returns {boolean} True if there are enough cubes, false otherwise.
   * @example
   * const game = new Game();
   * const hasEnoughCubes = game.hasEnoughCubes([{red: 3, green: 2, blue: 1}, {red: 1, green: 2, blue: 3}]);
   * console.log(hasEnoughCubes);
   */
  hasEnoughCubes(gameSets) {
    return !gameSets.some(set => !Object.keys(set).every(color => set[color] <= this.availableCubes[color]));
  }

  /**
   * Returns a colored tag based on whether there are enough cubes.
   * @param {string} tag - The tag to color.
   * @param {boolean} hasEnoughCubes - Whether there are enough cubes.
   * @returns {string} The colored tag.
   * @example
   * const game = new Game();
   * const coloredTag = game.colorTag("Game 1", true);
   * console.log(coloredTag);
   */
  colorTag(tag, hasEnoughCubes) {
    return hasEnoughCubes ? chalk.green(tag) : chalk.red(tag);
  }

  /**
   * Returns a colored side string based on the available cubes.
   * @param {string} side - The side string to color.
   * @returns {string} The colored side string.
   * @example
   * const game = new Game();
   * const coloredSide = game.colorSide("3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green");
   * console.log(coloredSide);
   */
  colorSide(side) {
    return side.replace(/(\d+)\s+(\w+)/g, (match, quantity, color) => {
      const num = parseInt(quantity, 10);
      return num <= this.availableCubes[color] ? `${chalk.green(num)} ${chalk.gray(color)}` : `${chalk.red(num)} ${chalk.gray(color)}`;
    });
  }

  /**
   * Returns a colored string representation of the minimum cubes needed.
   * @param {Object} minimumCubesNeeded - The minimum cubes needed.
   * @returns {string} The colored string representation.
   * @example
   * const game = new Game();
   * const coloredMinimumCubesNeeded = game.colorMinimumCubesNeeded({red: 3, green: 2, blue: 1});
   * console.log(coloredMinimumCubesNeeded);
   */
  colorMinimumCubesNeeded(minimumCubesNeeded) {
    return Object.entries(minimumCubesNeeded)
      .map(([color, quantity]) => `${chalk[color](color)} ${chalk.yellow(`${quantity}`.padEnd(3, ' '))}`)
      .join(' ');
  }

  /**
   * Processes the part 1 of the game.
   * @example
   * const game = new Game();
   * game.part1();
   */
  part1() {
    const availableCubesString = this.getAvailableCubesString();
    if (this.isLoggingEnabled) console.log('Available cubes:', availableCubesString, '\n');

    process.lines(this.dataLines, (line) => {
      let [tag, index, side] = split.line(line.padEnd(this.maxLineLength, ' '));
      const gameSets = this.getGameSets(side);
      let minimumCubesNeeded = this.getMinimumCubesNeeded(gameSets);
      const hasEnoughCubes = this.hasEnoughCubes(gameSets);
      tag = this.colorTag(tag, hasEnoughCubes);
      side = this.colorSide(side);
      minimumCubesNeeded = this.colorMinimumCubesNeeded(minimumCubesNeeded);
      const points = hasEnoughCubes ? index : 0;
      this.totalSum.part1 += points;
      if (this.isLoggingEnabled) {
        console.log(
          tag,
          `${chalk.yellow(index)}:`,
          side,
          minimumCubesNeeded,
          hasEnoughCubes ? '✅ ' : '❌ ',
          `${chalk.blue('points:')} ${chalk.yellow(`${points}`.padEnd(3, ' '))}`,
          `${chalk.blue('total:')} ${chalk.yellow(`${this.totalSum.part1}`.padEnd(2, ' '))}`,
        );
      }
    });
  }

  /**
   * Processes the part 2 of the game.
   * @example
   * const game = new Game();
   * game.part2();
   */
  part2() {
    const availableCubesString = this.getAvailableCubesString();
    if (this.isLoggingEnabled) console.log('Available cubes:', availableCubesString, '\n');

    process.lines(this.dataLines, (line) => {
      let [tag, index, side] = split.line(line.padEnd(this.maxLineLength, ' '));
      const gameSets = this.getGameSets(side);
      let minimumCubesNeeded = this.getMinimumCubesNeeded(gameSets);
      const hasEnoughCubes = this.hasEnoughCubes(gameSets);
      const power = minimumCubesNeeded.red * minimumCubesNeeded.green * minimumCubesNeeded.blue;
      this.totalSum.part2 += power;
      tag = this.colorTag(tag, hasEnoughCubes);
      side = this.colorSide(side);
      minimumCubesNeeded = this.colorMinimumCubesNeeded(minimumCubesNeeded);
      if (this.isLoggingEnabled) {
        console.log(
          tag,
          `${chalk.yellow(index)}:`,
          side,
          minimumCubesNeeded,
          hasEnoughCubes ? '✅ ' : '❌ ',
          `${chalk.blue('points:')} ${chalk.yellow(`${power}`.padEnd(4, ' '))}`,
          `${chalk.blue('total:')} ${chalk.yellow(`${this.totalSum.part2}`.padEnd(2, ' '))}`,
        );
      }
    });
  }
}
