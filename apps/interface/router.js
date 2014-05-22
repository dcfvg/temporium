var _ = require("underscore"); 

module.exports = function(app,io,m){

  /**
  * routing
  */
  //Handle route "GET /", as in "http://localhost:8080/"
  app.get("/", getIndex);
  app.get("/exposure", getExposure);
  app.get("/player", getPlayer);

  /**
  * routing functions
  */
  function getIndex(request, response) {
    //Render the view called "index"
    response.render("index", {pageData: {title : "museo"}});
  };
  function getPlayer(request, response) {
    //Render the view called "index"
    response.render("player", {pageData: {title : "exposure"}});
  };
  function getExposure(request, response) {
    //Render the view called "index"
    response.render("exposure", {pageData: {title : "exposure"}});
  };
};