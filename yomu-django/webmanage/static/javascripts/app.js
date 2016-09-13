angular.module('musicEdit', ['ngRoute'])
.config(function($interpolateProvider) {
        $interpolateProvider.startSymbol('((');
        $interpolateProvider.endSymbol('))');
})
.config(($routeProvider) => {

  $routeProvider
  .when('/', {
    controller: 'ViewCtrl',
    templateUrl: 'static/partials/viewEntries.html'
  })
  .when('/new', {
    controller: 'NewCtrl',
    templateUrl: 'static/partials/newEntry.html'
  })
  .when('/edit/:albumId', {
    controller: 'EditCtrl',
    templateUrl: 'static/partials/editAlbum.html'
  });
})
.controller('ViewCtrl', function($timeout, $location, $scope, RfidFactory) { 

	$scope.allAlbums =  RfidFactory.getAllAlbums().then(function(dataResponse) {
		// console.log("dataResponse = ", dataResponse);
        $scope.allAlbums = dataResponse.data;
    });

    console.log("Loading me");
    $scope.showAlbums = true;
	$scope.artist = null;
	$scope.albumName = null;
	$scope.playlist = null;
	$scope.rfid = null;


})
.controller('NewCtrl', function($scope, RfidFactory) {

	$scope.lastRfid = RfidFactory.getLastRfid().then(function(lastScan) {
		// console.log("lastScan = ", lastScan);
		$scope.lastRfid = lastScan.data.rfid;
	});

	$scope.postNewAlbum = function() {
                
		console.log("inside post new album");
		albumJson =   {
		    "title": $scope.albumName,
		    "artist": $scope.artistName,
		    "playlist": $scope.playList,
		    "rfid": $scope.lastRfid
		};

		RfidFactory.postNewAlbum(albumJson);

	};

})
.controller('EditCtrl', function($scope, $timeout, $routeParams, RfidFactory) {
	console.log("routparams = ",$routeParams.albumId);

	$scope.getAlbum = RfidFactory.getCurrentAlbum($routeParams.albumId).then(function(dataResponse) {
		albumObject = dataResponse.data;
		$scope.artist = albumObject.artist,
		console.log("$scope.artist = ",$scope.artist),
		$scope.albumName = albumObject.title,
		$scope.playlist = albumObject.playlist,
		$scope.rfid = albumObject.rfid,
		$timeout();
	});

	$scope.playlistList = null;

	$scope.getplaylists = RfidFactory.getAllPlaylists().then(function(playlists){
		console.log("playlists = ", playlists.data.playlists);
		$scope.playlistList = playlists.data.playlists;
		$timeout();
	});
	// $scope.showAlbums = !$scope.showAlbums,
	// console.log("albumObject = ", albumObject),
})
.factory('RfidFactory', function($http) {

	HOST = 'http://yomu.com:8000';

	allAlbums = null;
	return {
	  getAllAlbums: () => {

	  	return $http({
	  	            method: 'GET',
	  	            url: HOST+"/api/albums/"
	  	        });
	  },
	  getLastRfid: () => {

	  	return $http({
	  		method: 'GET',
	  		url: HOST+"/api/currentRfid/1/"
	  	});
	  },
	  getAllPlaylists: () => {

	  	return $http({
	  		method: 'GET',
	  		url: HOST+"/getPlaylists/"
	  	});
	  },
	  getCurrentAlbum: (albumRfid) => {

	  	return $http({
	  		method: 'GET',
	  		url:HOST+"/api/albums/"+albumRfid
	  	});
	  },
	  postNewAlbum:(albumInfo) => {
	    console.log("albumInfo = ", albumInfo);
	    return $http.post(HOST+"/api/albums/", albumInfo)
	    .then(
	      res => console.log("res = ", res.data)
	    );
	  },
	};
});

