/* eslint-disable class-methods-use-this */

import chalk from 'chalk';

/**
 * @class
 *
 * @description Represents a day in a game. It holds the game details and performs operations related to the game.
 *
 * @property {Array} dataLines - The lines of data for the game.
 * @property {boolean} isLoggingEnabled - Whether logging is enabled.
 * @property {number} totalSum - The total sum of the numbers.
 */
export class Day3 {
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

  numberRange(start, end) {
    return new Array(end - start).fill().map((d, i) => i + start);
  }

  getLineLength() { return this.dataLines.indexOf('\n') + 1; }

  getSymbolPositions(symbolRegexp) { return [...this.dataLines.matchAll(symbolRegexp)].map(match => match.index); }

  getNumbers(numberRegexp) { return [...this.dataLines.matchAll(numberRegexp)].map(match => [match[0], match.index, match[0].length]); }

  getPositionsToCheck(number, lineLength) {
    const isEdgeLeft = number[1] % lineLength === 0;
    const isEdgeRight = (number[1] + number[2] + 1) % lineLength === 0;
    const positionsToCheck = [
      ...this.numberRange(number[1] - (!isEdgeLeft && 1) - lineLength, number[1] + number[2] - lineLength + (!isEdgeRight && 1)),
      !isEdgeLeft && number[1] - 1,
      !isEdgeRight && number[1] + number[2],
      ...this.numberRange(number[1] - (!isEdgeLeft && 1) + lineLength, number[1] + number[2] + lineLength + (!isEdgeRight && 1)),
    ];
    return positionsToCheck.filter(position => position >= 0 && position < this.dataLines.length);
  }

  getModifiedInput(numbers, symbolPositions, isPartNumber, part) {
    let modifiedInput = this.dataLines.split('\n'); // split the data into lines
    let sum = 0;

    let pairs = [];
    const products = [];

    modifiedInput = modifiedInput.map((line, index) => { // map each line to a new format
      let newLine = line;

      numbers.forEach((number) => {
        const replacement = isPartNumber(number) ? chalk.green(number[0]) : chalk.red(number[0]);
        const regex = new RegExp(`\\b${number[0]}\\b`, 'g');
        newLine = newLine.replace(regex, replacement);
      });

      symbolPositions.forEach((position) => {
        const symbol = this.dataLines[position];
        const escapedSymbol = symbol.replace(/[-/\\^$*+?.()|[\]{}]/g, '\\$&'); // escape special characters
        const regex = new RegExp(`${escapedSymbol}`, 'g');
        newLine = newLine.replaceAll(regex, chalk.cyanBright(symbol));
      });

      // Add this block to dim all non-chalked characters
      const chalkRegex = /\\u001b\[\d+m/g;
      if (!chalkRegex.test(newLine)) {
        newLine = chalk.gray(newLine);
      }

      sum += isPartNumber(numbers[index]) ? parseInt(numbers[index][0], 10) : 0;

      if (isPartNumber(numbers[index])) {
        pairs.push(numbers[index][0]);

        if (pairs.length === 2) {
          const product = pairs.reduce((a, b) => a * b);
          if (product > 0) {
            products.push(product);
          }
          pairs = [];
        }
      }

      const sumPart2 = products.reduce((a, b) => a + b, 0);

      // append the points and total to each line
      newLine += ` ${chalk.blue('points:')} ${isPartNumber(numbers[index]) ? chalk.yellow(numbers[index][0].padEnd(4, ' ')) : chalk.red('0'.padEnd(4, ' '))} ${chalk.blue('total:')} ${chalk.yellow(part === 'part1' ? sum : sumPart2)}`;
      return newLine;
    });

    modifiedInput = modifiedInput.join('\n'); // join the lines back together
    console.log(modifiedInput);

    return modifiedInput;
  }

  part1() {
    const lineLength = this.getLineLength();
    const symbolPositions = this.getSymbolPositions(/[^0-9.\n]/g);
    const numbers = this.getNumbers(/[0-9]+/g);

    const isPartNumber = (number) => {
      const positionsToCheck = this.getPositionsToCheck(number, lineLength);
      return positionsToCheck.some(position => symbolPositions.includes(position));
    };

    numbers.forEach((number) => {
      if (isPartNumber(number)) {
        this.totalSum.part1 += parseInt(number[0], 10);
      }
    });

    if (this.isLoggingEnabled) this.getModifiedInput(numbers, symbolPositions, isPartNumber, 'part1');
  }

  part2() {
    const lineLength = this.getLineLength();
    const symbolPositions = this.getSymbolPositions(/[*]/g);
    const numbers = this.getNumbers(/[0-9]+/g);
    const potentialGears = Array.from({ length: symbolPositions.length }, () => []);

    numbers.forEach((number) => {
      const positionsToCheck = this.getPositionsToCheck(number, lineLength);
      positionsToCheck.forEach((position) => {
        const symbolIndex = symbolPositions.findIndex(p => p == position);
        if (symbolIndex >= 0) {
          potentialGears[symbolIndex].push(number);
        }
      });
    });

    const gearsWithTwoParts = potentialGears.filter(gear => gear.length === 2);

    const isGearNumber = number => gearsWithTwoParts.some(subArray => subArray.some(item => item.every((val, index) => val === number[index])));

    if (this.isLoggingEnabled) this.getModifiedInput(numbers, symbolPositions, isGearNumber, 'part2');

    this.totalSum.part2 = potentialGears.reduce((total, gear) => {
      const isGear = gear.length === 2;
      return isGear ? total + parseInt(gear[0], 10) * parseInt(gear[1], 10) : total;
    }, 0);
  }
}
