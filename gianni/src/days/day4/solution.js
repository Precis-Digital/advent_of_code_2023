/* DIALY MESSAGE
============================================================================= */

/*
  part-1 done
  nice logs and documentation are WIP
*/

/* IMPORTS
============================================================================= */

import chalk from 'chalk';
import { getRuntime, getFileSize, loadTextFile } from '../../utils/getters.js';
import { log } from '../../utils/log.js';

/* CONSTANTS
============================================================================= */

const DAY = 'day4';

/* CORE FUNCTIONS
============================================================================= */
function generatLineNumbers(index, length) {
  const numbers = [];
  for (let i = index + 1; i <= index + length; i++) {
    numbers.push(i);
  }
  return numbers;
}

const parseCard = (cardLine, isLoggingEnabled) => {
  const parts = cardLine.split(': ');
  const index = parts[0].split(' ').filter(str => str.length).map(Number)[1];
  const numbers = parts[1].split(' | ');
  const winnerNumber = numbers[0].split(' ').filter(str => str.length).map(Number);
  const myNumber = numbers[1].split(' ').filter(str => str.length).map(Number);
  const matchingNumbers = myNumber.filter(num => winnerNumber.includes(num));
  const points = matchingNumbers.length > 0 ? 2 ** (matchingNumbers.length - 1) : 0;

  // get all copies now it only goes down one level but needs to be recursive
  const cardsClones = generatLineNumbers(index, matchingNumbers.length);

  if (isLoggingEnabled) {
    cardLine = cardLine.replace('Card', matchingNumbers.length > 0 ? chalk.green('Card') : chalk.red('Card'));
    cardLine = chalk.grey(cardLine);

    numbers.forEach(() => {
      matchingNumbers.forEach((num) => {
        const regex = new RegExp(` ${num} `, 'g');
        cardLine = chalk.grey(cardLine.replace(regex, ` ${chalk.green(num)} `));
      });
    });

    console.log(
      cardLine,
      `${chalk.blue('points:')} ${chalk.yellow(points)}`,
    );
  }

  return {
    index,
    // matchingNumbers,
    points,
    cardsClones,
  };
};

const recursiveCloneCards = (cards, dataLines, CARD_INDEXES, isLoggingEnabled) => {
  const clonesGroups = cards.map((card) => {
    // console.log(card.cardsClones);
    const cardsClones = [];

    card.cardsClones.forEach((cardClonesNumber) => {
      const cardCloneLine = dataLines[cardClonesNumber - 1];
      const cardCloneParsed = parseCard(cardCloneLine, false);
      if (cardCloneParsed.cardsClones.length > 0) {
        cardsClones.push(cardCloneParsed);
      }
    });

    if (card.cardsClones.length > 0 /* && cardsClones.length > 0 */) {
      CARD_INDEXES.push(card.cardsClones);
      return cardsClones;
    }

    return null;
  });

  clonesGroups.forEach((clonesGroup) => {
    if (clonesGroup) {
      recursiveCloneCards(clonesGroup, dataLines, CARD_INDEXES, isLoggingEnabled);
    }
  });
};

const getWinningCards = (dataLines, isLoggingEnabled) => {

  const CARD_INDEXES = [];
  // Check if the input is a non-empty array
  if (!Array.isArray(dataLines) || dataLines.length === 0) {
    // If not, throw an error
    throw new Error('Invalid input: dataLines must be a non-empty array');
  }

  // Initialize the total sum to 0
  let totalSum = 0;
  let lineCount = 1;
  const cards = [];

  // Loop over each line in the dataLines array
  for (const line of dataLines) {
    const card = parseCard(line, isLoggingEnabled);
    cards.push(card);
    CARD_INDEXES.push(lineCount);
    lineCount++;
  }

  cards.forEach((card) => {
    totalSum += card.points;
  });

  recursiveCloneCards(cards, dataLines, CARD_INDEXES, isLoggingEnabled);

  const counts = CARD_INDEXES.flat().reduce((acc, index) => {
    acc[index] = (acc[index] || 0) + 1;
    return acc;
  }, {});

  const scratchcards = Object.entries(counts).map(([index, count]) => ({ index: Number(index), count }));

  const scratchcardsObject = {
    scratchcards,
    total: scratchcards.reduce((acc, { count }) => acc + count, 0),
  };

  if (isLoggingEnabled) {
    console.log('\n', scratchcardsObject);
  }

  return {
    part1: totalSum,
    part2: scratchcardsObject,
  };
};

/* MAIN EXECUTION
============================================================================= */

// Load the data file and measure the time it takes
const [dataLines] = getRuntime(loadTextFile, `${process.cwd()}/src/days/${DAY}/data.txt`);

// Get the size of the data file and measure the time it takes
const [dataSize] = getRuntime(getFileSize, `${process.cwd()}/src/days/${DAY}/data.txt`);

// Load the part 1 and part 2 example data files
const [exampleData] = getRuntime(loadTextFile, `${process.cwd()}/src/days/${DAY}/example-data.txt`);

// Get the size of the solution file and measure the time it takes
const [solutionSize] = getRuntime(getFileSize, `${process.cwd()}/src/days/${DAY}/solution.js`);

// Calculate the solution for part 1 and measure the time it takes
const [solution, solutionTime] = getRuntime(getWinningCards, dataLines, false);


/* OUTPUT LOGS
============================================================================= */

console.log('\n🎄🎄🎄🎄🎄🎄🎄🎄🎄🎄\n');

// Print the day number
log(`${chalk.blue('Day:')} ${chalk.green(DAY[DAY.length - 1])}\n`);

// Print the solutions for part 1 and part 2
log(`${chalk.blue('Part-1:')} ${chalk.green(solution.part1)}`);
log(`${chalk.blue('Part-2:')} ${chalk.green(solution.part2.total)}\n`);

// Print the sizes of the script and data files
console.log(`${chalk.blue('Script:')} ${chalk.green(`${solutionSize}kb`)}`);
console.log(`${chalk.blue('Data:')} ${chalk.green(`${dataSize}kb\n`)}`);

// Print the total runtime
console.log(`${chalk.blue('Runtime:')} ${chalk.green(`${solutionTime}`)}\n`);

console.log('🎁🎁🎁🎁🎁🎁🎁🎁🎁🎁\n');

// Print the header for the part 1 example
console.log('Part 1 & 2\n');
const [exampleSolution, exampleTime] = getRuntime(getWinningCards, exampleData, true);
console.log('');
console.log(`${chalk.blue('Total points:')} ${chalk.green(exampleSolution.part1)}`);
console.log(`${chalk.blue('Total scratchcards:')} ${chalk.green(exampleSolution.part2.total)}`);
console.log(`${chalk.blue('Runtime:')} ${chalk.green(`${exampleTime}`)}\n`);

console.log('🎅🎅🎅🎅🎅🎅🎅🎅🎅🎅\n');
