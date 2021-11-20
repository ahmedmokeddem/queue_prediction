const express = require('express');
const router = express.Router();
const controllers = require('controllers.js');

router.get('/GetWaitTime', controllers.predict);