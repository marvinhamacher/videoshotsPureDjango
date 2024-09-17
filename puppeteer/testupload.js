const puppeteer = require('puppeteer');
const fs = require('fs');

let id = 1;
let totalMS = 0;
let currentMedian = 0;

async function resetFile() {
    const header = "\n" +
        "# _Ergebnisse individuell_\n" +
        "|Test NR|Werte|Testgruppe|\n" +
        "|-------|-----|----------|\n";
    fs.writeFile('testergebnis.md', header, (err) => {
        if (err) throw err;
    });
}

async function AddResults(nr, ms, group) {
    let result = `|${nr}|${ms}|${group}|\n`;
    fs.appendFile('testergebnis.md', result, (err) => {
        if (err) throw err;
    });
}

async function uploadFile(group) {
    const browser = await puppeteer.launch({ headless: true });
    const page = await browser.newPage();
    const startTime = new Date();

    // Öffnet die Seite
    await page.goto('http://localhost:8000/add');

    // Datei auswählen und hochladen
    const [fileChooser] = await Promise.all([
        page.waitForFileChooser(),
        page.click('#id_screenshot')
    ]);

    // Führt upload durch
    await fileChooser.accept(['./testfile/test.png']);

    // Füllt title und description
    await page.type('#id_title', `testtitel${id}`);
    await page.type('#id_description', `testbeschreibung${id}`);

    // Absenden
    try {
        await Promise.all([
            page.waitForNavigation({ waitUntil: 'domcontentloaded', timeout: 8000 }),
            page.click('#submitButton')
        ]);
        //await page.screenshot({ path: './success_images/success_screenshot.png' });
    } catch (error) {
        group += ">8000(!!!)";
        //await page.screenshot({ path: './error_images/error_screenshot.png' });
    }

    const totalResponseTime = new Date() - startTime;
    await AddResults(id, totalResponseTime, group);
    totalMS += totalResponseTime;
    id++;
    await page.close();
    await browser.close();
}

async function prepTest(usercount) {
    totalMS = 0;
    let actions = [];
    for (let i = 0; i < usercount; i++) {
        actions.push(uploadFile(`Users: ${usercount}`));
    }
    await Promise.all(actions);
    currentMedian = totalMS / usercount;
}

async function runTests(iterations) {
    await resetFile();
    let median_values = "\n # Medianwerte:";
    let usercount = 5;
    for (let i = 0; i < iterations; i++) {
        console.log("Running test...");
        await prepTest(usercount);
        median_values += ` > Bei ${usercount} Nutzern waren es: ${currentMedian} ms`;
        usercount *= 2;
    }
    fs.appendFile('testergebnis.md', median_values, (err) => {
        if (err) throw err;
    });
}

runTests(4);
