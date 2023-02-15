var http = require('http');
var fs = require('fs');

let pliki = [];
let uzywane_pliki = [];
let plik = ""

console.log("Starting http server at *:3000")
http.createServer(function (req, res) {
  if (req.method === "GET") {
    res.writeHead(200, {
      "Content-Type": "text/html"
    });
    
    pliki = fs.readdirSync("./images/"); 
    plik = pliki[Math.floor(Math.random()*pliki.length)];  
    if (uzywane_pliki.includes(plik)){
      plik = pliki[Math.floor(Math.random()*pliki.length)];  
      if (uzywane_pliki.includes(plik)){
        plik = pliki[Math.floor(Math.random()*pliki.length)];  
        if (uzywane_pliki.includes(plik)){
          plik = pliki[Math.floor(Math.random()*pliki.length)];  
          if (uzywane_pliki.includes(plik)){
            let ress = "" + fs.readFileSync("./websites/end_of_images.html");
            res.end(ress);
            return
          }
        }
      }
    }

    uzywane_pliki.push(plik);
    try {
      let base64img = Buffer.from(fs.readFileSync("./images/" + plik)).toString('base64');
      let ress = "" + fs.readFileSync("./websites/index.html");
      ress = ress.replace('https://thispersondoesnotexist.com/image',"data:image/png;base64," + base64img )
      ress = ress.replace('nazwapliku',plik)
      res.end(ress);
    } catch (error) {
      let ress = "" + fs.readFileSync("./websites/end_of_images.html");
      res.end(ress);
      return
    }
    
  } else if (req.method === "POST") {
    req.on('data', chunk => {
      chunk = chunk + ''
      let rate = chunk.split(",")[0]
      let src = chunk.split(",")[1]
      fs.rename("./images/" + src, "./out/" + rate +  "/" + plik, function (err) {
        if (err) console.log(err + "");
      })
      res.end("e");
    });
  }

}).listen(3000);