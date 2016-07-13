// Angular App Module
var mainApp = angular.module('mainApp', ['ui.bootstrap', 'ngRoute', 'ngAnimate']);

// Main App Config
mainApp.config(function($routeProvider) {

    // Route Config
    $routeProvider
        .when('/', {
            templateUrl: '/static/home.html',
            controller: 'homeController'
        })
        .when('/companies', {
            templateUrl: 'companies.html',
            controller: 'mainController'
        });


});

// Angular Controllers
mainApp.controller('mainController', function($scope) {

});

mainApp.controller('homeController', function($scope, $http) {
    $scope.readCard = function() {
        var httpURI = '/read';
        $http.get(httpURI)
            .success(function(data, status, headers, config) {
                $scope.readData = data;
            })
            .error(function(data, status, headers, config) {
                    alert(data);
            });
    };

    $scope.writeCard = function(card_hex) {
        if (card_hex) {
            //$scope.writeResponse = 'Card write with ID of \'' + card_hex + '\' complete.';
            var httpURI = '/write?id=' + card_hex;
            $http.get(httpURI)
                .success(function(data, status, headers, config) {
                    $scope.writeData = data;
                })
                .error(function(data, status, headers, config) {
                        alert(data);
                });
        } else {
            $scope.writeResponse = 'Please input a Card ID.';
        }
    };

});

mainApp.controller('navController', function($scope, $location) {
    $scope.isActive = function(viewLocation) {
        return viewLocation === $location.path();
    };
});
