import './App.css';
import React, { Component } from 'react';
import NussinovTable from './components/NussinovTable';

let baseURL = 'http://localhost:5000/';

class App extends Component {

  constructor(props) {
    super(props);
    this.state = {
      sequence: null,
      dp_table: null,
      dot_paren_strings: null,
      tracebacks: null,
      selected_idx: null
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
          var _tracebacks = result.tracebacks;

          this.setState(
            { 
              sequence: sequence,
              dot_paren_strings: _dot_paren_strings,
              dp_table: _dp_table,
              tracebacks: _tracebacks,
              selected_idx: 0
            }
          );
        }
      );
  
  }

  handleDotParenClick = (idx) => {
    this.setState({ selected_idx: idx })
  }

  renderDotParenData() {
    if (this.state.dot_paren_strings == null) {
      return null;
    }
    var items = this.state.dot_paren_strings.map((elem, idx) => {
      return (
        <tr key={idx} className={this.state.selected_idx === idx ? 'selected' : ''} onClick={ (event) => { this.handleDotParenClick(idx) }}>
          <td>{elem}</td>
        </tr>
      );
    });
    return (
      items
    );
  }

  renderDotParenTable() {
    return (
      <table id='dot-paren'>
        <thead>
          <tr>
            <th>Possible Dot-Parentheses</th>
          </tr>
        </thead>
        <tbody>
            {this.renderDotParenData()}
        </tbody>
      </table>
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
        <NussinovTable key={this.state.selected_idx} dp_table_prop={this.state.dp_table} traceback={this.state.tracebacks ? this.state.tracebacks[this.state.selected_idx] : null} sequence={this.state.sequence} />
        {this.renderDotParenTable()}
      </div>
    );
  }
}

export default App;
