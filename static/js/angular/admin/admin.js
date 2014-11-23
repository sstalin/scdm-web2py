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
            $scope.activeCheckBoxList = [];

            $scope.$watch('activeCheckBoxList.length', function(value){
               if(value > 0){
                   $scope.showRemove = true;
               }else{
                   $scope.showRemove = false;
               }
            });

            $scope.submit = function(){
                AdminSrvs.removeUsers($scope, $scope.$parent);
            };

            $scope.userClick = function (itemScope) {
                if (itemScope.checkBox === "on" || itemScope.checkBox == undefined) {
                    $scope.list[itemScope.$index] = itemScope.user;
                    $scope.activeCheckBoxList.push(1);
                } else if (itemScope.checkBox === "off") {
                    $scope.list.splice(itemScope.$index, 1);
                    $scope.activeCheckBoxList.pop();
                }

            };
        }])
    .service('AdminSrvs', [
        '$http', '$rootScope',
        function ($http, $rootScope) {
            this.getUsers = function (scope) {
                var URL = "/scdm/default/users";
                $http.get(URL).success(function (data, status) {
                    if (status == 200) {
                        scope.users = data.users;
                    }
                }).error(function (status) {

                });
            };

            this.removeUsers = function(scope, parent){
                var URL = "/scdm/default/users";
                var data = {users: scope.list};
                $http.post(URL, data)
                .success(function (data, status) {
                    if (status == 200) {
                        parent.users = data.users;
                        scope.list = [];
                        scope.activeCheckBoxList = [];
                        $rootScope.flash = data.flash;
                    }
                }).error(function (status) {

                });;
            };
        }]);