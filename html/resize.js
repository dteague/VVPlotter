var files = getListOfFiles("/plots/.", 'a[href]', ".png");


function dynamicSizing() {
    var w = window.outerWidth;

    var itemsPerLine = Math.floor(w/500);
    
    // Delete old
    document.getElementById("picTable").innerHTML = "";
    
    var line = document.createElement("tr")
    line.style.textAlign = "center";
    for(var i = 0; i < files.length; i++) {
        var element = document.createElement("td")
        element.style.textAlign = "center";
        
        var image = document.createElement("img")
        image.src = "./plots/" + files[i] + ".png";
        image.className = "autoResizeImage";

        var log = document.createElement("a");
        log.href = "./logs/" + files[i] + "_info.log";
        log.innerHTML = "[log]";
        
        var pdf = document.createElement("a");
        pdf.href = "./plots/" + files[i] + ".pdf";
        pdf.innerHTML = "[pdf]";
        
        element.appendChild(image);
        // element.appendChild(document.createElement("br"));
        element.appendChild(log);
        element.innerHTML += " - ";
        element.appendChild(pdf);
        line.appendChild(element);
        
        if(i % itemsPerLine == itemsPerLine - 1) {
            document.getElementById("picTable").appendChild(line);
            var line = document.createElement("tr");
            line.style.textAlign = "center";
        }
    }
    if(files.length % itemsPerLine != itemsPerLine) {
        document.getElementById("picTable").appendChild(line);
    }
}

function getChannels() {
    var chans = getListOfFiles('/extraInfo.xml', "Channel");
    var channelHolder = document.getElementById("channels");
    channelHolder.innerHTML = "";
    if(chans.length <= 1) {
        return;
    }
    
    var chanTitle = document.createElement("h2");
    chanTitle.innerHTML = "Plots by Channel:<br>"
    channelHolder.appendChild(chanTitle);
    for(var i = 0; i < chans.length-1; i++) {
        var chan = document.createElement("a");
        chan.href = "./" + chans[i];
        chan.innerHTML = chans[i];
        channelHolder.appendChild(chan);
        channelHolder.innerHTML += " - ";
    }
    var chan = document.createElement("a");
    chan.href = "./" + chans[chans.length-1];
    chan.innerHTML = chans[chans.length-1];
    channelHolder.appendChild(chan);
}

function getTitle() {
    var titleArr = getListOfFiles('/extraInfo.xml', "Title");
    document.getElementById("title").innerHTML = "";
    
    var title = document.createElement("h1");
    title.innerHTML = titleArr[0]
    document.getElementById("title").appendChild(title);
}


function getListOfFiles(urlExtra, tag, ending="") {
    var result = [];
    var scriptUrl = window.location.href + urlExtra;
    $.ajax({
        url: scriptUrl,
        type: 'get',
        //dataType: 'html',
        async:  false,
        success: function(data) {
            $(data).find(tag).each(function(){
                if(ending == "") {
                    result.push(this.innerHTML);
                } else if(this.href.search(ending) != -1) {
                    var name = this.innerHTML;
                    result.push(name.substr(0,name.length-ending.length));
                    //console.log(this.innerHTML);
                }
            });
            
        } 
    });
    
    return result;
}
