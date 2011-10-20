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
            $.get('/players', '', function(players) {
                $gravita.players = players;
            });
        }
    });
}

$gravita.createGame = function() {
    $.post('/create_game',
        $("#create-game-form").serialize(),
        function(game) {
            $gravita.players = game.players;
            $gravita.renderMap(game.map);
        });
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
    $.get('/ship_moves?ship_id=' + id, function(sectors) {
        $gravita.ship_moves = sectors;
        $('.map .sector')
            .css('background', 'transparent')
            .unbind('click');
        for (i = 0; i < sectors.length; i++) {
            $('#sector-' + sectors[i].x + '-' + sectors[i].y)
                .css('background', 'url("/static/images/sector-hilite.png")')
                .bind("click", $gravita.moveShip);;
        }
    });
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
        var target = $(event.target);
        $.post('/move_ship', {
            ship_id: $gravita.selectedShip.ship.id,
            x: target.attr("x"),
            y: target.attr("y"),
        }, function(ship) {
            $gravita.ships[ship.id] = ship;
            var ship_div = $gravita.selectedShip.div;
            var ship_offset = ship_div.offset();
            var sector = $("#sector-" + ship.x + "-" + ship.y);
            var sector_offset = sector.offset();
            var dx = ship_offset.left - sector_offset.left;
            var dy = ship_offset.top - sector_offset.top;
            var dist = Math.sqrt(dx*dx + dy*dy);
            $("#ship-selection").hide();
            $(".map").unbind("mouseover");
            $('.map .sector')
                .css('background', 'transparent')
                .unbind('click');
            $gravita.selectedShip.div.css("-webkit-transition-duration", 
                (ship.cls + 0.5) * (dist / 128) + "s");
            ship_div.offset({
                left: sector_offset.left + (ship_div.width() - sector.width()) / 2,
                top: sector_offset.top + (ship_div.height() - sector.height()) / 2,
            });
            $gravita.selectedShip = null;
        });
    }
}

