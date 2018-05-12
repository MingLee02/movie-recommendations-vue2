<template>
	<div>
		<h2>Find Local Cinemas</h2>
		<p>{{ address }}</p>
		<div v-if="address.length == 0"><input v-model="postcode" v-on:keyup.enter="getAddress" placeholder="Enter postcode"></div>
		<div id="map"></div>

		<ul v-if="cinemaList.length > 0">
			<li v-for="cinema in cinemaList" v-on:click="selectCinema(cinema)">
				<p>{{ cinema.name }}</p>
				<p>{{ cinema.rating }}</p>
				<p>{{ cinema.distance.text }}</p>
				<p>{{ cinema.address }}</p>
			</li>
		</ul>

		<ul v-if="recommendedFilms.length > 0">
			<li v-for="film in recommendedFilms">
				<p>{{ film.title }}</p>
				<p>{{ film.rating }}</p>
				<p>{{ film.genres }}</p>
				<p>{{ film.languages }}</p>
				<p>{{ film.plot_outline }}</p>
			</li>
		</ul>
	</div>    
</template>

<script>
	import axios from 'axios'
	var url = "http://127.0.0.1:5000/"

	export default {
		data() {
			return {
				address: '',
				postcode: '',
				cinemaList: '',
				recommendedFilms: ''
			};
		},
		name: 'Gplaces',
		methods: {
			getAddress: function () {
				var self = this;
				axios.get(url + "api/address/" + this.postcode)
				  .then((response) => {
						this.address = response.data.formatted_address
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
					title: 'Origin',
					icon: 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png'
				});

				this.getCinemas(latLang, map);
			},
			getCinemas: function (latLang, map) {
				var locations = []
				var origin = latLang.lat + ":" + latLang.lng;
				axios.get(url + "api/cinema-list/" +  origin)
					.then((response) => {
						var x;
						this.cinemaList = response['data'];
						for (x in response['data']) {
							locations.push(response['data'][x]) 
						}
						this.addMarkers(locations, map)
					})
					.catch((err) => {
						console.log(err);
					});
			},
			addMarkers: function (locations, map) {
				console.log(locations)
				for (var i = 0; i < locations.length; i++) { 
					new google.maps.Marker({
						position: locations[i]['latlng'],
						map: map,
						title: locations[i]['name'],
					});
				}
			},
			selectCinema: function (cinema) {
				axios.get(url + "api/get-recommendations/" + cinema.placeId +  "/" + cinema.name)
					.then((response) => {
						console.log(response)
						this.recommendedFilms = response.data

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