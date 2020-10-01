window.alert("hola");
let con = document.getElementById('list-content');   
										 
//var arr = JSON.stringify(arr);
if (arr.length > 0){

    
    var list = '<div class="list-group">';
    var active

    //loop for songs
    for(let i=0;i<arr.length;i++){

        var title = arr[i][1]
        var artist = arr[i][2]
        var album = arr[i][3]
        var href = arr[i][4]
        var image = arr[i][5]
        var pop = arr[i][6]
        var label = arr[i][7]
        

        // color changing
        if (i % 2 == 0){
            active = 'active'
        } else {
            active = ''
        }

        // songs adding
        list += `<a href="${href}" class="list-group-item list-group-item-action flex-column align-items-start ${active}">\
                <div class="d-flex w-100 justify-content-between">\
                    <h5 class="mb-1">${title.bold()} ● ${artist}</h5>\
                    <small><img src="${image}"></small>\
                </div>\
                <p class="mb-1">${album}</p>\
                <small>${label}</small>\
            </a>`;
        }

    list += '</div>';


    con.innerHTML = list;
    }