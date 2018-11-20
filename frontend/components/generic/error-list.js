import React from 'react'

module.exports = ({ errors }) => (
  <div>
    {errors.map(msg => (
      <div key={msg} className="alert alert-danger">
        {msg}
      </div>
    ))}
  </div>
)

