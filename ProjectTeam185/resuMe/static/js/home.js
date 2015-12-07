/**
 * Created by kangw on 11/4/15.
 */

/**
 * Register event handler, and set csrf token when page is ready
 */

var csrftoken;

$(document).ready(function () {
    $('#save-add-block').click(add_block);
    $(document).on("click", ".blogcontent-edit", edit_block);
    $(document).on("click", ".portfolio-link", photo_link);
    $(document).on("click", ".profile-save", edit_profile);
    $(document).on("click", ".block-delete", delete_block);
    $(document).on("click", ".blockcontent-delete", delete_block_content);
    $(document).on("click", ".delete-alert", delete_alert);
    $(document).on("click", "#save-edit-about", save_aboutInfo);
    $(document).on("click", ".move-up-block", moveup_block);
    $(document).on("click", ".move-down-block", movedown_block);
    $(document).on("click", ".up-blockcontent", moveup_blockcontent);
    $(document).on("click", ".down-blockcontent", movedown_blockcontent);
    $(document).on("click", "#email-submit", email_submit);
    $(document).on("click", "#info-edit", edit_info);
    $(document).on("click", ".slide-submenu", function() {
        $(this).closest('.list-group').fadeOut('slide');
      });
    $(document).on("click", ".mini-submenu", function(){
        var $item = $(this).next('.list-group');
        $item.toggle('slide');
    });

    // refresh photo when the picture file is selected
     $("#input-photo").change(function(e) {
        for (var i = 0; i < e.originalEvent.srcElement.files.length; i++) {
            var file = e.originalEvent.srcElement.files[i];
            var img = $("#edit-profile-photo");
            var reader = new FileReader();
            reader.onloadend = function() {
                 img.attr('src',reader.result);
            }
            reader.readAsDataURL(file);
        }
    });

    // set Cookies
    csrftoken = getCookie('csrftoken');
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    })
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    };
})


function add_block() {
    var title = $("#title-to-add").val();
    var id;
    $.post("/resuMe/add_block", {'title': title}).done(function (data) {
        id = data;
        if (title != null && title.length != 0) {
            var html = "<div class='block' id='block-" + id + "'><span class='h2'>" + title + "</span>\
                    <kbd class='pull-right'>\
                        <button data-toggle='modal' data-target='#blogcontent-modal'\
                                edit-id='" + id + "'class='blogcontent-edit'>EDIT</button>\
                                <button class='btn-sm delete-alert' data-toggle='modal' data-target='#blogcontent-modal'\
                                alert-id=" + id + "><i class='glyphicon glyphicon-trash'></i></button></kbd>\
            <hr class='resumeSeperator'>\
            </div><br>"
            $("#append-after").after(html);
        }
    });
}

function delete_alert() {
    empty();
    var id = $(this).attr('alert-id');
    var page = "<div class='modal-dialog'>";
    page += "    <div class='modal-content'>";
    page += "        <div class='modal-header'>";
    page += "            <button type='button' class='close' data-dismiss='modal'>X</button>";
    page += "            <h4 class='modal-title' id='myModalLabel'>Are you sure you want to delete?</h4>";
    page += "        </div>";
    page += "        <div style='text-align: center' class='modal-body'>";
    if ($(this).hasClass("btn-sm")){
        page += "            <button type='button' class='btn btn-info block-delete' data-dismiss='modal' delete-id='" + id +
        "'>Yes</button>";
    }else{
        page += "            <button type='button' class='btn btn-info blockcontent-delete' data-dismiss='modal' " +
            "delete-id='" + id + "'>Yes</button>";
        // FadeIn select options after click button
        $(this).parent().css("display","none");
    }
    page += "        </div>";
    page += "     </div>";
    page += "</div>";
    $("#blogcontent-modal").append(page);

}

function delete_block() {
    var id = $(this).attr('delete-id');
    $.post('/resuMe/delete_block', {id: id})
        .done(function () {
            $("#block-" + id).remove();
        });
}

function delete_block_content(){
    var id = $(this).attr('delete-id');
    $.post('/resuMe/delete_content', {id: id})
        .done(function () {
            $("div[blockcontent-id='"+id+"']").remove();
        });
}

