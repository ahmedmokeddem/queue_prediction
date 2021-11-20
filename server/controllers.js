var spawn = require("child_process").spawn;
require('dotenv').config();


exports.predict = (req, res) => {
    var axios = require('axios');

    var config = {
        method: 'get',
        url: 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=' + req.body.latitude + '%' + req.body.longtitude + '&radius=20000&keyword=poste&key=' + process.env.GOOGLE_API_KEY,
        headers: {}
    };

    axios(config)
        .then(function(response) {
            var process = spawn('python', ["./Team_visions_Time_series.py",
                JSON.stringify(response.data)
            ]);
            process.stdout.on('data', function(data) {
                res.send(data.toString());
            });
        })
        .catch(function(error) {
            console.log(error);
        });

};