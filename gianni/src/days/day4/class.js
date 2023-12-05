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
  calculateWinningCards() {
    if (!Array.isArray(this.dataLines) || this.dataLines.length === 0) {
      throw new Error('Invalid input: dataLines must be a non-empty array');
    }

    // Part-1
    if (this.isLoggingEnabled) {
      console.log('\ncards\n');
    }
    const cards = new Array(this.dataLines.length);
    const cardIndexes = new Array(this.dataLines.length);

    this.dataLines.forEach((cardLine, index) => {
      const card = this.parseCardLine(cardLine);
      cards[index] = card;
      cardIndexes[index] = index + 1;
      this.totalPoints += card.points;
    });

    this.cards = cards;
    // this.cardIndexes = cardIndexes;

    this.cardIndexes = cards.flatMap((card) => {
      if (card.cardIndexes.length > 0) {
        return [card.cardIndexes];
      }
      return [];
    });


    // Part-2

    // Loop thru all indexes in this.cardIndexes
    // For each indexGroup, loop thru all indexes
    // For each index, get the corresponding cardObject from this.cards
    // For each cardObject, get the cardIndexes
    // Add the cardIndexes to this.cardIndexes

    console.log('\ninitial card clones:\n\n', this.cardIndexes);

    ///////////////////////
    // PROBLEM HERE ///////
    ///////////////////////

    this.cardIndexes.forEach((indexGroup) => {
      indexGroup.forEach((index) => {
        const cardObject = this.cards[index - 1];
        if (cardObject) {
          const cardClonesIndexes = cardObject.cardIndexes;
          if (cardClonesIndexes.length > 0 && cardIndexes.length > 0) {
            this.cardIndexes = [...this.cardIndexes, [...cardClonesIndexes]];
            // console.log(groupIndex, indexGroup, cardObject, this.cardIndexes);
          }
        }
      });
    });

    ///////////////////////
    ///////////////////////

    console.log('\nafter cloning all: (something goes wrong here)\n\n', this.cardIndexes);

    this.cardIndexes.unshift(cardIndexes); // Add the original cardIndexes to the beginning of this.cardIndexes

    console.log('\nafter adding original card indexes:\n\n', this.cardIndexes);

    const cardInstances = this.cardIndexes.reduce((acc, curr) => {
      curr.forEach((index) => {
        if (acc[index]) {
          acc[index] += 1;
        } else {
          acc[index] = 1;
        }
      });
      return acc;
    }, {});

    const totalSum = Object.values(cardInstances).reduce((a, b) => a + b, 0);

    console.log('\nindex overview:\n\n', cardInstances, 'total:', totalSum); // Outputs: 24
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
      console.log(updatedCardLine, `${chalk.blue('points:')} ${chalk.yellow(logProperties.points)}`);
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
    if (matchingNumbers.length > 0) {
      const replacements = new Map(matchingNumbers.map((num) => {
        if (num >= 0 && num < 10) { // check if num is a single digit
          return [`  ${num}`, `  ${chalk.green(`${num}`)}`];
        }
        return [` ${num}`, ` ${chalk.green(num)}`];

      })); const regex = new RegExp(Array.from(replacements.keys()).join('|'), 'g');
      return cardLine.replace(regex, match => replacements.get(match));
    }
    return cardLine;
  }
}
