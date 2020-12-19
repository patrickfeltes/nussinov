import React, { Component } from 'react';

class NussinovTable extends Component {
    constructor(props) {
        super(props);

        var traceback = this.props.traceback;
        var _row_col_dict = {};

        if (traceback != null) {
            for (var i = 0; i < traceback.length; i++) {
                var row_col_list = traceback[i];
                _row_col_dict[row_col_list[0]] = row_col_list[1];
            }
        }

        this.state = {
            dp_table: this.props.dp_table_prop,
            row_col_dict: _row_col_dict
        };
    }

    renderTableData() {
        if (this.state.dp_table == null) {
            return null;
        }
        return this.state.dp_table.map((row, i) => {
           var entry = row.map((element, j) => {
                return (
                    <td className={this.state.row_col_dict[i] == j ? 'highlightedCell' : ''} key={j}>{element}</td>
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