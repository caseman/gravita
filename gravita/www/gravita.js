/* Copyright (c) 2011 Casey Duncan, All Rights Reserved.
 * This software is subject to the provisions of the MIT License
 */

$gravita = {}

$gravita.showTmpl = function(template, data) {
    $("#content").empty();
    $.tmpl(template, data).appendTo("#content");
}

$gravita.load = function() {
    $.get('/profile_info', '', function(user) {
        $gravita.profile_info = user;
        if (!user.in_game) {
            $gravita.showTmpl("title-template", user);
        }
    });
}
