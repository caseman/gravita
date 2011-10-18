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
        } else {
            $.get('/map', '', $gravita.renderMap);
        }
    });
}

$gravita.createGame = function() {
    $.post('/create_game',
        $("#create-game-form").serialize(),
        $gravita.renderMap);
}

$gravita.renderMap = function(map) {
    $gravita.ships = map.ships;
    $gravita.showTmpl("map-template", map);
    var map_table = $(".map");
    map_table.width(map.width * 64);
    map_table.height(map.height * 64);
    // Allow the browser to redraw then place ships
    setTimeout($gravita.placeShips, 0);
}

$gravita.placeShips = function() {
    for (id in $gravita.ships) {
        var ship = $gravita.ships[id];
        var sector_offset = $("#sector-" + ship.x + "-" + ship.y).offset();
        var ship_div = $("#ship-" + id)
        ship_div.offset({
            left: sector_offset.left + (64 - ship_div.width()) / 2,
            top: sector_offset.top + (64 - ship_div.height()) / 2,
        });
    }
}
