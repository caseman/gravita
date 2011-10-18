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
        var ship_div = $("#ship-" + id);
        ship_div.offset({
            left: sector_offset.left + (64 - ship_div.width()) / 2,
            top: sector_offset.top + (64 - ship_div.height()) / 2,
        });
    }
}

$gravita.selectShip = function(id) {
    var ship = $("#ship-" + id);
    var ship_offset = ship.offset();
    var selection = $("#ship-selection");
    selection.css("webkitAnimationName", "");
    selection.show();
    selection.offset({
        left: ship_offset.left + (ship.width() - selection.width()) / 2,
        top: ship_offset.top + (ship.height() - selection.height()) / 2,
    });
    selection.css("webkitAnimationName", "spin");
    $gravita.selectedShip = {ship: $gravita.ships[id], div: ship};
    $(".map").bind("mouseover", $gravita.followMouse);
    $(".map").bind("click", $gravita.moveShip);
}

$gravita.followMouse = function(event) {
    if ($gravita.selectedShip) {
        var ship_offset = $gravita.selectedShip.div.offset();
        var this_offset = $(event.target).offset();
        var angle = Math.atan2(
            ship_offset.top - this_offset.top,
            ship_offset.left - this_offset.left) - Math.PI / 2;
        $gravita.selectedShip.div.css("-webkit-transition-duration", 
            ($gravita.selectedShip.ship.cls + 0.5) + "s");
        $gravita.selectedShip.div.css("-webkit-transform", "rotate(" + angle + "rad)");
    }
}

$gravita.moveShip = function(event) {
    if ($gravita.selectedShip) {
        var ship_div = $gravita.selectedShip.div;
        var ship_offset = ship_div.offset();
        var this_offset = $(event.target).offset();
        var dx = ship_offset.left - this_offset.left;
        var dy = ship_offset.top - this_offset.top;
        var dist = Math.sqrt(dx*dx + dy*dy);
        console.log(Math.floor(dist));
        console.log($gravita.selectedShip.ship.range * 64);
        if (Math.floor(dist) <= $gravita.selectedShip.ship.range * 64) {
            $("#ship-selection").hide();
            $gravita.selectedShip.div.css("-webkit-transition-duration", 
                ($gravita.selectedShip.ship.cls + 0.5) * (dist / 128) + "s");
            ship_div.offset({
                left: this_offset.left + (ship_div.width() - $(event.target).width()) / 2,
                top: this_offset.top + (ship_div.height() - $(event.target).height()) / 2,
            });
        }
    }
}

