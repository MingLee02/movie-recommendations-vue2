<template>
    <div>
        <h2>Find Local Cinemas</h2>
        <p>{{ address }}</p>
        <p>No spaces in postcode. This will render the search inaccurate.</p>
        <input v-model="postcode" v-on:keyup.enter="getAddress" placeholder="Enter postcode">
        <div id="map"></div>
    </div>    
</template>

<script>
    import axios from 'axios'
    var address = ' ';
    var postcode = ' ';
    axios.defaults.headers.common = {
        "X-Requested-With": "XMLHttpRequest"
    };

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
                axios.get('get_origin/' + this.postcode + '/')
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
                console.log('123')
                var myLatLng = latLang;

                var map = new google.maps.Map(document.getElementById('map'), {
                    zoom: 15,
                    center: myLatLng
                });

                new google.maps.Marker({
                    position: myLatLng,
                    map: map,
                    title: 'Hello World!',
                    icon: 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png'
                });

                this.getCinemas(myLatLng, map);
            },
            getCinemas: function (latLang, map) {
               

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