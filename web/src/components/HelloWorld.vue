<template>
    <div>
        <h2>Find Local Cinemas</h2>
        <p>{{ address }}</p>
        <input v-model="postcode" v-on:keyup.enter="getAddress" placeholder="Enter postcode">
        <div id="map"></div>
    </div>    
</template>

<script>
    import axios from 'axios'
    var address = ' ';
    var postcode = ' ';
    var url = "http://127.0.0.1:5000/"

    export default {
        data() {
            return {
                address: address,
                postcode: postcode,
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

               var origin = latLang.lat + ":" + latLang.lng
                axios.get(url + "api/cinema-list/" +  origin)
                  .then((response) => {
                        console.log(response)
                    })
                    .catch((err) => {
                        console.log(err);
                    });
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