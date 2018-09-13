var latLon;
var geoplace;
var map;
var geocoder;
var marker;
var transitLayer;
function initMap() {
    geoplace = {lat:-9.3112, lng:-26.1331};
    map = new google.maps.Map(document.getElementById('map'), {
        styles: [
        {
            "elementType": "geometry",
            "stylers": [
                {
                "color": "#1d2c4d"
                }
            ]
            },
            {
            "elementType": "labels.text.fill",
            "stylers": [
                {
                "color": "#8ec3b9"
                }
            ]
            },
            {
            "elementType": "labels.text.stroke",
            "stylers": [
                {
                "color": "#1a3646"
                }
            ]
            },
            {
            "featureType": "administrative",
            "elementType": "geometry",
            "stylers": [
                {
                "visibility": "off"
                }
            ]
            },
            {
            "featureType": "administrative.country",
            "elementType": "geometry.stroke",
            "stylers": [
                {
                "color": "#4b6878"
                }
            ]
            },
            {
            "featureType": "administrative.land_parcel",
            "stylers": [
                {
                "visibility": "off"
                }
            ]
            },
            {
            "featureType": "administrative.land_parcel",
            "elementType": "labels.text.fill",
            "stylers": [
                {
                "color": "#64779e"
                }
            ]
            },
            {
            "featureType": "administrative.neighborhood",
            "stylers": [
                {
                "visibility": "off"
                }
            ]
            },
            {
            "featureType": "administrative.province",
            "elementType": "geometry.stroke",
            "stylers": [
                {
                "color": "#4b6878"
                }
            ]
            },
            {
            "featureType": "landscape.man_made",
            "elementType": "geometry.stroke",
            "stylers": [
                {
                "color": "#334e87"
                }
            ]
            },
            {
            "featureType": "landscape.natural",
            "elementType": "geometry",
            "stylers": [
                {
                "color": "#023e58"
                }
            ]
            },
            {
            "featureType": "poi",
            "stylers": [
                {
                "visibility": "off"
                }
            ]
            },
            {
            "featureType": "poi",
            "elementType": "geometry",
            "stylers": [
                {
                "color": "#283d6a"
                }
            ]
            },
            {
            "featureType": "poi",
            "elementType": "labels.text",
            "stylers": [
                {
                "visibility": "off"
                }
            ]
            },
            {
            "featureType": "poi",
            "elementType": "labels.text.fill",
            "stylers": [
                {
                "color": "#6f9ba5"
                }
            ]
            },
            {
            "featureType": "poi",
            "elementType": "labels.text.stroke",
            "stylers": [
                {
                "color": "#1d2c4d"
                }
            ]
            },
            {
            "featureType": "poi.park",
            "elementType": "geometry.fill",
            "stylers": [
                {
                "color": "#023e58"
                }
            ]
            },
            {
            "featureType": "poi.park",
            "elementType": "labels.text.fill",
            "stylers": [
                {
                "color": "#3C7680"
                }
            ]
            },
            {
            "featureType": "road",
            "elementType": "geometry",
            "stylers": [
                {
                "color": "#304a7d"
                }
            ]
            },
            {
            "featureType": "road",
            "elementType": "labels",
            "stylers": [
                {
                "visibility": "off"
                }
            ]
            },
            {
            "featureType": "road",
            "elementType": "labels.icon",
            "stylers": [
                {
                "visibility": "off"
                }
            ]
            },
            {
            "featureType": "road",
            "elementType": "labels.text.fill",
            "stylers": [
                {
                "color": "#98a5be"
                }
            ]
            },
            {
            "featureType": "road",
            "elementType": "labels.text.stroke",
            "stylers": [
                {
                "color": "#1d2c4d"
                }
            ]
            },
            {
            "featureType": "road.arterial",
            "stylers": [
                {
                "visibility": "off"
                }
            ]
            },
            {
            "featureType": "road.highway",
            "elementType": "geometry",
            "stylers": [
                {
                "color": "#2c6675"
                }
            ]
            },
            {
            "featureType": "road.highway",
            "elementType": "geometry.stroke",
            "stylers": [
                {
                "color": "#255763"
                }
            ]
            },
            {
            "featureType": "road.highway",
            "elementType": "labels",
            "stylers": [
                {
                "visibility": "off"
                }
            ]
            },
            {
            "featureType": "road.highway",
            "elementType": "labels.text.fill",
            "stylers": [
                {
                "color": "#b0d5ce"
                }
            ]
            },
            {
            "featureType": "road.highway",
            "elementType": "labels.text.stroke",
            "stylers": [
                {
                "color": "#023e58"
                }
            ]
            },
            {
            "featureType": "road.local",
            "stylers": [
                {
                "visibility": "off"
                }
            ]
            },
            {
            "featureType": "transit",
            "stylers": [
                {
                "visibility": "off"
                }
            ]
            },
            {
            "featureType": "transit",
            "elementType": "labels.text.fill",
            "stylers": [
                {
                "color": "#98a5be"
                }
            ]
            },
            {
            "featureType": "transit",
            "elementType": "labels.text.stroke",
            "stylers": [
                {
                "color": "#1d2c4d"
                }
            ]
            },
            {
            "featureType": "transit.line",
            "elementType": "geometry.fill",
            "stylers": [
                {
                "color": "#283d6a"
                }
            ]
            },
            {
            "featureType": "transit.station",
            "elementType": "geometry",
            "stylers": [
                {
                "color": "#3a4762"
                }
            ]
            },
            {
            "featureType": "water",
            "elementType": "geometry",
            "stylers": [
                {
                "color": "#0e1626"
                }
            ]
            },
            {
            "featureType": "water",
            "elementType": "labels.text",
            "stylers": [
                {
                "visibility": "off"
                }
            ]
            },
            {
            "featureType": "water",
            "elementType": "labels.text.fill",
            "stylers": [
                {
                "color": "#4e6d70"
                }
            ]
            }
        ],
        zoom: 10,
        center: geoplace
    });
    marker = new google.maps.Marker({
        position: geoplace,
        map: map
    });
}
function codeAddress() {
    geocoder = new google.maps.Geocoder();
    geocoder.geocode({
        'address': document.getElementById("selUF").value + ", " + document.getElementById("selCity").value + ", Brasil"
    }, function(results, status) {
        if (status == google.maps.GeocoderStatus.OK) {
            var myOptions = {
                styles: [
                {
                    "elementType": "geometry",
                    "stylers": [
                    {
                        "color": "#1d2c4d"
                    }
                    ]
                },
                {
                    "elementType": "labels.text.fill",
                    "stylers": [
                    {
                        "color": "#8ec3b9"
                    }
                    ]
                },
                {
                    "elementType": "labels.text.stroke",
                    "stylers": [
                    {
                        "color": "#1a3646"
                    }
                    ]
                },
                {
                    "featureType": "administrative",
                    "elementType": "geometry",
                    "stylers": [
                    {
                        "visibility": "off"
                    }
                    ]
                },
                {
                    "featureType": "administrative.country",
                    "elementType": "geometry.stroke",
                    "stylers": [
                    {
                        "color": "#4b6878"
                    }
                    ]
                },
                {
                    "featureType": "administrative.land_parcel",
                    "stylers": [
                    {
                        "visibility": "off"
                    }
                    ]
                },
                {
                    "featureType": "administrative.land_parcel",
                    "elementType": "labels.text.fill",
                    "stylers": [
                    {
                        "color": "#64779e"
                    }
                    ]
                },
                {
                    "featureType": "administrative.neighborhood",
                    "stylers": [
                    {
                        "visibility": "off"
                    }
                    ]
                },
                {
                    "featureType": "administrative.province",
                    "elementType": "geometry.stroke",
                    "stylers": [
                    {
                        "color": "#4b6878"
                    }
                    ]
                },
                {
                    "featureType": "landscape.man_made",
                    "elementType": "geometry.stroke",
                    "stylers": [
                    {
                        "color": "#334e87"
                    }
                    ]
                },
                {
                    "featureType": "landscape.natural",
                    "elementType": "geometry",
                    "stylers": [
                    {
                        "color": "#023e58"
                    }
                    ]
                },
                {
                    "featureType": "poi",
                    "stylers": [
                    {
                        "visibility": "off"
                    }
                    ]
                },
                {
                    "featureType": "poi",
                    "elementType": "geometry",
                    "stylers": [
                    {
                        "color": "#283d6a"
                    }
                    ]
                },
                {
                    "featureType": "poi",
                    "elementType": "labels.text",
                    "stylers": [
                    {
                        "visibility": "off"
                    }
                    ]
                },
                {
                    "featureType": "poi",
                    "elementType": "labels.text.fill",
                    "stylers": [
                    {
                        "color": "#6f9ba5"
                    }
                    ]
                },
                {
                    "featureType": "poi",
                    "elementType": "labels.text.stroke",
                    "stylers": [
                    {
                        "color": "#1d2c4d"
                    }
                    ]
                },
                {
                    "featureType": "poi.park",
                    "elementType": "geometry.fill",
                    "stylers": [
                    {
                        "color": "#023e58"
                    }
                    ]
                },
                {
                    "featureType": "poi.park",
                    "elementType": "labels.text.fill",
                    "stylers": [
                    {
                        "color": "#3C7680"
                    }
                    ]
                },
                {
                    "featureType": "road",
                    "elementType": "geometry",
                    "stylers": [
                    {
                        "color": "#304a7d"
                    }
                    ]
                },
                {
                    "featureType": "road",
                    "elementType": "labels",
                    "stylers": [
                    {
                        "visibility": "off"
                    }
                    ]
                },
                {
                    "featureType": "road",
                    "elementType": "labels.icon",
                    "stylers": [
                    {
                        "visibility": "off"
                    }
                    ]
                },
                {
                    "featureType": "road",
                    "elementType": "labels.text.fill",
                    "stylers": [
                    {
                        "color": "#98a5be"
                    }
                    ]
                },
                {
                    "featureType": "road",
                    "elementType": "labels.text.stroke",
                    "stylers": [
                    {
                        "color": "#1d2c4d"
                    }
                    ]
                },
                {
                    "featureType": "road.arterial",
                    "stylers": [
                    {
                        "visibility": "off"
                    }
                    ]
                },
                {
                    "featureType": "road.highway",
                    "elementType": "geometry",
                    "stylers": [
                    {
                        "color": "#2c6675"
                    }
                    ]
                },
                {
                    "featureType": "road.highway",
                    "elementType": "geometry.stroke",
                    "stylers": [
                    {
                        "color": "#255763"
                    }
                    ]
                },
                {
                    "featureType": "road.highway",
                    "elementType": "labels",
                    "stylers": [
                    {
                        "visibility": "off"
                    }
                    ]
                },
                {
                    "featureType": "road.highway",
                    "elementType": "labels.text.fill",
                    "stylers": [
                    {
                        "color": "#b0d5ce"
                    }
                    ]
                },
                {
                    "featureType": "road.highway",
                    "elementType": "labels.text.stroke",
                    "stylers": [
                    {
                        "color": "#023e58"
                    }
                    ]
                },
                {
                    "featureType": "road.local",
                    "stylers": [
                    {
                        "visibility": "off"
                    }
                    ]
                },
                {
                    "featureType": "transit",
                    "stylers": [
                    {
                        "visibility": "off"
                    }
                    ]
                },
                {
                    "featureType": "transit",
                    "elementType": "labels.text.fill",
                    "stylers": [
                    {
                        "color": "#98a5be"
                    }
                    ]
                },
                {
                    "featureType": "transit",
                    "elementType": "labels.text.stroke",
                    "stylers": [
                    {
                        "color": "#1d2c4d"
                    }
                    ]
                },
                {
                    "featureType": "transit.line",
                    "elementType": "geometry.fill",
                    "stylers": [
                    {
                        "color": "#283d6a"
                    }
                    ]
                },
                {
                    "featureType": "transit.station",
                    "elementType": "geometry",
                    "stylers": [
                    {
                        "color": "#3a4762"
                    }
                    ]
                },
                {
                    "featureType": "water",
                    "elementType": "geometry",
                    "stylers": [
                    {
                        "color": "#0e1626"
                    }
                    ]
                },
                {
                    "featureType": "water",
                    "elementType": "labels.text",
                    "stylers": [
                    {
                        "visibility": "off"
                    }
                    ]
                },
                {
                    "featureType": "water",
                    "elementType": "labels.text.fill",
                    "stylers": [
                    {
                        "color": "#4e6d70"
                    }
                    ]
                }
                ],
                zoom: 10,
                center: results[0].geometry.location,
            }
            map = new google.maps.Map(document.getElementById("map"), myOptions);

            var marker = new google.maps.Marker({
                map: map,
                position: results[0].geometry.location
            });
        }
    });
}
codeAddress();