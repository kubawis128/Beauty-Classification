var http = require('http');
var fs = require('fs');
const { Webhook, MessageBuilder } = require('discord-webhook-node');
const hook = new Webhook("https://discord.com/api/webhooks/1082767830589644912/0pxjMWD3MvJzsuIN5KhSP42wfo6C3aoASBif5DBGOx1U8NvnWh2zz2r6O8g8zSinX3hJ");

let pliki = [];
let uzywane_pliki = [];
let plik = ""
let port = 81
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
      try {
        const embed = new MessageBuilder()
        .setTitle('End reached!!!')
        .setAuthor('Beauty Classification Status', 'https://cdn.discordapp.com/embed/avatars/0.png', 'http://socool.ddns.net')
        .setDescription("Niewolnicy skończyli prace :D")
        .setColor('#77dd77')
        .setText("@everyone")
        .setFooter('Pozdrawiam Wiśnia', 'https://cdn.discordapp.com/avatars/547075900139896834/9f6d9f8aaa9710f49d4598957568d4b0.webp')
        .setTimestamp();
        
        hook.send(embed);
      }catch (err) {
        console.warn("Failed to send webhook")
      }

      return
    }
    
  } else if (req.method === "POST") {
    req.on('data', chunk => {
      donePhotosCount += 1
      try{
        if(donePhotosCount % 1000 == 0){
          const embed = new MessageBuilder()
            .setTitle('Milestone reached')
            .setAuthor('Beauty Classification Status', 'https://cdn.discordapp.com/embed/avatars/0.png', 'http://socool.ddns.net')
            .addField("Ilość zdjęć",donePhotosCount + "/" + allPhotosCount)
            .addField("Percent done", " " + ((donePhotosCount/allPhotosCount)*100).toFixed(2) + "%")
            .setColor('#00b0f4')
            .setFooter('Pozdrawiam Wiśnia', 'https://cdn.discordapp.com/avatars/547075900139896834/9f6d9f8aaa9710f49d4598957568d4b0.webp')
            .setTimestamp();
  
            hook.send(embed);
        }
      }catch (err) {
        console.warn("Failed to send webhook")
      }
      chunk = chunk + ''
      let rate = chunk.split(",")[0]
      let src = chunk.split(",")[1]
      fs.rename("./images/" + src, "./out/" + rate +  "/" + plik, function (err) {
        if (err) console.log(err + "");
      })

      res.end("e");
    });
  }
}).listen(port);