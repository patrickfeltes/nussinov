import './App.css';
import React, { Component } from 'react';
import NussinovTable from './components/NussinovTable';

let baseURL = 'http://localhost:5000/';

class App extends Component {

  constructor(props) {
    super(props);
    this.state = {
      dp_table: null,
      dot_paren_strings: null
    };
  }

  handleFormSubmit = (event) => {
    event.preventDefault();
    var sequence = event.target.sequence.value.toUpperCase();
    // TODO: sanitize input
    
    var nussinovURL = baseURL + 'nussinov?rna_sequence=' + sequence;
    fetch(nussinovURL)
      .then(res => res.json())
      .then(
        (result) => {
          var _dot_paren_strings = result.dot_paren_strings;
          var _dp_table = result.dp_table;
          this.setState(
            { 
              dot_paren_strings: _dot_paren_strings,
              dp_table: _dp_table 
            }
          );
        }
      );
  
  }

  render() {
    return (
      <div>
        <form onSubmit={this.handleFormSubmit}>
            <label>
              RNA Sequence: <input type="text" name="sequence" />
            </label>
            <button type="submit">Submit</button>
        </form>
        <NussinovTable key={this.state.dp_table} dp_table_prop={this.state.dp_table} />
      </div>
    );
  }
}

export default App;
