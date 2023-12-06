// import chalk from 'chalk';
import { process } from '../../utils/utils.js';

/**
 * @class
 *
 * @description Represents a day in a game. It holds the game details and performs operations related to the game.
 *
 * @property {Array} dataLines - The lines of data for the game.
 * @property {boolean} isLoggingEnabled - Whether logging is enabled.
 * @property {Object} availableCubes - The available cubes in the game.
 * @property {Array} colors - The colors in the game.
 * @property {Object} gameDetailsArray - The details of the game.
 * @property {Object} gamePowerArray - The power of the game.
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
    this.availableCubes = { red: 12, green: 13, blue: 14 };
    this.colors = ['red', 'green', 'blue'];
    this.gameDetailsArray = {};
    this.gamePowerArray = {};
    this.totalSum = {
      part1: 0,
      part2: 0,
    };
  }

  /**
   * This function prepares a cube set by sorting it according to the colors.
   *
   * @param {object} cubeSet - The original cube set. For example, {red: 2, green: 3, blue: 1}.
   * @returns {object} The sorted cube set. For example, {blue: 1, green: 3, red: 2}.
   *
   * @example
   * prepareCubeSet({red: 2, green: 3, blue: 1}); // returns {blue: 1, green: 3, red: 2}
   */
  prepareCubeSet(cubeSet) {
    return this.colors.reduce((sortedCubeSet, key) => {
      sortedCubeSet[key] = cubeSet[key] || 0;
      return sortedCubeSet;
    }, {});
  }

  /**
   * This function checks if there are enough cubes in the game object.
   *
   * @param {object} gameObject - The game object.
   * @returns {boolean} True if there are enough cubes, false otherwise.
   *
   * @example
   * checkIfThereIsEnoughCubes(gameObject); // returns true or false
   */
  checkIfThereIsEnoughCubes(gameObject) {
    return !gameObject.sets.some(set => !Object.keys(set).every(color => set[color] <= this.availableCubes[color]));
  }

  /**
   * This function calculates the minimum number of cubes needed for each color in the game object.
   *
   * @param {object} gameObject - The game object.
   * @returns {object} The minimum number of cubes needed for each color.
   *
   * @example
   * minimumCubesNeeded(gameObject); // returns {red: 2, green: 3, blue: 1}
   */
  minimumCubesNeeded(gameObject) {
    return gameObject.sets.reduce((acc, set) => {
      this.colors.forEach((color) => {
        acc[color] = Math.max(acc[color] || 0, set[color] || 0);
      });
      return acc;
    }, {});
  }

  /**
   * This function parses a set group into a cube set.
   *
   * @param {array} setGroup - The set group. For example, ['2 red', '3 green', '1 blue'].
   * @returns {object} The cube set. For example, {red: 2, green: 3, blue: 1}.
   *
   * @example
   * parseSetGroup(['2 red', '3 green', '1 blue']); // returns {red: 2, green: 3, blue: 1}
   */
  parseSetGroup(setGroup) {
    const cubeSet = {};
    setGroup.forEach((color) => {
      const [cubeAmount, cubeColor] = color.trim().split(' ');
      cubeSet[cubeColor] = parseInt(cubeAmount, 10);
    });
    return this.prepareCubeSet(cubeSet);
  }

  /**
   * This function parses a game from a line.
   *
   * @param {string} line - The line. For example, 'Game 1: 2 red, 3 green, 1 blue'.
   * @returns {object} The game object.
   *
   * @example
   * parseGameFromLine('Game 1: 2 red, 3 green, 1 blue'); // returns game object
   */
  parseGameFromLine(line) {
    const [gameString, setsString] = line.split(':');
    const game = gameString.split(' ');
    const gameIndex = parseInt(game[game.length - 1], 10);
    const sets = setsString.split(';');
    const gameObject = { line, index: gameIndex, sets: [] };

    sets.forEach((set) => {
      const setGroup = set.trim().split(',');
      gameObject.sets.push(this.parseSetGroup(setGroup));
    });

    gameObject.hasEnoughCubes = this.checkIfThereIsEnoughCubes(gameObject);
    gameObject.minimumCubesNeeded = this.minimumCubesNeeded(gameObject);

    return gameObject;
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
      const gameObject = this.parseGameFromLine(line);

      // If the game has enough cubes, add its index to the total sum of indexes
      if (gameObject.hasEnoughCubes) {
        this.totalSum.part1 += gameObject.index;
      }

      // Add the game details to the array
      this.gameDetailsArray[gameObject.index] = gameObject.hasEnoughCubes ? '✅' : '❌';

    });
    // If logging is enabled, log the game details
    if (this.isLoggingEnabled) {
      console.log(this.gameDetailsArray);
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
      // Parse the game from the line
      const gameObject = this.parseGameFromLine(line);

      // Calculate the power of the game
      gameObject.power = gameObject.minimumCubesNeeded.red * gameObject.minimumCubesNeeded.green * gameObject.minimumCubesNeeded.blue;

      // Add the power of the game to the total sum of power
      this.totalSum.part2 += gameObject.power;

      this.gamePowerArray[gameObject.index] = gameObject.power;

    });
    // If logging is enabled, log the game details
    if (this.isLoggingEnabled) {
      console.log(this.gamePowerArray);
    }
  }
}











