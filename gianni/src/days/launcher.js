import chalk from 'chalk';
// Import descriptions and utility functions
import descriptions from './descriptions.js';
import { get, log } from '../utils/utils.js';

// Constants for file names and paths
const CLASS_FILE = 'class.js';
const CLASS_FILE_MINIFIED = 'class.min.js';
const DATA_FILE = 'data.txt';
const EXAMPLE_FILE = 'example-data.txt';
const EXAMPLE_PART_1_FILE = 'example-part1.txt';
const EXAMPLE_PART_2_FILE = 'example-part2.txt';
const MODULE_PATH = (day, shouldMinify) => `./${day}/${shouldMinify ? CLASS_FILE_MINIFIED : CLASS_FILE}`;

const SPECIAL_DAY_HANDLING = {
  day1: {
    moreThanOneExample: true,
  },
  day3: {
    dontSplitData: true,
    // Add more properties or actions if needed
  },
  // Add more special day configurations as necessary
};

/**
 * Manages challenge execution and logging of results.
 */
export class ChallengeLauncher {
  /**
   * Constructs a ChallengeLauncher object.
   * @class
   * @param {string} day - The day identifier for the challenge.
   * @property {string} day - The day identifier for the challenge.
   * @property {number} dayNumber - The number representing the day.
   * @example
   * // Example usage:
   * const launcher = new ChallengeLauncher('day1');
   */
  constructor(day, shouldMinify) {
    this.day = day;
    this.dayNumber = Number(this.day.slice(-1));
    this.shouldMinify = shouldMinify;
    this.initialize(); // Initializes the application

  }

  /**
   * Initializes the challenge application.
   * @returns {Promise<void>}
   * @throws {Error} When an error occurs during initialization.
   * @example
   * // Example usage:
   * await launcher.initialize();
   */
  async initialize() {
    try {
      await this.loadClasses(); // Load challenge-specific classes
      await this.checkDay(); // Check for any special configurations for the day
      await this.executeSolutions(); // Execute challenge solutions
      await this.logResults(); // Log results
    } catch (error) {
      console.error('Error during initialization:', error);
    }
  }

  /**
   * Loads challenge-specific classes dynamically.
   * @returns {Promise<void>}
   * @throws {Error} When an error occurs during class loading.
   * @example
   * // Example usage:
   * await launcher.loadClasses();
   */
  async loadClasses() {
    try {
      const module = await import(MODULE_PATH(this.day, this.shouldMinify));
      this.DayClass = module[this.day.charAt(0).toUpperCase() + this.day.slice(1)];
    } catch (error) {
      console.error(`Error loading class for day ${this.day} from path ${MODULE_PATH(this.day, this.shouldMinify)}:`, error);
      throw error;
    }
  }

  /**
   * Checks for any special configurations for the day.
   * @returns {void}
   * @throws {Error} When an error occurs during checking.
   * @example
   * // Example usage:
   * launcher.checkDay();
   */
  async checkDay() {
    const specialDayConfig = SPECIAL_DAY_HANDLING[this.day];
    if (specialDayConfig) {
      this.dontSplitData = specialDayConfig.dontSplitData || false;
      this.moreThanOneExample = specialDayConfig.moreThanOneExample || false;
      // Handle other configurations for the special day if necessary
    }
  }

  /**
   * Loads data from files.
   * @param {string} fileName - The name of the file to load.
   * @param {number} partNumber - The part number of the example data.
   * @returns {Promise<void>}
   * @throws {Error} When an error occurs during data loading.
   * @example
   * // Example usage:
   * await launcher.loadData('data.txt', 1);
   */
  async loadData(fileName, partNumber) {
    try {
      // Load data from files and store them in instance properties
      const data = get.dataAndSize(fileName, this.day, this.dontSplitData);
      this[`examplePart${partNumber}`] = data;
    } catch (error) {
      console.error(`Error loading ${fileName}:`, error);
      throw error;
    }
  }

  /**
   * Executes challenge solutions after loading necessary data.
   * @returns {Promise<void>}
   * @throws {Error} When an error occurs during execution.
   * @example
   * // Example usage:
   * await launcher.executeSolutions();
   */
  async executeSolutions() {
    try {
      this.lines = get.dataAndSize(DATA_FILE, this.day, this.dontSplitData);
      if (this.moreThanOneExample) {
        await this.loadData(EXAMPLE_PART_1_FILE, 1);
        await this.loadData(EXAMPLE_PART_2_FILE, 2);
      } else {
        this.exampleLines = get.dataAndSize(EXAMPLE_FILE, this.day, this.dontSplitData);
      }
      this.classFile = get.dataAndSize(this.shouldMinify ? CLASS_FILE_MINIFIED : CLASS_FILE, this.day, this.dontSplitData);

      this.solution = new this.DayClass(this.lines.data, false);
      this.solution.time.part1 = get.runtime(() => this.solution.part1());
      this.solution.time.part2 = get.runtime(() => this.solution.part2());
    } catch (error) {
      console.error('Error executing solutions:', error);
      throw error;
    }
  }

  /**
   * Logs challenge results and descriptions.
   * @returns {Promise<void>}
   * @throws {Error} When an error occurs during logging.
   * @example
   * // Example usage:
   * await launcher.logResults();
   */
  async logResults() {
    try {
      log.message(`\n${'🎄'.repeat(this.dayNumber)} ${descriptions[this.day].title}\n`);
      log.results(this.day, this.classFile.size, this.lines.size, this.solution);
      if (!this.shouldMinify) {
        console.log(`${'🎁'.repeat(20)}\n`);
        console.log(`${chalk.red('Problem:')} ${descriptions[this.day].description}\n`);
        if (this.moreThanOneExample) {
          log.execute(this.DayClass, 1, this.examplePart1.data);
          log.execute(this.DayClass, 2, this.examplePart2.data);
        } else {
          log.execute(this.DayClass, 1, this.exampleLines.data);
          log.execute(this.DayClass, 2, this.exampleLines.data);
        }
      }
    } catch (error) {
      console.error('Error logging results:', error);
      throw error;
    }
  }
}
