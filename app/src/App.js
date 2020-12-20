import './App.css';
import React, { Component } from 'react';
import NussinovTable from './components/NussinovTable';

let baseURL = 'http://localhost:5000/';

const styles = {
  bannerStyle: {
    width: "100vw",
    height: "10vh",
    backgroundColor: "#0EBBD1"
  },
  titleStyle: {
    marginTop: 0,
    fontSize: "30px",
    textAlign: "center",
    paddingTop: "3vh"
  },
  formStyle: {
    marginTop: "3vh",
    marginLeft: "18vw"
  },
  inputStyle: {
    width: "50vw",
    height: "3vh",
    fontSize: "20px",
    color: "black",
    paddingLeft: "1vw",
    paddingTop: "0.5vh",
    paddingBottom: "0.5vh",
    border: "2px solid gray",
    borderRadius: "8px",
    marginRight: "1vw"
  },
  buttonStyle: {
    height: "4vh",
    backgroundColor: "#2CB27A",
    width: "5vw",
    fontSize: "25px",
    borderRadius: "6px",
  },
  dotStyle: {
    marginLeft: "18vw",
    marginTop: "3vh"
  },
  dotTitleStyle: {
    paddingTop: "1vh",
    paddingBottom: "1vh",
    paddingLeft: "2vh",
    paddingRight: "2vh",
    backgroundColor: "#14AD5B"
  }
}

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      sequence: null,
      dp_table: null,
      dot_paren_strings: null,
      tracebacks: null,
      selected_idx: null,
      input_invalid: false
    };
  }

  validateInput(sequence) {
    for (var i = 0; i < sequence.length; i++) {
      var c = sequence.charAt(i);
      if (c != 'G' && c != 'A' && c != 'U' && c != 'C') {
        return false;
      }
    }

    return true;
  }

  handleFormSubmit = (event) => {
    event.preventDefault();
    this.setState({ input_invalid: false });

    var sequence = event.target.sequence.value.toUpperCase();
    if (!this.validateInput(sequence)) {
      this.setState({ input_invalid: true });
      return;
    }
    
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
      <table style={styles.dotStyle} id='dot-paren'>
        <thead>
          <tr>
            <th style={styles.dotTitleStyle}>Possible Dot-Parentheses</th>
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
        <div style={styles.bannerStyle}>
          <p style={styles.titleStyle}>Nussinov Calculator</p>
        </div>
        <form style={styles.formStyle} onSubmit={this.handleFormSubmit}>
            <label>
              <input style={styles.inputStyle} type="text" placeholder="RNA Sequence" name="sequence" />
            </label>
            <button style={styles.buttonStyle} type="submit">Go</button>
        </form>
        {this.state.input_invalid ? <center><p className="errorMessage">Your input string should only have the characters A, U, G, and C.</p></center> : null}
        {this.state.sequence === null ? null : this.renderDotParenTable()}
        <NussinovTable key={this.state.selected_idx + this.state.sequence} dp_table_prop={this.state.dp_table} traceback={this.state.tracebacks ? this.state.tracebacks[this.state.selected_idx] : null} sequence={this.state.sequence} />
      </div>
    );
  }
}

export default App;
