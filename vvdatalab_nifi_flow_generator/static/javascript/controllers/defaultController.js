app.controller("defaultController", function($scope, $http) {
    $scope.statusMessage = "Set up the Data Flow";

    $http.get("/static/data/default.json")
    .then(function(response) {
        $scope.template = response.data;
    });

    $scope.createDataFlow = function(){
        var request = angular.element(document).find('pre').find('code').html();
        $http.post("/default", {"process_group": request})
            .then(function(response) {
                $scope.statusMessage = response.data;
            }
        );
    };
});