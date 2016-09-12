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
  // .when('/register', {
  //   controller: 'AuthCtrl',
  //   controllerAs: 'auth',
  //   templateUrl: '/auth/register.html'
  // });
})
.controller('ViewCtrl', function($timeout, $scope, RfidFactory) { 
	$scope.test = "it worked"
	$scope.allAlbums =  RfidFactory.getAllAlbums().then(function(dataResponse) {
		console.log("dataResponse = ", dataResponse)
        $scope.allAlbums = dataResponse.data;
    });

	

})
.controller('NewCtrl', function($timeout, $scope, RfidFactory) {
	$scope.worx = "this worx 2"

	$scope.lastRfid = RfidFactory.getLastRfid().then(function(lastScan) {
		console.log("lastScan = ", lastScan)
		$scope.lastRfid = lastScan.data.rfid
	});

})
.factory('RfidFactory', function($http) {

	allAlbums = null
	return {
	  getAllAlbums: () => {

	  	return $http({
	  	            method: 'GET',
	  	            url: "http://localhost:8000/api/albums/"
	  	        });
	  },
	  getLastRfid: () => {

	  	return $http({
	  		method: 'GET',
	  		url: "http://localhost:8000/api/currentRfid/1/"
	  	});
	  },
	  postNewAlbum:(albumInfo) => {
	    console.log("albumInfo = ", albumInfo)
	    return $http.post("http://localhost:8000/api/albums/", albumInfo)
	    .then(
	      res => console.log("res = ", res.data)
	    )
	  },
	}
})

