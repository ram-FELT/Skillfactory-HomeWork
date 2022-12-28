import * as React from "react";

import "../styles/Main.css"


class Main extends React.Component {
    render() {
        return (
            <form onSubmit={this.props.weatherMethod}>
                <input type="text" name="city" placeholder="Введите название города"/>
                <button type="submit">Узнать погоду</button>
            </form>
        );
    }

}

export default Main;