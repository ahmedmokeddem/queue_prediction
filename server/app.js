const express = require('express');
const bp = require('body-parser');
require('dotenv').config();
const port = process.env.PORT || 5000;
const app = express();

app.use(bp.urlencoded({ extended: false }));

app.use(bp.json());

app.listen(port, () => {
    console.log("Express server listening on port " + port);
});