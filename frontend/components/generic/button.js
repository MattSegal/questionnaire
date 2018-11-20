import React from 'react'

module.exports = ({ onClick, children, disabled }) =>(
  <button
    className="btn btn-primary mb-2"
    onClick={onClick}
    disabled={disabled}
  >
    { children }
  </button>
)

