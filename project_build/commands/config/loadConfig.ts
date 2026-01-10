
import * as fs from "fs";
import * as path from "path";
import { Config } from "./Config";

const CONFIG_PATH = path.resolve(__dirname, "../../config.json");

export function loadConfig(): Config {
    if (!fs.existsSync(CONFIG_PATH)) {
        throw new Error("Config not found. Run `getbrave connect` first.");
    }

    const raw = fs.readFileSync(CONFIG_PATH, "utf-8");
    return JSON.parse(raw) as Config;
}
