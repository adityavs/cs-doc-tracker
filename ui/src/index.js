import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';

class HeaderRow extends React.Component {
  render() {
    return (
      <tr className="header-row">
          <th classname="header-column">Id</th>
          <th classname="header-column">State</th>
          <th classname="header-column">Abbreviation</th>
      </tr>
    );
  }
}

class Table extends React.Component {
  render() {
    return (
      <table className="table">
          <HeaderRow />
      </table>
    );
  }
}

// ========================================

ReactDOM.render(
  <Table />,
  document.getElementById('root')
);
