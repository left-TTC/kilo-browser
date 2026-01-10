import { prompt } from "./prompt";


export async function waitConfirm(
    message: string,
    defaultYes = false
): Promise<boolean> {
    const hint = defaultYes ? "(Y/n)" : "(y/N)";
    const answer = (await prompt(`${message} ${hint} `))
        ?.trim()
        .toLowerCase();

    if (!answer) return defaultYes;
    return answer === "y" || answer === "yes";
}