// This file is the main entry point for the application.
import path from 'path';
import { get, log } from '../../utils/utils.js';

// The name of the parent folder is used to determine the day.
const day = path.basename(path.dirname(import.meta.url));

// The class for the current day is dynamically imported.
import('./class.js').then((module) => {
  const DayClass = module[day.charAt(0).toUpperCase() + day.slice(1)];
  const DayNumber = day.slice(-1);

  /* MAIN EXECUTION
  ============================================================================= */

  // The data for the current day is loaded.
  const { data: dataLines, size: dataSize } = get.dataAndSize('data.txt', day);
  const { data: exampleLines } = get.dataAndSize('example-data.txt', day);
  const { size: classSize } = get.dataAndSize('class.js', day);

  // A new instance of the class for the current day is created.
  // The time it takes to calculate the solution for part 1 and part 2 is measured.
  const solution = new DayClass(dataLines.join('\n'), false);
  solution.time = solution.time || {};
  solution.time.part1 = get.runtime(() => solution.part1());
  solution.time.part2 = get.runtime(() => solution.part2());

  /* OUTPUT LOGS
  ============================================================================= */

  // The day and results are logged to the console.
  log.message(`\n${'🎄'.repeat(DayNumber)} ⭐⭐ ⭐⭐ ⭐⭐\n`);
  log.results(day, classSize, dataSize, solution);

  // Present box separator
  console.log(`${'🎁'.repeat(20)}\n`);

  // The solution for part 1 and part 2 is executed and logged.
  log.execute(DayClass, 1, exampleLines.join('\n'));
  log.execute(DayClass, 2, exampleLines.join('\n'));
});
