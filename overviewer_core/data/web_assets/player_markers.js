var playerListElement	=	'#player_list'; //The HTML element ID of the <ul> to display the player list
var JSONFile			=	'markers.json'; //The JSON file containing the player data
var playerMarkers		=	[]; //The array of player objects


/**
 * Create a new Player Marker
 *
 * @param	location	google.maps.LatLng	The initial location of the marker
 * @param	map			google.maps.Map		The map where the marker shoudl be displayed (the overviewer map)
 * @param	name		string				The name of the player
 * @param	icon		string				The image icon of the player
 * @param	visible		boolean				True if the marker should be displayed
 * @return	google.maps.Marker
 */
function createPlayerMarker(location,map,name,icon,visible){
	var marker =  new google.maps.Marker({
		position: location,
		map: map,
		title: name,
		icon: icon,
		visible: visible,
		zIndex: 999
	});
	return marker;
}


/**
 *  Create a new Informational Window for a Player Marker
 *
 *  @param	name	string	The name of the player
 *  @return	goolge.maps.InfoWindow
 */
function createInfoWindow(name){
	var html = "<div class=\"infoWindow\" style='width: 300px'><img src='player.php?"+name+"'/><h1>"+name+"</h1></div>";
	var infoWindow = new google.maps.InfoWindow({content: html});
	return infoWindow;
}

/**
 * Create a new Listener for the Marker
 *
 * @param	marker		google.maps.Marker
 * @param	infoWindow	google.maps.InfoWindow
 * @return	google.maps.event.MapEventListener
 */
function createInfoWindowListener(marker,infoWindow){
	var listener	=	google.maps.event.addListener(marker, 'click', function() {
		infoWindow.open(marker.getMap(),marker);
	});
	return listener;
}


/**
 * Create a new Player Listing
 *
 * @param	list	string	The html <ul> element ID to display the listing
 * @param	name	string	The name of the player
 * @return	jQuery
 */
function createPlayerListing(list,name){
	$(list).append('<li id="li_'+name+'" style="background-image: url(player.php?'+name+');">'+name+'(hidden)</li>');
	return $('#li_'+name);
}

/**
 * Load the players JSON file and update the map
 *
 * @return void
 */
function loadPlayers(){
	$.ajax({
		url:JSONFile,
		dataType: 'json',
		cache: false,
		success: function(data){
			for (var i in data) {
                var curTileSet = overviewer.mapView.options.currentTileSet;
                if (curTileSet.get("world_name") != data[i].world) {
                    continue;
                }
				var item			=	data[i];
				var name			=	item.msg;
				var world			=	item.world;
				var x				=	item.x;
				var y				=	item.y;
				var z				=	item.z;
				var display			=	item.display;
				var timestamp		=	new Date(item.timestamp);
				var icon			=	'player.php?'+name;
				var location		=	overviewer.util.fromWorldToLatLng(x,y,z, curTileSet);
				var visible			=	(display!="hidden");

				/**
				 * If we receive a player that is not in the list, it must be created
				 */
				if(playerMarkers[name]==undefined){
					var marker		=	createPlayerMarker(location,overviewer.map,name,icon,visible); //create the marker
					var infoWindow	=	createInfoWindow(name); //create the info window
					var listener	=	createInfoWindowListener(marker,infoWindow); //create the listener on the marker for the info window
					var listing		=	createPlayerListing(playerListElement,name,icon); //create the player listing

					/**
					 * The player object
					 */
					playerMarkers[name]	=	{
						name:		name, //The player's name
						marker:		marker, //The player's map marker
						infoWindow:	infoWindow, //The player's informational window
						listener:	listener, //The map marker listener
						listing:	listing, //The player's listing in the <ul>
						location:	location, //The player's map location'
						timestamp:	timestamp, //The timestamp sent from the server
						updated:	new Date(), //The last time JS updated (heard from) the player
						removed:	false, //Has the player been removed from the map
						x:			x, //The player's in-game X coordinate
						y:			y, //The player's in-game Y coordinate
						z:			z, //The player's in-game Z coordinate
						icon:		icon, //The player's image icon
						visible:	visible //Is the player visible
					}
				}
				playerMarkers[name].location	=	location; //Update the player's location
				playerMarkers[name].x			=	x;
				playerMarkers[name].y			=	y;
				playerMarkers[name].z			=	z;
				playerMarkers[name].visible		=	visible; //Update if the player is visible
				playerMarkers[name].updated		=	new Date(); //Update the last time JS heard from the player

				updatePlayer(name); //Update the player on the map
			}
			checkPlayers(); //Check for offline players
		}
	});
}


/**
 * Update the player on the map
 *
 * @param	name	string	The name of the player
 * @return	void
 */
function updatePlayer(name){
	var player	=	playerMarkers[name];

	player.marker.setPosition(player.location); //Set the marker position on the map
	player.marker.setVisible(player.visible); //Set the marker visibility on the map
	player.infoWindow.setPosition(player.location); //Set the InfoWindow position on the map
	player.listing.toggle(true); //Set the listing to visible (default)

	/**
	 * If the player has been removed from the map (went offline) and is now back
	 *
	 * We wouldn't be here unless the player is now online, but we had already created
	 * this player, and we don't want to re-create it because that would be wasteful :)
	 */
	if(player.removed){
		player.marker.setMap(overviewer.map); //Set the marker's map (google's way of enabling the marker)
		player.infoWindow.setMap(overviewer.map); //Set the infoWindow's map (again google's way)
		player.infoWindow.close(); //Close the infoWindow (google automaticly opens an InfoWindow when it's map is set)
	}
	player.removed	=	false; //The player is no longer removed
	$(player.listing).unbind('click'); //We unbind clicking on the <li> by default (for hidden players)

	/**
	 *If the player's visibility is set to false (through the in-game /hide command)
	 */
	if(!player.visible){
		player.infoWindow.close(); //close the InfoWindow (incase it was open at the time)
		$(player.listing).empty().append(player.name+' (hidden)'); //Empty the <li> and re-insert the player with (hidden) instead of the coordinates
	}else{
		$(player.listing).empty().append(player.name+' ('+Math.round(player.x)+','+Math.round(player.y)+','+Math.round(player.z)+')'); //Empty the <li> and re-insert the player with their in-game coordinates (rounding for prettyness)
		/**
		 *We re-bind the click event only if they are visible
		 *This prevents clicking on the <li> to get the player's last location and a pointless InfoWindow
		 */
		$(player.listing).click(function(){
			player.infoWindow.open(overviewer.map,player.marker);
		});
	}
}

/**
 * Check the players for inactivity and remove them if not updated
 *
 * @return void
 */
function checkPlayers(){
	var timeout	=	new Date(new Date()-3000); //The timeout date object
	/**
	 *Iterate over all known players to check for their last update
	 */
	for(var i in playerMarkers){
		var player	=	playerMarkers[i];
		/**
		 *If the player has not updated within the timeout window
		 *They need to be removed, but only if we haven't already removed them
		 */
		if(player.updated<timeout && !player.removed){
			removePlayer(player.name);
		}
	}
}

/**
 * Remove a player from the map
 *
 * @param	name	string	The name of the player
 * @return void
 */
function removePlayer(name){
	var player	=	playerMarkers[name];
	player.infoWindow.close(); //close the InfoWindow (probably not needed, but let's be consistant)
	player.infoWindow.setMap(null); //Unlink the InfoWindow from the map
	player.marker.setMap(null); //Unlink the marker from the map
	$(player.listing).toggle(false); //Hide the player listing in the <ul>
	player.removed	=	true; //The player has been removed
}

setInterval(loadPlayers, 1000 * 3);
