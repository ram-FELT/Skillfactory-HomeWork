import * as React from "react";

import "../styles/App.css";

import Header from "./Header";
import Main from "./Main";
import Weather from "./Weather";

const API_KEY = "728b178ef1ae8ae48d6292aa48705f12"

class App extends React.Component {

    state = {
        temp: undefined,
        city: undefined,
        country: undefined,
        feels_like: undefined,
        wind: undefined,
        error: undefined
    }

    gettingWeather = async (e) => {
        e.preventDefault();
        const city = e.target.elements.city.value;

        if (city) {
            const api_url = await fetch(`http://api.openweathermap.org/data/2.5/weather?q=${city}&units=metric&exclude=current,minutely&lang=ru&APPID=${API_KEY}`);
            const daily_api_url = await fetch(`https://pro.openweathermap.org/data/2.5/forecast/hourly?q=${city}&units=metric&lang=ru&appid=${API_KEY}`);
            const data = await api_url.json();
            const daily_data = await daily_api_url.json();
            console.log(data);
            console.log(daily_data);
            this.setState({
                temp: data.main.temp,
                city: data.name,
                country: data.sys.country,
                feels_like: data.main.feels_like,
                wind: data.wind.speed,

                error: "Incorrect data"
            });
        }
    }

    render() {
        return (
            <div>
                <Header />
                <Main weatherMethod={this.gettingWeather}/>
                <Weather
                    temp={this.state.temp}
                    city={this.state.city}
                    country={this.state.country}
                    feels_like={this.state.feels_like}
                    wind={this.state.wind}
                    error={this.state.error}
                />
            </div>
        );
    }

}

export default App;