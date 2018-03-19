// content.js

var url = chrome.runtime.getURL('pytania.json');
var xhr = new XMLHttpRequest();
var json, qids;
xhr.open('GET', url, true);
xhr.onreadystatechange = function()
{
    if(xhr.readyState == XMLHttpRequest.DONE && xhr.status == 200)
    {
        var json = JSON.parse(xhr.responseText);
        var qids = [];
        var n_answers = [];
        var els = document.getElementsByClassName('dd-postcontent dd-postcontent-0 clearfix')[2];
        var els = els.childNodes[2].textContent;
        var E12 = (els.search('E12') != -1) || (els.search('E.12') != -1);
        var E13 = els.search('E13') != -1 || els.search('E.13') != -1;
        var E14 = els.search('E14') != -1 || els.search('E.14') != -1;
        var qs = document.getElementsByName('cid');
        var odp = document.getElementsByClassName('odp');
        for (i=0; i < qs.length; i++) {
        	qids.push(qs[i].value);
        }
        var nn = 0;
        if (E12) {
            var aa = json.E12;
        } else if (E13) {
            var aa = json.E13;
        } else if (E14) {
            var aa = json.E14;
        }
        for (i=0; i < qids.length; i++) {
        	n_answers.push(parseInt(aa[qids[i]][6]) + nn);
        	nn += 4;
        }
        doc(0,0,0, json, n_answers, odp);
        chrome.runtime.onMessage.addListener(
		  function(request, sender, sendResponse) {
		    if( request.message === "clicked_browser_action" ) {
                /*var els = document.getElementsByClassName('dd-postcontent dd-postcontent-0 clearfix')[2];
                var els = els.childNodes[2].textContent;
                var E12 = (els.search('E12') != -1) || (els.search('E.12') != -1);
                var E13 = els.search('E13') != -1 || els.search('E.13') != -1;
                var E14 = els.search('E14') != -1 || els.search('E.14') != -1;
                alert(E12);
                alert(E13);
                alert(E14);*/
		    	doc(request, sender, sendResponse, json, n_answers, odp);
		    }
		  }
		);
    }
};
xhr.send();

function doc(request, sender, sendResponse, json, n_answers, odp) {
    for (i=0; i < odp.length; i++) {
        var x = odp[i];
        var n = x.getElementsByTagName("p")[0].childNodes[1];
        var str = x.textContent;
        while (str[str.length-1] === ".")
            str = str.slice(0,-1);
        n.textContent = str;
    }
	for (i=0; i < n_answers.length; i++) {
		var x = odp[n_answers[i]]; 
		var n = x.getElementsByTagName("p")[0].childNodes[1];
		n.textContent = n.textContent + ".";
	}
}