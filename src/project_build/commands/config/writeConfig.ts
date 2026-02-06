import { Config } from "./Config";
import * as fs from "fs";
import * as path from "path";

const CONFIG_PATH = path.resolve(__dirname, "../../config.json");

export function writeConfig(newConfig: Config){
    const raw = JSON.stringify(newConfig, null, 4); 
    fs.writeFileSync(CONFIG_PATH, raw, "utf-8");
}