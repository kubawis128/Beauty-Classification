var http = require('http');
var fs = require('fs');

let pliki = [];
let uzywane_pliki = [];
let plik = ""
let port = 80
let allPhotosCount = fs.readdirSync('./images/').length
let donePhotosCount = 0
console.log("Starting http server at *:" + port)
http.createServer(function (req, res) {
  if (req.method === "GET") {
    res.writeHead(200, {
      "Content-Type": "text/html"
    });
    try{
      pliki = fs.readdirSync("./images/"); 
    }catch {
      console.error("No source images")
      let ress = "" + fs.readFileSync("./websites/end_of_images.html");
      res.end(ress);
      return
    }
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
      ress = ress.replace('ileprocent', ((donePhotosCount/allPhotosCount)*100).toFixed(2) + "%")
      ress = ress.replace('ileprocent', ((donePhotosCount/allPhotosCount)*100).toFixed(2) + "%")
      ress = ress.replace('https://thispersondoesnotexist.com/image',"data:image/png;base64," + base64img )
      ress = ress.replace('nazwapliku',plik)
      console.log("All photos:", allPhotosCount)
      console.log("Done donePhotosCount:", donePhotosCount)
      console.log("percent:", ((donePhotosCount/allPhotosCount)*100).toFixed(2))
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
      donePhotosCount += 1
      res.end("e");
    });
  }
}).listen(port);