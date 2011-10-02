/* Copyright (c) 2011 Casey Duncan, All Rights Reserved.
 * This software is subject to the provisions of the MIT License
 */

$gravita = {}

$gravita.load = function() {
    $.get('/profile_info', '', function(user) {
        if (!user.in_game) {
            $.tmpl("title-template", user).appendTo("#content");
        }
    });
}
