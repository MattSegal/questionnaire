import React from 'react'

module.exports = ({ label, type, placeholder, value, onChange }) =>(
  <div className="input-group mb-3">
    <div className="input-group-prepend">
      <span className="input-group-text">{ label }</span>
    </div>
    <input
      type={type}
      className="form-control"
      placeholder={ placeholder }
      value={ value }
      onChange={ onChange }
    />
  </div>
)