function edit_profile(){
    var option = {
        type:'post',
        url:'/resuMe/edit_profile',
        cache:false,
        dataType:'text',
        success:function(data){
            var name= $("#first_name").val() + " " + $("#last_name").val();
            $("#profile-name").text(name);
            var summary = $("#summary").val();
            $("#profile-summary").text(summary);
            var user_id = parseInt($("#userID").val());
            $("#user-photo").attr('src','/resuMe/photo/'+user_id + "?" + new Date());
            $("#edit-profile-photo").attr('src','/resuMe/photo/'+user_id + "?" + new Date());
        }
    }
    $("#profile").ajaxSubmit(option);
    return false;
}

function edit_block() {
    empty();
    var id = $(this).attr("edit-id");
    var block = $("#block-" + id);
    var list_of_li = [];
    var list_of_div = [];
    block.find(".sub-block").each(function (index) {
        var html = $(this).html();
        var li;
        var div;
        var blockcontent_id = $(this).attr("blockcontent-id");
        var title_text = $("#sub-block-title-" + blockcontent_id).text().trim();
        var content_text = $("#sub-block-content-" + blockcontent_id).text().trim();
        if (index == 0) {
            div = "<form class='tab-pane fade in active' action='/resuMe/edit_block_content/" + blockcontent_id
                + "'id='content-" + blockcontent_id + "' method='post' enctype='multipart/form-data'>";
            li = "<li class='active li-title'><a data-toggle='pill' href='#content-" + blockcontent_id + "'>"
                + title_text + "</a></li>";
        } else {
            div = "<form class='tab-pane fade' method='post' action='/resuMe/edit_block_content/" + blockcontent_id
                + "'id='content-" + blockcontent_id + "' method='post' enctype='multipart/form-data'>";
            li = "<li class='li-title'><a data-toggle='pill' href='#content-" + blockcontent_id + "'>" + title_text +
                "</a></li>";
        }
        div += "<input type='hidden' name='csrfmiddlewaretoken' value='" + csrftoken + "'>";
        div += html;
        div += "<hr>";
        div += "<label class='pull-left'>Title Name</label>";
        div += "<input type='text' class='form-control' name='sub_title' " +
            "value='" + title_text + "' id='title-" + blockcontent_id + "'>";
        div += "<label class='pull-left'>Content</label>";
        div += "<textarea type='text' class='form-control' name='content' " +
            "id='content-" + blockcontent_id + "'>"+content_text+"</textarea>";
        div += "<label class='pull-left'>Subject</label>"
        div += "<select class='pull-left form-control' id='select-" + blockcontent_id + "' name='link-select'>";
        div += "<option value='default' class='default'>Please selcet one.....</option>" +
            "<option value='link' class='link' link-id='" + blockcontent_id + "'>Link Website</option>" +
            "<option value='photo' class='photo' photo-id='" + blockcontent_id + "'>Link Photo</option>";
        div += " </select>";
        div += "<input type='text' class='form-control link-input' name='url' style='display:none'" +
            "placeholder='Enter the link you want...' id='link-input-" + blockcontent_id + "'>";
        div += "<span class='btn btn-info btn-file' style='display:none' id='upload-btn-" + blockcontent_id +
            "'>Upload Photo <input type='file' name='picture_file" +  "' id='upload-" + blockcontent_id + "'></span>";
        div += "<div>";
        div += '<hr>';
        div += "<div style='text-align: center'>"
        div += "<button type='submit' class='btn btn-default save-remove' >Save</button>";
        div += "</div>"
        div += "</div>";
        div += "</form>"
        list_of_div.push(div);
        list_of_li.push(li);
    });
    var page = "<div class='modal-dialog'>\
                    <div class='modal-content'>\
                      <div class='modal-header'>\
                         <button type='button' class='close' data-dismiss='modal'>X</button>\
                         <button class='btn btn-success btn-circle' add-blockcontent-id='" + id +
                        "'data-toggle='popover' data-trigger='hover' data-content='Add Blockcontent'>\
                        <i class='glyphicon glyphicon-link'>\
        </i>ADD</button>\
         <h4 class='modal-title' id='myModalLabel'>Profile Edition</h4>\
         <ul class='nav nav-pills'>"

    for (i = 0; i < list_of_li.length; i++) {
        page += list_of_li[i];
    }

    page += "</ul>\
                </div>\
                    <div class='modal-body'>\
                        <div style='text-align: center' class='tab-content'>";

    for (i = 0; i < list_of_div.length; i++) {
        var html = list_of_div[i];
        page += html;
    }
    page += "</div>\
               </div>";

    // apend the dynamic page
    $("#blogcontent-modal").append(page);
    // eleminate the redundant element
    $("#blogcontent-modal").find(".caption").remove();
    $("#blogcontent-modal").find(".sidebar").remove();

    $(".btn-circle").click(add_block_content);
    $("select").change(showInput);
    // give the user feedback what file he has choosen when upload file
    $(".btn-file :file").change(fileChoose);

}

