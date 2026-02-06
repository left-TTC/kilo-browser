import { Config } from "../config/Config";
import { loadConfig } from "../config/loadConfig";
import { writeConfig } from "../config/writeConfig";
import { BraveState, checkBrave } from "../lib/checkBraveCode";
import { waitConfirm } from "../lib/confirm";
import { prompt } from "../lib/prompt";
import chalk from "chalk";


const args = process.argv.slice(2);

const finalArgs = args.length === 0 ? ["connect"] : args;

enum Args{
    connect = "connect",
    sync = "sync",
    error = "error",
}

function getArgs(finalArgs: string[]): Args {
    if(finalArgs.includes(Args.connect)){
        return Args.connect
    }else if(finalArgs.includes(Args.sync)){
        return Args.sync
    }

    return Args.error
}

function updataBravePath(
    bravePath: string,
    config: Config
){
    let newConfig = config

    newConfig.brave.path = bravePath
    writeConfig(newConfig)
}


export async function getBrave(){

    const config = loadConfig();

    if(config.brave.path.length > 0){
        console.log(chalk.yellow("current brave location: ", config.brave.path))

        const ok = await waitConfirm(
            "Continue and overwrite?",
            false
        );

        if (!ok) {
            console.log(chalk.gray("Aborted."));
            process.exit(0);
        }
    }

    switch(getArgs(finalArgs)){
        case Args.error:
            console.error(chalk.red("Error: Unknown command."));
            console.error(`Received: ${finalArgs.join(" ")}`);
            console.error(chalk.yellow("Run with --help to see available commands."));
            process.exit(1)
        case Args.connect:
            let bravePath = finalArgs[1];

            if (!bravePath) {
                bravePath = await prompt("Please enter path to src/brave: ");
            }
            if (!bravePath) {
                console.error("Error: Brave path is required.");
                process.exit(1);
            }

            switch(checkBrave(bravePath, config)){
                case BraveState.noChromium:
                    console.log();
                    console.log(chalk.yellow("No chromium, will sync"))
                    updataBravePath(bravePath, config)
                    break
                case BraveState.packageJsonMissing:
                    console.log();
                    console.log(chalk.red("brave isn't complete"))
                    process.exit(1)
                case BraveState.pathError:
                    console.log();
                    console.log(chalk.red("Give fault path"))
                    process.exit(1)
                case BraveState.readError:
                    console.log();
                    console.log(chalk.red("Error happends when read brave path"))
                    process.exit(1)
                case BraveState.versionDismatched:
                    console.log();
                    console.log(chalk.red("brave's version dismatch, VERSION should be ", config.brave.version))
                    process.exit(1)
                case BraveState.fine:
                    console.log();
                    console.log(chalk.green("right enviroment"))
                    updataBravePath(bravePath, config)
                    break
            }
        
    }
}


if (require.main === module) {
    getBrave();
}