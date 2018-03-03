
function $create(el){
	return document.createElement(el);
}

function fillTable(id, arr){
	
	for(var i = 0; i < arr.length; i++){
		var tr = $create('tr');
		
		var td = $create('td');
		var a = $create('a');
			a.setAttribute('href', 'syllabus.html');
		var atext = document.createTextNode(arr[i].title);
			a.appendChild(atext);
			td.appendChild(a);
			
		var td2 = $create('td');
		var td2text = document.createTextNode(arr[i].subject);
			td2.appendChild(td2text);
			
		var td3 = $create('td');
		var td3text = document.createTextNode(arr[i].description);
			td3.appendChild(td3text);
		
		tr.appendChild(td);
		tr.appendChild(td2);
		tr.appendChild(td3);
		document.getElementById(id).appendChild(tr);
	}
	
}

function fillMyTable(id, arr){
	
	for(var i = 0; i < arr.length; i++){
		var tr = $create('tr');
		
		var td = $create('td');
		var a = $create('a');
			a.setAttribute('href', 'syllabus.html');
		var atext = document.createTextNode(arr[i].title);
			a.appendChild(atext);
			td.appendChild(a);
			
		var td2 = $create('td');
		var td2text = document.createTextNode(arr[i].subject);
			td2.appendChild(td2text);
			
		var td3 = $create('td');
		var td3text = document.createTextNode(arr[i].description);
			td3.appendChild(td3text);
		
		var td4 = $create('td');
		var td4text = document.createTextNode(arr[i].create_date);
			td4.appendChild(td4text);
		
		var td5 = $create('td');
		var td5text = document.createTextNode(arr[i].last_updated);
			td5.appendChild(td5text);
		
		tr.appendChild(td);
		tr.appendChild(td2);
		tr.appendChild(td3);
		tr.appendChild(td4);
		tr.appendChild(td5);
		document.getElementById(id).appendChild(tr);
	}
	
}

function buildSyllabus(syl){
	for(var i = 0; i < syl.length; i++){
		var li = $create('li');
		var str = $create('strong');
		var inst = document.createTextNode(syl[i].instruction);
			str.appendChild(inst);
			li.appendChild(str);
		
		if(syl[i].type == 'bookLink'){
			var a = $create('a');
				a.setAttribute('href', syl[i].content.url);
				a.setAttribute('target', '_blank');
			var linkString = document.createTextNode(" " + syl[i].content.txt);
				a.appendChild(linkString);
			li.appendChild(a);
		}
		else if(syl[i].type == 'vidLink'){
			var ifrm = $create('iframe');
				ifrm.setAttribute('width', '560');
				ifrm.setAttribute('height', '315');
				ifrm.setAttribute('src', syl[i].content);
				ifrm.setAttribute('frameborder', '0');
				ifrm.setAttribute('allowFullScreen', '')
				ifrm.setAttribute('allow', 'autoplay ; encrypted-media');
				ifrm.setAttribute('width', '560');
			var brk = $create('br');	
			
			li.appendChild(brk);
			li.appendChild(ifrm);
		}
		else if(syl[i].type == 'assignment'){
			var oList = $create('ol');
			for(var a = 0; a < syl[i].content.length; a++){
				var lItem = $create('li');
				var tNode = document.createTextNode(syl[i].content[a]);
					lItem.appendChild(tNode);
				oList.appendChild(lItem);
			}
			li.appendChild(oList);
		}
		
		document.getElementById('sylStepList').appendChild(li);
	}
}





