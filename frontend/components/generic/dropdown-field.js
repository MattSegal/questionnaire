import React from 'react'

module.exports = ({ label, placeholder, value, onChange, options, disabled }) => (
  <div className="input-group mb-3">
    <div className="input-group-prepend">
      <span className="input-group-text">{ label }</span>
    </div>
    <select
      disabled={disabled}
      className="form-control"
      onChange={ onChange }
      value={ value }
    >
      <option value="">{ placeholder }</option>
      {options.map(([val, display]) => (
        <option key={ val } value={ val }>{ display }</option>
      ))}
    </select>
  </div>
)

