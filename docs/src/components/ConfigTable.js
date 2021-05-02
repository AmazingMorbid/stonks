import React from 'react';

const columns = [
  "Key", "Required", "Default", "Type", "Description"
];

export const ConfigTableItem = ({ k, required, d, t, description }) => (
  <tr>
    <td>{k}</td>
    <td>{required ? "Y" : "N"}</td>
    <td>{d || "null"}</td>
    <td>{t}</td>
    <td>{description}</td>
  </tr>
);

const ConfigTable = ({ children }) => {
  return (
    <table>
      <thead>
        <tr>
          {columns.map((column) => (
            <th key={column}>{column}</th>
          ))}
        </tr>
      </thead>
      <tbody>
        {children}
      </tbody>
    </table>
  );
};

export default ConfigTable;
