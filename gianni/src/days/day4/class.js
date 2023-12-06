/* eslint-disable no-unused-vars */
/* eslint-disable class-methods-use-this */

import chalk from 'chalk';

/**
 * The Day4 class processes data lines for a card game.
 * @class
 * @example
 * const dataLines = [
 *   "Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53",
 * ];
 * const isLoggingEnabled = true;
 * const day4 = new Day4(dataLines, isLoggingEnabled);
 * console.log(day4); // logs the new instance of the Day4 class
 */
export class Day4 {

  /**
   * Constructs a new instance of the Day4 class.
   * @constructor
   * @param {Array<string>} dataLines - The data lines to process.
   * @param {boolean} isLoggingEnabled - Whether logging is enabled.
   */
  constructor(dataLines, isLoggingEnabled) {
    this.dataLines = dataLines;
    this.isLoggingEnabled = isLoggingEnabled;
    this.time = {};
    this.totalSum = {
      part1: 0,
      part2: 0,
    };
  }

  /**
   * Processes the data lines and calculates the sum for part 1.
   * @method
   * @example
   * const dataLines = [
   *   "Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53",
   * ];
   * const isLoggingEnabled = true;
   * const day4 = new Day4(dataLines, isLoggingEnabled);
   * day4.part1();
   * console.log(day4.totalSum.part1);
   */
  part1() {
    const sum = this.dataLines.reduce((total, card) => {
      const [_, sides] = this.splitCard(card);
      const [leftList, rightList] = this.splitSides(sides);
      const leftArray = this.splitList(leftList);
      const rightArray = this.splitList(rightList);
      const winningNumbers = this.findWinningNumbers(leftArray, rightArray);

      if (this.isLoggingEnabled) {
        const logProperties = {
          winningNumbers,
          total,
        };
        this.logCard(card, logProperties);
      }
      return winningNumbers.length > 0 ? total + 2 ** (parseInt(winningNumbers.length, 10) - 1) : total;
    }, 0);
    this.totalSum.part1 = sum;
  }

  /**
   * Processes the data lines and calculates the sum for part 1.
   * @method
   * @example
   * const dataLines = [
   *   "Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53",
   * ];
   * const isLoggingEnabled = true;
   * const day4 = new Day4(dataLines, isLoggingEnabled);
   * day4.part2();
   * console.log(day4.totalSum.part1);
   */
  part2() {
    const instances = Array.from({ length: this.dataLines.length }, () => 1);
    this.dataLines.forEach((card) => {
      const [tag, sides] = this.splitCard(card);
      const cardNumber = parseInt(tag.split(/[ ]+/)[1], 10);
      const [leftList, rightList] = this.splitSides(sides);
      const leftArray = this.splitList(leftList);
      const rightArray = this.splitList(rightList);
      const winningNumbers = this.findWinningNumbers(leftArray, rightArray);
      for (let i = 0; i < winningNumbers.length; i++) {
        if (cardNumber + i < instances.length) {
          instances[cardNumber + i] = instances[cardNumber + i] + instances[cardNumber - 1];
        }
      }
      if (this.isLoggingEnabled) {
        const logProperties = {
          winningNumbers,
          instances,
          total: instances.reduce((total, instance) => total + instance, 0),
        };
        this.logCard(card, logProperties);
      }
    });

    this.totalSum.part2 = instances.reduce((total, instance) => total + instance, 0);
  }

  /**
   * Splits a card string into two parts based on the pattern ': '
   * @param {string} card - The card string to split.
   * @returns {Array<string>} The split card string.
   * @example
   * const card = "Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53";
   * const splitCard = splitCard(card);
   * console.log(splitCard); // ["Card 1", "41 48 83 86 17 | 83 86  6 31 17  9 48 53"]
   */
  splitCard(card) { return card.split(/[:][ ]+/); }

  /**
   * Splits a sides string into two parts based on the pattern ' | '
   * @param {string} sides - The sides string to split.
   * @returns {Array<string>} The split sides string.
   * @example
   * const sides = "41 48 83 86 17 | 83 86  6 31 17  9 48 53";
   * const splitSides = splitSides(sides);
   * console.log(splitSides); // ["41 48 83 86 17", "83 86  6 31 17  9 48 53"]
   */
  splitSides(sides) { return sides.split(/[ ]+[|][ ]+/); }

  /**
   * Splits a list string into an array of numbers.
   * @param {string} list - The list string to split.
   * @returns {Array<number>} The split list as an array of numbers.
   * @example
   * const list = "41 48 83 86 17";
   * const splitList = splitList(list);
   * console.log(splitList); // [41, 48, 83, 86, 17]
   */
  splitList(list) { return list.split(/[ ]+/); }

