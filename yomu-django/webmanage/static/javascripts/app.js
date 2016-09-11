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
.controller('ViewCtrl', function($timeout, $scope) { 
	$scope.test = "it worked"

})
.factory('RfidFactory', function($http) {

})