
import * as readline from "readline";

import chalk from "chalk";

export function prompt(question: string): Promise<string> {
    const rl = readline.createInterface({
        input: process.stdin,
        output: process.stdout
    });

    const coloredQuestion = chalk.cyan(question);

    return new Promise(resolve => {
        rl.question(coloredQuestion, answer => {
        rl.close();
            resolve(answer.trim());
        });
    });
}
