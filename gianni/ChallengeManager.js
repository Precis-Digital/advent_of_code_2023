import { readdirSync, readFileSync, writeFileSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
import { minify } from 'uglify-js';
import { ChallengeLauncher } from './src/days/launcher.js';

/**
 * Manages challenges for different days and provides functionality for minification.
 */
class ChallengeManager {
  /**
   * Initializes the ChallengeManager with the root directory of the project.
   * @property {string} root - The root directory of the project.
   *
   * @example
   * // Creates a new instance of ChallengeManager
   * const challengeManager = new ChallengeManager();
   */
  constructor() {
    this.root = dirname(fileURLToPath(import.meta.url)); // Set the root directory
  }

  /**
   * Starts the challenge for a specific day. If no day is provided, it starts the challenge for all days.
   *
   * @param {string} day - The day for which the challenge needs to be started. If not provided, the challenge starts for all days.
   * @param {boolean} [shouldMinify=false] - Flag indicating whether to minify the file or not.
   *
   * @example
   * // Starts the challenge for day1 and minifies the file
   * start('1', true);
   * @example
   * // Starts the challenge for all days without minifying the files
   * start();
   */
  start(day, shouldMinify = false) {
    if (day) {
      if (shouldMinify) {
        this.minifyFile(`day${day}`);
      }
      new ChallengeLauncher(`day${day}`, shouldMinify); // Start the challenge for a specific day
    } else {
      const daysDir = join(this.root, 'src', 'days'); // Get the directory for all days
      readdirSync(daysDir).forEach((folder) => {
        if (!folder.startsWith('day')) return; // Ignore non-day folders and files
        if (shouldMinify) {
          this.minifyFile(folder);
        }
        new ChallengeLauncher(folder, shouldMinify); // Start the challenge for the current day
      });
    }
  }

  /**
   * Minifies the JavaScript file in a given folder. The minified file is saved as 'class.min.js' in the same folder.
   * @param {string} folder - The name of the folder containing the file to be minified.
   *
   * @example
   * // Minifies the 'class.js' file in the 'day1' folder
   * minifyFile('day1');
   */
  minifyFile(folder) {
    const filePath = join(this.root, 'src', 'days', folder, 'class.js'); // Path to the file to be minified
    const minifiedFilePath = join(this.root, 'src', 'days', folder, 'class.min.js'); // Path to the output minified file
    const fileContent = readFileSync(filePath, 'utf8'); // Read the content of the file to be minified
    const minifyOptions = {
      compress: {
        drop_console: true, // Remove console statements
      },
      mangle: true, // Minify variable and function names
      toplevel: true, // Minify top-level variables and functions
      output: {
        comments: false, // Do not include comments in the output
      },
    };
    const minifiedContent = minify(fileContent, minifyOptions).code; // Minify the file content
    writeFileSync(minifiedFilePath, minifiedContent); // Write the minified content to the output file
  }

  /**
   * Executes a specified command with the provided arguments.
   *
   * @param {string} commandName - The name of the command to be executed.
   * @param {*} arg1 - The first argument for the command.
   * @param {*} arg2 - The second argument for the command.
   *
   * @example
   * // Executes the 'start' command with '1' as the first argument and 'true' as the second argument
   * executeCommand('start', '1', true);
   */
  executeCommand(commandName, arg1, arg2) {
    const commands = { start: this.start.bind(this) }; // Define the available commands
    commands[commandName](arg1, arg2); // Execute the specified command with the provided argument
  }

  /**
   * Handles the command-line arguments and executes the appropriate command.
   *
   * @param {Array.<string>} args - The array of command-line arguments.
   *
   * @example
   * // Handles the arguments and executes the 'start' command for 'day1' with minification
   * handleArgs(['start', '--day=1', '--shouldMinify=true']);
   */
  handleArgs(args) {
    const commandName = args[0]; // Get the first argument as the command name
    const day = this.getArgValue(args, 'day='); // Get the value of the --day= argument
    const shouldMinify = this.getArgValue(args, 'minify=') === 'true'; // Check if the --shouldMinify= argument is set to true

    this.executeCommand(commandName, day, shouldMinify); // Execute the command with the given arguments
  }

  /**
   * Retrieves the value of a specified argument from the provided array of arguments.
   *
   * @param {Array.<string>} args - The array of arguments.
   * @param {string} argName - The name of the argument whose value is to be retrieved.
   * @returns {string|null} The value of the specified argument if it exists; otherwise, null.
   *
   * @example
   * // Retrieves the value of the '--day' argument from the provided array of arguments
   * getArgValue(['start', '--day=1', '--shouldMinify=true'], '--day');
   */
  getArgValue(args, argName) {
    this.args = args; // Assign the passed arguments to the class property
    const argument = this.args.find(arg => arg.startsWith(argName)); // Find the argument that starts with the provided name
    return argument ? argument.split('=')[1] : null; // If the argument exists, return its value. Otherwise, return null.
  }
}

const challengeManager = new ChallengeManager(); // Create a new instance of ChallengeManager
const args = process.argv.slice(2); // Get the command line arguments passed to the script
challengeManager.handleArgs(args); // Pass the arguments to the handleArgs method of the ChallengeManager instance
