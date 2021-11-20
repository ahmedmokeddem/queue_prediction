import React, { useState, useEffect, useRef } from 'react';
import arrowLeft from './arrow-left.svg';
import mapPin from './map-pin.svg';
import mapMarker from './map-marker.png';
import calendar from './calendar.svg';
import clock from './clock.svg';
import { useNavigate } from 'react-router-dom';
import * as L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import posteAlger from './algerie-poste.jpg';


function Card({img, name, distance, time, color}) {
    return (
        <div className="card">
            <img src={img} alt={name} />
            <div className={`card-time ${color}`}>{time}</div>
            <div className="card-name">{name}</div>
        </div>
    )
}

function Map() {
    const [location, setLocation] = useState("");
    const [date, setDate] = useState("");
    const [hour, setHour] = useState("");
    const [posts, setPosts] = useState([
        {
            img: posteAlger,
            name: "poste bir khadem",
            distance: 500,
            time: "3min",
            color: "green"
        },
        {
            img: posteAlger,
            name: "poste bir khadem",
            distance: 500,
            time: "3min",
            color: "orange"
        },
        {
            img: posteAlger,
            name: "poste bir khadem",
            distance: 500,
            time: "3min",
            color: "red"
        },
        {
            img: posteAlger,
            name: "poste bir khadem",
            distance: 500,
            time: "3min",
            color: "green"
        },
    ]);


    async function fetchPosts() {
        try {
            const response = await fetch('localhost:5000/GetWaitTime', {
                body: JSON.stringify({
                    latitude: location.latitude,
                    longitude: location.longitude
                })
            });

            const data = await response.json();
            setPosts(data);

        } catch(err) {
            console.log(err);
            alert("There was a problem while loading data!")
        }
    }


    const navigate = useNavigate();

    let mymap = useRef();


    useEffect(() => {

        mymap.current = L.map('map',  {
            zoomControl: false,
            scrollWheelZoom: false,
            maxHeight: 100,
            maxWidth: 100,
            center: [36.725876, 3.0546954],
            zoom: 13,
        }).setView([51.505, -0.09], 13);

        L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoiaXNsYW0zNiIsImEiOiJja3c3YXZvdmcwNDU4MnZsZjMza3VtaHcyIn0.7ckMNi_iJ0k3GgdApV_aXQ', {
            maxZoom: 18,
            id: 'mapbox/streets-v11',
            tileSize: 512,
            zoomOffset: -1,
            accessToken: 'pk.eyJ1IjoiaXNsYW0zNiIsImEiOiJja3c3YXZvdmcwNDU4MnZsZjMza3VtaHcyIn0.7ckMNi_iJ0k3GgdApV_aXQ'
        }).addTo(mymap.current);

        let myIcon = L.icon({
            iconUrl: mapMarker,
        });

        L.marker([51.505, -0.09], { icon: myIcon}).addTo(mymap.current);

        const day = new Date();
        let h = day.getHours();
        let m = day.getMinutes();
        h = (h < 10) ? `0${h}` : `${h}`;
        m = (m < 10) ? `0${m}` : `${m}`;
        setHour(`${h}:${m}`);
        setDate(day.toLocaleDateString());

        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition((pos) => {
                setLocation(pos.coords);
                console.log(location);
            }, (err) => {
                console.log(err);
            });
        } else {
            alert("Error: can't access geolocation");
        }

        if(location) {
            const pos = L.latLng(location.latitude, location.longitude);
            mymap.current.setView(pos, 11);
        }

        console.log(mymap.current)


    }, []);

    return (
        <div className="map-bg">
            <div className="top-bar">
                <div className="navbar">
                    <img src={arrowLeft} alt="arrow-left"
                        onClick={() => {
                            navigate("/services", { replace: true });
                        }}
                    />
                    <h3>Post Office</h3>
                    <button className="btn"
                        onClick={() => {
                            fetchPosts();
                        }}
                    >Predict</button>
                </div>

                <div className="location-input">
                    <img src={mapPin} alt="map-pin" />
                    <input type="text" name="location"
                        value={location ? `${location.latitude}, ${location.longitude}` : ""}
                        onChange={(e) => {
                            setLocation(e.target.value);
                        }}
                    />
                </div>

                <div className="time-inputs">
                    <div className="date-input">
                        <input type="text" name="date" value={date}
                            onChange={(e) => {
                                setDate(e.target.value);
                            }}
                        />
                        <img src={calendar} alt="calendar" />
                    </div>

                    <div className="hour-input">
                        <input type="text" name="hour" value={hour}
                            onChange={(e) => {
                                setHour(e.target.value);
                            }}
                        />
                        <img src={clock} alt="clock" />
                    </div>
                </div>

            </div>
            
            <div id="map">
            </div>

            <h2 style={{marginTop: '20px'}}>Best results</h2>
            <div className="cards">
                {
                    posts.length > 0 ?
                        posts.map((post, index) => (
                            <Card key={index} {...post} />
                        ))
                    :
                        <div>no available post offices!</div>
                }
            </div>
        </div>
    );
}

export default Map;