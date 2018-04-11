angular.module("verifierApp",[])
    .constant("getWebsiteListUrl","/api/getWebsiteList/")
    .controller("VerifierCtrl", VerifierCtrl)
    .factory("VerifierApi", VerifierApi)
    .config(function($interpolateProvider, $httpProvider) {
        $interpolateProvider.startSymbol("{[{");
        $interpolateProvider.endSymbol("}]}");
    });

    function VerifierCtrl($scope, $http, VerifierApi, $log) {
        var intervalId;
        $scope.period = 60;
        $scope.ifAutomatic = false;
        $scope.data = {};
        $scope.promise;

        $scope.initialize = function(period) {
            $scope.period = period;
            $scope.getPageList();
        };

        $scope.getPageList = function(){
            VerifierApi.getWebsiteList()
                .then(function successCallback(response){
                        $scope.data = response.data;
                    }, function errorCallback(response){
                        $log.log("Wystąpił błąd:");
                        $log.log(response);
                });
        };

        $scope.stopAutomatic = function(){
            $scope.ifAutomatic = false;
            clearInterval(intervalId);
        };

        $scope.startAutomatic = function(){
            $scope.ifAutomatic = true;
            intervalId = setInterval(function(){
                    $scope.getPageList();
                }, $scope.period*1000);
        };
    }

    function VerifierApi($log, $http, getWebsiteListUrl) {
        function get(urlTmp, id, data) {
            return request("GET", id, urlTmp, data);
        }

        function request(verb, id, urlTmp, data) {
            var req = {
              method: verb,
              url: url(id, urlTmp),
              data: data
            };
            return $http(req);
        }

        function url(id, urlTmp) {
            if(id == null || !angular.isDefined(id))
            {
              return urlTmp;
            }
            return urlTmp + id + "/";
        }

        return {
            getWebsiteList: function()
            {
                return get(getWebsiteListUrl);
            }
        }
    }