  /**
   * Finds the numbers that are present in both arrays.
   * @param {Array<number>} leftArray - The first array of numbers.
   * @param {Array<number>} rightArray - The second array of numbers.
   * @returns {Array<number>} The numbers that are present in both arrays.
   * @example
   * const leftArray = [41, 48, 83, 86, 17];
   * const rightArray = [83, 86,  6, 31, 17,  9, 48, 53];
   * const winningNumbers = findWinningNumbers(leftArray, rightArray);
   * console.log(winningNumbers); // [41, 48, 83, 86, 17]
   */
  findWinningNumbers(leftArray, rightArray) { return leftArray.filter(number => rightArray.includes(number)); }

  /**
   * Logs the card with its properties.
   * @param {string} card - The card string to log.
   * @param {Object} logProperties - The properties to log with the card.
   * @example
   * const card = "Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53";
   * const logProperties = { winningNumbers: [41, 48, 83, 86, 17], total: 225 };
   * logCard(card, logProperties); // logs the card with its properties
   */
  logCard(card, logProperties) {

    const updatedCardLine = this.logCardLineUpdate(card, logProperties.winningNumbers);
    if (logProperties.winningNumbers.length > 0 && !logProperties.instances) {
      console.log(
        updatedCardLine,
        `${chalk.dim.cyan('points:')} ${chalk.yellow(logProperties.winningNumbers.length)}`,
        `${chalk.dim.cyan('total:')} ${chalk.yellow(logProperties.total)}`,
      );
    } else if (logProperties.instances) {
      console.log(
        updatedCardLine,
        `${chalk.dim.cyan('instances:')} ${chalk.yellow(logProperties.instances)}`,
        `${chalk.dim.cyan('total:')} ${chalk.yellow(logProperties.total)}`,
      );
    } else {
      console.log(updatedCardLine);
    }
  }


  /**
   * Updates the card line for logging.
   * @param {string} card - The card string to update.
   * @param {Array<number>} winningNumbers - The winning numbers to highlight in the card.
   * @returns {string} The updated card line.
   * @example
   * const card = "Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53";
   * const winningNumbers = [41, 48, 83, 86, 17];
   * const updatedCardLine = logCardLineUpdate(card, winningNumbers);
   * console.log(updatedCardLine); // logs the updated card line
   */
  logCardLineUpdate(card, winningNumbers) {
    const cardColor = winningNumbers.length > 0 ? chalk.green : chalk.red;
    let updatedCardLine = this.logCardColorUpdate(card, cardColor, winningNumbers);
    updatedCardLine = this.logCardNumberHighlight(updatedCardLine, winningNumbers);
    return updatedCardLine;
  }

  /**
 * Updates the card color for logging.
 * @param {string} card - The card string to update.
 * @param {Function} cardColor - The chalk color function to use.
 * @param {Array<number>} winningNumbers - The winning numbers to check.
 * @returns {string} The updated card color.
 * @example
 * const card = "Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53";
 * const cardColor = chalk.green;
 * const winningNumbers = [41, 48, 83, 86, 17];
 * const updatedCardColor = logCardColorUpdate(card, cardColor, winningNumbers);
 * console.log(updatedCardColor); // logs the updated card color
 */
  logCardColorUpdate(card, cardColor, winningNumbers) {
    return winningNumbers.length > 0
      ? card.replace('Card', cardColor('Card'))
      : card.replace(card, cardColor(card));
  }

  /**
 * Highlights the winning numbers in the card for logging.
 * @param {string} card - The card string to update.
 * @param {Array<number>} winningNumbers - The winning numbers to highlight.
 * @returns {string} The card with the winning numbers highlighted.
 * @example
 * const card = "Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53";
 * const winningNumbers = [41, 48, 83, 86, 17];
 * const highlightedCard = logCardNumberHighlight(card, winningNumbers);
 * console.log(highlightedCard); // logs the card with the winning numbers highlighted
 */
  logCardNumberHighlight(card, winningNumbers) {
    const [cardName, numbers] = card.split(':');
    const parts = cardName.split(' ');
    const cardString = parts.slice(0, -1).join(' ');
    const cardIndex = parts[parts.length - 1];

    if (winningNumbers.length > 0) {
      const replacements = new Map(winningNumbers.map((num) => {
        if (num >= 0 && num < 10) { // check if num is a single digit
          return [`  ${num}`, `  ${chalk.green(`${num}`)}`];
        }
        return [` ${num}`, ` ${chalk.green(num)}`];

      }));
      const regex = new RegExp(Array.from(replacements.keys()).join('|'), 'g');
      return `${cardString} ${cardIndex.replace(cardIndex, chalk.yellow(`${cardIndex}:`))}${chalk.grey(numbers.replace(regex, match => replacements.get(match)))}`;
    }
    return card;
  }
}
