import React from 'react';
import logo from './BlackLogo.svg';
import arrow from './arrow-left.svg';
import algeriePoste from './algerie-poste.jpg';
import { useNavigate } from 'react-router';

const Card = ({ img, service }) => {
    const navigate = useNavigate();

    return (
        <div className="card-container"
            onClick={() => {
                navigate("/app", { replace: true });
            }}
        >
            <img src={img} alt={service} />

            <div className="card-bottom">
                <span className="card-service">{service}</span>
                <img src={arrow} alt="arrow" className="arrow-right" />
            </div>
        </div>
    );
}

function Services() {

    const services = [
        {
            img: algeriePoste,
            service: 'Algérie Poste'
        }
    ]

    return (
        <div className="services-bg">
            <div className="logo-container">
                <img src={logo} alt="logo" />
                <h3>Our Services</h3>
            </div>

            <div>Please choose a service...</div>

            <div className="cards">
                {
                    services.map((service, index) => (
                        <Card key={index} {...service} />
                    ))
                }
            </div>
        </div>
    );
}

export default Services;