function empty() {
    $("#blogcontent-modal").empty();
}

function add_block_content() {
    var block_id = $(this).attr('add-blockcontent-id');
    console.log(block_id);
    $.post("/resuMe/add_block_content/" + block_id).done(function (data) {
        var tab_panel = $(".tab-content");
        var nav_pill = $(".nav-pills");
        var id = data;
        var li = "<li class='active'><a data-toggle='pill' href='#content-" + id + "'>" + 'New Content' + "</a></li>";
        var div = "<form class='tab-pane fade in active' method='POST' enctype='multipart/form-data' " +
            "action='/resuMe/edit_block_content/" + data + "' id='content-" + id + "'>";
        div += "<input type='hidden' name='csrfmiddlewaretoken' value='" + csrftoken + "'>";
        div += "<label class='pull-left'>Title Name</label>";
        div += "<input type='text' class='form-control' value='Description' name='sub_title' id='title-" + id + "'>";
        div += "<label class='pull-left'>Content</label>";
        div += "<input type='text' class='form-control' value='Description' name='content' id='title-" + id + "'>";
        div += "<label class='pull-left'>Subject</label>"
        div += "<select class='pull-left form-control link-select' id='select-" + id + "' name='link-select'>";
        div += "<option selected value='default'>Please selcet one.....</option>" +
            "<option value='link' class='link' link-id='" + id + "'>Link Website</option>" +
            "<option value='photo' class='photo' photo='" + id + "'>Link Photo</option>";
        div += " </select>";
        div += "<input type='text' class='form-control link-input' style='display:none'" +
            "placeholder='Enter the link you want...' name='url' id='link-input-" + id + "'>";
        div += "<span class='btn btn-info btn-file' style='display:none' id='upload-btn-" + id +
            "'>Upload Photo <input type='file' name='picture_file'" +" id='upload-" + id + "'></span>";
        div += "<div>";
        div += "<div style='text-align: center'>";
        div += '<hr>';
        div += "<button type='submit' class='btn btn-default save-remove' >Save</button>";
        div += "</div>";
        div += "</div>";
        div += "</form>"

        nav_pill.append(li);
        $("div .active").removeClass("in active");
        $("ul:last-child").addClass("active");
        tab_panel.append(div);
        // add event listener to select button
        $("select").change(showInput);
        // give the user feedback what file he has choosen when upload file
        $(".btn-file :file").change(fileChoose);
    });

}

function showInput() {
    var id = /\d+/.exec($(this).attr('id'));
    var select = $("#select-" + id + " option:selected");
    if (select.hasClass("link")) {
        $("#link-input-" + id).show();
        $("#upload-btn-" + id).hide();
    } else if (select.hasClass("photo")) {
        $("#upload-btn-" + id).show();
        $("#link-input-" + id).hide();
    } else {
        $("#link-input-" + id).hide();
        $("#upload-btn-" + id).hide();
    }

}

