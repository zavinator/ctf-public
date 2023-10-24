# Keyword of the day

## Zadání

```
Ahoy, officer,

one of deck cadets (remember your early days onboard) had a simple task to prepare simple web application to announce keyword of the day. He claimed that the task is completed, but he forgot on which port the application is running. Unfortunately, he also prepared a lot of fake applications, he claims it was necessary for security reasons. Find the keyword of the day, so daily routines on ship can continue.

May you have fair winds and following seas!

The webs are running somewhere on server keyword-of-the-day.cns-jv.tcc.
```

## Řešení

```bash
nmap -p 1-65535 -T4 -A -v keyword-of-the-day.cns-jv.tcc
```

Výstup:

```
Discovered open port 60163/tcp on 10.99.0.155
Discovered open port 60357/tcp on 10.99.0.155
Discovered open port 60459/tcp on 10.99.0.155
Discovered open port 60277/tcp on 10.99.0.155
Discovered open port 60447/tcp on 10.99.0.155
Discovered open port 60352/tcp on 10.99.0.155
Discovered open port 60004/tcp on 10.99.0.155
...
```

Nalezeno spoustu otevřených portů na kterých běží web: http://keyword-of-the-day.cns-jv.tcc:60163/
Weby vypadají všechny stejně a vlajka asi bude pouze na jednom, takže bude třeba vyzkoušet všechny.
Bohužel nám nepomůže navštívit všechny weby jednoduchým skriptem, protože klíčová část je skryta v javaskriptu a všechny stránky obsahují stejný počet znaků.
S přepsáním obsfucated javascript kódu nám pomůže stránka https://obf-io.deobfuscate.io/

```javascript
function getRandomInt(_0x12721b, _0x4bd30f) {
  _0x12721b = Math.ceil(_0x12721b);
  _0x4bd30f = Math.floor(_0x4bd30f);
  return Math.floor(Math.random() * (_0x4bd30f - _0x12721b) + _0x12721b);
}
setTimeout(function () {
  fn = getRandomInt(1, 4);
  document.getElementById("loader").style.display = "none";
  qn = "cc0fa7ad7f";
  document.getElementById("myImage").src = "img/" + fn + ".png";
}, getRandomInt(1, 7) * 1000);
```

Program tedy po časové prodlevě zobrazí náhodný obrázek z adresáře `img`.
Bude tedy potřeba projít všechny stránky a podívat se na jaký obrázek se daný web odkazuje.
K tomu lze použít `nodejs` + `puppeteer`, s programem pomůže Chat-GPT4.
Výsledný program po několika úpravách AI i ručních:

```javascript
const puppeteer = require('puppeteer');

async function extractImageSrc(page, port) {
    // Construct the URL using the given port
    const url = `http://keyword-of-the-day.cns-jv.tcc:${port}/`;
    await page.goto(url);

    // Wait for the image to have a src attribute
    await page.waitForSelector('#myImage[src]');

    // Extract the img src
    const imageSrc = await page.$eval('#myImage', img => img.src);
    console.log(`Port ${port}: ${imageSrc}`);
}

(async () => {
    const ports = [
        60000, 60071, 60134, 60197, 60266, 60320, 60398, 60445, 
        60004, 60074, 60138, 60201, 60269, 60322, 60400, 60447, 
        60009, 60079, 60140, 60204, 60273, 60327, 60402, 60450, 
        60015, 60084, 60143, 60209, 60276, 60331, 60405, 60456, 
        60018, 60087, 60157, 60212, 60280, 60341, 60408, 60457, 
        60023, 60089, 60159, 60217, 60283, 60343, 60411, 60459, 
        60029, 60096, 60161, 60221, 60286, 60347, 60413, 60466, 
        60030, 60099, 60163, 60225, 60288, 60350, 60415, 60468, 
        60035, 60104, 60165, 60228, 60290, 60352, 60418, 60471, 
        60041, 60107, 60169, 60234, 60294, 60354, 60419, 60473, 
        60045, 60111, 60174, 60239, 60297, 60356, 60421, 60482, 
        60047, 60115, 60177, 60242, 60299, 60360, 60424, 60487, 
        60051, 60118, 60185, 60244, 60303, 60367, 60426, 60494, 
        60058, 60120, 60187, 60247, 60307, 60371, 60430, 
        60063, 60122, 60189, 60249, 60309, 60378, 60432, 
        60066, 60125, 60192, 60253, 60313, 60382, 60437, 
        60068, 60129, 60195, 60257, 60318, 60389, 60440
        ];

    const browser = await puppeteer.launch();
    const page = await browser.newPage();

    for (const port of ports) {
        await extractImageSrc(page, port);
    }

    await browser.close();
})();
```

Výstup:

```
...
Port 60195: http://keyword-of-the-day.cns-jv.tcc:60195/img/2.png
Port 60257: http://keyword-of-the-day.cns-jv.tcc:60257/img/948cd06ca7.png
Port 60318: http://keyword-of-the-day.cns-jv.tcc:60318/img/2.png
```

Na uvedené "podezřelé" stránce je obrázek s nápisem: `For FLAG follow this URI /948cd06ca7`

http://keyword-of-the-day.cns-jv.tcc:60257/948cd06ca7/

## Vlajka

```
FLAG{DEIE-fiOr-pGV5-8MPc}
```
