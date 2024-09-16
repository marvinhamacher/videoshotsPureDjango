const puppeteer = require('puppeteer');
let id = 1;
let totalMS = 0;
let currentMedian = 0;
const fileservice = require("fs")
// Stelle sicher:
//  -das zuerst minio und Django laufen
//  -das du Puppeteer installiert hast

async function resetFile(){
    const header = "\n" +
        "# _Ergebnisse individuell_\n" +
        "|Test NR|Werte|Testgruppe|\n" +
        "|-------|-----|----------|\n"
    fileservice.writeFile('testergebnis.md', header, (err) => {

    // In case of a error throw err.
    if (err) throw err;
})
}
async function AddResults(nr,ms,group){
    let result = "|"+nr+"|"+ms+"|"+group+"|\n"
    fileservice.appendFile('testergebnis.md', result, (err) => {
    // In case of a error throw err.
    if (err) throw err;
})
}


async function uploadFile(group) {
    const browser = await puppeteer.launch({headless:true});
    const page = await browser.newPage();
    const startTime = new Date(); //START

    // Öffne die Seite
    page.goto('http://localhost:8000/add');

    // Datei auswählen und hochladen
    const [fileChooser] = await Promise.all([
        page.waitForFileChooser(),
        page.click('#id_screenshot')
    ]);

    await fileChooser.accept(['./testfile/test.png']);

    // Titel
    await page.type('#id_title', "testtitel"+id);  // Selektor und Text für den Titel

    // Beschreibung eingeben
    await page.type('#id_description', "testbeschreibung"+id);  // Selektor und Text für die Beschreibung

    // Absenden
    await page.click('#submitButton');

    // Warte, bis die Seite die Antwort gibt
    try {
        const response = await page.waitForResponse(response => response.url() === 'http://localhost:8000/' && response.status() === 200, { timeout: 7000 });
        //await page.screenshot({ path: './success_images/success_screenshot.png' });
    } catch (error) {
        //await page.screenshot({ path: './error_images/error_screenshot.png' });
        group += ">8000(!!!)"
    }


    const totalResponseTime = new Date() - startTime;
    await AddResults(id,totalResponseTime,group)
    totalMS += totalResponseTime;
    id++;
    await page.close()
}






async function prepTest(usercount){
    totalMS = 0
    let actions = []
    for (let i=0;i<usercount;i++){
        actions.push(uploadFile("Users: "+usercount))
    }
    await Promise.all(actions)
    currentMedian = totalMS/usercount
}

async function runTests(iterations){
    resetFile()
    let median_values = "\n # Medianwerte:"
    let usercount = 5;
    for(let i=0;i<iterations;i++){
        console.log("hiiii")
        await prepTest(usercount)
        median_values += ` > Bei ${usercount} Nutzern waren es: ${currentMedian} ms`
        usercount *= 2
    }
    fileservice.appendFile('testergebnis.md',median_values, (err) => {

    // In case of a error throw err.
    if (err) throw err;
})
}
//uploadFile(1)
runTests(3)