// give the user feedback what file he has choosen when upload file
function fileChoose() {
    var input = $(this),
        numFiles = input.get(0).files ? input.get(0).files.length : 1,
        label = input.val().replace(/\\/g, '/').replace(/.*\//, '');
    input.trigger('fileselect', [numFiles, label]);
    alert(label + " has been choosen");
}

function photo_link() {
    $(".jk-slider").empty();
    var id = $(this).parents(".sub-block").attr("blockcontent-id");
    if (id==undefined) return;
    $.get("/resuMe/get_picture_ids/"+id).always(function (data) {
        if (data.length==0) return;

        var page = "<div id='photo_move' class='carousel slide row' data-ride='carousel'>";
        page += "<ol class='carousel-indicators'>";

        for (var i = 0; i < data.length; i++) {
            if (i != 0)
                page += "<li data-target='#photo_move' data-slide-to='" + i + "'></li>";
            else
                page += "<li data-target='#photo_move' data-slide-to='" + i + "' class='active'></li>";
        }

        page +="</ol>";
        page += "<div class='carousel-inner'>";
        for (var i = 0; i < data.length; i++) {
            if (i != 0) {
                page += "<div class='item'>";
            } else {
                page += "<div class='item active'>";
            }
            page += "<img class='content-pic' src='/resuMe/get_picture/" + data[i] + "'>";
            page += "<div class='hero'>";
            page += "<hgroup>";
            page += "</hgroup>";
            page += "</div></div>";
        }
        page += "</div>";
        page += "<a class='left col-md-2 carousel-control' href='#photo_move' data-slide='prev'>";
        page += "<span class='glyphicon glyphicon-chevron-left'></span>";
        page += "</a>";
        page += "<a class='right col-md-2 carousel-control' href='#photo_move' data-slide='next'>";
        page += "<span class='glyphicon glyphicon-chevron-right'></span>";
        page += "</a>";
        page += "</div>";
        $(".jk-slider").append(page);
    });
}


function save_aboutInfo(){
    var text = $("#about-to-add").val();
    $.post("/resuMe/edit_about",{about: text}).done(function(data){
        if (data == 'success') {
            $("#about-content").text(text);
        }else {
            window.alert('Invalid update!')
        }
    })
}

function edit_info(){
    var address = $("#address").val();
    var phone =$("#user-phone").val();
    var email =$("#user-email").val();
    console.log(address);
    console.log(phone);
    console.log(email);
    $.post("/resuMe/edit_contact",{address: address, phone:phone, email: email}).done(function (data){
        if (data == "success") {
            $("#address-to-show").text($("#address").val());
            $("#phone-to-show").text($("#user-phone").val());
            $("#email-to-show").text($("#user-email").val());
        }else {
            window.alert("Invalid Update!!")
        }
    });

}

function moveup_block(){
    var id = $(this).attr("block-up-id");
    var block = $("#block-"+id);
    var up_block = block.prev();
    var upblock_id = up_block.attr("block-id");
    if (upblock_id == undefined) return;
    else{
        $.post("/block_up", {id: id, upblock_id: upblock_id}).done(function () {
            swap(block,up_block);
        });
    }
}

function movedown_block(){
    var id = $(this).attr("block-down-id");
    var block = $("#block-"+id);
    var down_block = block.next();
    var down_id = down_block.attr("block-id");
    if (down_id == undefined) return;
    else{
        $.post("/block_down", {id: id, down_id: down_id}).done(function () {
            swap(block,down_block);
        });
    }
}

function swap(block,block2){
    // swap id and block-id
    var id1 = block.attr("id");
    var id2 = block2.attr("id");
    block2.attr("id",id1);
    block.attr("id",id2);
    var tmp_block_id = block.attr("block-id");
    block.attr("block-id",block2.attr("block-id"));
    block2.attr("block-id",tmp_block_id);
    // swap innerHtml
    var temp = block.html();
    block.html(block2.html());
    block2.html(temp);
}

function moveup_blockcontent(){
    var id = $(this).attr("blockcontent-up-id");
    var blockcontent = $("div[blockcontent-id='" + id +"']");
    var prev_blockcontent = blockcontent.prev().prev();
    var prev_id = prev_blockcontent.attr("blockcontent-id");
    if (prev_id==undefined) return;
    else{
        var item = $(this).parent();
        item.css('display',"none");
        $.post("/content_up", {id: id, next_id: prev_id}).done(function () {
            swap_blockcontent(blockcontent,prev_blockcontent);
        });
    }
}

function movedown_blockcontent(){
    var id = $(this).attr("blockcontent-down-id");
    var blockcontent = $("div[blockcontent-id='"+id+"']");
    var next_blockcontent = blockcontent.next().next();
    var next_id = next_blockcontent.attr("blockcontent-id");
    if (next_id==undefined) return;
    else{
        var item = $(this).parent();
        item.css('display',"none");
        $.post("/content_down", {id: id, next_id: next_id}).done(function () {
            swap_blockcontent(blockcontent,next_blockcontent);
        });
    }

}

function swap_blockcontent(blockcontent1,blockcontent2){
     // swap blockcontent-id
    var tmp_block_id = blockcontent1.attr("blockcontent-id");
    blockcontent1.attr("blockcontent-id",blockcontent2.attr("blockcontent-id"));
    blockcontent2.attr("blockcontent-id",tmp_block_id);
    // swap innerHtml
    var temp = blockcontent1.html();
    blockcontent1.html(blockcontent2.html());
    blockcontent2.html(temp);

}

function email_submit() {
    var name = $("#name").val();
    var email = $("#email").val();
    var phone = $("#phone").val();
    var message = $("#message").val();
    var id = $("#userID").val();
    $.get("/send_email/"+id, {name:name, email:email, phone:phone, message:message}).done(function(data) {
        if (data == 'success') {
            window.alert('Send email success!!');
        }else {
            window.alert("Fields can't be blank!!");
        }
    });
}



