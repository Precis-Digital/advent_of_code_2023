/* eslint-disable class-methods-use-this */

import chalk from 'chalk';

export default class Solution {
  constructor(dataLines, isLoggingEnabled) {
    this.dataLines = dataLines;
    this.cards = [];
    this.isLoggingEnabled = isLoggingEnabled;
    this.cardIndexes = [];
    this.totalPoints = 0;
    this.totalScratchcards = 0;
  }

  // core method

  part1() {
    if (!Array.isArray(this.dataLines) || this.dataLines.length === 0) {
      throw new Error('Invalid input: dataLines must be a non-empty array');
    }

    if (this.isLoggingEnabled) {
      console.log('\npart-1:\n');
    }
    const cards = new Array(this.dataLines.length);
    const cardIndexes = new Array(this.dataLines.length);

    this.dataLines.forEach((cardLine, index) => {
      const card = this.parseCardLine(cardLine);
      cards[index] = card;
      cardIndexes[index] = index + 1;
      this.totalPoints += card.points;
    });

    if (this.isLoggingEnabled) {
      console.log('total points:', this.totalPoints, '\n')
    }

    this.cards = cards;

    this.cardIndexes = cards.flatMap((card) => {
      if (card.cardIndexes.length > 0) {
        return card.cardIndexes;
      }
      return [];
    });
  }

  part2() {
    if (!Array.isArray(this.dataLines) || this.dataLines.length === 0) {
      throw new Error('Invalid input: dataLines must be a non-empty array');
    }

    this.cardIndexes = this.cardIndexes.flat();

    // Call the function
    this.loopThroughCards();

    const originalCardIndexes = Array.from({ length: this.dataLines.length }, (_, i) => i + 1);

    this.cardIndexes.unshift(originalCardIndexes); // Add the original cardIndexes to the beginning of this.cardIndexes
    this.cardIndexes = this.cardIndexes.flat(); // Flatten the array

    const indexOverview = this.cardIndexes.reduce((acc, curr) => {
      acc[curr] = (acc[curr] || 0) + 1;
      return acc;
    }, {});

    this.totalScratchcards = Object.values(indexOverview).reduce((a, b) => a + b, 0);

    if (this.isLoggingEnabled) {
      console.log('\npart-2:\n\n', indexOverview, 'total:', this.totalScratchcards); // Outputs: 24
    }
  }

  // loopThroughCards main method
  loopThroughCards() {
    const queue = [...this.cardIndexes];

    while (queue.length > 0) {
      const index = queue.shift();
      const { cardIndexes } = this.cards[index - 1];

      if (cardIndexes.length > 0) {
        this.cardIndexes.push(...cardIndexes);
        queue.push(...cardIndexes);
      }
    }
  }

  // splitCardLine main method
  splitCardLine(cardLine) {
    const { cardIndexPart, winnerNumberPart, myNumberPart } = this.splitCardLineIntoParts(cardLine);
    const index = this.extractIndexFromCardPart(cardIndexPart);
    const winnerNumbers = this.extractNumbersFromNumberPart(winnerNumberPart);
    const myNumbers = this.extractNumbersFromNumberPart(myNumberPart);

    return {
      index,
      winnerNumbers,
      myNumbers,
    };
  }

  // splitCardLine sub methods
  splitCardLineIntoParts(cardLine) {
    const [cardIndexPart, numbersPart] = cardLine.split(': ');
    const [winnerNumberPart, myNumberPart] = numbersPart.split(' | ');
    return { cardIndexPart, winnerNumberPart, myNumberPart };
  }

  extractIndexFromCardPart(cardIndexPart) {
    const indexArray = cardIndexPart.split(' ');
    const index = Number(indexArray[indexArray.length - 1]);
    return index;
  }

  extractNumbersFromNumberPart(numberPart) {
    return numberPart.split(' ').filter(item => item !== '').map(Number);
  }

  // parseCardLine main method
  parseCardLine(cardLine, isClone = false) {
    const parsedData = this.splitCardLine(cardLine);
    const matchingNumbers = this.getMatchingNumbers(parsedData.winnerNumbers, parsedData.myNumbers);
    const points = this.calculatePoints(matchingNumbers);
    const cardIndexes = this.generateCardIndexes(Number(parsedData.index), matchingNumbers.length);

    if (this.isLoggingEnabled) {
      const logProperties = {
        matchingNumbers,
        points,
        isClone,
      };
      this.logCardLine(cardLine, logProperties);
    }

    return {
      index: parsedData.index,
      points,
      cardIndexes,
    };
  }

  // parseCardLine sub methods
  getMatchingNumbers(winnerNumbers, myNumbers) {
    const winnerNumbersSet = new Set(winnerNumbers);
    return myNumbers.filter(num => winnerNumbersSet.has(num));
  }

  calculatePoints(matchingNumbers) {
    return matchingNumbers.length > 0 ? 2 ** (matchingNumbers.length - 1) : 0;
  }

  generateCardIndexes(index, length) {
    return Array.from({ length }, (_, i) => i + index + 1);
  }

  // logCardLine main method
  logCardLine(cardLine, logProperties) {
    const updatedCardLine = this.updateCardLine(cardLine, logProperties.matchingNumbers);
    if (logProperties.isClone) {
      console.log(updatedCardLine);
    } else {
      if (logProperties.points > 0) {
        console.log(updatedCardLine, `${chalk.dim.cyan('points:')} ${chalk.yellow(logProperties.points)}`);
      } else {
        console.log(updatedCardLine);
      }
    }
  }

  // logCardLine sub methods
  updateCardLine(cardLine, matchingNumbers) {
    const cardColor = matchingNumbers.length > 0 ? chalk.green : chalk.red;
    let updatedCardLine = this.updateCardColor(cardLine, cardColor, matchingNumbers);
    updatedCardLine = this.highlightMatchingNumbers(updatedCardLine, matchingNumbers);
    return updatedCardLine;
  }

  updateCardColor(cardLine, cardColor, matchingNumbers) {
    return matchingNumbers.length > 0
      ? cardLine.replace('Card', cardColor('Card'))
      : cardLine.replace(cardLine, cardColor(cardLine));
  }

  highlightMatchingNumbers(cardLine, matchingNumbers) {
    const [cardName, numbers] = cardLine.split(':');
    const parts = cardName.split(' ');
    const cardString = parts.slice(0, -1).join(' ');
    const cardIndex = parts[parts.length - 1];

    if (matchingNumbers.length > 0) {
      const replacements = new Map(matchingNumbers.map((num) => {
        if (num >= 0 && num < 10) { // check if num is a single digit
          return [`  ${num}`, `  ${chalk.green(`${num}`)}`];
        }
        return [` ${num}`, ` ${chalk.green(num)}`];

      }));
      const regex = new RegExp(Array.from(replacements.keys()).join('|'), 'g');
      return `${cardString} ${cardIndex.replace(cardIndex, chalk.yellow(`${cardIndex}:`))}${chalk.grey(numbers.replace(regex, match => replacements.get(match)))}`;
    }
    return cardLine;
  }
}
