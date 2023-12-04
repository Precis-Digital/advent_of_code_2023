/* eslint-disable class-methods-use-this */

import chalk from 'chalk';

export default class CardGame {
  constructor(dataLines, isLoggingEnabled) {
    this.dataLines = dataLines;
    this.isLoggingEnabled = isLoggingEnabled;
    this.cardIndexes = [];
    this.cards = [];
    this.totalSum = 0;
  }

  generateCardIndexes(index, length) {
    return Array.from({ length }, (_, i) => i + index + 1);
  }

  parseCardData(cardData) {
    const [cardIndexPart, numbersPart] = cardData.split(': ');
    const [, index] = cardIndexPart.split(' ');
    const [winnerNumberPart, myNumberPart] = numbersPart.split(' | ');
    const winnerNumbers = winnerNumberPart.split(' ').map(Number);
    const myNumbers = myNumberPart.split(' ').map(Number);
    const matchingNumbers = myNumbers.filter(num => winnerNumbers.includes(num));
    const points = matchingNumbers.length > 0 ? 2 ** (matchingNumbers.length - 1) : 0;
    const cardIndexes = this.generateCardIndexes(Number(index), matchingNumbers.length);

    if (this.isLoggingEnabled) {
      cardData = cardData.replace('Card', matchingNumbers.length > 0 ? chalk.green('Card') : chalk.red('Card'));
      cardData = chalk.grey(cardData);

      numbersPart.map(() => matchingNumbers.reduce((updatedData, num) => {
        const regex = new RegExp(` ${num} `, 'g');
        return chalk.grey(updatedData.replace(regex, ` ${chalk.green(num)} `));
      }, cardData)).join('');

      console.log(
        cardData,
        `${chalk.blue('points:')} ${chalk.yellow(points)}`,
      );
    }

    return {
      index,
      points,
      cardIndexes,
    };
  }

  cloneCardsRecursively() {
    this.cards = this.cards.map((card) => {
      const cardsClones = card.clonedCards.map((cardClonesNumber) => {
        const cardCloneLine = this.dataLines[cardClonesNumber - 1];
        const cardCloneParsed = this.parseCardData(cardCloneLine);
        return cardCloneParsed.cardsClones.length > 0 ? cardCloneParsed : null;
      }).filter(cardCloneParsed => cardCloneParsed !== null);

      if (card.clonedCards.length > 0) {
        this.cardIndexes.push(card.clonedCards);
        this.cloneCardsRecursively(cardsClones);
      }

      return card;
    });
  }

  calculateWinningCards() {
    if (!Array.isArray(this.dataLines) || this.dataLines.length === 0) {
      throw new Error('Invalid input: dataLines must be a non-empty array');
    }

    this.dataLines.reduce((acc, line, index) => {
      const card = this.parseCardData(line);
      this.cards.push(card);
      this.cardIndexes.push(index + 1);
      this.totalSum += card.points;

      return card;
    }, 0);

    this.cloneCardsRecursively();

    const cardCounts = this.cardIndexes.flatMap(indexes => indexes)
      .reduce((acc, index) => {
        acc[index] = (acc[index] || 0) + 1;
        return acc;
      }, {});

    const scratchCardStats = Object.entries(cardCounts).map(([index, count]) => ({ index: Number(index), count }));

    const scratchcardsObject = {
      scratchCardStats,
      total: scratchCardStats.reduce((acc, { count }) => acc + count, 0),
    };

    if (this.isLoggingEnabled) {
      console.log('\n', scratchcardsObject);
    }

    return {
      part1: this.totalSum,
      part2: scratchcardsObject,
    };
  }
}
