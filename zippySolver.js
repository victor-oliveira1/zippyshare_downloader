var page = require('webpage').create(), system = require('system');
page.settings.resourceTimeout = 60000;
page.open(system.args[1], function(status) {
  var dllink = page.evaluate(function() {
    return document.getElementById('dlbutton').href;
  });
  console.log(dllink);
  phantom.exit();
});

