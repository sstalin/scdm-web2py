'use strict';

angular.module('myApp.admin', ['ngRoute'])

    .config(['$routeProvider', function ($routeProvider) {
//        $routeProvider.when('/view1', {
//            templateUrl: 'view1/view1.html',
//            controller: 'View1Ctrl'
//        });
    }])

    .controller('AdminCtrl',
    ['$scope', 'AdminSrvs',
        function ($scope, AdminSrvs) {
            $scope.users = [];
            AdminSrvs.getUsers($scope);
        }])
    .controller('UsersCtrl',
    ['$scope', 'AdminSrvs',
        function ($scope, AdminSrvs) {
            $scope.list = [];

            $scope.$watch('list.length', function(value){
               if(value > 0){
                   $scope.showRemove = true;
               }else{
                   $scope.showRemove = false;
               }
            });

            $scope.submit = function(){
                AdminSrvs.removeUsers($scope.list, $scope.$parent);
            };

            $scope.userClick = function (itemScope) {
                if (itemScope.checkBox === "on" || itemScope.checkBox == undefined) {
                    $scope.list[itemScope.$index] = itemScope.user;
                } else if (itemScope.checkBox === "off") {
                     $scope.list.splice(itemScope.$index, 1);
                }

            };
        }])
    .service('AdminSrvs', [
        '$http',
        function ($http) {
            this.getUsers = function (scope) {
                var URL = "/scdm/default/users";
                $http.get(URL).success(function (data, status) {
                    if (status == 200) {
                        scope.users = data.users;
                    }
                }).error(function (status) {

                });
            };

            this.removeUsers = function(list, scope){
                var URL = "/scdm/default/users";
                var data = {users: list};
                $http.post(URL, data)
                .success(function (data, status) {
                    if (status == 200) {
                        scope.users = data.users;
                    }
                }).error(function (status) {

                });;
            };
        }]);