import chalk from "chalk";
import path from "path";
import fs from "fs";
import { loadConfig } from "../config/loadConfig";
import { getBrave } from "./getBrave";



function loadOverlayMap() {
    const mapPath = path.resolve(
        process.cwd(),
        "project_build/overlay/map.json"
    );

    if (!fs.existsSync(mapPath)) {
        throw new Error(`overlay map not found: ${mapPath}`);
    }

    const raw = fs.readFileSync(mapPath, "utf-8");
    return JSON.parse(raw) as Record<string, string>;
}

function copyDir(src: string, dst: string) {
    if (!fs.existsSync(src)) return;

    fs.mkdirSync(dst, { recursive: true });

    for (const item of fs.readdirSync(src)) {
        const srcItem = path.join(src, item);
        const dstItem = path.join(dst, item);
        const stat = fs.statSync(srcItem);

        if (stat.isDirectory()) {
            copyDir(srcItem, dstItem);
        } else {
            fs.copyFileSync(srcItem, dstItem);
            console.log(
                chalk.gray(srcItem),
                chalk.green("→"),
                chalk.gray(dstItem)
        );
        }
    }
}

export async function applyPatch(){

    let config = loadConfig();
    let bravePath = config.brave.path

    if(bravePath.length > 0){
        console.log(chalk.green("apply patch to ", bravePath, "\n"))
    }else{
        console.log(chalk.blue("no brave work space, load...\n"))
        getBrave()

        config = loadConfig()
        bravePath = config.brave.path
        console.log(chalk.green("Continue applying the patch..."))
    }

    const srcRoot = path.resolve(bravePath, "../..");
    console.log("root", srcRoot)

    const overlayMap = loadOverlayMap();

    for (const [fromKey, toPath] of Object.entries(overlayMap)) {
        const srcDir = path.join(process.cwd(), fromKey);
        const dstDir = path.join(srcRoot, toPath);

        console.log(chalk.white(`${fromKey} → ${toPath}`));
        copyDir(srcDir, dstDir);
    }

    console.log(chalk.green("\nPatch applied successfully."));
}


if (require.main === module) {
    applyPatch();
}