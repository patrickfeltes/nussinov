import React, { Component } from 'react';

class NussinovTable extends Component {
    constructor(props) {
        super(props);
        this.state = {
            dp_table: this.props.dp_table_prop
        };
    }

    renderTableData() {
        if (this.state.dp_table == null) {
            return null;
        }
        return this.state.dp_table.map((row, i) => {
           var entry = row.map((element, j) => {
                return (
                    <td key={j}>{element}</td>
                );
           });
           return (
              <tr key={i}>
                  {entry}   
              </tr>
           );
        });
    }
  
    render() {
        return (
            <div>
                <table id='nussinov'>
                    <tbody>
                        {this.renderTableData()}
                    </tbody>
                </table>
            </div>
        );
    }
}

export default NussinovTable;