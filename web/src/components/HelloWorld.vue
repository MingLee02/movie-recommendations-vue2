<template>
    <div>
        <h2>Find Local Cinemas</h2>
        <p>{{ address }}</p>
        <input v-model="postcode" v-on:keyup.enter="getAddress" placeholder="Enter postcode">
        <div id="map"></div>
        <ul v-if="cinemaList.length > 0">
          <li v-for="todo in cinemaList" v-on:click="selectCinema(todo)">
              {{ todo.name }}
              {{ todo.rating }}
              {{ todo.distance }}
              {{ todo.address }}
          </li>
        </ul>
    </div>    
</template>

<script>
    import axios from 'axios'
    var address = ' ';
    var postcode = ' ';
    var cinemaList = '';
    var url = "http://127.0.0.1:5000/"

    export default {
        data() {
            return {
                address: address,
                postcode: postcode,
                cinemaList: cinemaList
            };
        },
        name: 'Gplaces',
        methods: {
            getAddress: function () {
                var self = this;
                axios.get(url + "api/address/" + this.postcode)
                  .then((response) => {
                        // var results =  response.json.results[0]
                        this.address = response.data.formatted_address
                        // var placeId = results.place_id
                        var latLang = response.data.geometry.location
                        console.log(latLang)
                        this.drawMap(latLang)
                    })
                    .catch((err) => {
                        console.log(err);
                    });
            },
            drawMap: function (latLang) {
                var map = new google.maps.Map(document.getElementById('map'), {
                    zoom: 15,
                    center: latLang
                });

                new google.maps.Marker({
                    position: latLang,
                    map: map,
                    title: 'Hello World!',
                    icon: 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png'
                });

                this.getCinemas(latLang, map);
            },
            getCinemas: function (latLang, map) {
              var locations = []
               var origin = latLang.lat + ":" + latLang.lng
                axios.get(url + "api/cinema-list/" +  origin)
                  .then((response) => {
                      var x;
                      this.cinemaList = response['data'];
                      console.log(response['data'])
                      for (x in response['data']) {
                        locations.push(response['data'][x]['latlng']) 
                      }
                      this.addMarkers(locations, map)
                    })
                    .catch((err) => {
                        console.log(err);
                    });
            },
            addMarkers: function (locations, map) {
                for (var i = 0; i < locations.length; i++) { 
                  new google.maps.Marker({
                    position: locations[i],
                    map: map
                  });
                }
            },
            selectCinema: function (cinema) {
              console.log('clicked')
              console.log(cinema.name)
              console.log(cinema.address)
            }
        }
    }
</script>

<style>
    #map {
        height: 100%;
        width: 300px;
        overflow: auto !important;
        position: fixed !important;
    }
</style>