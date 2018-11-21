import React, { Component } from 'react'
import { connect } from 'react-redux'
import { Link } from 'react-router-dom'

import { actions } from 'state'


export default class Header extends Component {

  onUploadClick = e => this.input.click()
  onUploadChange = e => {
    const files = e.target.files
    if (files.length > 0) {
      const reader = new FileReader()
      const file = files[0]
      reader.onload = e => {
        const script = JSON.parse(e.target.result)
        this.props.uploadScript(script)
      }
      reader.readAsText(file);
    }
  }

  render() {
    const { script } = this.props
    return (
      <div className="jumbotron">
        <h1 className="mb-3">Questionnaire Form Builder</h1>
        <button
          onClick={this.onUploadClick}
          className="btn btn-secondary mr-1"
        >
          Upload
        </button>
        <input
          type="file"
          style={{display: 'none'}}
          onChange={this.onUploadChange}
          ref={r => { this.input = r; }}
        />
        <DownloadLink script={script}>
          <button className="btn btn-secondary mr-1">
            Download
          </button>
        </DownloadLink>
        <Link to="/graph">
          <button className="btn btn-secondary mr-1">
            View Graph
          </button>
        </Link>
        <Link to="/">
          <button className="btn btn-secondary mr-1">
            Builder
          </button>
        </Link>
        <Link to="/test">
          <button className="btn btn-secondary">
            Test
          </button>
        </Link>
      </div>
    )
  }
}


const DownloadLink = ({ script, children }) => {
  const json = JSON.stringify(script, null, 2)
  const data = "text/json;charset=utf-8," + encodeURIComponent(json);
    return (
      <a href={`data:${data}`} download="script.json">
        {children}
      </a>
    )
  }

const mapStateToProps = state => ({
  script: state.script,
})
const mapDispatchToProps = dispatch => ({
  uploadScript: (script) => dispatch(actions.script.upload(script)),
})
module.exports = connect(mapStateToProps, mapDispatchToProps)(Header)
