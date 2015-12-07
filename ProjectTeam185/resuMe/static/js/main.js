/**
 * Created by kangw on 12/6/15.
 */

// Register event handler when ready
$(document).ready(function () {
    $(".popular-btn").click(get_popular);
    $(".new-btn").click(get_latest);
    $(".recommend-btn").click(get_recommend);
    $(".all-btn").click(get_all);
    $(".search-btn").click(search);
    $(".search-input").keypress(function(e){
       if (e.which==13){
            search();
        }
    });
    get_latest();
});

// get the popular resume
function get_popular(){
    $.get("/get_popular").always(function(data){
        console.log(data.Infos);
        if (data != undefined && data.Infos.length>0){
            load_page(data);
        }
    });
}

// get the latest resume
function get_latest(){
     $.get("/get_new").done(function(data){
        if (data != undefined && data.Infos.length>0){
            load_page(data);
        }
    });
}

// get the recommended resume
function get_recommend(){
     $.get("/get_recommend").done(function(data){
        if (data != undefined && data.Infos.length>0){
           load_page(data);
        }
    });
}

// get all resume
function get_all(){
     $.get("/get_all").done(function(data){
        if (data != undefined && data.Infos.length>0){
           load_page(data);
        }
    });

}

// load page after retrieving data from server
function load_page(data){
    $(".block-container").empty();
    var infos = data.Infos;
    var page = "<block class='block'>";
    for (var i = 0; i < infos.length; i++) {
        page += infos[i].html;
    }
    page += "</div>";
    $(".block-container").append(page);
}

// search the keyword
function search(){
    var searcharea = $(".search-input");
    if (searcharea.val()==undefined || searcharea.val().length == 0) return;
    $.get("/search",{key:searcharea.val()})
        .done(function(data){
            if (data != undefined && data.Infos.length>0){
                load_page(data);
            }else{
                $(".info").remove();
                $(".block-container").prepend("<div class='info'><h4 class='text-warning'>Unfortunatelly " +
                    "We can not find the resume you want,you may want read resumes below!</h4><hr>" +
                    "</div>");
            }
    });
}