import React, { Component } from 'react'
import { Link } from 'react-router-dom'

class PageNotFound extends Component {
    render() {
        return (
            <div>
                <h1>Sorry! The page you requested could not be found!</h1>
                <Link to='/'>Return to Homepage</Link>
            </div>
        )
    }
}

export default PageNotFound
