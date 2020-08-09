import React from "react";
import "./App.css";
import { Component } from "react";
import Title from "./components/CustomHtml/Title";
import MapComponent from "./components/Maps/MapComponent";

export default class App extends Component {
  render() {
    return (
      <div className="App">
        <Title></Title>
        <MapComponent></MapComponent>
        {/* <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <p>
            Edit <code>src/App.js</code> and save to reload.
          </p>
          <a
            className="App-link"
            href="https://reactjs.org"
            target="_blank"
            rel="noopener noreferrer"
          >
            Learn React
          </a>
        </header> */}
      </div>
    );
  }
}
